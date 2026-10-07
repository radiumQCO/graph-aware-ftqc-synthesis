"""Run only after toy_c4.py. Exact exponent/circuit checks and resource vectors."""
import argparse
import collections
import gzip
import hashlib
import io
import itertools
import json
import math
import random
from pathlib import Path

from circuits import compact_c4,cycle_fan,direct_edge_phases,generic,grid_plaquettes,metrics

HERE=Path(__file__).resolve().parent

def cycle(n):return sorted({tuple(sorted((i,(i+1)%n))) for i in range(n)})
def grid(w,h,periodic=False,copies=1):
    edges=set();faces=[]
    def q(x,y,copy):return copy*w*h+(y%h)*w+(x%w)
    for copy in range(copies):
        for y in range(h):
            for x in range(w):
                for dx,dy in ((1,0),(0,1)):
                    if periodic or (x+dx<w and y+dy<h):edges.add(tuple(sorted((q(x,y,copy),q(x+dx,y+dy,copy)))))
        for y in range(h if periodic else h-1):
            for x in range(w if periodic else w-1):
                if (x+y)%2==0:faces.append((q(x,y,copy),q(x+1,y,copy),q(x+1,y+1,copy),q(x,y+1,copy)))
    if periodic:assert w%2==h%2==0 and w>=4 and h>=4
    counts=collections.Counter(tuple(sorted((f[i],f[(i+1)%4]))) for f in faces for i in range(4))
    assert all(count==1 for count in counts.values()) and counts.keys()<=edges
    if periodic:assert counts.keys()==edges
    return sorted(edges),faces

def assignments(n,shots):
    if n<=16:
        for mask in range(1<<n):yield [(mask>>i)&1 for i in range(n)]
    else:
        rng=random.Random(20261006+n)
        yield [0]*n;yield [1]*n
        for i in range(n):
            bits=[0]*n;bits[i]=1;yield bits
        for _ in range(shots):yield [rng.randrange(2) for _ in range(n)]

def anf_degrees(n,edges):
    width=(len(edges)//2).bit_length();degrees=[]
    vals=[sum(((x>>a)&1)^((x>>b)&1) for a,b in edges)//2 for x in range(1<<n)]
    for j in range(width):
        a=[(v>>j)&1 for v in vals]
        for k in range(n):
            for x in range(1<<n):
                if x&(1<<k):a[x]^=a[x^(1<<k)]
        degrees.append(max((x.bit_count() for x,v in enumerate(a) if v),default=0))
    return degrees

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--random-shots',type=int,default=1024)
    args=parser.parse_args()
    toy=json.loads((HERE/'c4_results.json').read_text())
    assert toy['status']=='C4_EXHAUSTIVELY_VERIFIED_BEFORE_SCALING' and toy['binary_AND_minimum']==2
    cases=[]
    for n in (4,6,8,10):cases.append((f'C{n}',n,cycle(n),None))
    for w,h in ((2,2),(2,3),(3,3),(3,4),(4,4)):
        edges,faces=grid(w,h);cases.append((f'open_{w}x{h}',w*h,edges,faces))
    for side in (4,6,8,10):
        edges,faces=grid(side,side,True);cases.append((f'torus_{side}x{side}',side*side,edges,faces))
    edges,faces=grid(10,10,True,2);cases.append(('two_torus_10x10',200,edges,faces))
    results=[];records=[]
    for name,n,edges,faces in cases:
        even=all(sum(v in edge for edge in edges)%2==0 for v in range(n))
        methods=[direct_edge_phases(n,edges),generic(n,edges)]
        if even:methods.append(generic(n,edges,True))
        methods.extend([generic(n,edges,even,True),generic(n,edges,even,True,True)])
        if faces is None:
            methods.extend([cycle_fan(n),cycle_fan(n,True),cycle_fan(n,True,True)])
            if n==4:methods.extend([compact_c4(),compact_c4(True)])
        else:
            methods.extend([grid_plaquettes(n,edges,faces,False),grid_plaquettes(n,edges,faces),grid_plaquettes(n,edges,faces,True,True),grid_plaquettes(n,edges,faces,True,True,True)])
        tests=0
        for bits in assignments(n,args.random_shots):
            target=sum(bits[a]^bits[b] for a,b in edges)
            for c in methods:assert c.verify(bits)==target,(name,c.name,bits)
            tests+=1
        # Every measurement branch on C4, not just deterministic outcomes.
        branch_tests=0
        if name=='C4':
            for bits in itertools.product((0,1),repeat=4):
                target=sum(bits[a]^bits[b] for a,b in edges)
                for c in methods:
                    k=metrics(c)['AND_compute']
                    for m in range(1<<k):assert c.verify(bits,m)==target;branch_tests+=1
        rows=[metrics(c) for c in methods]
        assert len({c.name for c in methods})==len(methods)
        row={'case':name,'vertices':n,'edges':len(edges),'even_cut_for_all_inputs':even,
             'edge_disjoint_C4_faces':len(faces or []),'cases_checked':tests,'exhaustive':n<=16,
             'all_C4_cleanup_branch_cases':branch_tests,'methods':rows,
             'proof_scope':'Exact C4 identity + checked edge partition + exact full-/half-adder identities prove all large inputs; samples test implementation.'}
        if faces is None:
            ds=anf_degrees(n,edges);low=max(ds)-1
            upper=next(m['AND_compute'] for m in rows if m['name']=='generic_even')
            assert low==upper
            row['binary_half_cut_ANF_degrees']=ds
            row['binary_half_cut_proved_AND_minimum']=low
        else:
            best=next(m for m in rows if m['name']=='generic_balanced_partial')
            new=next(m for m in rows if m['name']=='plaquette_balanced_partial')
            assert best['angle_multipliers']==new['angle_multipliers'],(name,best['angle_multipliers'],new['angle_multipliers'])
            row['saving_against_same_rotation_generic_partial']=best['AND_compute']-new['AND_compute']
            expected=len(faces)-1 if even and len(edges)==4*len(faces) else len(faces)
            assert row['saving_against_same_rotation_generic_partial']==expected
        results.append(row)
        for c in methods:records.append({'case':name,'method':c.name,'data_qubits':n,'total_qubits':c.width,'gate_fields':['kind','targets','angle_multiplier_if_P'],'gates':c.full()})
        print(json.dumps({'case':name,'verified':tests,'AND_R':{m['name']:[m['AND_compute'],m['rotation_count']] for m in rows}},ensure_ascii=False),flush=True)
    # Independent 8-row arithmetic checks for the two carry-save identities.
    for a,b,z in itertools.product((0,1),repeat=3):
        assert a+b+z==(a^b^z)+2*int(a+b+z>=2)
    for a,b in itertools.product((0,1),repeat=2):assert a+b==(a^b)+2*(a&b)
    archive=HERE/'circuits.json.gz'
    with archive.open('wb') as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as compressed,io.TextIOWrapper(compressed,encoding='utf8') as f:
        json.dump(records,f,separators=(',',':'))
    result={'cases':results,'seed':20261006,'random_shots':args.random_shots,
            'c4_result_sha256':hashlib.sha256((HERE/'c4_results.json').read_bytes()).hexdigest(),
            'circuit_archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
            'theorem':'For an edge-partition into q C4s, replace each by two weight-2 predicates using one AND; common downstream carry net saves q AND, or q-1 when all edges covered and global-even generic baseline removes one AND.'}
    (HERE/'scaling_results.json').write_text(json.dumps(result,indent=2),encoding='utf8', newline='\n')

if __name__=='__main__':main()
