"""Stream full fixed branches in QASM2 and QC; no synthetic physical model."""
import gzip
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'graph_cut_phase'))
from circuits import expanded

def inverse(g):return {'T':'TDAG','TDAG':'T','S':'SDAG','SDAG':'S'}.get(g,g)
def lift(ops):
    for g,qs in ops:
        if g=='AND':yield from expanded([('AND',tuple(qs))])
        elif g=='UNAND':yield from ((inverse(h),w) for h,w in reversed(expanded([('AND',tuple(qs))])))
        else:yield g,qs
def normalize(block):
    # Ordinary clean-ancilla lifetime allocation, applied to EVERY method.
    # X arithmetic scratch and ZZ scratch do not overlap in time.
    for g,qs in block['ops']:
        yield g,tuple(q-400 if block['family'].startswith('X') and 600<=q<805 else q for q in qs)

def main():
    payload=json.loads(gzip.decompress((HERE/'programs.json.gz').read_bytes()))
    folder=HERE/'circuits';folder.mkdir(exist_ok=True)
    metadata={}
    for mode in ('qualtran_literal','even_tower','graph_tower'):
        blocks=payload['programs'][mode]['blocks']
        active=sorted(set(range(200))|{q for block in blocks for g,qs in normalize(block) for q in qs})
        mapping={q:i for i,q in enumerate(active)};counts={};last=[0]*len(active)
        path=folder/(mode+'__full.input.qasm')
        names={'CNOT':'cx','TDAG':'tdg','SDAG':'sdg','H':'h','T':'t','S':'s','Z':'z','X':'x'}
        with path.open('w') as f:
            f.write(f'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[{len(active)}];\n')
            for block in blocks:
                for g,qs in lift(normalize(block)):
                    qs=[mapping[q] for q in qs];counts[g]=counts.get(g,0)+1
                    end=max(last[q] for q in qs)+1
                    for q in qs:last[q]=end
                    f.write(names[g]+' '+','.join(f'q[{q}]' for q in qs)+';\n')
        metadata[mode]={'qubits':len(active),'T':counts.get('T',0)+counts.get('TDAG',0),'counts':counts,'ASAP_depth':max(last),
                        'path':str(path),'contract':'unitary lift, 8T per AND/cleanup; X/ZZ clean workspace reuse'}
        print(mode,metadata[mode]['qubits'],metadata[mode]['T'],flush=True)
    (HERE/'export_resources.json').write_text(json.dumps(metadata,indent=2))

if __name__=='__main__':main()
