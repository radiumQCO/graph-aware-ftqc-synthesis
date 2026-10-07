"""Matched carry delivery RESOURCE MODEL, not an all-factory physical benchmark.

Exact existing HWP macro demand is replayed on one explicit corridor fixture.
The middle phase circuit, physical factories, and full-program error are not
simulated. Missing cultivation interfaces are rejection gates, never zero cost.
"""
import argparse
import collections
import gzip
import hashlib
import heapq
import io
import json
import math
import statistics
import sys
from pathlib import Path

from hwp_schedule import macros_for

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results'
METHOD = 'hwp_global_joint_batch_in_circuit_tower_mixed_diagonal'


def percentile(values, p):
    vals = sorted(values)
    at = (len(vals)-1)*p
    lo = int(at)
    return vals[lo]*(1-at+lo)+vals[min(lo+1,len(vals)-1)]*(at-lo)


def ccz_factory_scan():
    # Reuse the reviewed adapter; source channels/circuit order stay unchanged.
    from factory_audit import distillation_audit
    distillation_audit()
    from twolevel8toCCZ import cost_of_two_level_8toccz
    captures = {}
    def profile(frame,event,arg):
        if event=='return' and frame.f_code.co_name=='cost_of_two_level_8toccz':
            captures.update({key:float(frame.f_locals[key]) for key in ('pfail','pfail2','pl1','l1time')})
    rows = []
    sys.setprofile(profile)
    try:
        for dx2 in (21,23,25):
            for dz2 in (9,11,13):
                for dm2 in (11,13,15):
                    for nl1 in (4,6):
                        f=cost_of_two_level_8toccz(.001,13,5,5,dx2,dz2,dm2,nl1)
                        rows.append({'distances':[13,5,5,dx2,dz2,dm2,nl1], 'qubits':f.qubits,
                                     'cycles_per_accepted_batch':f.distillation_time_in_cycles,
                                     'output_error_proxy':f.distilled_magic_state_error_rate,
                                     'qubitcycles_per_output':f.qubits*f.distillation_time_in_cycles,**captures})
    finally:
        sys.setprofile(None)
    # Same per-AND error allowance as 4 delivered T states; half reserved.
    threshold=4*(.002/3/253617)/2
    admitted=[r for r in rows if 0<r['output_error_proxy']<=threshold]
    best=min(admitted,key=lambda r:r['qubitcycles_per_output'])
    return {'points':rows,'admitted_points':len(admitted),'quality_limit':threshold,
            'best':best,'scope':'54 pre-existing parameter points; L1 fixed (13,5,5), not global optimum'}


