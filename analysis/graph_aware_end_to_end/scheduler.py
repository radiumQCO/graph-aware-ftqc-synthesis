"""Conditional whole-program resource replay on the unchanged corridor fixture.

Not a physical surface-code circuit simulation. No complete shared noise model
or anisotropic-output bridge is available. Factory switching is a sensitivity
parameter, not a known reconfiguration protocol. Time units are 400 ns cycles.
"""
from __future__ import annotations

import hashlib
import heapq
import math
from collections import Counter, defaultdict
from functools import lru_cache

from workload import ANALYSIS
from delivered_benchmark import Fixture, percentile

CYCLE_SECONDS = 400e-9


class SharedProduction:
    """One area-compatible source at a time; independent finite inventory pools.

    CCZ uses 6 buffer qubits (two 3-qubit outputs), T uses 6 (four-output batches).
    Accepted outputs grow immediately. Unused final T surplus is drained/reset.
    Average retries are already in source cadence; retry tails are not sampled.
    """
    def __init__(self, sources, fixture, switch_cycles, concurrent=False):
        self.sources = sources; self.fixture = fixture; self.switch_cycles = switch_cycles
        self.concurrent=concurrent;self.instances={'CCZ':1,'T':3 if concurrent else 1}
        self.kind_free={k:[0.]*n for k,n in self.instances.items()}
        self.free = 0.; self.mode = None; self.switches = 0
        self.ready = {'CCZ': [], 'T': []}
        self.width = {'CCZ': 3, 'T': 1}
        self.offset = {'CCZ': 0, 'T': 6}
        self.buffree = {'CCZ': [0.]*2, 'T': [0.]*6}
        self.starts = {}; self.intervals = []
        self.batches = Counter(); self.intrinsic = Counter(); self.switch_work = 0.
        assert fixture.buffer_qubits == 12
        assert max(s['qubits'] for s in sources.values()) <= fixture.factory_area
        if concurrent:assert sum(sources[k]['qubits']*self.instances[k] for k in sources)<=fixture.factory_area
        else:assert sum(s['qubits'] for s in sources.values()) > fixture.factory_area

    def buffer_ids(self, kind, group):
        return tuple(1091+self.offset[kind]+group*self.width[kind]+i for i in range(self.width[kind]))

    def acquire(self, kind, release):
        src = self.sources[kind]
        if not self.ready[kind]:
            # Existing finite-inventory prefetch: one batch per installed source,
            # triggered when inventory empties; every surplus output is charged.
            count=src['batch']*self.instances[kind]
            groups = sorted(range(len(self.buffree[kind])), key=self.buffree[kind].__getitem__)[:count]
            assert all(math.isfinite(self.buffree[kind][g]) for g in groups)
            for i in range(self.instances[kind]):
                chosen=groups[i*src['batch']:(i+1)*src['batch']]
                available=self.kind_free[kind][i] if self.concurrent else self.free
                start=max(release,available,*(self.buffree[kind][g] for g in chosen))
                if not self.concurrent and self.mode is not None and self.mode!=kind:
                    start+=self.switch_cycles;self.switches+=1
                    self.switch_work+=self.fixture.factory_area*self.switch_cycles
                self.mode=kind;accepted=start+src['cycles']
                self.kind_free[kind][i]=accepted
                if not self.concurrent:self.free=accepted
                self.batches[kind]+=1;self.intrinsic[kind]+=src['qubits']*src['cycles']
                for g in chosen:
                    self.buffree[kind][g]=math.inf;self.starts[(kind,g)]=accepted
                    heapq.heappush(self.ready[kind],(accepted+self.fixture.d,g))
        return heapq.heappop(self.ready[kind])

    def consume(self, kind, group, end):
        start = self.starts.pop((kind,group))
        assert end >= start and math.isinf(self.buffree[kind][group])
        self.intervals.append((kind,group,start,end))
        self.buffree[kind][group] = end

    def drain(self, end):
        surplus = Counter()
        for kind in self.ready:
            while self.ready[kind]:
                ready,g = heapq.heappop(self.ready[kind]); surplus[kind] += 1
                end = max(end,ready)+self.fixture.d
                self.consume(kind,g,end)
        assert not self.starts
        return end, dict(surplus)

    def peak(self):
        events=[]; intervals=defaultdict(list)
        for kind,g,start,end in self.intervals:
            w=self.width[kind]; events.extend(((start,w),(end,-w)));intervals[(kind,g)].append((start,end))
        for values in intervals.values():
            values.sort(); assert all(b[0]>=a[1]-1e-7 for a,b in zip(values,values[1:]))
        current=peak=0
        for _,change in sorted(events):
            current += change; peak=max(current,peak); assert 0<=current<=12
        assert current==0
        return peak


