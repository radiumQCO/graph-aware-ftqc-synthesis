"""Validate accounting, aggregate completed attempts, and hash audit artifacts.

This checks resource arithmetic and file provenance, NOT quantum equivalence
of the large optimized circuits. A timeout never becomes a zero-cost result.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE/name).read_text())


def main():
    ledger=read('logical_resources.json')
    export=read('export_resources.json')
    budget=.002/3
    for mode,r in ledger.items():
        assert r['AND']==r['measurements']==r['conditional_CZ']
        assert r['T_measured_AND_sampled']==4*r['AND']+r['rotation_T_sampled']
        assert r['diamond_bound']<=budget
        if mode in export:
            assert export[mode]['T']==8*r['AND']+r['rotation_T_sampled']
            assert export[mode]['qubits']==200+r['peak_ancillas']
    a,b=ledger['even_tower'],ledger['graph_tower']
    assert a['AND']-b['AND']==9900
    assert a['rotation_T_sampled']==b['rotation_T_sampled']
    assert a['T_measured_AND_sampled']-b['T_measured_AND_sampled']==39600
    pg=read('gradient_preparation_frontier.json')
    choice=read('qualtran_frontier.json')['selected']
    assert pg['full_diamond_bound']<=budget
    assert pg['CCZ_if_ALL_AND_and_Toffoli_use_CCZ']==choice['HWP_AND_total']+choice['Toffoli_total']
    assert pg['full_T_if_7T_Toffoli']==4*choice['HWP_AND_total']+7*choice['Toffoli_total']+pg['T_sampled']
    assert all(f['shifted_additions_verified'] for f in choice['families'].values())
    attempts={}
    for kind in ('basic','strong','full','feynman','surgery'):
        rows=read(kind+'_attempts.json')
        attempts[kind]={'statuses':dict(Counter(r['status'] for r in rows)),
                        'limits_seconds':sorted({r['timeout'] for r in rows}),
                        'ids':[r['id'] for r in rows]}
    block=[]
    for path in sorted(HERE.glob('*__basic__block.json')):
        r=json.loads(path.read_text())
        assert r['before']['T']==r['after']['T']
        for suffix,key in (('input','input_sha256'),('optimized','output_sha256')):
            f=HERE/'circuits'/(path.stem+'.'+suffix+'.qasm')
            assert hashlib.sha256(f.read_bytes()).hexdigest()==r[key]
        block.append({k:r[k] for k in ('mode','family','before','after','certificate')})
    assert len(block)==15
    tiny=read('tiny_optimizer_results.json')
    assert len(tiny)==6 and all(r['ZX_identity'] for r in tiny)
    pg_compare={'CCZ_extra_vs_graph':pg['CCZ_if_ALL_AND_and_Toffoli_use_CCZ']-b['AND'],
                'sampled_synthesis_T_saved_vs_graph':b['rotation_T_sampled']-pg['T_sampled'],
                'declared_7T_Toffoli_T_total':pg['full_T_if_7T_Toffoli'],
                'arbitrary_rotation_calls':pg['arbitrary_rotation_calls'],
                'rounding_additions':sum(f['actual_additions']*f['copies'] for f in choice['families'].values())}
    attempted_widths={}
    for mode in ('even_tower','graph_tower'):
        path=HERE/'circuits'/f'{mode}__ZZ_common__todd__full.input.qasm'
        with path.open() as f:
            header=''.join(next(f) for _ in range(3))
        attempted_widths[mode]=int(re.search(r'qreg q\[(\d+)\]',header)[1])
    result={'status':'LOGICAL_ACCOUNTING_VERIFIED_COMPILER_AUDIT_UNRESOLVED',
            'A':'Pinned Qualtran phase-gradient does not dominate graph in all resources',
            'B':'UNRESOLVED: strong large-circuit optimization did not complete',
            'C':'UNRESOLVED: no matched lattice-surgery result',
            'attempts':attempts,'completed_representative_basic_blocks':block,
            'tiny_exact_ZX_certificates':len(tiny),'phase_gradient_comparison':pg_compare,
            'historical_full_PyZX_attempt_qubits':attempted_widths,
            'graph_AND_saved':9900,'graph_4T_saved':39600,
            'physical_model_refinement':'STOPPED; no new physical numbers'}
    (HERE/'audit_summary.json').write_text(json.dumps(result,indent=2))
    files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts
           and p.name not in ('artifact_manifest.json',)]
    manifest={str(p.relative_to(HERE)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                                      'empty_failed_output':p.stat().st_size==0}
              for p in sorted(files)}
    (HERE/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='completed_representative_basic_blocks'},indent=2))


if __name__=='__main__':
    main()