def trace():
    costs=json.loads((OUT/'paper_counts_proxy.costs.json').read_text())
    selected=next(m for m in costs['methods'] if m['method']==METHOD)
    structure=json.loads((OUT/'paper_counts_proxy.structure.json').read_text())
    all_ops=[]
    count=collections.Counter()
    for group in selected['groups']:
        n=group['n']; k=n-n.bit_count(); b=n.bit_length()
        # Shared physical mapping across backends. X data 0..199; ZZ parity
        # carriers 200..599; carries/output registers recycled each layer.
        if group['pauli']=='X':
            qs=list(range(200))+list(range(600,600+k+b))
            outer=[('H',(q,)) for q in range(200)]
        else:
            qs=list(range(200,600))+list(range(600,600+k+b))
            outer=[]
            for copy in range(2):
                for i,(a,z) in enumerate(structure['edges']):
                    carrier=200+copy*200+i
                    outer.extend([('CNOT',(copy*100+a,carrier)),('CNOT',(copy*100+z,carrier))])
        macros=[(gate,tuple(qs[q] for q in targets)) for gate,targets in macros_for(n)]
        seq=outer+macros+[('PHASE_INTERFACE_UNTIMED',tuple(qs[n+k:]))]
        seq += [('CNOT' if gate=='CNOT' else 'UNAND',targets) for gate,targets in reversed(macros)]
        seq += list(reversed(outer))
        for gate,targets in seq:
            count[gate]+=1
            all_ops.append((gate,targets,group['layer'],group['pauli']))
    assert count['AND']==count['UNAND']==59597
    assert count['PHASE_INTERFACE_UNTIMED']==201
    target=OUT/'carry_demand_trace.json.gz'
    with target.open('wb') as raw, gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as packed, io.TextIOWrapper(packed,encoding='utf8') as f:
        json.dump({'status':'EXACT_CARRY_SUBTRACE_WITH_UNTIMED_PHASE_INTERFACES_NOT_FULL_PROGRAM',
                   'source_cost_sha256':hashlib.sha256((OUT/'paper_counts_proxy.costs.json').read_bytes()).hexdigest(),
                   'operation_fields':['gate','logical_qubits','Suzuki_layer','Pauli'], 'operations':all_ops},f,separators=(',',':'))
    return all_ops, {'operations':len(all_ops),'counts':dict(count),
                     'hwp_AND_demand':59597,'four_T_demand':238388,
                     'excluded_T_maximum':253617-238388,
                     'excluded_phase_status':'Phase/tower circuit timing not certified; no invented timings',
                     'trace_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}


class Fixture:
    def __init__(self,d=29,columns=36,rows=32,factory_area=64000,feedback=25,buffer_qubits=12):
        self.d=d; self.columns=columns; self.rows=rows
        self.factory_area=factory_area; self.feedback=feedback
        self.buffer_qubits=buffer_qubits
        assert 1091+buffer_qubits<=columns*rows
        self.width=2*columns+1; self.height=2*rows+1
        self.total_qubits=self.width*self.height*2*d*d+factory_area
    def xy(self,q):
        assert 0<=q<1091+self.buffer_qubits
        site=q+self.buffer_qubits if q<1091 else q-1091
        return 2*(site%self.columns)+1,2*(site//self.columns)+1
    def path(self,a,b):
        # Deterministic rectilinear corridor route. No crossing occupied data.
        points=[a]
        def to(x,y):
            px,py=points[-1]
            while px!=x:
                px+=1 if x>px else -1; points.append((px,py))
            while py!=y:
                py+=1 if y>py else -1; points.append((px,py))
        if a==(0,0):
            to(0,b[1]-1);to(b[0],b[1]-1);to(*b)
        else:
            to(a[0],a[1]-1);to(b[0]-1,a[1]-1);to(b[0]-1,b[1]);to(*b)
        assert all(x%2==0 or y%2==0 for x,y in points[1:-1])
        return tuple(points)


class Production:
    """On-demand factory cycles; reuse is allowed only after accepted output.

    Source cadence is expected, not sampled tail latency. Buffered accepted
    inventory is scheduled by ready timestamps. No resource expires silently.
    """
    def __init__(self,qubits,cycles,batch,area,buffer_qubits,width):
        self.qubits=qubits;self.cycles=cycles;self.batch=batch
        self.instances=area//qubits
        assert self.instances>0
        self.factory_free=[0.0]*self.instances
        self.ready=[];self.cost=0.;self.batches=0
        self.width=width
        self.buffer_free=[0.]*(buffer_qubits//width)
        assert len(self.buffer_free)>=batch
        self.buffer_starts={};self.buffer_intervals=[]
    def acquire(self,release):
        if not self.ready:
            i=min(range(self.instances),key=self.factory_free.__getitem__)
            groups=sorted(range(len(self.buffer_free)),key=self.buffer_free.__getitem__)[:self.batch]
            assert all(math.isfinite(self.buffer_free[g]) for g in groups)
            # A batch begins only when its finite output buffers are available.
            end=max(release,self.factory_free[i],*(self.buffer_free[g] for g in groups))+self.cycles
            self.factory_free[i]=end;self.cost+=self.qubits*self.cycles;self.batches+=1
            for g in groups:
                self.buffer_free[g]=math.inf
                self.buffer_starts[g]=end
                heapq.heappush(self.ready,(end,g))
        return heapq.heappop(self.ready)
    def buffer_ids(self,g):
        return tuple(1091+g*self.width+i for i in range(self.width))
    def release(self,g,time):
        assert not math.isfinite(self.buffer_free[g])
        assert time>=self.buffer_starts[g]
        self.buffer_intervals.append((g,self.buffer_starts.pop(g),time))
        self.buffer_free[g]=time
    def peak_occupancy(self):
        events=[];by_group=collections.defaultdict(list)
        for g,start,end in self.buffer_intervals:
            events.extend(((start,self.width),(end,-self.width)))
            by_group[g].append((start,end))
        for intervals in by_group.values():
            intervals.sort()
            assert all(b[0]>=a[1]-1e-6 for a,b in zip(intervals,intervals[1:]))
        count=peak=0
        for _,change in sorted(events):
            count+=change;peak=max(peak,count)
            assert 0<=count<=len(self.buffer_free)*self.width
        assert count==0 and not self.ready and not self.buffer_starts
        return peak


def replay(ops,fixture,source,backend):
    d=fixture.d; pL=.1*(.1)**((d+1)/2)
    prod=Production(source['qubits'],source['cycles'],source['batch'],fixture.factory_area,fixture.buffer_qubits,1 if backend=='T' else 3)
    last=collections.defaultdict(float); corridor=collections.defaultdict(float)
    resource_latencies=[]; and_latencies=[]; component_work=collections.Counter()
    resource_error=0.;logical_active_cycles=0.;resource_store_cycles=0.
    resource_routes=0;growth_work=0.;growth_error=0.;protected_idle_cycles=0.
    low_distance_store_error=0.;low_distance_store_work=0.
    def one(gate,qs,duration,paths=(),release=0.,work_key='logical_ops'):
        nonlocal logical_active_cycles
        cells=set(p for path in paths for p in path[1:-1])
        start=max([release]+[last[q] for q in qs]+[corridor[p] for p in cells])
        end=start+duration
        for q in qs:last[q]=end
        for p in cells:corridor[p]=end
        logical_active_cycles+=(len(qs)+len(cells))*duration
        component_work[work_key]+=(len(qs)+len(cells))*2*d*d*duration
        return end
    def pair(a,b,key='logical_ops'):
        return one('CX',(a,b),2*d,[fixture.path(fixture.xy(a),fixture.xy(b))],work_key=key)
    def resource(qs):
        nonlocal resource_error,resource_routes,growth_work,growth_error,low_distance_store_error,low_distance_store_work,protected_idle_cycles
        request=max(last[q] for q in qs)
        ready,group=prod.acquire(request)
        buffers=prod.buffer_ids(group)
        # Logical bridge proxy: output distance -> common computation distance.
        # This is an added sensitivity allowance, not a simulated code switch.
        # All outputs of a batch enter their already-reserved full-distance
        # buffer immediately at acceptance. This is a scheduled operation,
        # not retroactive growth on a later consumer's request.
        growth=d;growth_start=ready;finish=growth_start+growth
        assert all(last[b]<=growth_start+1e-6 for b in buffers)
        low_wait=growth_start-ready
        low_distance_store_error+=len(qs)*low_wait*.1*(.1)**((source['output_distance']+1)/2)
        low_distance_store_work+=len(qs)*low_wait*2*source['output_distance']**2
        growth_work+=len(qs)*2*d*d*growth
        growth_error+=len(qs)*growth*.1*(.1)**((source['output_distance']+1)/2)
        paths=[fixture.path(fixture.xy(b),fixture.xy(q)) for b,q in zip(buffers,qs)]
        route_end=one('delivery',tuple(qs)+buffers,2*d,paths,release=finish,work_key='resource_delivery')
        store=max(0.,route_end-2*d-finish)
        protected_idle_cycles+=len(qs)*store
        resource_routes+=sum(len(path)-2 for path in paths)
        resource_error+=source['output_error']
        resource_latencies.append(route_end-request)
        return group,buffers,finish
    def consume(group,buffers,finish,end):
        nonlocal resource_store_cycles
        # Count residence through final consumption, including route and feedback.
        resource_store_cycles+=len(buffers)*max(0.,end-finish)
        prod.release(group,end)
    def compute_AND(a,b,t):
        start=max(last[a],last[b],last[t])
        if backend=='T':
            one('H',(t,),d)
            g,bs,finish=resource((t,));one('T_inject',(t,)+bs,d,work_key='final_injection');end=one('feedback',(t,)+bs,fixture.feedback,work_key='classical_wait');consume(g,bs,finish,end)
            for x,z in ((a,t),(b,t),(t,a),(t,b)):pair(x,z)
            # The 3 T/Tdagger layer is genuinely parallel except shared paths
            # and factory supply. Correction branches are conservatively waited.
            for q in (a,b,t):
                g,bs,finish=resource((q,));one('T_inject',(q,)+bs,d,work_key='final_injection');end=one('feedback',(q,)+bs,fixture.feedback,work_key='classical_wait');consume(g,bs,finish,end)
            pair(t,a);pair(t,b);one('H',(t,),d);one('S',(t,),d)
        else:
            # Existing CCZ teleportation: 3 resource halves, 3 CNOTs,
            # Z measurements and outcome-controlled Clifford corrections.
            one('H',(t,),d);g,bs,finish=resource((a,b,t))
            one('three_CX',(a,b,t)+bs,2*d,work_key='final_injection')
            one('measure_resources',bs,d,work_key='final_injection')
            end=one('feedback',(a,b,t)+bs,fixture.feedback,work_key='classical_wait');consume(g,bs,finish,end)
            # Conservative all-branches schedule, not a favourable outcome.
            for x,z in ((a,b),(a,t),(b,t)):pair(x,z,'ccz_Clifford_fixup')
            one('Z_fixups',(a,b,t),d,work_key='ccz_Clifford_fixup');one('H',(t,),d)
        and_latencies.append(max(last[a],last[b],last[t])-start)
    def execute(gate,qs):
        if gate=='AND':compute_AND(*qs)
        elif gate=='CNOT':pair(*qs)
        elif gate=='H':one(gate,qs,d)
        elif gate=='UNAND':
            a,b,t=qs;one('H',(t,),d);one('MX',(t,),d)
            one('feedback',(a,b,t),fixture.feedback,work_key='classical_wait')
            pair(a,b,'measured_inverse_fixup');one('reset',(t,),d)
        else:raise ValueError(gate)
    def segment_schedule(segment):
        # Ordinary dependency-list scheduling: reorder only disjoint macros.
        # Same policy for both resource types. No quantum rewrite/synthesis.
        predecessors=[set() for _ in segment]
        successors=[[] for _ in segment]
        tail={}
        for i,(_,qs) in enumerate(segment):
            for q in qs:
                if q in tail:predecessors[i].add(tail[q])
                tail[q]=i
            for j in predecessors[i]:successors[j].append(i)
        pending=[len(p) for p in predecessors]
        ready=[]
        def push(i):
            heapq.heappush(ready,(max(last[q] for q in segment[i][1]),i))
        for i,n in enumerate(pending):
            if not n:push(i)
        done=0
        while ready:
            _,i=heapq.heappop(ready)
            execute(*segment[i]);done+=1
            for j in successors[i]:
                pending[j]-=1
                if not pending[j]:push(j)
        assert done==len(segment)
    # Preserve whole-layer and phase barriers: noncommuting blocks never overlap.
    layer=-1;segment=[]
    def flush():
        segment_schedule(segment)
        segment.clear()
        barrier=max(last.values(),default=0.)
        for q in range(1091):last[q]=barrier
    for gate,qs,li,pauli in ops:
        if li!=layer:
            flush();layer=li
        if gate=='PHASE_INTERFACE_UNTIMED':flush()
        else:segment.append((gate,qs))
    flush()
    cycles=max(last.values())
    # A conservative memory proxy reserves all existing baseline qubits.
    data_memory=1091*cycles*pL
    route_gate_error=logical_active_cycles*pL
    resource_store_error=resource_store_cycles*pL
    gates=len(and_latencies)
    error=resource_error+growth_error+data_memory+route_gate_error+resource_store_error+low_distance_store_error
    component_work['factory_intrinsic']=prod.cost
    component_work['output_growth_proxy']=growth_work
    component_work['low_distance_storage']=low_distance_store_work
    component_work['protected_resource_idle_storage']=protected_idle_cycles*2*d*d
    active_work=sum(component_work.values())
    qseconds=fixture.total_qubits*cycles*400e-9
    return {'status':'MATCHED_LOGICAL_RESOURCE_MODEL_ONLY_NOT_PHYSICAL_BENCHMARK',
            'backend':backend,'AND_completed_in_model':gates,'factory_instances':prod.instances,
            'factory_batches':prod.batches,'cycles':cycles,'runtime_seconds':cycles*400e-9,
            'fixed_fixture_physical_qubits':fixture.total_qubits,'reserved_qubitseconds':qseconds,
            'intrinsic_component_qubitseconds':{k:v*400e-9 for k,v in component_work.items()},
            'component_metric':'active operation volume excludes holding data memory; reserved volume is separate',
            'AND_service_latency_us':{'mean':statistics.mean(and_latencies)*.4,'p50':percentile(and_latencies,.5)*.4,'p95':percentile(and_latencies,.95)*.4,'p99':percentile(and_latencies,.99)*.4,'max':max(and_latencies)*.4},
            'resource_request_to_ready_us':{'mean':statistics.mean(resource_latencies)*.4,'p50':percentile(resource_latencies,.5)*.4,'p95':percentile(resource_latencies,.95)*.4,'p99':percentile(resource_latencies,.99)*.4,'max':max(resource_latencies)*.4},
            'throughput_AND_per_second':gates/(cycles*400e-9),'error_union_proxy':error,
            'error_components':{'factory_output':resource_error,'output_growth_proxy':growth_error,'data_memory':data_memory,'route_and_gate':route_gate_error,'protected_resource_buffer':resource_store_error,'low_distance_buffer':low_distance_store_error},
            'resource_buffer_qubitcycles':resource_store_cycles,'strict_same_physical_noise':False,
            'strict_full_program_contract_validated':False,'measured_logical_error_rate':None,
            'produced_resource_count':prod.batches*prod.batch,'finite_buffer_logical_qubits':fixture.buffer_qubits,
            'peak_reserved_output_buffer_qubits':prod.peak_occupancy(),
            'routing_corridor_tile_traversals':resource_routes,
            'retry_status':'expected accepted cadence from source; stochastic retry tails NOT sampled',
            'scheduler':'ordinary dependency list, earliest known operand release, source index tie-break; not global optimum',
            'buffer_policy':'grow all accepted batch outputs immediately in finite reserved full-distance slots',
            'output_bridge_status':'d-cycle allowance using output dx only; anisotropic-source-to-SC fidelity NOT certified',
            'error_status':'uncertified overlapping location allowances; NOT a physical failure probability'}


def verify_ccz_injection():
    # Exact diagonal Kraus amplitudes of CCZ|+++> + 3 CX + MZ.
    # Correct phase polynomial f(x xor m)+f(x), then strip global f(m).
    maxerr=0.;cases=0
    for m in range(8):
        ma,mb,mc=((m>>i)&1 for i in (2,1,0))
        for x in range(8):
            a,b,c=((x>>i)&1 for i in (2,1,0))
            phase=((a^ma)&(b^mb)&(c^mc))
            correction=(ma*b*c)^(mb*a*c)^(mc*a*b)^(ma*mb*c)^(ma*mc*b)^(mb*mc*a)
            actual=(-1)**(phase^correction^ (ma*mb*mc))/math.sqrt(8)
            expected=(-1)**(a*b*c)/math.sqrt(8)
            maxerr=max(maxerr,abs(actual-expected));cases+=1
    assert maxerr<1e-15
    return {'basis_amplitudes':cases,'measurement_branches':8,'max_error':maxerr,
            'scope':'ideal CCZ injection channel identity, no physical noise validation'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--distance',type=int,default=29)
    args=parser.parse_args()
    scan=ccz_factory_scan();ops,tr=trace();fixture=Fixture(args.distance)
    source=json.loads((OUT/'factory_audit.json').read_text())
    ap=source['distillation']['best_within_limited_scan']; cp=scan['best']
    a={'qubits':ap['qubits'],'cycles':ap['expected_cycles_per_accepted_batch'],'batch':4,
       'output_error':ap['output_error_proxy'],'output_distance':ap['distances'][3]}
    c={'qubits':cp['qubits'],'cycles':cp['cycles_per_accepted_batch'],'batch':1,
       'output_error':cp['output_error_proxy'],'output_distance':cp['distances'][3]}
    metadata={'distance':fixture.d,'p_physical_scale':.001,'cycle_seconds':400e-9,
              'physical_noise_status':'Scale fixed; complete matched physical circuits unavailable',
              'logical_noise_proxy':'pL=.1*(100p)^((d+1)/2), independent-location union accounting',
              'logical_cells':[36,32],'corridor_tile_grid':[fixture.width,fixture.height],
              'occupied_logical_slots_reserved':1091,'output_buffer_slots_reserved':fixture.buffer_qubits,'tile_qubits':2*fixture.d**2,
              'factory_capacity_physical_qubits':64000,'classical_feedback_cycles':25,
              'static_coordinates':'buffer sites 0..11; computation q uses row-major site q+12; centres (2*column+1,2*row+1)',
              'resource_entry_port':[0,0],'routing':'deterministic corridor paths, exclusive cell reservation',
              'layout_status':'NEW EXPLICIT BENCHMARK FIXTURE, NOT THE RECOVERED 200-QUBIT CHIP',
              'timing_status':'2d logical route/CX proxy; d Clifford/injection/reset proxy; no circuit-level certification'}
    (OUT/'common_delivery_fixture.json').write_text(json.dumps(metadata,indent=2))
    rows=[replay(ops,fixture,a,'T'),replay(ops,fixture,c,'CCZ')]
    cultiv={'status':'NOT_ADMITTED_TO_DELIVERED_GATE_COMPARISON','runtime_seconds':None,
            'reserved_qubitseconds':None,'mean_latency':None,'p50':None,'p95':None,'p99':None,
            'throughput':None,'delivered_error':None,
            'reason':['d5 real-T S-proxy/erratum validation missing','grafted-to-common-SC growth circuit missing',
                      'consumption/delivery fidelity missing','400ns clock with 10us decoder wait needs resimulation'],
            'factory_produced_error_proxy':2e-9,'per_T_residual_delivery_budget':source['workload']['GSJ_delivery_error_margin_per_output']}
    result={'strict_benchmark_status':'INCOMPLETE_NO_THREE_WAY_PHYSICAL_WINNER',
            'benchmark_scope':'Existing HWP carry sandwich, same semantic AND task and static logical corridor fixture',
            'full_200_logical_program_benchmark':False,'trace':tr,'fixture':metadata,'ccz_factory_scan':scan,
            'gate_verification':verify_ccz_injection(),'resource_model_rows':rows,'cultivation':cultiv,
            'missing_shared_input':['complete certified phase/tower timing','three physical factory interfaces with common noise',
                                    'validated output growth and gate delivery','actual fixed hardware control/decoder timing'],
            'strongest_decoder_benchmark':'not run; fixed pL proxy is not decoder measurement'}
    (OUT/'delivered_benchmark.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'strict_status':result['strict_benchmark_status'],'trace':tr,'ccz_best':cp,'rows':rows,'cultivation_status':cultiv['status']},indent=2))


if __name__=='__main__':main()
