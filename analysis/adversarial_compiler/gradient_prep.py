"""Charge the shared gradient preparation with the same synthesis contract."""
import json
import random
import argparse
from pathlib import Path
from prepare import cc,DELTA,rotation,SEED
HERE=Path(__file__).resolve().parent

def main(frontier=False):
    pg=json.loads((HERE/'qualtran_resources.json').read_text())
    if frontier:
        chosen=json.loads((HERE/'qualtran_frontier.json').read_text())['selected']
        pg.update(chosen)
    b=pg['shared_gradient_bits']; rng=random.Random(SEED); records=[];ops=[]
    # Big endian gradient: P(-pi), P(-pi/2), P(-pi/4), then arbitrary angles.
    ops=[('H',(q,)) for q in range(b)]+[('Z',(0,)),('SDAG',(1,)),('TDAG',(2,))]
    for j in range(3,b):
        program,rec=rotation(-cc.mp.pi/(2**j),j,rng,f'gradient:{j}')
        ops+=program;records.append(rec)
    t=1+sum(r['T_actual'] for r in records)
    e=1+sum(r['T_expected'] for r in records)
    bound=pg['rounding_diamond_sum']+sum(r['diamond_bound'] for r in records)
    assert bound<float(cc.SYN_BUDGET)
    result={'gradient_bits':b,'arbitrary_rotation_calls':len(records),'T_sampled':t,'T_expected':e,
            'diamond_bound_preparation':sum(r['diamond_bound'] for r in records),'full_diamond_bound':bound,
            'full_T_if_7T_Toffoli':4*pg['HWP_AND_total']+7*pg['Toffoli_total']+t,
            'optimistic_4T_per_Toffoli_NOT_IMPLEMENTED':4*(pg['HWP_AND_total']+pg['Toffoli_total'])+t,
            'CCZ_if_ALL_AND_and_Toffoli_use_CCZ':pg['HWP_AND_total']+pg['Toffoli_total'],
            'peak_known_ancillas':806+b,'adder_scratch_ancillas':'UNKNOWN: leaf has no gate decomposition',
            'phase_add_depth':'UNKNOWN: resource call graph is not a schedule','ops':ops,'rotations':records}
    (HERE/('gradient_preparation_frontier.json' if frontier else 'gradient_preparation.json')).write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('ops','rotations')},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--frontier',action='store_true');a=p.parse_args();main(a.frontier)