class Replay:
    def __init__(self, program, inputs, policy, switch_cycles=29., correction='sampled_frame', factory_policy='time_multiplexed_Aprime'):
        self.program=program; self.policy=policy; self.correction=correction
        self.factory_policy=factory_policy
        self.fixture=Fixture(); self.d=self.fixture.d
        cp=inputs['delivery']['ccz_factory_scan']['best']
        tp=inputs['factory']['distillation']['best_within_limited_scan']
        self.sources={
            'CCZ': {'qubits':cp['qubits'],'cycles':cp['cycles_per_accepted_batch'],'batch':1,'error':cp['output_error_proxy']},
            'T': {'qubits':tp['qubits'],'cycles':tp['expected_cycles_per_accepted_batch'],'batch':4,'error':tp['output_error_proxy']}}
        concurrent=factory_policy=='concurrent_small_T_3'
        if concurrent:
            small=inputs['factory']['distillation']['factories']['small_15_to_15']
            self.sources['T']={'qubits':small['physical_qubits_including_measurement_ancillas'],
                               'cycles':small['expected_cycles_per_accepted_batch'],'batch':1,
                               'error':small['published_equations_output_error_proxy']}
        self.prod=SharedProduction(self.sources,self.fixture,switch_cycles,concurrent)
        self.last=defaultdict(float); self.corridor=defaultdict(float);self.unit=defaultdict(int)
        self.frame=defaultdict(lambda:[0,0]);self.count=Counter(); self.operation=Counter();self.route_work=Counter()
        self.route_tiles=Counter(); self.waits=defaultdict(list);self.layer_records=[]
        self.logical_work=0.; self.scratch_hold=0.; self.tower_hold=0.
        self.layer=-1;self.segment_id=0;self.ordinal=0;self.frame_flushes=0;self.feedbacks=0

    @lru_cache(maxsize=None)
    def path(self,a,b):
        return tuple(y*self.fixture.width+x for x,y in self.fixture.path(self.fixture.xy(a),self.fixture.xy(b))[1:-1])

    def one(self, gate, qs, duration, cells=(), release=0., key='Clifford', logical=True):
        cells=set(cells)
        start=max([release]+[self.last[q] for q in qs]+[self.corridor[c] for c in cells]);end=start+duration
        for q in qs:self.last[q]=end
        for c in cells:self.corridor[c]=end
        self.operation[key] += len(qs)*duration;self.route_work[key] += len(cells)*duration
        self.logical_work += (len(qs)+len(cells))*duration;self.count[gate]+=1
        if logical:
            t=max((self.unit[q] for q in qs),default=0)+int(duration>0)
            for q in qs:self.unit[q]=t
        return end

    def pauli_propagate(self,gate,qs):
        if self.correction != 'sampled_frame':return
        if gate=='H':
            f=self.frame[qs[0]];f[0],f[1]=f[1],f[0]
        elif gate in ('S','SDAG'):
            f=self.frame[qs[0]];f[1]^=f[0]
        elif gate=='CNOT':
            a,b=qs;self.frame[b][0]^=self.frame[a][0];self.frame[a][1]^=self.frame[b][1]
        elif gate=='CZ':
            a,b=qs;xa,xb=self.frame[a][0],self.frame[b][0]
            self.frame[a][1]^=xb;self.frame[b][1]^=xa

    def unary(self,gate,q,key='Clifford'):
        end=self.one(gate,(q,),self.d,key=key);self.pauli_propagate(gate,(q,));return end

    def pair(self,gate,a,b,key='Clifford'):
        cells=self.path(a,b);self.route_tiles[key]+=len(set(cells))
        end=self.one(gate,(a,b),2*self.d,cells,key=key);self.pauli_propagate(gate,(a,b));return end

    def flush_frames(self,qs):
        if self.correction != 'sampled_frame':return
        for q in qs:
            if any(self.frame[q]):
                self.one('Pauli_frame_flush',(q,),self.d,key='frame_materialization')
                self.frame[q]=[0,0];self.frame_flushes+=1

    def bits(self,tag,width):
        if self.correction=='conservative':return (1<<width)-1
        # Source-operation keys pair the unchanged phase/startup/X branches
        # across A/B and across scheduler policies, independent of execution order.
        digest=hashlib.sha256(f'20261006:{self.layer}:{self.segment_id}:{self.ordinal}:{tag}'.encode()).digest()
        return int.from_bytes(digest[:4],'little')&((1<<width)-1)

    def resource(self,kind,operands):
        request=max(self.last[q] for q in operands)
        ready,g=self.prod.acquire(kind,request);bs=self.prod.buffer_ids(kind,g)
        assert all(self.last[b]<=ready-self.d+1e-6 for b in bs)
        for b in bs:self.last[b]=ready
        cells=set(c for b,q in zip(bs,operands) for c in self.path(b,q))
        self.route_tiles['resource_delivery']+=len(cells)
        end=self.one('resource_delivery',tuple(operands)+bs,2*self.d,cells,ready,'resource_delivery',False)
        self.waits[kind].append(end-request)
        return g,bs,end

    def feedback(self,qs):
        self.feedbacks+=1
        return self.one('feedback',qs,self.fixture.feedback,key='feedback',logical=False)

    def compute_and(self,a,b,t):
        self.flush_frames((a,b,t));self.unary('H',t)
        g,bs,_=self.resource('CCZ',(a,b,t))
        # Delivery endpoint/merge geometry remains an unvalidated allowance.
        self.one('CCZ_injection_CX3',(a,b,t)+bs,2*self.d,key='CCZ_injection')
        self.one('CCZ_MZ3',bs,self.d,key='CCZ_injection')
        end=self.feedback((a,b,t)+bs);self.prod.consume('CCZ',g,end)
        m=self.bits('CCZ',3);ma,mb,mc=(m>>2)&1,(m>>1)&1,m&1
        for flag,pair in ((ma,(b,t)),(mb,(a,t)),(mc,(a,b))):
            if flag:self.pair('CZ',*pair,key='CCZ_CZ_corrections')
        zflags=(mb*mc,ma*mc,ma*mb)
        for q,flag in zip((a,b,t),zflags):
            if flag:
                if self.correction=='sampled_frame':self.frame[q][1]^=1;self.count['Z_frame_updates']+=1
                else:self.unary('Z',q,'CCZ_Z_corrections')
        self.unary('H',t)

    def uncompute_and(self,a,b,t):
        self.flush_frames((a,b,t));self.unary('H',t)
        self.one('MZ_for_X_readout',(t,),self.d,key='measured_inverse')
        self.feedback((a,b,t))
        if self.bits('UNAND',1):self.pair('CZ',a,b,'inverse_CZ_corrections')
        self.one('reset',(t,),self.d,key='measured_inverse');self.frame[t]=[0,0]

    def inject_t(self,q):
        self.flush_frames((q,));g,bs,_=self.resource('T',(q,))
        self.one('T_injection_CX',(q,)+bs,2*self.d,key='T_injection')
        self.one('T_MZ',bs,self.d,key='T_injection')
        end=self.feedback((q,)+bs);self.prod.consume('T',g,end)
        # Ordinary T injection needs an S correction on the wrong branch.
        if self.bits('T',1):self.unary('S',q,'T_S_corrections')

    def execute(self,gate,qs):
        if gate=='AND':self.compute_and(*qs)
        elif gate=='UNAND':self.uncompute_and(*qs)
        elif gate=='CNOT':self.pair(gate,*qs)
        elif gate=='T':self.inject_t(qs[0])
        elif gate in ('H','S','SDAG','X','Z'):self.unary(gate,qs[0])
        else:raise AssertionError(gate)

    def segment(self,ops):
        tails={};pred=[];succ=[[] for _ in ops]
        for i,(_,qs) in enumerate(ops):
            ps={tails[q] for q in qs if q in tails};pred.append(len(ps))
            for p in ps:succ[p].append(i)
            for q in qs:tails[q]=i
        rank=[0]*len(ops)
        for i in reversed(range(len(ops))):
            gate,qs=ops[i];cost=12 if gate=='AND' else 5 if gate=='UNAND' else 4 if gate=='T' else 1
            rank[i]=cost+max((rank[j] for j in succ[i]),default=0)
        ready=[]
        def push(i):
            gate,qs=ops[i];earliest=max(self.last[q] for q in qs)
            route=len(self.path(*qs)) if gate=='CNOT' else 0
            # Ordinary list-scheduler objectives; no claim of optimal schedules.
            priority=route if self.policy=='resource' else -rank[i] if self.policy=='depth' else .1*route-rank[i]
            heapq.heappush(ready,(earliest,priority,i))
        for i,n in enumerate(pred):
            if n==0:push(i)
        done=0
        while ready:
            _,_,i=heapq.heappop(ready);self.ordinal=i;self.execute(*ops[i]);done+=1
            for j in succ[i]:
                pred[j]-=1
                if pred[j]==0:push(j)
        assert done==len(ops)

    def barrier(self):
        end=max(self.last.values(),default=0.);unit=max(self.unit.values(),default=0)
        for q in range(1091):self.last[q]=end;self.unit[q]=unit
        return end

    def run(self):
        for block in self.program['blocks']:
            self.layer=block['id'];self.ordinal=0;start=self.barrier();phase_elapsed=0.
            for i,segment in enumerate(block['segments']):
                self.segment_id=i
                before=self.barrier();self.segment(segment);after=self.barrier()
                if block['id']>=0 and i==1:phase_elapsed=after-before
            end=self.barrier()
            self.scratch_hold += block['arithmetic_ancillas']*(end-start)
            self.tower_hold += block['tower_scratch']*phase_elapsed
            self.layer_records.append({'id':block['id'],'family':block['family'],'start':start,'end':end,'phase_cycles':phase_elapsed})
        self.flush_frames(tuple(range(1091)));end=self.barrier()
        end,surplus=self.prod.drain(end)
        runtime=end*CYCLE_SECONDS; tile=2*self.d*self.d
        buffer_hold=sum(self.prod.width[k]*(b-a) for k,_,a,b in self.prod.intervals)
        active_components={
            'data_memory':200*tile*end*CYCLE_SECONDS,
            'catalyst_memory':40*tile*end*CYCLE_SECONDS,
            'arithmetic_workspace_lifetime':self.scratch_hold*tile*CYCLE_SECONDS,
            'tower_scratch_lifetime':self.tower_hold*tile*CYCLE_SECONDS,
            'reserved_output_inventory_lifetime':buffer_hold*tile*CYCLE_SECONDS,
            'busy_routing_corridors':sum(self.route_work.values())*tile*CYCLE_SECONDS,
            'factory_intrinsic':sum(self.prod.intrinsic.values())*CYCLE_SECONDS,
            'factory_mode_switch_allowance':self.prod.switch_work*CYCLE_SECONDS,
        }
        pL=.1*(.1)**((self.d+1)/2)
        produced={k:self.prod.batches[k]*s['batch'] for k,s in self.sources.items()}
        output_error=sum(produced[k]*self.sources[k]['error'] for k in produced)
        growth=sum(produced[k]*self.prod.width[k]*self.d for k in produced)*.1*(.1)**11
        error_components={'produced_magic_state_proxy':output_error,'uncertified_output_dx21_growth_allowance':growth,
                          'reserved_patch_memory_proxy':1091*end*pL,'gate_path_proxy':self.logical_work*pL,
                          'buffer_residence_proxy':buffer_hold*pL}
        ledger=self.program['ledger']; wait={}
        for kind,values in self.waits.items():
            wait[kind]={name:val*.4 for name,val in {
                'mean':sum(values)/len(values),'p50':percentile(values,.5),'p95':percentile(values,.95),
                'p99':percentile(values,.99),'max':max(values)}.items()}
        return {
            'variant':ledger['variant'],'policy':self.policy,'correction_policy':self.correction,'factory_policy':self.factory_policy,
            'model_status':'WHOLE_LOGICAL_WORKLOAD_CONDITIONAL_RESOURCE_MODEL_NOT_PHYSICAL_VALIDATION',
            'factory_switch_cycles_assumed':self.prod.switch_cycles,'factory_mode_changes':self.prod.switches,
            'factory_peak_active_physical_qubits':sum(self.sources[k]['qubits']*self.prod.instances[k] for k in self.sources) if self.prod.concurrent else max(s['qubits'] for s in self.sources.values()),
            'factory_source_instances':self.prod.instances,
            'factory_capacity_physical_qubits':self.fixture.factory_area,'factory_batches':dict(self.prod.batches),
            'produced_resources':produced,'unused_final_surplus':surplus,
            'finite_buffer_logical_qubits':12,'peak_buffer_reserved_logical_qubits':self.prod.peak(),
            'peak_compilation_logical_qubits':ledger['peak_compilation_logical_qubits'],
            'conservative_peak_logical_including_buffer_capacity':ledger['peak_compilation_logical_qubits']+12,
            'reserved_physical_qubits':self.fixture.total_qubits,
            'SC_cycles_conditional':end,'runtime_seconds_conditional':runtime,
            'reserved_qubitseconds_conditional':self.fixture.total_qubits*runtime,
            'active_qubitseconds_conditional':sum(active_components.values()),
            'active_components_qubitseconds_conditional':active_components,
            'active_metric':'lifetime/corridor/factory union ledger; no addition to reserved area-time; endpoint allowances not fully embedded',
            'operation_volume_patchcycles':dict(self.operation),'routing_volume_tilecycles':dict(self.route_work),
            'routing_volume_qubitseconds_conditional':sum(self.route_work.values())*tile*CYCLE_SECONDS,
            'routing_corridor_traversals':dict(self.route_tiles),'actual_model_gate_counts':dict(self.count),
            'measurement_count':3*ledger['total_CCZ']+ledger['total_AND']+ledger['T_synthesis_sampled'],
            'feedback_wait_events':self.feedbacks,'Pauli_frame_materializations':self.frame_flushes,
            'all_to_all_logical_primitive_depth_conditional':max(self.unit.values(),default=0),
            'resource_request_through_delivery_us':wait,
            'synthesis_diamond_bound':ledger['synthesis_diamond_bound'],
            'physical_failure_sensitivity_proxy':sum(error_components.values()),'error_components':error_components,
            'proxy_plus_synthesis_NOT_validated_failure_probability':sum(error_components.values())+ledger['synthesis_diamond_bound'],
            'validated_physical_failure_rate':None,'strict_shared_circuit_noise':False,
            'factory_cold_start_and_reconfiguration_validation':'UNKNOWN beyond source accepted-cadence and explicit switch allowance',
            'reset_physical_timing_and_channel':'UNKNOWN; same d-cycle reset macro allowance as previous fixture',
            'retry_tail_status':'NOT SAMPLED; operation quantiles from expected-cadence replay only',
            'layers':self.layer_records,
        }
