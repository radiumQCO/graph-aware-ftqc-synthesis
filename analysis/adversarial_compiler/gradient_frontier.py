"""Parameter sweep of existing Qualtran QVR precision, not a new circuit."""
import json
import math
from pathlib import Path
import numpy as np
from qualtran.bloqs.rotations.hamming_weight_phasing import HammingWeightPhasingViaPhaseGradient
from qualtran.bloqs.rotations.phase_gradient import AddScaledValIntoPhaseReg,AddIntoPhaseGrad
from qualtran import QFxp
from qualtran.resource_counting import SympySymbolAllocator
import cirq
HERE=Path(__file__).resolve().parent
base=json.loads((HERE/'qualtran_resources.json').read_text())
rows=[]
for factor in (1,2,3,4,5,6,8,12,16):
    eps=base['EPS_radians_per_block']*factor
    pg={f:HammingWeightPhasingViaPhaseGradient(p['n'],p['angle']/np.pi,eps=eps) for f,p in base['families'].items()}
    b=max(int(p.b_grad) for p in pg.values());families={};count=0;error=0
    for f,p in base['families'].items():
        qvr=pg[f].phase_oracle;gate=AddScaledValIntoPhaseReg(qvr.cost_dtype,b,qvr.gamma,qvr.gamma_dtype)
        xs=np.array(cirq.LineQubit.range(qvr.cost_dtype.bitsize));grad=np.array(cirq.LineQubit.range(100,100+b))
        ops=list(cirq.flatten_op_tree(gate.decompose_from_registers(context=cirq.DecompositionContext(cirq.SimpleQubitManager()),x=xs,phase_grad=grad)))
        tof=sum(sum(int(v) for v in op.gate.build_call_graph(SympySymbolAllocator()).values()) for op in ops)
        values=[]
        for w in range(0,p['n']+1,2 if f.startswith('ZZ') else 1):
            bits=f'{w:0{qvr.cost_dtype.bitsize}b}'
            summed=0
            for op in ops:
                subx=int(''.join(bits[q.x] for q in op.qubits[:op.gate.x_bitsize]),2)
                summed+=op.gate.sign*op.gate.scaled_val(subx)
            assert summed%(2**b)==gate.scaled_val(w)%(2**b), (factor,f,w)
            angle=2*np.pi*gate.scaled_val(w)/(2**b)-p['angle']*w
            values.append(math.atan2(math.sin(angle),math.cos(angle)))
        diamond=2*math.sin((max(values)-min(values))/2)
        families[f]=dict(Toffoli_per_block=tof,actual_additions=len(ops),copies=p['copies_of_block'],diamond=diamond,
                         checked_weight_values=len(values),shifted_additions_verified=True)
        count+=tof*p['copies_of_block'];error+=diamond*p['copies_of_block']
    # Conservative charge for preparation with the EXACT SAME local synthesis precision.
    prep_upper=(b-3)*(.002/3/1708)
    rows.append(dict(eps_factor=factor,eps=eps,shared_gradient_bits=b,Toffoli_total=count,
                     HWP_AND_total=59597,rounding_diamond_sum=error,preparation_diamond_upper=prep_upper,
                     full_diamond_upper=error+prep_upper,admitted=error+prep_upper<=.002/3,families=families))
    print(factor,b,count,error,'admitted',rows[-1]['admitted'],flush=True)
best=min((r for r in rows if r['admitted']),key=lambda r:(r['Toffoli_total'],r['shared_gradient_bits']))
(HERE/'qualtran_frontier.json').write_text(json.dumps(dict(candidates=rows,selected=best,
    claim='lowest declared Toffoli count among TESTED official-QVR settings, not proof of global optimum'),indent=2))
