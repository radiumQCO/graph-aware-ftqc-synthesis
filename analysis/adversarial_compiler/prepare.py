"""Same workload, same local synthesis tolerance; existing circuits only.

Run with analysis/.venv/Scripts/python.exe. Cache writes stay in this directory.
"""
import gzip
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent
sys.path[:0] = [str(ANALYSIS), str(ANALYSIS/'graph_cut_phase'), str(ANALYSIS/'graph_aware_end_to_end')]
import compile_costs as cc
from circuits import Circuit, generic, expanded
from scaling import grid
from workload import rotation_program, tower, x_arithmetic, graph_arithmetic

cc.CACHE = HERE/'synthesis_cache.json'
if cc.CACHE.exists():
    cc.cache = json.loads(cc.CACHE.read_text())

DELTA = cc.SYN_BUDGET / 1708
SEED = 20261006

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rotation(angle, q, rng, label):
    rec = cc.synth_mixed(angle, DELTA)
    ops, info = rotation_program(cc.cache, rec, rng, q, label)
    return ops, info

def logical_depth(ops, t_only=False):
    last = Counter()
    for g, qs in ops:
        if g == 'UNAND':
            sub = [('H',(qs[2],)), ('M',(qs[2],)), ('conditional_CZ',qs), ('reset',(qs[2],))]
        elif g == 'AND':
            sub = [(x[0],x[1]) for x in expanded([(g,qs)])]
        else: sub = [(g,qs)]
        for h, wires in sub:
            end = max((last[q] for q in wires), default=0) + (int(h in ('T','TDAG')) if t_only else 1)
            for q in wires: last[q] = end
    return max(last.values(), default=0)

def build(mode, groups):
    rng = random.Random(SEED)
    edges, _ = grid(10,10,periodic=True,copies=2)
    xc, xu, xw, xa = x_arithmetic()
    if mode in ('graph_direct','graph_tower'):
        zc, zu, zw, za, _, _ = graph_arithmetic('B')
        zcoeff = [2**j for j in range(1,9)]
    elif mode == 'even_tower':
        zc, zu, zw, za, _, _ = graph_arithmetic('A')
        zcoeff = [2**j for j in range(1,9)]
    else:
        # Literal HWC via the same published three-to-two network.
        c = generic(200,edges,False,False,False)
        # Qualtran rotates even the known-zero output LSB. Charge/export it.
        if mode == 'qualtran_literal':
            output_lsb = 600
            c.phase(output_lsb,1)
        def snake(q):
            if q >= 200: return q
            copy, i = divmod(q,100); r,col = divmod(i,10)
            return 100*copy+10*r+(col if r%2==0 else 9-col)
        zc = [(g,tuple(snake(q) for q in qs)) for g,qs in c.compute]
        zu = [('UNAND' if g=='AND' else g,qs) for g,qs in reversed(zc)]
        pp = sorted((a,qs[0]) for _,qs,a in c.phases)
        zcoeff, zw = [a for a,q in pp], [q for a,q in pp]
        za = c.width-200
    banks = {f:list(range(1006+17*i,1006+17*(i+1))) for i,f in enumerate(sorted({g['family'] for g in groups}))}
    blocks, records = [], []
    if mode.endswith('tower'):
        startup=[]
        for f,bank in banks.items():
            base=cc.theta_for(f)*(2 if f.startswith('ZZ') else 1)
            for j,q in enumerate(bank[:8]):
                ops,rec=rotation(base*2**j,q,rng,f'catalyst:{f}:{j}')
                startup += [('H',(q,))]+ops; records.append(rec)
        blocks.append(dict(id=-1,family='startup',ops=startup))
    for group in groups:
        isx=group['pauli']=='X'; f=group['family']; basis=[('H',(q,)) for q in range(200)] if isx else []
        compute,undo,weights,coeff=(xc,xu,xw,[2**j for j in range(8)]) if isx else (zc,zu,zw,zcoeff)
        middle=[]
        if mode.endswith('tower'):
            base=cc.theta_for(f)*(1 if isx else 2)
            ops,rec=rotation(base*2**8,banks[f][15],rng,f'seed:{group["layer"]}:{f}')
            middle=tower(weights,banks[f],ops); records.append(rec)
        else:
            for a,q in zip(coeff,weights):
                ops,rec=rotation(cc.theta_for(f)*a,q,rng,f'phase:{group["layer"]}:{a}')
                middle+=ops; records.append(rec)
        blocks.append(dict(id=group['layer'],family=f,ops=basis+compute+middle+undo+basis[::-1]))
    counts=Counter(g for b in blocks for g,qs in b['ops'])
    synth_error=sum(r['diamond_bound'] for r in records)
    assert synth_error<=float(cc.SYN_BUDGET)
    measured_depth=sum(logical_depth(b['ops']) for b in blocks)
    ledger=dict(method=mode,macro_counts=dict(counts),rotation_calls=len(records),
                rotation_T_sampled=counts['T'],rotation_T_expected=sum(r['T_expected'] for r in records),
                rotation_T_max=sum(r['T_branch_max'] for r in records),
                AND=counts['AND'],CCZ_if_all_clean_AND=counts['AND'],
                T_measured_AND_sampled=4*counts['AND']+counts['T'],
                T_measured_AND_expected=4*counts['AND']+sum(r['T_expected'] for r in records),
                measurements=counts['UNAND'],conditional_CZ=counts['UNAND'],
                peak_ancillas=max(xa,za)+(85 if mode.endswith('tower') else 0),
                serial_block_ASAP_depth=measured_depth,
                serial_block_ASAP_T_depth=sum(logical_depth(b['ops'],True) for b in blocks),
                diamond_bound=synth_error,local_diamond_tolerance=str(DELTA))
    return dict(blocks=blocks,rotations=records,ledger=ledger)

def main():
    source=ANALYSIS/'results/paper_counts_proxy.costs.json'
    original=json.loads(source.read_text())
    selected=next(x for x in original['methods'] if x['method']=='hwp_global_joint_batch_in_circuit_tower_mixed_diagonal')
    modes=('qualtran_literal','qualtran_even_phase','graph_direct','even_tower','graph_tower')
    programs={}
    for mode in modes:
        print('Building',mode,flush=True)
        programs[mode]=build(mode,selected['groups'])
        print(json.dumps(programs[mode]['ledger']),flush=True)
    payload=dict(seed=SEED,precision_contract='same positive-mixture synthesizer and same local full-diamond tolerance on every arbitrary rotation',
                 total_execution_target=.002,synthesis_budget=float(cc.SYN_BUDGET),
                 groups=selected['groups'],source_sha256=digest(source),programs=programs)
    (HERE/'programs.json.gz').write_bytes(gzip.compress(json.dumps(payload,separators=(',',':')).encode(),mtime=0))
    (HERE/'logical_resources.json').write_text(json.dumps({k:v['ledger'] for k,v in programs.items()},indent=2))
    cc.CACHE.write_text(json.dumps(cc.cache,indent=2))

if __name__=='__main__': main()
