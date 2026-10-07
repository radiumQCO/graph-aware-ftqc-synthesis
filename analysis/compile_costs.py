"""Known-method cost audit. Counts actual pygridsynth gates, not asymptotic fits.

HWP formulas: Gidney 1709.06648; Qualtran HammingWeightCompute/Phasing.
Tower formulas: Sun & Koczor 2508.06236, in-circuit binary-angle tower.
Logical depth is an explicit unrouted primitive upper bound, NOT ISA cycles.
"""
import argparse
import json
import math
import sys
import time
import types
from collections import Counter
from pathlib import Path
from hwp_schedule import schedule as hwp_schedule

import mpmath as mp
# Numba's compiled helper DLL is blocked by Application Control on this host.
# Gridsynth itself is pure mpmath; only unrelated mixture utility decorators
# require numba at import time. Use their ordinary Python bodies, without loading
# that DLL or editing the installed package. No synthesized gate algorithm changes.
try:
    import numba
    NUMBA_MODE = "installed JIT available"
except ImportError:
    fallback = types.ModuleType("numba")
    def identity_njit(func=None, **kwargs):
        return func if func is not None else lambda f: f
    fallback.njit = identity_njit
    sys.modules["numba"] = fallback
    NUMBA_MODE = "pure Python decorator compatibility; blocked DLL not loaded"
from pygridsynth.gridsynth import gridsynth_gates, get_synthesized_unitary

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
CACHE = OUT / "synthesis_cache.json"
mp.mp.dps = 90
SYN_BUDGET = mp.mpf("0.002") / 3
cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}

def synth_mixed(theta, delta):
    """Published over/under-rotation + Clifford twirl mixed-diagonal recipe.

    Campbell 1612.02689, Kliuchnikov et al. 2203.10064.
    Analytic positive mixture; certify its actual Pauli-channel diamond error.
    This is not the published mixed-FALLBACK routine or its lower T-count fit.
    """
    key = "MIX|" + mp.nstr(theta,75) + "|" + mp.nstr(delta,75)
    if key in cache:
        return cache[key]
    eta = mp.sqrt(delta)
    branches = [synth(theta + sign*eta, eta/2) for sign in (-1,1)]
    vals=[]
    for r in branches:
        u = get_synthesized_unitary(r["gates"], dps=90)
        u /= mp.sqrt(mp.det(u))
        vals.append((mp.exp(1j*theta)*u[0,0]**2, abs(u[1,0])**2))
    z0,s0=vals[0]; z1,s1=vals[1]
    assert mp.im(z0)*mp.im(z1)<0
    p=-mp.im(z1)/(mp.im(z0)-mp.im(z1))
    assert 0<p<1
    z=p*z0+(1-p)*z1
    s=p*s0+(1-p)*s1
    error=1-mp.re(z)+s
    assert abs(mp.im(z))<mp.mpf("1e-70") and 0<=error<=delta
    expected=float(p)*branches[0]["t_count"]+float(1-p)*branches[1]["t_count"]
    r=dict(theta=mp.nstr(theta,75),delta=mp.nstr(delta,75),
           t_count=expected,branch_max_t_count=max(b["t_count"] for b in branches),
           primitive_depth=max(b["primitive_depth"] for b in branches)+2,
           measured_diamond=float(error),probability_first=mp.nstr(p,75),
           branch_keys=[mp.nstr(theta+sign*eta,75)+"|"+mp.nstr(eta/2,75) for sign in (-1,1)],
           twirl="sample I,S,S-dagger,Z independently per occurrence",
           residual_pauli_probabilities=[float((1+mp.re(z)-s)/2),float(s/2),float(s/2),float((1-mp.re(z)-s)/2)])
    cache[key]=r
    CACHE.write_text(json.dumps(cache,indent=2),encoding="utf-8")
    return r

