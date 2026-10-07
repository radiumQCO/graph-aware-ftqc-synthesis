"""Run actual pinned Qualtran APIs; no asymptotic T-fit is used here."""
import hashlib
import inspect
import json
import math
from collections import Counter
from pathlib import Path
import cirq
import numpy as np
from qualtran.bloqs.rotations.hamming_weight_phasing import HammingWeightPhasing, HammingWeightPhasingViaPhaseGradient
from qualtran.bloqs.rotations.phase_gradient import AddScaledValIntoPhaseReg, AddIntoPhaseGrad
from qualtran.bloqs.arithmetic import HammingWeightCompute
from qualtran.resource_counting import SympySymbolAllocator
from importlib.metadata import version

HERE=Path(__file__).resolve().parent
data=json.loads((HERE.parent/'results/paper_counts_proxy.costs.json').read_text())
groups=next(x for x in data['methods'] if x['method']=='hwp_global_joint_batch_in_circuit_tower_mixed_diagonal')['groups']
structure=json.loads((HERE.parent/'results/paper_counts_proxy.structure.json').read_text())
angles={a['family']:a['theta_radians'] for a in structure['angle_families']}
EPS=(.002/3)/(4*201)  # conservative full-diamond rounding budget half of synthesis share
probes={}
for family in sorted(angles):
    n=400 if family.startswith('ZZ') else 200
    # ZPow exponent is angle/pi, not the radian angle.
    hwp=HammingWeightPhasing(n,exponent=angles[family]/np.pi,eps=EPS)
    pg=HammingWeightPhasingViaPhaseGradient(n,exponent=angles[family]/np.pi,eps=EPS)
    qvr=pg.phase_oracle
    add=AddScaledValIntoPhaseReg(qvr.cost_dtype,qvr.b_grad,qvr.gamma,qvr.gamma_dtype)
    probes[family]={'n':n,'copies_of_block':sum(g['family']==family for g in groups),
                    'angle':angles[family],'gradient_bits':int(pg.b_grad),
                    'formula_bits':int(qvr.b_grad_via_formula),'optimized_bits':int(qvr.b_grad_via_fxp_optimization),
                    'gamma_bits':int(qvr.gamma_dtype.bitsize),'gamma_frac':int(qvr.gamma_dtype.num_frac),
                    'gamma_binary':str(qvr.gamma_fxp.bin()),'HWP_call_graph':{str(k):int(v) for k,v in hwp.build_call_graph(SympySymbolAllocator()).items()}}

b=max(p['gradient_bits'] for p in probes.values())
all_additions=0
for family,p in probes.items():
    n=p['n']; pg=HammingWeightPhasingViaPhaseGradient(n,exponent=p['angle']/np.pi,eps=EPS)
    qvr=pg.phase_oracle
    add=AddScaledValIntoPhaseReg(qvr.cost_dtype,b,qvr.gamma,qvr.gamma_dtype)
    x=np.array(cirq.LineQubit.range(qvr.cost_dtype.bitsize),dtype=object)
    grad=np.array(cirq.LineQubit.range(100,100+b),dtype=object)
    additions=list(cirq.flatten_op_tree(add.decompose_from_registers(context=cirq.DecompositionContext(cirq.SimpleQubitManager()),x=x,phase_grad=grad)))
    assert all(isinstance(op.gate,AddIntoPhaseGrad) for op in additions)
    toffoli=sum(int(sum(op.gate.build_call_graph(SympySymbolAllocator()).values())) for op in additions)
    errors=[]; weights=range(0,n+1,2) if family.startswith('ZZ') else range(n+1)
    for weight in weights:
        bits=f'{weight:0{qvr.cost_dtype.bitsize}b}'
        summed=0
        for op in additions:
            subx=int(''.join(bits[q.x] for q in op.qubits[:op.gate.x_bitsize]),2)
            summed+=op.gate.sign*op.gate.scaled_val(subx)
        assert summed%(2**b)==add.scaled_val(weight)%(2**b), (family,weight)
        phase=2*np.pi*add.scaled_val(weight)/(2**b)
        errors.append(math.atan2(math.sin(phase-p['angle']*weight),math.cos(phase-p['angle']*weight)))
    width=max(errors)-min(errors)
    p.update(shared_gradient_bits=b,actual_additions=len(additions),Toffoli_per_block=toffoli,
             abstract_additions=[dict(x_bits=int(op.gate.x_bitsize),right_shift=int(op.gate.right_shift),sign=op.gate.sign) for op in additions],
             maximum_phase_deviation=max(abs(e) for e in errors),exact_diagonal_diamond=2*math.sin(width/2),
             checked_weight_values=len(errors),HWC_AND=int(HammingWeightCompute(n).junk_bitsize),
             HWC_ancillas=int(HammingWeightCompute(n).junk_bitsize+HammingWeightCompute(n).out_bitsize))
    all_additions+=len(additions)*p['copies_of_block']

# A leaf really is resource-counted but lacks a gate decomposition; record this rather than invent one.
leaf=additions[0].gate
try:
    cirq.decompose(leaf.on_registers(x=x[:leaf.x_bitsize],phase_grad=grad),
                   keep=lambda op:isinstance(op.gate,(cirq.HPowGate,cirq.CXPowGate,cirq.ZPowGate,cirq.CCXPowGate)),
                   on_stuck_raise=lambda op:ValueError('Undecomposed leaf '+repr(op.gate)))
    export_status='leaf decomposable'
except Exception as e: export_status=f'{type(e).__name__}: {e}'
modules=[inspect.getfile(HammingWeightPhasing),inspect.getfile(AddScaledValIntoPhaseReg),inspect.getfile(type(qvr)),inspect.getfile(HammingWeightCompute)]
result={'qualtran_version':version('qualtran'),'cirq_version':version('cirq-core'),
        'EPS_radians_per_block':EPS,'shared_gradient_bits':b,'families':probes,
        'scaled_additions':all_additions,'Toffoli_total':sum(p['Toffoli_per_block']*p['copies_of_block'] for p in probes.values()),
        'HWP_AND_total':sum(p['HWC_AND']*p['copies_of_block'] for p in probes.values()),
        'rounding_diamond_sum':sum(p['exact_diagonal_diamond']*p['copies_of_block'] for p in probes.values()),
        'leaf_export_status':export_status,
        'source_files':{str(Path(m).name):{'path':m,'sha256':hashlib.sha256(Path(m).read_bytes()).hexdigest()} for m in modules}}
(HERE/'qualtran_resources.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
