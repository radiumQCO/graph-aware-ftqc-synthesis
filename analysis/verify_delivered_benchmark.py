"""Integrity, ideal-gate equivalence and resource-accounting checks only."""
import collections
import gzip
import hashlib
import json
import math
import re
from pathlib import Path

from delivered_benchmark import Fixture, Production, verify_ccz_injection
from weight_arithmetic_audit import and_isometry_audit, basis_audit

ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results/delivered_benchmark.json').read_text())
manifest=[m for m in json.loads((ROOT/'sources/factories/manifest.json').read_text()) if 'file' in m]
for item in manifest:
    p=ROOT/'sources/factories'/item['file']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],str(p)
p=ROOT/'results/carry_demand_trace.json.gz'
assert hashlib.sha256(p.read_bytes()).hexdigest()==r['trace']['trace_sha256']
with gzip.open(p,'rt',encoding='utf8') as f:trace=json.load(f)
counts=collections.Counter(op[0] for op in trace['operations'])
assert dict(counts)==r['trace']['counts']
assert counts['AND']==101*(200-(200).bit_count())+100*(400-(400).bit_count())==59597
assert counts['UNAND']==counts['AND']
assert len({op[2] for op in trace['operations']})==201
assert hashlib.sha256((ROOT/'results/paper_counts_proxy.costs.json').read_bytes()).hexdigest()==trace['source_cost_sha256']

f=Fixture()
coords=[f.xy(q) for q in range(1091+12)]
assert len(set(coords))==len(coords)
for q in range(1091):
    for b in (1091,1102):f.path(f.xy(b),f.xy(q))

# A factory batch must wait when every finite output buffer is occupied.
factory=Production(10,7,4,10,4,1)
first=[factory.acquire(0) for _ in range(4)]
assert all(ready==7 for ready,_ in first)
for _,g in first:factory.release(g,100)
ready,g=factory.acquire(0)
assert ready==107
rest=[(ready,g)]+[factory.acquire(0) for _ in range(3)]
for _,g in rest:factory.release(g,110)
assert factory.peak_occupancy()==4

for row in r['resource_model_rows']:
    assert row['AND_completed_in_model']==59597
    assert row['produced_resource_count']==(238388 if row['backend']=='T' else 59597)
    assert 0<row['peak_reserved_output_buffer_qubits']<=12
    assert math.isclose(row['reserved_qubitseconds'],8045090*row['runtime_seconds'])
    assert row['measured_logical_error_rate'] is None
    assert row['strict_same_physical_noise'] is False
assert r['strict_benchmark_status']=='INCOMPLETE_NO_THREE_WAY_PHYSICAL_WINNER'
assert r['cultivation']['runtime_seconds'] is None

report=ROOT.parent/'docs/delivered_non_clifford_benchmark.md'
links=[]
for link in re.findall(r'\]\(([^)]+)\)',report.read_text(encoding='utf8')):
    if '://' in link:continue
    target=(report.parent/link.split('#')[0]).resolve()
    if target.name=='delivered_verification.json':continue
    assert target.exists(),str(target)
    links.append(link)
result={'public_source_hashes_verified':len(manifest),'trace_counts_and_hash':'passed',
        'common_layout_unique_sites':len(coords),'buffer_corridor_paths_checked':2182,
        'finite_capacity_batch_backpressure':'passed','recorded_buffer_peak_capacity':'passed',
        'temporary_AND':and_isometry_audit(),'CCZ_injection':verify_ccz_injection(),
        'large_popcount_basis_checks':{str(n):basis_audit(n,[0,(1<<n)-1,1,1<<(n-1),int('10'*(n//2),2)]) for n in (200,400)},
        'relative_document_links_verified':len(links),
        'scope':'Model/input integrity and ideal identities ONLY; no full physical fidelity validation'}
(ROOT/'results/delivered_verification.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
