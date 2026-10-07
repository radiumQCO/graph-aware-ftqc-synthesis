"""Independent stored-circuit resource counts and extremal-input checks."""
import collections
import gzip
import hashlib
import json
import re
from pathlib import Path

from circuits import Circuit,depth,expanded
from scaling import cycle,grid

HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'scaling_results.json').read_text())
with gzip.open(HERE/'circuits.json.gz','rt',encoding='utf8') as f:records=json.load(f)
assert hashlib.sha256((HERE/'circuits.json.gz').read_bytes()).hexdigest()==r['circuit_archive_sha256']
assert hashlib.sha256((HERE/'c4_results.json').read_bytes()).hexdigest()==r['c4_result_sha256']
lookup={(x['case'],m['name']):m for x in r['cases'] for m in x['methods']}
assert len(lookup)==len(records)
checks=0
for record in records:
    name=record['case'];n=record['data_qubits'];m=lookup[(name,record['method'])]
    gates=[(g[0],tuple(g[1]),*g[2:]) for g in record['gates']]
    counts=collections.Counter(g[0] for g in gates)
    assert counts['AND']==m['AND_compute']==m['CCZ_resource_compute']
    assert counts['M_AND']==m['AND_compute']==m['cleanup_X_measurements']
    assert m['fixed_T_compute']==4*counts['AND']
    assert counts['P']==m['rotation_count']
    assert [g[2] for g in gates if g[0]=='P']==m['angle_multipliers']
    assert record['total_qubits']-n==m['clean_ancillas_excluding_magic_injection']
    assert counts['CNOT']==m['CNOT_full_sandwich_macro']
    assert depth(expanded(gates))==m['expanded_logical_depth']
    if name.startswith('C'):
        edges=cycle(n);checker=[i%2 for i in range(n)]
    else:
        periodic='torus' in name;copies=2 if name.startswith('two_') else 1
        width,height=map(int,name.rsplit('_',1)[1].split('x'))
        edges,_=grid(width,height,periodic,copies)
        checker=[((i%(width*height))%width+(i%(width*height))//width)%2 for i in range(n)]
    patterns=[[0]*n,[1]*n,checker,[1-x for x in checker]]
    pair=[0]*n
    for v in edges[0]:pair[v]=1
    patterns.append(pair)
    if name.startswith('two_'):patterns.append(checker[:n//2]+[0]*(n//2))
    c=Circuit(n,record['method']);c.width=record['total_qubits'];c.full=lambda:gates
    for bits in patterns:
        assert c.verify(bits)==sum(bits[a]^bits[b] for a,b in edges)
        checks+=1

reference=HERE.parents[0]/'results/paper_counts_proxy.structure.json'
if reference.exists():
    old=json.loads(reference.read_text())
    # The old reconstruction labels alternate rows in reverse (snake order).
    relabel=[(i//10)*10+(i%10 if (i//10)%2==0 else 9-i%10) for i in range(100)]
    assert len(set(relabel))==100
    native={tuple(sorted((relabel[a],relabel[b]))) for a,b in grid(10,10,True)[0]}
    assert {tuple(sorted(e)) for e in old['edges']}==native

report=HERE.parents[1]/'docs/graph_cut_phase_synthesis.md'
text=report.read_text(encoding='utf8')
assert not any(ord(c)<32 and c not in '\n\t' for c in text),'Bad escaped LaTeX/control character'
assert text.rstrip().endswith('are not established.')
assert 'A. real scalable reduction found' in text
links=0
for target in re.findall(r'\]\(([^)]+)\)',text):
    if '://' in target:continue
    p=(report.parent/target.split('#')[0]).resolve()
    if p.name!='artifact_verification.json':assert p.exists(),str(p)
    links+=1
result={'stored_circuits_checked':len(records),'independent_extremal_circuit_cases':checks,
        'resource_counts_and_recorded_depths':'passed','checkerboard_maxcuts':'passed',
        'periodic_reference_edge_set':'matched after explicit snake-label permutation',
        'row_major_to_reference_snake_labels':relabel,'report_links_checked':links,
        'C4_first_sha256':r['c4_result_sha256'],'circuit_archive_sha256':r['circuit_archive_sha256'],
        'scripts_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.py'))},
        'scope':'Exact ideal-circuit/input/resource accounting, not hardware/factory error validation'}
(HERE/'artifact_verification.json').write_text(json.dumps(result,indent=2),encoding='utf8', newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='scripts_sha256'},indent=2))
