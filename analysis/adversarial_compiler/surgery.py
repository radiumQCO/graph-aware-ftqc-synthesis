"""Official TopoLS reference engine and WISQ portability probe.

TopoLS outputs are free-T topological proxies for unitary-lift blocks. They
are not a new factory/noise model, and not a CCZ/measurement-aware program.
"""
import argparse
import json
import sys
import time
import types
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'sources/compilers'

def wisq():
    package=types.ModuleType('wisq');package.__path__=[str(SOURCE/'wisq/src/wisq')];sys.modules['wisq']=package
    # Import the official routing API directly: the Java optimizer is not needed for scmr.
    try:
        from wisq.sarouting import sim_anneal_route
        sim_anneal_route([(0,)],{'width':3,'height':3,'alg_qubits':[4],'magic_states':[0]},[(0,4)],
                        temperature=10,cooling_rate=.1,termination_temp=.1,order_fraction=1,timeout=1)
        result={'status':'PORTABILITY_SMOKE_PASSED'}
    except Exception as e:result={'status':'PORTABILITY_SMOKE_FAILED','exception':type(e).__name__,'message':str(e)}
    import signal
    result['SIGALRM_available']=hasattr(signal,'SIGALRM')
    result['signal_alarm_available']=hasattr(signal,'alarm')
    result['scope']='official API, one-gate smoke, not workload benchmark; no algorithm modifications'
    (HERE/'wisq_portability.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

def topols(mode,variant):
    sys.path.insert(0,str(SOURCE/'TopoLS/src'))
    from topols.pipeline import prepare_graph
    from topols.driver import operation
    from topols.embedding.ports import calculate_space_time
    src=HERE/'circuits'/f'{mode}__ZZ_common__basic__block.{"input" if variant=="input" else "optimized"}.qasm'
    start=time.perf_counter();prep=prepare_graph(str(src),block_size_max=20,zx_opt=1,dir_opt=1,spread_num=0)
    print('prepared',prep.q_num,len(prep.rows),'layers',flush=True)
    state,pos,ori,paths,typ=operation(prep.circuit,prep.graph,prep.layer_labels,prep.layer_to_block,prep.block_info,
        prep.idx_to_row,prep.rows,prep.q_num,z_floor=1,seed_init_tuple=(17,1),time_bound=.02,
        iter_num=10,move_num=6,length=32,dir_opt=1,spread_num=0,hadamard_edges=prep.h_table,io_info=prep.io_info,backtrack=0)
    x,y,z,volume=calculate_space_time(pos,paths,state.x_min_floor,state.x_max_floor,state.y_min_floor,state.y_max_floor)
    result=dict(status='COMPLETE',method='TopoLS Python reference',mode=mode,input_variant=variant,
                logical_qubits=prep.q_num,layers=len(prep.rows),x=x,y=y,z=z,active_volume=volume,
                bounding_volume=x*y*z,compile_seconds=time.perf_counter()-start,
                model='same length=32, seeds=17,1; ten MCTS iterations, budget=.02 each call, free T supply',
                extrapolation='NO full-program qubit-seconds or failure claim')
    (HERE/f'topols_{mode}_{variant}.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('tool',choices=['wisq','topols']);p.add_argument('--mode',default='graph_tower');p.add_argument('--variant',default='input')
    a=p.parse_args();wisq() if a.tool=='wisq' else topols(a.mode,a.variant)