def theta_for(family, notebook=False):
    gamma = 1 / (4 - mp.root(4, 3))
    coeff = {"X_boundary": gamma / 2, "X_common": gamma,
             "X_mixed": (1 - 3 * gamma) / 2, "ZZ_common": gamma,
             "ZZ_central": 1 - 4 * gamma}[family]
    sign = (-1 if family.startswith("ZZ") else 1) * (-1 if notebook else 1)
    return sign * mp.mpf("0.5") * coeff

def synth(theta, delta):
    # delta is full diamond norm, epsilon passed to gridsynth is operator tolerance.
    key = mp.nstr(theta, 75) + "|" + mp.nstr(delta, 75)
    if key in cache:
        return cache[key]
    start = time.perf_counter()
    gates = gridsynth_gates(theta, delta / 2, seed=17, dps=90, up_to_phase=True)
    u = get_synthesized_unitary(gates, dps=90)
    target = mp.matrix([[mp.exp(-1j * theta / 2), 0], [0, mp.exp(1j * theta / 2)]])
    # Independent exact 2x2 unitary-channel diamond formula, phase invariant.
    overlap = abs(mp.trace(target.H * u)) / 2 if hasattr(mp, "trace") else abs(sum((target.H * u)[i,i] for i in range(2))) / 2
    diamond = 2 * mp.sqrt(max(mp.mpf(0), 1 - overlap**2))
    assert diamond <= delta * mp.mpf("1.00000001"), (key, diamond, delta)
    r = dict(theta=mp.nstr(theta, 75), delta=mp.nstr(delta, 75), gates=gates,
             t_count=gates.count("T"), primitive_depth=len(gates.replace("W", "")),
             measured_diamond=float(diamond), compile_seconds=time.perf_counter()-start)
    cache[key] = r
    CACHE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    return r

def hwp_size(n):
    return n - n.bit_count(), n.bit_length()

def groups(data, mode):
    result = []
    for layer in data["layers"]:
        sizes = [100] if layer["pauli"] == "X" else [len(data["edges"])] if mode == "global" else data["edge_group_sizes"]
        for size in sizes:
            result.append(dict(family=layer["family"], n=size, layer=layer["index"], pauli=layer["pauli"]))
    return result

