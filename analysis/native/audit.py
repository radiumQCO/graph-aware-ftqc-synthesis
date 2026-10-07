"""Bounded native compiler checks on unchanged fixed synthesis branches.

Raw Hadamard-gadgetized output is not assumed to be a deterministic unitary.
This script does not change synthesis precision or perform physical simulation.
"""
import argparse
import cmath
import hashlib
import json
import math
from pathlib import Path
from run import HERE, PROJECT, SOURCES, job

INPUTS=HERE/'benchmark/inputs'
OUTPUTS=HERE/'benchmark/outputs'
OUTPUTS.mkdir(exist_ok=True)


def parse(path):
    labels=[];gates=[];active=False
    for raw in path.read_text().splitlines():
        line=raw.split('#',1)[0].strip()
        if line.startswith('.v '):labels=line.split()[1:]
        if line=='BEGIN':active=True;continue
        if line=='END':active=False
        if active and line:
            name,*qubits=line.split()
            gates.append((name,[labels.index(q) for q in qubits]))
    return labels,gates


def simulate(path,basis):
    labels,gates=parse(path)
    assert len(labels)<=8,'Tiny diagnostics only'
    state=[0j]*(1<<len(labels));state[basis]=1
    for name,qs in gates:
        if name=='H':
            bit=1<<qs[0]
            for i in range(len(state)):
                if not i&bit:
                    a,b=state[i],state[i|bit]
                    state[i]=(a+b)/math.sqrt(2);state[i|bit]=(a-b)/math.sqrt(2)
        elif name in ('T','T*','S','S*','Z'):
            angle={'T':math.pi/4,'T*':-math.pi/4,'S':math.pi/2,'S*':-math.pi/2,'Z':math.pi}[name]
            for i in range(len(state)):
                if all(i&(1<<q) for q in qs):state[i]*=cmath.exp(1j*angle)
        elif name in ('X','cnot','tof'):
            target=1<<qs[-1]
            for i in range(len(state)):
                if not i&target and all(i&(1<<q) for q in qs[:-1]):
                    state[i],state[i|target]=state[i|target],state[i]
        else:raise ValueError(name)
    return state


def gadget_check():
    source=INPUTS/'internal_h.qc'
    source.write_text('.v a\n.i a\n.o a\nBEGIN\nT a\nH a\nT a\nEND\n')
    result=job('fasttodd_internal_h',[HERE/'fasttodd-target/release/quantum_circuit_optimization.exe','FastTODD',source],SOURCES/'FastTODD',60)
    output=SOURCES/'FastTODD/circuits/outputs/internal_h.qc'
    if result['status']!='COMPLETE':return
    columns=[simulate(source,i) for i in (0,1)]
    expanded=[simulate(output,i) for i in (0,1)]
    projected=[c[:2] for c in expanded]
    ratios=[projected[j][i]/columns[j][i] for j in (0,1) for i in (0,1) if abs(columns[j][i])>1e-12]
    alpha=ratios[0]
    residual=max(abs(a-alpha) for a in ratios)
    leakage=[sum(abs(x)**2 for x in c[2:]) for c in expanded]
    result.update(output=str(output),output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                  output_qubits=len(parse(output)[0]),
                  zero_ancilla_projection_factor={'real':alpha.real,'imag':alpha.imag},
                  numerical_projection_residual=residual,probability_outside_clean_ancilla=leakage,
                  contract='Postselected equivalence only if projection is proportional; not a deterministic clean-ancilla unitary certificate.',
                  numerical_tolerance=1e-12)
    (HERE/'benchmark/internal_h_contract.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


def ppf(mode,block=False):
    suffix='__ZZ_common' if block else ''
    name=mode+suffix
    source=INPUTS/f'{name}.qc'
    if block:
        from prepare_inputs import convert
        original=HERE.parent/'adversarial_compiler/circuits'/f'{mode}__ZZ_common__basic__block.input.qasm'
        provenance=convert(original,source)
        provenance.update(scope='one representative fixed ZZ_common block, not a full-program result',source=str(original))
        (HERE/'benchmark'/f'{name}__input.json').write_text(json.dumps(provenance,indent=2))
    result=job('ppf_'+name,[HERE/'bin/feynopt.exe','-ppf',source,'+RTS','-M3G','-RTS'],PROJECT,90 if block else 240)
    result['scope']='representative block' if block else 'full program'
    if result['status']=='COMPLETE':
        log=Path(result['log']).read_text()
        start=log.find('\n.v ')
        if start<0:raise RuntimeError('No output circuit in completed Feynman log')
        output=OUTPUTS/f'{name}__ppf.qc'
        output.write_text(log[start+1:])
        labels,gates=parse(output)
        result.update(output=str(output),output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                      qubits=len(labels),T=sum(name in ('T','T*') for name,_ in gates),
                      equivalence='NOT_YET_CERTIFIED')
    (HERE/'benchmark'/f'{name}__ppf.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['gadget-check','even_tower','graph_tower'])
    parser.add_argument('--block',action='store_true')
    args=parser.parse_args();action=args.action
    if action=='gadget-check':gadget_check()
    else:ppf(action,args.block)
