"""Lossless gate-format conversion of the already fixed audit branches.

No rotations are resynthesized. Non-data inputs remain known clean |0>.
All original wires are listed as outputs for an isometry check.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent/'adversarial_compiler'
OUT=HERE/'benchmark/inputs'
GATES={'h':'H','x':'X','z':'Z','s':'S','sdg':'S*','t':'T','tdg':'T*','cx':'cnot'}


def convert(path,out):
    counts=Counter()
    with path.open() as src,out.open('w') as dst:
        n=None
        for line in src:
            line=line.strip()
            if not line or line.startswith('//') or line.startswith(('OPENQASM','include')):continue
            if line.startswith('qreg'):
                n=int(re.search(r'\[(\d+)\]',line)[1])
                labels=[f'q{i}' for i in range(n)]
                dst.write('.v '+' '.join(labels)+'\n.i '+' '.join(labels[:200])+'\n.o '+' '.join(labels)+'\nBEGIN\n')
                continue
            name=line.split()[0]
            assert name in GATES, line
            qs=[int(q) for q in re.findall(r'q\[(\d+)\]',line)]
            counts[name]+=1
            dst.write(GATES[name]+' '+' '.join(f'q{q}' for q in qs)+'\n')
        dst.write('END\n')
    return dict(qubits=n,primary_inputs=200,T=counts['t']+counts['tdg'],counts=dict(counts),
                input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                output_sha256=hashlib.sha256(out.read_bytes()).hexdigest())


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records={}
    ledgers=json.loads((AUDIT/'export_resources.json').read_text())
    for mode in ('even_tower','graph_tower'):
        path=AUDIT/'circuits'/f'{mode}__full.input.qasm'
        records[mode]=convert(path,OUT/f'{mode}.qc')
        assert records[mode]['T']==ledgers[mode]['T']
        assert records[mode]['qubits']==ledgers[mode]['qubits']
    (OUT/'smoke.qc').write_text('.v a b\n.i a b\n.o a b\nBEGIN\nT a\nT a\ncnot a b\nT b\nT* b\ncnot a b\nEND\n')
    (HERE/'benchmark/input_manifest.json').write_text(json.dumps(records,indent=2))
    print(json.dumps(records,indent=2))


if __name__=='__main__':main()
