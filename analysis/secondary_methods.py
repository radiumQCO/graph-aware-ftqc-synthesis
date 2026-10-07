"""Angle/error diagnostics and explicit existing phase-gradient costing.

These are derived resource formulas, not measured routed circuits.
Qualtran AddScaledValIntoPhaseReg counts (b_grad-2) Toffolis per addition.
I use ordinary exact 7-T Toffolis for this row; no free 4-T unitary Toffoli.
"""
import json
import math
from pathlib import Path
from compile_costs import groups, hwp_size, synth, SYN_BUDGET, mp, theta_for

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"

def main():
    for name in ("paper_counts_proxy","notebook_literal"):
        data=json.loads((OUT/f"{name}.structure.json").read_text())
        result={"case":name,"small_angle":[],"phase_gradient":[]}
        for mode in ("matching","global"):
            gs=groups(data,mode)
            num_rot=2*sum(hwp_size(g["n"])[1] for g in gs)
            delta=float(SYN_BUDGET)/num_rot
            phis=[]
            for g in gs:
                for k in range(hwp_size(g["n"])[1]):
                    # Bothe et al. use exp(+i phi Z), NOT exp(-i theta Z/2).
                    phi=float(theta_for(g["family"]))*2**k/2
                    phi=abs((phi+math.pi/8)%(math.pi/4)-math.pi/8)
                    phis.append(phi)
            result["small_angle"].append(dict(mode=mode,
                delta=delta,min_clifford_reduced_phi=min(phis),
                min_phi_squared_over_delta=min(p*p/delta for p in phis),
                conclusion="All angles in delta << phi^2 regime; no identity-underrotation saving established",
                contract="positive channel mixtures only; quasiprobability expectation-value task excluded"))
            count=2*len(gs)
            max_m=max(g["n"] for g in gs)
            # Angle rounding by nearest fixed point: |theta-theta_hat|<=pi/2^b.
            # Full block diamond error <=2*m*pi/2^b (safe, global phases ignored).
            # Reserve half synthesis budget for rounding and half for gradient prep.
            b=math.ceil(math.log2(4*count*max_m*math.pi/float(SYN_BUDGET)))
            prep_delta=SYN_BUDGET/(4*(b-2))
            prep=[synth(mp.pi/(2**i),prep_delta) for i in range(2,b)]
            toffoli=0
            ands=2*sum(hwp_size(g["n"])[0] for g in gs)
            for g in gs:
                theta=theta_for(g["family"],name=="notebook_literal")
                # Literal constant multiplier by shift/add, no imagined free oracle.
                q=int(mp.nint((theta/(2*mp.pi)%1)*2**b))%2**b
                toffoli+=2*q.bit_count()*(b-2)
            total=4*ands+7*toffoli+2*sum(r["t_count"] for r in prep)
            rounding=count*2*max_m*math.pi/2**b
            prep_err=2*sum(r["measured_diamond"] for r in prep)
            max_kb=max(sum(hwp_size(g["n"]))+(g["n"] if mode=="global" and g["pauli"]=="ZZ" else 0) for g in gs)
            result["phase_gradient"].append(dict(mode=mode,gradient_bits_per_instance=b,
                exact_toffoli_count=toffoli,hwp_and_count=ands,t_count=total,
                gradient_preparation_t=2*sum(r["t_count"] for r in prep),
                peak_additional_logical_qubits_before_routing=2*(max_kb+2*b),
                full_diamond_bound=rounding+prep_err,rounding_bound=rounding,
                t_depth_serial_upper=2*ands//2+7*toffoli//2+sum(r["t_count"] for r in prep),
                logical_primitive_depth_serial_upper=27*ands//2+15*toffoli//2+sum(r["primitive_depth"] for r in prep),
                ccz_demand_if_using_ccz_instead_of_7t_toffoli=toffoli,
                status="DERIVED literal shift-add variant; not best phase-gradient compiler; no routed schedule"))
        (OUT/f"{name}.secondary.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
        print(name,result,flush=True)

if __name__=="__main__":
    main()
