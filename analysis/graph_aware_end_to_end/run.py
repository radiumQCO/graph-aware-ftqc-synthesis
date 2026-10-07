"""Matched complete-logical-workload replays and sensitivity, reusable checkpoints."""
import argparse
import json
import time
from collections import Counter,defaultdict

from workload import HERE, build, read_inputs, write_workloads, sha
from scheduler import Replay
from delivered_benchmark import Fixture


def change(a,b):
    return None if a in (None,0) or b is None else 100*(b-a)/a


def static_macro_routes(program):
    """Exact deterministic CNOT-corridor work, independent of runtime ordering.

    Separates phase-wiring penalties from arithmetic savings without rerunning
    the physical-cost model. Injection/CZ/resource paths are excluded here and
    remain in the separately measured whole-replay routing-volume ledger.
    """
    fixture=Fixture();counts=Counter()
    for block in program['blocks']:
        for i,segment in enumerate(block['segments']):
            stage='startup' if block['id']<0 else block['pauli']+'_'+['compute','phase','cleanup'][i]
            for gate,qs in segment:
                if gate=='CNOT':counts[(stage,tuple(qs))]+=1
    stages=defaultdict(lambda:{'CNOT':0,'corridor_tilecycles':0,'corridor_qubitseconds':0.})
    for (stage,qs),count in counts.items():
        cells=len(set(fixture.path(fixture.xy(qs[0]),fixture.xy(qs[1]))[1:-1]))
        stages[stage]['CNOT']+=count;stages[stage]['corridor_tilecycles']+=count*cells*2*fixture.d
        stages[stage]['corridor_qubitseconds']+=count*cells*2*fixture.d*2*fixture.d**2*400e-9
    return dict(stages)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--quick',action='store_true',help='One matched balanced run, no sensitivity.')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--concurrent',action='store_true',help='Additional matched runs with existing small T sources that fit concurrently.')
    args=parser.parse_args()
    inputs=read_inputs();programs={v:build(v,inputs) for v in ('A','B')}
    static_routes={v:static_macro_routes(p) for v,p in programs.items()}
    trace_hash=write_workloads(inputs,programs)
    target=HERE/'results.json'
    engine_hashes={name:sha(HERE/name) for name in ('workload.py','scheduler.py')}
    old=json.loads(target.read_text()) if args.resume and target.exists() else None
    if old and old.get('replay_engine_sha256') not in (None,engine_hashes):
        raise RuntimeError('Replay engine changed; rerun without --resume.')
    rows=old['runs'] if old else []
    requests=[(p,29.,'sampled_frame','time_multiplexed_Aprime') for p in (['balanced'] if args.quick else ['resource','depth','balanced'])]
    if not args.quick:
        requests.extend([('balanced',0.,'sampled_frame','time_multiplexed_Aprime'),('balanced',290.,'sampled_frame','time_multiplexed_Aprime'),('balanced',29.,'conservative','time_multiplexed_Aprime')])
    if args.concurrent:
        requests.extend((p,0.,'sampled_frame','concurrent_small_T_3') for p in ['resource','depth','balanced'])
    def save():
        cp=inputs['delivery']['ccz_factory_scan']['best']
        ledger={v:p['ledger'] for v,p in programs.items()}
        comparisons=[]
        keys=['runtime_seconds_conditional','reserved_physical_qubits','reserved_qubitseconds_conditional',
              'active_qubitseconds_conditional','routing_volume_qubitseconds_conditional',
              'measurement_count','feedback_wait_events','all_to_all_logical_primitive_depth_conditional',
              'physical_failure_sensitivity_proxy','proxy_plus_synthesis_NOT_validated_failure_probability',
              'peak_compilation_logical_qubits','factory_mode_changes']
        for policy,switch,correction,factory in requests:
            pair={r['variant']:r for r in rows if r['policy']==policy and r['factory_switch_cycles_assumed']==switch and r['correction_policy']==correction and r.get('factory_policy','time_multiplexed_Aprime')==factory}
            if len(pair)==2:
                comparisons.append({'policy':policy,'switch_cycles':switch,'correction':correction,'factory_policy':factory,
                                    'percentage_change_B_minus_A_over_A':{k:change(pair['A'][k],pair['B'][k]) for k in keys}})
        results={
            'final_status':'D. Benchmark remains incomplete because critical physical components are missing',
            'date':'2026-10-06','scope':'Complete conditional P logical circuit; conditional routing/production model, not physical benchmark',
            'workload_trace_sha256':trace_hash,'input_manifest':inputs['manifest'],'logical_ledgers':ledger,
            'replay_engine_sha256':engine_hashes,
            'static_macro_routes_by_stage':static_routes,
            'runs':rows,'comparisons':comparisons,
            'waterfall_exact_counts':{
                'ZZ_AND_saved_per_layer':99,'ZZ_layers':100,'CCZ_saved':9900,
                'unchanged_X_AND':19897,'unchanged_tower_AND':1608,
                'T_synthesis_expected_unchanged':ledger['A']['T_synthesis_expected'],
                'CCZ_intrinsic_factory_cycles_saved':9900*cp['cycles_per_accepted_batch'],
                'CCZ_intrinsic_factory_qubitseconds_saved':9900*cp['qubitcycles_per_output']*400e-9,
                'CCZ_buffer_halves_no_longer_delivered':29700,
                'CCZ_injection_CX_removed':29700,'CCZ_injection_readouts_removed':29700,
                'inverse_readouts_removed':9900,'feedback_events_removed':19800,
                'arithmetic_CNOT_removed':ledger['A']['macro_counts']['CNOT']-ledger['B']['macro_counts']['CNOT'],
                'expected_CCZ_CZ_corrections_removed':14850,'expected_inverse_CZ_corrections_removed':4950,
                'ZZ_4T_gadget_unrouted_depth_change_per_layer':448-430,
                'net_physical_end_to_end_result':'UNKNOWN; conditional replay is reported separately'},
            'unknown_components':[
                'Complete shared circuit-level physical noise model and decoder on surgery/factory/transfer operations',
                'Real factory layouts embedded in common area, including source-mode reconfiguration and cold startup',
                'Anisotropic (dx21,dz9) factory outputs to ordinary d29 patches: verified growth/escape fidelity and time',
                'Destination resource landing sites, injection merge/boundary geometry and endpoint congestion',
                'Physical reset timing/channel and latency tails of classical feed-forward/decoder',
                'Stochastic retry/postselection tails and correlated delivery failures',
                'Validated physical whole-program failure probability'],
            'fairness':{
                'physical_platform':'same p-scale 1e-3, 2D nearest-neighbor surface-code-like conditional fixture',
                'same_complete_physical_noise_model_available':False,'total_failure_target':.002,
                'synthesis_budget':.002/3,'other_two_budgets_each':.002/3,'distance_policy':'same fixed d29 from previous admitted replay',
                'ordinary_cycle_ns':400,'physical_gate_ns':50,'physical_readout_ns':100,'physical_reset_ns':None,
                'feedback_allowance_cycles':25,'factory_capacity_physical_qubits':64000,
                'simultaneous_T_and_CCZ_factory_qubits':39976+35062,'simultaneous_fit':False,
                'switching':'one source mode at a time; 0/29/290-cycle sensitivity, actual cost UNKNOWN',
                'buffer_logical_slots_total':12,'CCZ_slots':6,'T_slots':6,'layout_and_routing':'unchanged Fixture; shared snake data targets',
                'schedulers':'same standard list priorities, same timing and resource rules for A and B; not global optima',
                'rotation_random_branches':'same seed and exactly same 241 sampled synthesis programs',
                'corrections':'same branch-resolved ordinary CCZ; optional conservative envelope; no AutoCCZ substitution'},
        }
        target.write_text(json.dumps(results,indent=2),encoding='utf-8')
    for policy,switch,correction,factory in requests:
        for variant in ('A','B'):
            if any(r['variant']==variant and r['policy']==policy and r['factory_switch_cycles_assumed']==switch and r['correction_policy']==correction and r.get('factory_policy','time_multiplexed_Aprime')==factory for r in rows):continue
            start=time.perf_counter();row=Replay(programs[variant],inputs,policy,switch,correction,factory).run()
            row['analysis_wall_seconds']=time.perf_counter()-start;rows.append(row);save()
            print(json.dumps({k:row[k] for k in ('variant','policy','factory_policy','factory_switch_cycles_assumed','correction_policy','runtime_seconds_conditional','active_qubitseconds_conditional','analysis_wall_seconds')}),flush=True)
    save()


if __name__=='__main__':main()
