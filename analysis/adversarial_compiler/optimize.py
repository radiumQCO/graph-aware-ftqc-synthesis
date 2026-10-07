"""Actual PyZX passes on fixed Clifford+T branches.

Temporary-AND cleanup is replaced by the adjoint of its 4T unitary lift.
Thus exports cost 8T per compute/cleanup pair, not the adaptive 4T cost.
This preserves the ideal clean-input isometry. It does not pretend measured
branches are unitary, or that a selected synthesis branch meets mixture error.
"""
import argparse
import gzip
import hashlib
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path
import numpy as np
import pyzx as zx
from importlib.metadata import version

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'graph_cut_phase'))
from circuits import expanded

def inverse(g,qs):
    return {'T':'TDAG','TDAG':'T','S':'SDAG','SDAG':'S'}.get(g,g),qs

def lift(ops):
    for g,qs in ops:
        if g=='AND':
            yield from ((h,tuple(w)) for h,w in expanded([(g,tuple(qs))]))
        elif g=='UNAND':
            yield from (inverse(h,tuple(w)) for h,w in reversed(expanded([('AND',tuple(qs))])))
        else: yield g,tuple(qs)

def as_circuit(ops,n_data=200):
    ops=list(lift(ops)); active=sorted(set(range(n_data))|{q for _,qs in ops for q in qs})
    mapping={q:i for i,q in enumerate(active)}
    c=zx.Circuit(len(active))
    names={'H':'HAD','S':'S','SDAG':'S','T':'T','TDAG':'T','CNOT':'CNOT','X':'NOT','Z':'Z'}
    for g,qs in ops:
        kw={'adjoint':True} if g in ('TDAG','SDAG') else {}
        c.add_gate(names[g],*(mapping[q] for q in qs),**kw)
    return c,active

def metrics(c):
    basic=c.to_basic_gates(); last=[0]*c.qubits; td=[0]*c.qubits
    for g in basic.gates:
        wires=[getattr(g,a) for a in ('control','target') if hasattr(g,a)]
        t=int(g.tcount()); level=max((last[q] for q in wires),default=0)+1
        tlevel=max((td[q] for q in wires),default=0)+t
        for q in wires:last[q]=level;td[q]=tlevel
    return dict(qubits=c.qubits,gates=len(basic.gates),T=int(c.tcount()),depth=max(last,default=0),T_depth=max(td,default=0),
                CNOT=sum(g.name=='CNOT' for g in basic.gates))

def equal(a,b):
    # Exact symbolic ZX certificate when simplification closes the difference.
    return bool(a.verify_equality(b))

def run_task(mode,family,method,scope,skip_verify=False):
    payload=json.loads(gzip.decompress((HERE/'programs.json.gz').read_bytes()))
    blocks=payload['programs'][mode]['blocks']
    if scope=='full':
        ops=[op for block in blocks for op in block['ops']]; multiplicity=1
    else:
        block=next(b for b in blocks if b['family']==family)
        ops=block['ops']; multiplicity=sum(b['family']==family for b in blocks)
    c,mapping=as_circuit(ops)
    stem=f'{mode}__{family}__{method}__{scope}'
    folder=HERE/'circuits'; folder.mkdir(exist_ok=True)
    original=c.to_qasm(); path=folder/(stem+'.input.qasm'); path.write_text(original)
    start=time.perf_counter(); random.seed(17); np.random.seed(17)
    if method=='basic': opt=zx.optimize.basic_optimization(c)
    elif method=='todd': opt=zx.optimize.full_optimize(c)
    elif method=='teleport':
        graph=c.to_graph(); graph=zx.simplify.teleport_reduce(graph)
        opt=zx.Circuit.from_graph(graph).to_basic_gates()
        opt=zx.optimize.basic_optimization(opt)
    else: raise ValueError(method)
    elapsed=time.perf_counter()-start
    outfile=folder/(stem+'.optimized.qasm'); outfile.write_text(opt.to_qasm())
    result={'mode':mode,'family':family,'scope':scope,'method':method,'library_version':version('pyzx'),
            'before':metrics(c),'after':metrics(opt),'multiplicity_in_workload':multiplicity,
            'compile_seconds':elapsed,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'output_sha256':hashlib.sha256(outfile.read_bytes()).hexdigest(),'mapping_original_slots':mapping,
            'export_contract':'unitary 8T compute/cleanup lift; fixed sampled positive-mixture branch',
            'certificate':'NOT_RUN'}
    (HERE/(stem+'.json')).write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='mapping_original_slots'}),flush=True)
    if skip_verify:return
    # Verification separated so a timeout cannot erase measured pass output.
    start=time.perf_counter()
    result['certificate']='ZX_identity' if equal(c,opt) else 'ZX_did_not_close_NOT_A_COUNTEREXAMPLE'
    result['verify_seconds']=time.perf_counter()-start
    (HERE/(stem+'.json')).write_text(json.dumps(result,indent=2))
    print('certificate',result['certificate'],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',required=True);p.add_argument('--family',default='ZZ_common')
    p.add_argument('--method',choices=['basic','teleport','todd'],default='todd');p.add_argument('--scope',choices=['block','full'],default='block')
    p.add_argument('--skip-verify',action='store_true')
    a=p.parse_args();run_task(a.mode,a.family,a.method,a.scope,a.skip_verify)
