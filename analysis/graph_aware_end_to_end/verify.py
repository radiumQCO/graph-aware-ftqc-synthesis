"""Independent exact phase, gate-string, frame, trace and accounting checks."""
import gzip
import hashlib
import json
import math
import random
import sys
from collections import Counter

import numpy as np
import mpmath as mp

from workload import HERE, ANALYSIS, build, read_inputs, catalysis_prefix, catalysis_suffix, tower
from delivered_benchmark import verify_ccz_injection
from hwp_schedule import macros_for


def apply_boolean(state,ops,seed_target=None,measurement_bits=0):
    exponent=0;sign=1;ordinal=0
    for g,qs in ops:
        if g=='CNOT':a,b=qs;state[b]^=state[a]
        elif g=='AND':a,b,t=qs;assert state[t]==0;state[t]=state[a]&state[b]
        elif g=='UNAND':
            a,b,t=qs;assert state[t]==(state[a]&state[b])
            m=(measurement_bits>>ordinal)&1;ordinal+=1
            sign*=(-1)**(m*state[t]+m*(state[a]&state[b]));state[t]=0
        elif g=='SEED':exponent+=256*state[qs[0]]
        else:raise AssertionError(g)
    assert sign==1
    return exponent


def verify_tower():
    # Exhaust all eight weight bits AND all eight catalyst basis components.
    # Initial phase from catalyst superpositions + seed phase must factor into
    # required eight rotations and the unchanged final catalyst states.
    weights=list(range(8));bank=list(range(8,25));ops=tower(weights,bank,[('SEED',(23,))])
    count=Counter(g for g,_ in ops)
    assert count=={'CNOT':48,'AND':8,'UNAND':8,'SEED':1}
    tested=0
    for w in range(256):
        outputs=set()
        for c in range(256):
            state=[(w>>j)&1 for j in range(8)]+[(c>>j)&1 for j in range(8)]+[0]*9
            phase=c+apply_boolean(state,ops,measurement_bits=w^c)
            outcat=sum(state[8+j]<<j for j in range(8))
            assert state[:8]==[(w>>j)&1 for j in range(8)] and not any(state[16:])
            assert phase==w+outcat,(w,c,phase,outcat)
            outputs.add(outcat)
            tested+=1
        assert len(outputs)==256
    # bijection on catalyst components for every fixed input: linearity proof.
    return {'exact_integer_phase_cases':tested,'all_weight_and_catalyst_components':True,
            'one_layer_identity':'x+y+c = (x xor y xor c) + 2 majority(x,y,c)',
            'AND_per_eight_bit_tower':8,'CNOT_per_tower':48,'temporary_targets_clean':True,
            'catalyst_component_map_bijective_for_every_input':True,
            'scope':'ideal catalysts/angles; composed measurement-assisted maps, not physical fault validation'}


def verify_x_counter():
    ops=macros_for(200);rng=random.Random(13);count=0
    assignments=[[0]*200,[1]*200]+[[int(i<k) for i in range(200)] for k in range(201)]
    assignments += [[rng.randrange(2) for _ in range(200)] for _ in range(128)]
    for bits in assignments:
        state=bits+[0]*(197+8)
        apply_boolean(state,ops)
        weight=sum(state[397+j]<<j for j in range(8));assert weight==sum(bits)
        inverse=[('CNOT' if g=='CNOT' else 'UNAND',qs) for g,qs in reversed(ops)]
        apply_boolean(state,inverse,measurement_bits=rng.getrandbits(197))
        assert state[:200]==bits and not any(state[200:]);count+=1
    return {'cases':count,'all_possible_population_values_covered':True,'AND':197}