def hwp(data, mode, tower=False, mixed=False, joint_batch=False):
    gs = groups(data, mode)
    copies=1 if joint_batch else 2
    if joint_batch:
        gs=[dict(g,n=2*g["n"]) for g in gs]
    def width(g):
        return hwp_size(g["n"])[1] - int(mode=="global" and g["pauli"]=="ZZ" and data["all_degrees_even"])
    def base_angle(g):
        return theta_for(g["family"], data["case"]=="notebook_literal") * (2 if width(g)<hwp_size(g["n"])[1] else 1)
    binary_rotations = copies * sum(width(g) for g in gs)
    and_count = copies * sum(hwp_size(g["n"])[0] for g in gs)
    # Conservative reuse: independent catalyst chain per family and register width,
    # per instance. No free catalysts and no guessed free sharing between replicas.
    towers = sorted(set((g["family"], width(g)) for g in gs))
    cat_count = copies * sum(b for _,b in towers) if tower else 0
    seed_occurrences = copies * len(gs) if tower else binary_rotations
    delta = SYN_BUDGET / (2 * seed_occurrences) if tower else SYN_BUDGET / binary_rotations
    cat_delta = SYN_BUDGET / (2 * cat_count) if tower else None
    notebook = data["case"] == "notebook_literal"
    synthesizer = synth_mixed if mixed else synth
    startup = []
    if tower:
        for family,b in towers:
            g=next(g for g in gs if g["family"]==family and width(g)==b)
            startup.extend(synthesizer(base_angle(g) * 2**k, cat_delta) for k in range(b))
    rotation_t = 0
    rotation_t_max = 0
    primitive_upper = 0
    t_depth_upper = 0
    max_anc = 0
    scheduled_t_depth = 0
    scheduled_primitive_depth = 0
    measured_error_bound = copies * sum(r["measured_diamond"] for r in startup)
    breakdown = Counter()
    group_records = []
    for g in gs:
        k,allocated_b = hwp_size(g["n"])
        b=width(g)
        theta = base_angle(g)
        rs = [synthesizer(theta * 2**b, delta)] if tower else [synthesizer(theta * 2**i, delta) for i in range(b)]
        rt = sum(r["t_count"] for r in rs)
        rotation_t += copies * rt
        rotation_t_max += copies * sum(r.get("branch_max_t_count",r["t_count"]) for r in rs)
        measured_error_bound += copies * sum(r["measured_diamond"] for r in rs)
        # Safe serial schedule: each published 3-to-2 compute <=16 primitive layers,
        # its measured inverse <=11. The AND has T-depth 2 and cost 4 T.
        # Binary rotations on separate output qubits run in parallel without tower.
        t_middle = (rs[0].get("branch_max_t_count",rs[0]["t_count"]) + 2*b) if tower else max(r.get("branch_max_t_count",r["t_count"]) for r in rs)
        logical_middle = (rs[0]["primitive_depth"] + 30*b) if tower else max(r["primitive_depth"] for r in rs)
        # Global ZZ parity carriers: degree4 gives <=8 CNOT layers each way;
        # matching ZZ: 1 CNOT each way. X: 1 H each way.
        outer_depth = 16 if g["pauli"] == "ZZ" and mode == "global" else 2
        hd=hwp_schedule(g["n"])
        scheduled_t_depth += hd["compute_t_depth"]+t_middle
        scheduled_primitive_depth += hd["compute_primitive_depth"]+hd["uncompute_primitive_depth"]+logical_middle+outer_depth+2*b
        t_depth_upper += 2*k + t_middle
        primitive_upper += 27*k + logical_middle + outer_depth + 2*b
        max_anc = max(max_anc, k+allocated_b+(g["n"] if mode == "global" and g["pauli"] == "ZZ" else 0))
        breakdown[g["family"]] += copies * (4*k + rt + (4*b if tower else 0))
        group_records.append(dict(**g, and_count=k, weight_bits=b, synthesized_t=rt,
                                  t_depth_upper=2*k+t_middle))
    tower_and = binary_rotations if tower else 0
    t_total = 4*and_count + rotation_t + 4*tower_and + copies*sum(r["t_count"] for r in startup)
    t_max = 4*and_count + rotation_t_max + 4*tower_and + copies*sum(r.get("branch_max_t_count",r["t_count"]) for r in startup)
    # Published n-layer tower needs 2n+1 ancillas: n catalysts, n AND targets,
    # one unused rotation target. Reserve each bank in full (no guessed sharing).
    tower_scratch = copies*sum(b+1 for _,b in towers) if tower else 0
    primitive_upper += sum(r["primitive_depth"] for r in startup)
    t_depth_upper += sum(r.get("branch_max_t_count",r["t_count"]) for r in startup)
    scheduled_t_depth += sum(r.get("branch_max_t_count",r["t_count"]) for r in startup)
    scheduled_primitive_depth += sum(r["primitive_depth"] for r in startup)
    assert measured_error_bound <= float(SYN_BUDGET)
    return dict(method=f"hwp_{mode}" + ("_joint_batch" if joint_batch else "") + ("_in_circuit_tower" if tower else "") + ("_mixed_diagonal" if mixed else "_deterministic"),
        t_count=t_total, t_depth_conservative_upper=t_depth_upper,
        t_count_branch_maximum=t_max,
        t_depth_asap_published_hwp_with_block_barriers=scheduled_t_depth,
        logical_primitive_depth_asap_with_ct_sizing_model=scheduled_primitive_depth,
        logical_primitive_depth_conservative_upper=primitive_upper,
        binary_rotation_occurrences=batch_value(binary_rotations), synthesized_rotation_occurrences=seed_occurrences,
        hwp_and_count=and_count, tower_and_count=tower_and,
        peak_additional_logical_qubits_before_routing=copies*max_anc+cat_count+tower_scratch,
        catalyst_qubits=cat_count, catalyst_startup_t=copies*sum(r["t_count"] for r in startup),
        ccz_consumption=0, direct_t_model="all temporary ANDs use four T; CCZ alternative not assumed free",
        full_diamond_synthesis_bound=measured_error_bound, allocated_synthesis_budget=float(SYN_BUDGET),
        physical_fault_budget_remaining=float(mp.mpf("0.002")-SYN_BUDGET),
        synthesis_count_status="measured gate strings + published gadget formulas; tower not end-to-end simulated",
        primitive_depth_model="unrouted serial sizing model: 27 per HWP AND compute/uncompute, 30 per CT; not certified ISA depth",
        t_count_type="expected over positive mixtures" if mixed else "fixed deterministic",
        constant_propagation_even_cut_lsb=mode=="global" and data["all_degrees_even"],
        joint_batch_phasing=joint_batch,
        group_counts_by_family=dict(breakdown), groups=group_records)

