"""Render the audit from checked resource JSON files; no new optimisation."""
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
DOC=ROOT.parent/"docs/non_clifford_structure.md"

def read(name,suffix):
    return json.loads((OUT/f"{name}.{suffix}.json").read_text(encoding="utf-8"))

def number(x):
    return f"{x:,.0f}".replace(","," ")

LABELS={
 "direct_deterministic":"Individual deterministic gridsynth",
 "hwp_matching_deterministic":"HWP inside four matching groups",
 "hwp_matching_in_circuit_tower_deterministic":"Matching HWP + in-circuit towers",
 "hwp_matching_in_circuit_tower_mixed_diagonal":"Matching HWP + towers + positive mixture",
 "hwp_global_deterministic":"HWP Total commuting ZZ group",
 "hwp_global_in_circuit_tower_deterministic":"Global HWP + in-circuit towers",
 "hwp_global_in_circuit_tower_mixed_diagonal":"Global HWP + towers + positive mixture",
 "hwp_global_joint_batch_in_circuit_tower_deterministic":"Joint-batch HWP + towers, deterministic",
 "hwp_global_joint_batch_in_circuit_tower_mixed_diagonal":"Joint-batch HWP + towers + positive mixture",
}

def table(costs):
    rows=["| A known compilation | T demand batch | Maximum branch | T depth† | Logical primitive depth† | Dop. logical qubits‡ | Synthesis diamond bound |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for m in costs["methods"]:
        t=m["t_count"]
        tc=number(t)+( " expected" if m.get("t_count_type","").startswith("expected") else "")
        td=m.get("t_depth",m.get("t_depth_asap_published_hwp_with_block_barriers"))
        gd=m.get("logical_primitive_depth",m.get("logical_primitive_depth_asap_with_ct_sizing_model"))
        rows.append(f"| {LABELS[m['method']]} | {tc} | {number(m.get('t_count_branch_maximum',t))} | {number(td)} | {number(gd)} | {m['peak_additional_logical_qubits_before_routing']} | {m['full_diamond_synthesis_bound']:.3g} |")
    return "\n".join(rows)

def main():
    p=read("paper_counts_proxy","structure"); n=read("notebook_literal","structure")
    pc=read("paper_counts_proxy","costs"); nc=read("notebook_literal","costs")
    ps=read("paper_counts_proxy","secondary"); ns=read("notebook_literal","secondary")
    best=pc["methods"][-1]; separate=pc["methods"][6]; literal=nc["methods"][-1]
    hw=4*best["hwp_and_count"]; tower=4*best["tower_and_count"]
    seeds=best["t_count"]-hw-tower-best["catalyst_startup_t"]
    angles="\n".join(f"| {a['family']} | {a['theta_radians']:.12f} | {number(a['batch_multiplicity'])} | {number(next(b['batch_multiplicity'] for b in n['angle_families'] if b['family']==a['family']))} |" for a in p["angle_families"])
    secondary=[]
    for s in (ps,ns):
        for v in s["phase_gradient"]:
            secondary.append(f"| {s['case']}, {v['mode']} | {v['gradient_bits_per_instance']} | {number(v['exact_toffoli_count'])} | {number(v['t_count'])} | {number(4*v['hwp_and_count']+4*v['exact_toffoli_count']+v['gradient_preparation_t'])} | {v['peak_additional_logical_qubits_before_routing']} | {v['full_diamond_bound']:.3g} |")
    fit_tower=hw+tower+201*(.53*math.log2(2*201/(.002/3))+4.86)+40*(.53*math.log2(2*40/(.002/3))+4.86)
    text=f"""# Non-Clifford structure: What remains after the known transformations

Date: 4 October 2026. Basis: [prior_art.md](prior_art.md), [open_bottlenecks.md](open_bottlenecks.md), [software_headroom.md](software_headroom.md), [modern_ftqc_ledger.md](modern_ftqc_ledger.md). Only developed reconstruction/cost/verification scripts for **Existing** of methods. No new algorithm proposed.

**Main result:** 4.8 million T You can\'t leave modern baseline. For clearly defined numerical completion versions from 60 200 rotations known HWP, catalyst towers and positive mixtures Give **{number(best['t_count'])} expected T**, maximum **{number(best['t_count_branch_maximum'])}** T by selected branches. But original paper workload not fully restored: official Q# sample It\'s breaking up with him counts. Not that number, not that decrease T demand are not proven to be an improvement in the value of the whole FTQC machine.

**The exact remaining structure:** The sequence of phases from two whole functions: number of units in by the time the phase is used X basis and the number of ribs cut lattice graph in Z basis. Each commuting group It\'s already compressing to binary weight register. Balance in calculated compilation — **Coherent carries with these weights calculated**, Final phase accuracy and recalculation after change of non-composite base. It\'s a description circuit, not proof of the best bottom line.

## 1. Source, reconstruction, and honest boundary of apples-to-apples

Checked [Beverland et al., Appendix D/F](https://arxiv.org/html/2211.07629) and two immutable versions [Official Q# notebook, 2022](https://github.com/microsoft/Quantum/blob/d78c2c0348048a13c04da5f69aba3810914f268f/samples/azure-quantum/resource-estimation/estimation-dynamics.ipynb) / [2023](https://github.com/microsoft/Quantum/blob/f92f2074507696224fae440e4164d2751754fa2c/samples/azure-quantum/resource-estimation/estimation-dynamics.ipynb). Local bytes and SHA-256 in [manifest](../analysis/sources/manifest.json). Both notebook versions have the same essential rotation structure; raw QIR and old estimator outputs not retained.

| Parameter | P: paper-count proxy | N: literal notebook |
|---|---|---|
| Workers qubits | 2 independent instances × 100 = 200 | Same |
| Suzuki order | 4 | 4 |
| Number product-formula steps as at instance | 20, from article | ceil(20/0.25) = 80, code |
| J, g, Δ | B Appendix F not recorded; **completion** J=g=1, Δ=0.25 | J=g=1, Δ=0.25 Clearly |
| Evolution time | 5 **for completion**, not specified time paper run | 20 |
| One rib lattice | 200 for reproduction paper formula; used periodic torus proxy | 180, open 10×10 square from loop bounds |
| Effective Hamiltonian | +ΣX − ΣZZ, field outside | −ΣX + ΣZZ, alpha code |
| Rotations, one instance / batch | 30 100 / 60 200 | 112 100 / 224 200 |
| Rotation layers as at instance | 501 | 2001 |
| Maximal commuting blocks as at instance | 201 | 801 |
| Matching-group dimensions ZZ | 50,50,50,50 | 50,40,50,40 |
| Total modelled execution target | ≤0.002 as at batch | Same for this comparison |

**I\'re not replacing these two tasks.** Paper count formula uses bulk edge count 2N; It\'s not proof that the original QIR Had periodic boundaries. Torus — A clear way to build circuit With these counts. Him. wrap edges are not free of charge immediate neighbours planar hardware. B N `SetSequences` applies −J coefficient to X and +g to ZZ, Although prose notebook it\'s the opposite. Prin J=g=1 It\'s a change of sign. Hamiltonian; as at bipartite graph Yes Clifford frame equivalence, But the code doesn\'t add the corresponding input/output frames. I keep literal circuit separately.

From the previous one reference retained: 200 working qubits Like two launches, surface-code / planar nearest-neighbour platform, physical p=10⁻³, 50 ns gates, 100 ns measurement, cycle proxy 400 ns and total execution target. New ancillas, logical operation errors and routing shall be counted. Physical decoder Not here. benchmarked. Quantum-dynamics/Trotter discretisation error and repetitions for observable Have not been certified historical execution budget; I don\'t say full simulation error ≤0.002.

## 2. Which rotates are re-established

I\'re gonna use one. convention R_P(θ)=exp(−iθP/2). Q# `Rx(2θ)` So you can\'t confuse it with exp(−iθX).

γ=(4−4^(1/3))⁻¹; c=1−4γ. Each step coefficients Internal ZZ kicks: γ,γ,c,γ,γ. After the merger of the neighbouring X half-kicks:

- X boundary: γ/2, two blocks as at instance;
- X common: γ, 3T−1 blocks;
- X mixed: (1−3γ)/2, 2T blocks;
- ZZ common: γ, 4T blocks;
- ZZ central: 1−4γ, T blocks.

For intended field-outside decomposition symbolic angles: X boundary = gΔγ; X common = 2gΔγ; X mixed = gΔ(1−3γ); ZZ common = −2JΔγ; ZZ central = −2JΔ(1−4γ). **Exactly. symbolic structure Recovers more reliable than the number of parameters original paper run.** Lower P-completion. For N All signs change when J=g=1; multiplicities taken from the code itself.

| Family | θ radians, P completion | Batch multiplicity P | Batch multiplicity N |
|---|---:|---:|---:|
{angles}

These are five signed families, four distinct absolute angles: common X and common ZZ have opposite signs when J=g. Boundary angle half as much as common. Several binary-weight angles can be derived from one synthesis programme; reuse **Classical programme** Doesn\'t. quantum gates/magic states free of charge. Special Clifford coincidences for other unknown J,g,Δ Not excluded.

Inside X kick All 100 terms commute. Inside ZZ kick All edges commute, including edges, Who divide qubit; four matchings necessary for parallel CNOT execution, Not for mathematical switching. But X_j anticommutes c Z_j Z_k. So repeated angles You can\'t just fold through the next few days kick. Full Pauli supports, layer IDs and predecessor IDs exported to [P CSV](../analysis/results/paper_counts_proxy.rotations.csv) and [N CSV](../analysis/results/notebook_literal.rotations.csv). CSV contains one instance; Second - independent copy. Dependencies - I\'m sure you will. anticommuting incidences between neighbouring countries blocks; This is circuit dependency graph, not physical layout.

Binary incidence rank The ribs are equal 99 both connected graphs. This is **not** Means that 200 ZZ rotations can be replaced 99 rotations: XOR relations does not retain the normal whole amount parity bits. For periodic degree-4 proxy cut weight Always even; known constant propagation allows for a phase at the permanent zero youngest weight bit. Total global P This optimization is included. For open lattice There is no such limit.

## 3. Reconciliation of historical numbers

| Historical value | What\'s repeated | Status |
|---|---|---|
| 60 200 rotations | 2×(15×20+1)×100 | It\'s exactly what it says formula; literal notebook Not consistent |
| 4.8M T | ≈60 200×80; 80 T/rotation in accordance with coarse deterministic synthesis | Unreconciled executable; not final modern baseline |
| 150 000 logical steps | Current Appendix F M_meas=1 400 000; One this term greater 150k | **Unable to reconcile with published inputs** |

Check published equations: ε_syn one instance =0.001/3; ε_rot=ε_syn/30100. Current formula ceil(0.53 log₂(1/ε_rot)+5.3) ♪ Gives me ♪ **20**, I mean, 602 000 T as at instance / **1 204 000** as at batch. Substitution M_meas=1 400 000 and D_R=501 ♪ Gives me ♪ C_min=**1 440 120** as at instance. Prin 80 T I\'m getting it. **1 470 180**, Still not.. 150k. Correct M_meas or model constants without raw QIR would be a fiction. Real deterministic recompile P completion ♪ Gives me ♪ {number(pc['methods'][0]['t_count'])} T as at batch, But group known methods are much stronger.

B notebook `eps` It\'s passed on as argument, but in operation body not used for rotations. Baseline run 2022 causes noops=0; Individual slowed version Adds measurements End. It\'s not a reason to give him a name paper M_meas. [Source notebook](https://github.com/microsoft/Quantum/blob/d78c2c0348048a13c04da5f69aba3810914f268f/samples/azure-quantum/resource-estimation/estimation-dynamics.ipynb).

## 4. Output contract and accuracy budget

Comparison Contract — Approach **Idem product-formula quantum channel**, including arbitrary input, entanglement with a reference both output registers. All maintained kicks; I\'re not reducing Trotter order/steps, I\'re not replacing simulation algorithm And I shall not remove terminal gates based on unknown measurement.

Used full diamond norm, ε_syn=0.002/3. For ordinary synthesized gates tolerance gridsynth in operator norm I\'m gonna go. δ/2; actual single-qubit channel error checked with 90-digit arithmetic: 2√(1−|Tr(U†V)/2|²). Amount local diamond bounds limits all circuit. For HWP δ divided by number **new** synthesized weighted rotations, Not at 60 200 Remote rotation occurrences.

For towers half synthesis budget selected initial catalysts, half of all seed occurrences. With the perfect others gadgets Primary difference catalyst state Limit joint output once over contractivity quantum channels; It is not considered a free or independent error for each use. Physical error catalyst during storage - separate storage/exposure cost, which should take into account physical ledger. Primary approximation may create correlations between uses; independence for them triangle bound No need..

Balance physical-fault allowance — 0.001333333. It\'s not proof that it\'s new routed circuit It reaches: gates, ancilla lifetimes, injected-state quality and decoder/cycle throughput I must go through a new one resource/error estimation.

## 5. Tested existing approaches and the environment for the future

### Deterministic rotation synthesis

Used published [pygridsynth 2.0.0](https://github.com/quantum-programming/pygridsynth), implementation [Ross–Selinger](https://arxiv.org/abs/1403.2975), seed=17. Retained actual gate strings, T counts and diamond errors. Result near-optimal for single-qubit ancilla-free task under the conditions of the method; global circuit optimality Not declared. Demands finite-precision compilation Every one of you phase, not catalyst/CCZ. Clifford gates included in primitive-depth column.

### Hamming-weight phasing: key existing structural savings. and the

For m Same commuting phases I\'re going to figure it out. w=Σx_i. Then.. product phase, to the nearest global phase, equals exp(iθw); w is stored in b=floor(log₂m)+1 bits. Needed b weighted rotations θ,2θ,…,2^(b−1)θ instead m rotations. [Gidney](https://arxiv.org/abs/1709.06648), [public Qualtran implementation](https://qualtran.readthedocs.io/en/latest/bloqs/rotations/hamming_weight_phasing.html).

Calculated existing implementation has K=m−popcount(m) temporary ANDs, **4K T**, K+b scratch/output logical qubits and measurement-based zero-T uncompute. Non-Clifford demand Doesn\'t disappear.: coherent integer carries Quantum is calculated. X phases used Hadamard basis change. For matching ZZ in-place CNOT parity carriers I already have.. For whole ZZ block in conservative implementation Added m clean parity carriers, Clifford compute/uncompute; Dependent parity inputs permissible. Analogous existing Ising/HWP The example is available to the public [Quantinuum](https://docs.quantinuum.com/guppy/algorithms/examples/hamiltonian_simulation/trotter_hamming_weight_phasing.html); its 1D benchmark numbers No one is allowed to move in here.

Joint-batch row applies **the same HWP** For all equal-angle commuting terms two independent instances. Perfect operation stays U⊗U; quantum arithmetic Temporary use of general register. It\'s a permit. algebraic compilation, but requires a connection between two areas hardware. Therefore, separate-instance row saved as a simpler locality/lesser option depth.

### In-circuit catalyst towers

Binary-weight phases They have the required sequence θ,2θ,4θ,… . Published b-layer tower replaces b independent syntheses one seed Rz(2^bθ) + **4b T** and b persistent catalysts. Initial preparation included. Everyone bank Added b AND targets and one unused rotation target: **2b+1 ancillary qubits**, without routing. [Sun et al., complete circuit/resource formulas](https://arxiv.org/pdf/2409.04587), [Sun–Koczor, surface-code costs](https://arxiv.org/abs/2508.06236).

This is in-circuit variant, without RUS tails. Independent produce-and-store towers They\'re applicable, but they\'re expected logarithmic injection depth not equal full runtime: supply, storage, doubled-angle correction branches and finite buffer separately recorded. Exact TFIM schedule/quality frontier They are not built here option-pricing speedup not applicable.

### Positive probability mixtures

Implemented **Acquainted mixed-diagonal over/under + Clifford twirl**, [Campbell](https://arxiv.org/abs/1612.02689), [Kliuchnikov et al.](https://arxiv.org/abs/2203.10064), above existing gridsynth. No new synthesis rule no. Two synthesized branches straddle θ; positive probabilities He\'s gone. imaginary residual coherence. After twirl residual channel has clearly calculated nonnegative Pauli probabilities, full diamond error =2(1−p_I). Retained probabilities, branch strings, expected and maximum T counts. Randomness is re-chosen at each occurrence; Repeat one random choice for all circuit not intended.

Like this.. CPTP mixture preserves quantum-output contract **in averaged-channel diamond sense**. He doesn\'t promise a little coherent error to conditioning for each random branch; for that purpose given deterministic row. Quasiprobability reweighting, TE-PAI/qDRIFT-style replacement and Evaluation only observable excluded: they change contract or price repeated runs.

### Stronger mixed-fallback synthesis: evaluation not issued for measurement: of the measurement compiler

Published expected fit 0.53 log₂(1/δ)+4.86 ♪ Gives you ♪ raw P Near **1 135 791 T**. After joint HWP+towers and payment catalyst preparation projection is **{number(fit_tower)} expected T**. It\'s even stronger existing-method candidate, but fit Under random angles not certified gate construction, worst-case bound or measured latency these specific angles. Implementation from paper and dataset were not provided here exact-angle fallback circuits. That\'s why this is projection does not replace verified mixed-diagonal baseline. [Primary formulas](https://arxiv.org/html/2605.31544).

### Small-angle methods

Only Comparative positive-mixture variant with required diamond budget. B [Bothe et al.](https://arxiv.org/html/2605.31544) small-angle advantage disappears into δ≪φ² regime; their convention exp(iφZ) different from ours twice and a sign. B P weighted-angle sets min reduced |φ|≈0.030434; min φ²/δ >4 000 for global HWP and >8 000 for matching HWP. B N The gap is even bigger. Consequently, published, p. 1 identity-underrotation small-angle mechanism does not give an additional large reduction for **these completions and this output target**. Other unknown paper parameters can change the conclusion. Quasiprobability chemistry reductions not same-contract result for TFIM.

### Phase-gradient / quantum variable rotations

Checked existing shift/add phase-kickback option: HWP weight × classical angle constant Added to phase-gradient register. Explicit bits selected from total rounding budget; gradient preparation I\'m paid for, too. Used [Qualtran phase-gradient resource definitions](https://github.com/quantumlib/Qualtran/blob/main/qualtran/bloqs/rotations/phase_gradient.py). This is **literal shift-add upper-cost variant**, not the best multiplier or all phase-gradient frontier.

| Case/group | Gradient bits / instance | Exact Toffolis | T c ordinary 7-T Toffoli | T c existing measured 4-T Toffoli§ | Dop. qubits, 7-T row | Diamond bound |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(secondary)}

§ 4-T replacement uses measurements, and additional ancilla, How [Jones](https://arxiv.org/abs/1212.5069); Not free unitary Toffoli. Table qubits applicable 7-T row; measured variant needs additional scratch/feedback. CCZ-based implementation would require one of these accepted CCZ for each specified Toffoli Instead of them, T decomposition. Even this one. count does not include CCZ production automatically. In a proven version phase-gradient loses HWP+towers Under T count; It\'s not excluded as possible. space/time tradeoff other implementation. Depth upper bounds in secondary JSON.

### Pauli / phase-polynomial optimizations

Already on basis changes, commuting grouping, adjacent-angle fusion, exact parity extraction and constant propagation even cut bit. Classical reuse Cuts corners compile time, not demand quantum resources. [Phase-polynomial / Fourier description](https://www.cs.sfu.ca/~meamy/) Helps to Share CNOT parity networks and routing. For generic continuous coefficients distinct edge characters remaining different real Fourier terms; GF(2) rank reduction Doesn\'t remove them by themselves. π/4-specific Reed–Muller identities Cannot automatically be moved to algebraic Suzuki angles. Unrestricted whole-circuit ZX/tket/Pauliopt optimisation No evidence has been proved, nor have any unconfirmed witnesses been found to be present. is not clear savings She\'s not assigned to any of these things..

## 6. Recalculated baseline, depth and all ancillary resources

Each line — SAME circuit **Inside its version of the subject**, SAME quantum-channel synthesis allowance, SAME total execution target. T demand Includes temporary ANDs, seed rotations and initial catalysts. Direct row — in-place synthesis; No hidden offline synthesized resource states.

### P: paper-count proxy, conditional numeric completion

{table(pc)}

### N: literal archived notebook, Not an improvement P

{table(nc)}

† **Miscellaneous units Cannot mix.** T depth — gate/dependency upper bound c block barriers; for HWP This is ASAP scheduling published Qualtran decomposition, for tower middle used seed T depth +2b. Startup preparation Placed consecutively for conservative bound. Primitive depth — Clifford/T/measurement layers unit price and sizing coefficient 30/b-layer CT. This is **MODEL**, not measured surface-code ISA depth, wall-clock latency or optimal scheduling. Completely serial, Even more conservative bounds also retained in JSON. Spatial routing, heterogeneous duration gates, classical feedback stalls and offline production not included. Two separate instances Going parallel; joint grouping Doesn\'t double. T demand, But it increases arithmetic critical path.

‡ Ancillas — Over 200 working qubits, **to** surgery corridors, factory ports, decoder resources, buffers and spares. For global P separate baseline: 810 parity/HWP qubits +70 catalyst qubits +80 tower scratch/dummy =960. Joint baseline: 806 parity/HWP +40 catalysts +45 scratch/dummy =891. Matching variants without full dial edge carriers and use 350 additional qubits c towers. This is lifetime-aware capacity accounting Inside explicit banks, Not finished planar allocation. Existing row K+b means peak per active block; No folding scratch All 201 blocks simultaneously.

**Most heavily tested by components T-count point:** joint-batch HWP+towers+positive mixture, {number(best['t_count'])} expected / {number(best['t_count_branch_maximum'])} max T. **A shorter option with separate instances:** {number(separate['t_count'])} expected / {number(separate['t_count_branch_maximum'])} max T. Select one line as globally cheapest FTQC Can\'t be without routed spacetime ledger. Tower circuit counts taken from verified published identities; ours TFIM end-to-end tower circuit not simulated on 200 qubits. Mixed branches, phase identities and fusion separately verified. Strongest existing exact-angle compiler across all implementations has not been established by this analysis.

## 7. What\'s spent now? non-Clifford resources

For lowest-T P point (CALC, not published benchmark):

| Term | T demand batch | Percentage T demand, CALC |
|---|---:|---:|
| HWP integer carries: {best['hwp_and_count']} temporary ANDs | {number(hw)} | {100*hw/best['t_count']:.2f}% |
| Tower logical ANDs: {best['tower_and_count']} | {number(tower)} | {100*tower/best['t_count']:.2f}% |
| Seed rotations | {number(seeds)} expected | {100*seeds/best['t_count']:.2f}% |
| Initial catalyst preparation | {number(best['catalyst_startup_t'])} expected | {100*best['catalyst_startup_t']/best['t_count']:.2f}% |

YES. isolated P row arithmetic term =235 976 T; y joint row =238 388 T. So, downplay **only** cost synthesis remaining seeds/catalysts — Small reserve. TOY: If you make these phases free of charge, AND arithmetic and towers previous, T demand reduced only in **{best['t_count']/(hw+tower):.3f}×**. It\'s not physically permissible baseline and not lower bound; This is sensitivity selected existing decomposition. TOY: 2× reduction HWP carry T cost I\'d cut it down. total T demand in **{best['t_count']/(best['t_count']-hw/2):.3f}×**. No new way to achieve this is proposed.

For literal N lowest-T point stays {number(literal['t_count'])} expected T; longer simulation doesn\'t get cheap out of-for small quantities angle families. Fresh compilation He\'s already been carrying it precision dependence each lattice term for small weight register. Growth N/steps continues to pay coherent arithmetic, storage and supply/delivery of nonlinear resources.

**Factory-quality consequence, only CALC:** to ε_dis=0.0008 P branch-max demand {number(best['t_count_branch_maximum'])} Allows average accepted-state error Near {0.0008/best['t_count_branch_maximum']:.3g}; in old 4.8M required 1.67×10⁻¹⁰. It can change the choice existing resource protocol. It does not prove the suitability of a particular of the individual cultivation implementation: heterogeneous resource errors, catalyst storage and full circuit budget I\'ve got to check it out.. CCZ swaps They must have their own demand/quality ledger, Not to be transferred to free «T equivalents».

## 8. Answer: Which mathematical structure is responsible for the residual price?

For ZZ group as at graph G:

```text
w_G(x) = sum over edges (x_u XOR x_v)
sum ZZ eigenvalues = |E| - 2*w_G(x)
U_ZZ(theta)|x> = exp[-i*theta*|E|/2] * exp[i*theta*w_G(x)] |x>
```

For X group same c w_X(s)=Σs_j **in X eigenbasis**. Large List rotations encodes the phase from a small whole number; known HWP already using this structure. But figure out the binary record w Coherent is ordinary integer addition c nonlinear carries, Not one CNOT linear transformation. For cut weight inputs additional cycle XOR constraints, But these constraints They don\'t turn integer weight in linear function.

Switch between X kicks and ZZ kicks Maintains the barrier:

\u2003[X_j, Z_j Z_k] ≠0.

So you can\'t just figure it out once w_X and w_G, To accumulate all phases and restore data End. Another kick changes amplitudes/superpositions in basis other weight observable. Generic nonzero algebraic angles of this completion not accurate Clifford/T angles: finite-precision The phase still needs to be maintained, but catalyst amortisation has already significantly restricted her share of the T count. Special-angle exact cases and giving up the task output contract Need separate analysis.

It\'s not proof that a stronger existing one can\'t be whole-circuit compilation, other known Hamiltonian simulation algorithm or special scientific-output reduction. I hold this one circuit/contract; A comparison of such changes would require a separate faithful accuracy analysis. From 200-qubit unitary problem should not be classical hardness/quantum advantage by the size alone of the same value T count.

**Practical conclusion:** analogue «representation \"It\'s a problem that is less expensive\" already exists in the HWP and catalyst towers. Balance battlefield — coherent graph-cut/population-count arithmetic in the alternate non-muting bases, locality/ancilla/depth tradeoff and physical delivery accepted nonlinear resources. Promise a new breakthrough on the basis of 4.8M would be a mistake.. A large reserve relative to the is measured in a reliable way historical per-rotation decomposition; real residual end-to-end software headroom Not yet measured.

## 9. Reproduction and checks performed

Scripts and frozen outputs:

- [fetch_sources.py](../analysis/fetch_sources.py): immutable public notebooks, SHA-256; network You only need to reload.
- [tfim_structure.py](../analysis/tfim_structure.py): supports/angles/groups/dependencies, separately P and N; standard library.
- [compile_costs.py](../analysis/compile_costs.py): actual deterministic/mixed branch gate strings, existing HWP/tower costing.
- [hwp_schedule.py](../analysis/hwp_schedule.py): ordinary ASAP schedule published by the HWP decomposition.
- [secondary_methods.py](../analysis/secondary_methods.py): convention-correct small-angle diagnostic and explicit phase-gradient row.
- [verify_analysis.py](../analysis/verify_analysis.py): counts, supports/dependencies, HWP phase equivalence, Suzuki merging and mixture-channel certificates.
- [write_report.py](../analysis/write_report.py): from checked JSONs.
- [synthesis_cache.json](../analysis/results/synthesis_cache.json), [P costs](../analysis/results/paper_counts_proxy.costs.json), [N costs](../analysis/results/notebook_literal.costs.json), [verification](../analysis/results/verification.json).

From project root, After installation dependencies in the local environment:

```powershell
analysis/.venv/Scripts/python.exe analysis/tfim_structure.py
analysis/.venv/Scripts/python.exe analysis/compile_costs.py
analysis/.venv/Scripts/python.exe analysis/secondary_methods.py
analysis/.venv/Scripts/python.exe analysis/verify_analysis.py
analysis/.venv/Scripts/python.exe analysis/write_report.py
```

Used pygridsynth 2.0.0, mpmath 1.4.1, numpy 2.3.5; [requirements](../analysis/requirements.txt). On this one. Windows host Application Control prohibited Numba helper DLL. Pure-Python compatibility shim Disables only JIT decorators Imported optional mixture utilities; DLL not loaded, installed package unchanged, number-theoretic gridsynth implementation remains the same. Him. outputs separately verified. Ours positive-mixture certificate uses mpmath, Not inaccessible JIT path.

Checked immutable-source hashes; Straight 60 200 / 224 200 batch rotations; valid anticommuting predecessor edges; random 100-spin HWP phases and even-cut constraint; Suzuki fusion as at entangled four-spin state; positive Pauli probabilities and all synthesis error allocations. Errors numerical identity checks Near 10⁻¹⁵. This is mathematical/compiler-component verification, **not decoder benchmark and not full FT physical execution**.
"""
    DOC.write_text(text,encoding="utf-8")
    print(DOC, len(text),"characters")

if __name__=="__main__":
    main()