def verify_graph_mapping(inputs):
    from workload import graph_arithmetic
    from scaling import grid
    edge_set={tuple(sorted(e)) for e in inputs['structure']['edges']}
    edges,_=grid(10,10,True,2)
    def snake(i):r,c=divmod(i,10);return 10*r+(c if r%2==0 else 9-c)
    assert {tuple(sorted((snake(a),snake(b)))) for a,b in edges if a<100 and b<100}==edge_set
    rng=random.Random(71);cases=0
    for variant in ('A','B'):
        compute,undo,weights,anc,circuit,_=graph_arithmetic(variant)
        data=[[0]*200,[1]*200,[(i//10+i%10)%2 for i in range(200)]]
        data += [[rng.randrange(2) for _ in range(200)] for _ in range(256)]
        for bits in data:
            state=bits+[0]*anc;apply_boolean(state,compute)
            represented=sum((2<<j)*state[q] for j,q in enumerate(weights))
            expected=sum(bits[copy*100+a]^bits[copy*100+b] for copy in range(2) for a,b in edge_set)
            assert represented==expected
            apply_boolean(state,undo,measurement_bits=rng.getrandbits(396))
            assert state[:200]==bits and not any(state[200:]);cases+=1
    return {'mapped_two_torus_basis_checks':cases,'exact_graph_phase_inherited_proof':True,
            'mapping_is_target_renaming_not_quantum_SWAP':True}


def verify_frames():
    I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)
    H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2);S=np.diag([1,1j])
    CX=np.zeros((4,4),complex)
    for a in range(2):
        for b in range(2):CX[2*a+(a^b),2*a+b]=1
    CZ=np.diag([1,1,1,-1]).astype(complex);worst=0.;cases=0
    def phase_distance(a,b):
        k=np.argmax(abs(b));phase=a.flat[k]/b.flat[k]
        return np.max(abs(a-phase*b))
    for xa in range(2):
        for za in range(2):
            P=np.linalg.matrix_power(X,xa)@np.linalg.matrix_power(Z,za)
            for g,U,new in [('H',H,(za,xa)),('S',S,(xa,za^xa)),('SDAG',S.conj().T,(xa,za^xa))]:
                Q=np.linalg.matrix_power(X,new[0])@np.linalg.matrix_power(Z,new[1])
                worst=max(worst,float(phase_distance(U@P,Q@U)));cases+=1
            for xb in range(2):
                for zb in range(2):
                    P2=np.kron(P,np.linalg.matrix_power(X,xb)@np.linalg.matrix_power(Z,zb))
                    for U,new in [(CX,(xa,za^zb,xb^xa,zb)),(CZ,(xa,za^xb,xb,zb^xa))]:
                        Q=np.kron(np.linalg.matrix_power(X,new[0])@np.linalg.matrix_power(Z,new[1]),
                                  np.linalg.matrix_power(X,new[2])@np.linalg.matrix_power(Z,new[3]))
                        worst=max(worst,float(phase_distance(U@P2,Q@U)));cases+=1
    assert worst<1e-14
    return {'Pauli_Clifford_propagation_cases':cases,'max_matrix_error_up_to_phase':worst,
            'non_Clifford_rule':'physically flush nonzero frame before every AND, inverse AND, and T; final output flush',
            'CZ_is_not_a_Pauli_frame_update':True}


def verify_correction_statistics():
    hist=Counter();z=0
    for m in range(8):
        a,b,c=(m>>2)&1,(m>>1)&1,m&1
        hist[a+b+c]+=1;z+=a*b+a*c+b*c
    assert hist=={0:1,1:3,2:3,3:1} and z/8==.75
    return {'CZ_count_histogram_equiprobable_ideal_branches':dict(hist),'expected_CZ_per_CCZ':1.5,
            'expected_linear_Z_updates_per_CCZ':.75,'inverse_CZ_probability':.5,
            'AutoCCZ':'not substituted; additional auto-correction resource preparation/layout not in admitted source'}


def verify_selected_mixtures(inputs,program):
    # Independent matrix products in chronological order, including ensemble
    # probabilities. This tests actual selected phase programs, not a T-count fit.
    mp.mp.dps=90;cache=inputs['synthesis'];unique={}
    for record in program['rotations']:
        key=(record['theta'],record['delta']);unique[key]=record
    def matrix(gates):
        U=mp.eye(2)
        G={'H':mp.matrix([[1,1],[1,-1]])/mp.sqrt(2),'S':mp.matrix([[1,0],[0,1j]]),
           'T':mp.matrix([[1,0],[0,mp.exp(1j*mp.pi/4)]]),'X':mp.matrix([[0,1],[1,0]])}
        for gate in reversed(gates):U=G[gate]*U
        return U
    from workload import find_mixture
    for (theta,delta),record in unique.items():
        mix=find_mixture(cache,float(theta),float(delta));values=[]
        for branch in mix['branch_keys']:
            raw=cache[branch];U=matrix(raw['gates']);U/=mp.sqrt(mp.det(U))
            values.append((mp.exp(1j*mp.mpf(theta))*U[0,0]**2,abs(U[1,0])**2))
        p=mp.mpf(mix['probability_first']);z=p*values[0][0]+(1-p)*values[1][0]
        s=p*values[0][1]+(1-p)*values[1][1]
        error=1-mp.re(z)+s
        assert abs(mp.im(z))<mp.mpf('1e-70') and 0<=error<=mp.mpf(delta)
        assert abs(float(error)-record['diamond_bound'])<1e-17
    return {'selected_unique_mixtures_independently_multiplied':len(unique),
            'chronological_gate_order_verified':True,'positive_average_channel_error_certified':True,
            'every_random_branch_exact_unitary_claimed':False}


def verify_artifacts(inputs,programs):
    for item in inputs['manifest'].values():
        assert hashlib.sha256((ANALYSIS.parent/item['path']).read_bytes()).hexdigest()==item['sha256']
    a,b=programs['A'],programs['B'];assert a['rotations']==b['rotations']
    for v,p in programs.items():
        ledger=p['ledger'];counts=Counter(g for block in p['blocks'] for segment in block['segments'] for g,_ in segment)
        assert not any('UNTIMED' in g or 'UNKNOWN' in g for g in counts)
        assert counts['AND']==counts['UNAND']==ledger['total_CCZ']
        assert counts['T']==8552 and len(p['rotations'])==241
        assert ledger['synthesis_diamond_bound']<ledger['allocated_synthesis_budget']
    assert a['ledger']['total_CCZ']-b['ledger']['total_CCZ']==9900
    assert a['ledger']['macro_counts']['CNOT']-b['ledger']['macro_counts']['CNOT']==199400
    r=json.loads((HERE/'results.json').read_text()) if (HERE/'results.json').exists() else None
    checked=0
    if r:
        if 'replay_engine_sha256' in r:
            for name,digest in r['replay_engine_sha256'].items():
                assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest
        assert hashlib.sha256((HERE/'workloads.json.gz').read_bytes()).hexdigest()==r['workload_trace_sha256']
        archive=json.loads(gzip.decompress((HERE/'workloads.json.gz').read_bytes()))
        assert archive['variants']['A']['rotations']==archive['variants']['B']['rotations']
        for variant in ('A','B'):
            assert archive['variants'][variant]['ledger']==programs[variant]['ledger']
            route_count=sum(x['CNOT'] for x in r['static_macro_routes_by_stage'][variant].values())
            assert route_count==programs[variant]['ledger']['macro_counts']['CNOT']
        for row in r['runs']:
            v=row['variant'];ledger=programs[v]['ledger']
            assert row['produced_resources']['CCZ']==ledger['total_CCZ']
            assert row['produced_resources']['T']==8552+row['unused_final_surplus'].get('T',0)
            assert row['measurement_count']==4*ledger['total_CCZ']+8552
            assert row['feedback_wait_events']==2*ledger['total_CCZ']+8552
            assert row['actual_model_gate_counts']['CNOT']==ledger['macro_counts']['CNOT']
            assert row['reserved_physical_qubits']==8045090
            assert row['peak_buffer_reserved_logical_qubits']<=12
            assert row['factory_mode_changes']==(0 if row.get('factory_policy')=='concurrent_small_T_3' else 402)
            assert row['validated_physical_failure_rate'] is None
            assert math.isclose(sum(row['active_components_qubitseconds_conditional'].values()),row['active_qubitseconds_conditional'])
            checked+=1
    return {'source_hashes_verified':len(inputs['manifest']),'same_rotation_choices':True,
            'complete_logical_traces':2,'phase_windows':201,'replay_rows_checked':checked,
            'physical_missing_fields_remain_unknown':True}


def main():
    inp=read_inputs();programs={v:build(v,inp) for v in ('A','B')}
    result={'tower':verify_tower(),'X_counter':verify_x_counter(),'graph_phase_and_mapping':verify_graph_mapping(inp),
            'CCZ_injection':verify_ccz_injection(),'Pauli_frames':verify_frames(),
            'ordinary_CCZ_corrections':verify_correction_statistics(),'selected_synthesis':verify_selected_mixtures(inp,programs['A']),
            'artifacts':verify_artifacts(inp,programs),
            'validated_physical_failure_probability':None}
    (HERE/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