def batch_value(n):
    return n

def direct(data):
    n = data["batch_rotations"]
    delta = SYN_BUDGET / n
    notebook = data["case"] == "notebook_literal"
    fam = {f["family"]: synth(theta_for(f["family"], notebook), delta) for f in data["angle_families"]}
    tc = sum(f["batch_multiplicity"]*fam[f["family"]]["t_count"] for f in data["angle_families"])
    td = sum(fam[l["family"]]["t_count"]*(1 if l["pauli"]=="X" else 4) for l in data["layers"])
    gd = sum((fam[l["family"]]["primitive_depth"]+2)*(1 if l["pauli"]=="X" else 4) for l in data["layers"])
    error = sum(f["batch_multiplicity"]*fam[f["family"]]["measured_diamond"] for f in data["angle_families"])
    return dict(method="direct_deterministic",t_count=tc,t_depth=td,
                logical_primitive_depth=gd,peak_additional_logical_qubits_before_routing=0,
                catalyst_qubits=0,ccz_consumption=0,full_diamond_synthesis_bound=error, family_synthesis=fam)

def mixture_estimates(data):
    # Published expected fits, not executable branch-verified compilers.
    result = []
    raw=data["batch_rotations"]
    for mode in ("raw", "matching", "global"):
        if mode == "raw":
            n,ands = raw,0
        else:
            gs=groups(data,mode)
            n=2*sum(hwp_size(g["n"])[1] for g in gs)
            ands=2*sum(hwp_size(g["n"])[0] for g in gs)
        delta=float(SYN_BUDGET)/n
        fit=.53*math.log2(1/delta)+4.86
        result.append(dict(method=f"{mode}_mixed_fallback_PUBLISHED_EXPECTATION_ONLY",
                           expected_t_count=4*ands+n*fit, rotation_delta=delta,
                           branch_t_depth="UNKNOWN", worst_case_t_count="UNKNOWN",
                           approximation_guarantee="requires explicit certified mixtures; fit alone is not a bound"))
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--case", choices=["paper_counts_proxy","notebook_literal","all"],default="all")
    args=parser.parse_args()
    names=[args.case] if args.case!="all" else ["paper_counts_proxy","notebook_literal"]
    for name in names:
        data=json.loads((OUT/f"{name}.structure.json").read_text())
        methods=[direct(data)]
        for mode in ("matching","global"):
            methods.extend([hwp(data,mode),hwp(data,mode,tower=True),hwp(data,mode,tower=True,mixed=True)])
        methods.extend([hwp(data,"global",tower=True,joint_batch=True),hwp(data,"global",tower=True,mixed=True,joint_batch=True)])
        result=dict(case=name,total_execution_target=.002,synthesis_budget=float(SYN_BUDGET),
                    backend_numba_mode=NUMBA_MODE,
                    numerical_completion_status=data["numeric_parameters_status"],
                    methods=methods,unverified_probability_mixture_fits=mixture_estimates(data))
        (OUT/f"{name}.costs.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
        print(name,[(m["method"],m["t_count"],m["peak_additional_logical_qubits_before_routing"]) for m in methods],flush=True)

if __name__=="__main__":
    main()
