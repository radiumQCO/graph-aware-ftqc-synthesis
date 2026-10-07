# Modern FTQC ledger: 200 logical qubits

Audit date: 4 October 2026. Sources and calculation artifacts are listed below
and in [modern_ftqc_ledger.calculations.json](modern_ftqc_ledger.calculations.json).

**Historical ledger boundary:** the selected calculation assigned approximately
**65%** of counted quantum area and reserved qubit-seconds to T-state production.
This is a model calculation using the old demand scenario, not a modern hardware
measurement. It must not be reused after the later rotation recompilation.

[non_clifford_structure.md](non_clifford_structure.md) supersedes **4.8M T** as a
modern compilation baseline. Known HWP/towers give approximately **253k expected
T** for the explicitly conditional paper-count completion; the archived Q#
notebook has different counts and is treated separately. Changed circuits,
workspace, and depth require a new routed/error ledger before transferring
factory fractions, runtime, or qubit-seconds.

Published modern configurations can be substantially cheaper than the old
components, but independently best headline results cannot be assembled into a
certified best stack without matching noise, interfaces, fidelity, and
throughput. The main software target is the complete non-Clifford stack:
rotation compilation, production, and delivery. The later
[factory audit](factory_bottleneck.md) separates produced states from delivered
gates. No new algorithm or completed decoder benchmark is reported here.


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## 1. What I're seeing and what I've been told

Keep the old one reference: two independent 100-spin TFIM circuits parallel, i.e **200 logical qubits**. This is batch two tasks, not one related 200-spin Hamiltonian. Fourth-order Trotter, 20 steps from Appendix F; 60 200 arbitrary-angle rotations in batch. Saved ISA snapshot: **150 000 logical steps**, **4.8 million accepted T states**, target total modeled execution error **≤0.002**. Reference counts See of the present report. [Beverland et al., Appendix F / Table 4](https://arxiv.org/html/2211.07629).

Physical assumptions Previous: hypothetical superconducting transmon-like processor, **2D nearest-neighbour**, gate **50 ss**, measurement **100 ss**, primitive error parameter **p=10⁻³**. Family code — planar surface code / lattice surgery. I'll use the old one. cycle proxy **400 ss = 4×50 + 2×100**. The device for millions of cubes doesn't exist in this.. workspace: This is reference model. New couplers, biased-noise qubits, erasure readout, FPGA or TPU Not considered free software upgrade.

Change distance and select published protocols. Save d=19 after model change accuracy would be wrong.. Number compiled steps and T demand Keep it as **contract comparison of historical snapshot**; New compilation of the same logical workload may change them, but must be re-established counts and quality.

Reduction Q below means less occupied capacity or less required machine when designing on the same platform or less than required. If the physical chip is already manufactured and fixed, software - He's freeing up places for other work fabrication cost It doesn't decrease. Reserved qubit-seconds are not equal to monetary value, energy or of the world's largest economies. on integral actually active qubits.

### Amendments to previous ledger

1. **460 ISA positions does not include all necessary for parallel synthesis and delivery.** The source directly excludes these additional ancillas. Inter-level transfer units factories are also excluded from the old estimate. Previous language on the already taken transfers was too strong; it was corrected at software_headroom.md.
2. **Published snapshot not reproduced unequivocally from all the formulas in the same version of the article.** For one instance Appendix F at the same time indicates M_R=30 100, D_R=501, M_meas=1 400 000, C_min=150 000, M=2.4M. Meanwhile, the setup A=0.53, B=5.3 and ε_syn=0.001/3 in Eq. (7)–(9) ♪ Gives me ♪ R_T=20, M=602 000 and C_min=1 440 120. It is an arithmetical incompatibility of the text, confirmed also PDF, Not the reason to replace workload. Therefore, 150k / 4.8M remains historic snapshot; his exact circuit trace No restoration...
3. Total error target Source includes approximation/synthesis error. It's not a proven probability of all hardware failures. Trotter approximation, repetitions for scientific observable, drift/bursts and defects require separate verification.

These clarifications are important: you can't compare the new full-size glass to the previous incomplete number and call it an honest acceleration attitude. Places to be checked: [Appendix C–F / PDF, Page 23, 29–30, 33](https://arxiv.org/pdf/2211.07629).

## 2. How Strong Alternatives were Selected

«Modern" means the best practically relevant published candidate available to the verification date, not necessarily the article 2026 year. There is no one better decoder or compiler for all circuits. Number anchor uses existing distance-tuned distillation; more innovative methods are tested for replacement techniques for replacing it a new technique to be.

| Component/nominated | What changes | Conformity with reference | Decision for ledger |
|---|---|---|---|
| Distance-tuned 15-to-1 → 20-to-4 | Sets the distance and interior under output quality | 2D surface code, p=10⁻³; scalar p matching, full noise/decoder validation None | Recalculate anchor, without a global optimum declaration |
| GSJ magic-state cultivation | Preparing a resource to grow / postselection Instead of a big factory | Published p=10⁻³ point Near 2×10⁻⁹; for 4.8M outputs Not enough | Do not apply direct replacement |
| Efficient cultivation with lattice surgery, version 2026 | It's cheaper. transfer/escape | Cheaper reported point Doesn't have the right one output quality | Strong candidate after separate examination fidelity, not numerical divisor |
| Constant-depth cultivation by gauging, version 29.09.2026 | Lesser depth logical Clifford checks | Prin p=10⁻³ high-distance yield Very low; appropriate full-output point not established | Not to declare a ready-made cheap factory |
| High-rate / fold-transversal cultivation | Uses flexible/nonlocal interactions | Record results require other transactions or connectivity | Delete the transport of record numbers as at NN transmons |
| Recursive surface-code distillation, 2026 | Recycles recursive layout and its asymptotic prefactor | 2D compatible, but preliminary error model and lower effective threshold | Do not carry small area without repeating distance/yield calculation |
| BB second-round distillation / constant-overhead distillation | Changes the code and scaling non-Clifford resource preparation | Other.. connectivity/encoded operations and their implementation | Not count drop-in software replacement |
| FlowRouter, September 2026 | Compiling Together Clifford routing and stochastic cultivation | NN surface family :: compatible; published accuracy / timing / workloads Other | Recompilation candidate, not apply average published gain |
| PureMagic, July version 2026 | Delight ancillas between cultivation and routing | ♪ Demands the right one ♪ ♪ cultivation supply; 1 μs-cycle regime different | Strong public scheduler-Nominated, numerical result UNKNOWN |
| TopoLS + TQEC | Optimize topological surgery and permits physical lowering | Useful for same-circuit verification; Free availability T does not cover production | Public strong candidate for the factory-fed Clifford scheduling |
| Correlated PyMatching / BeliefMatching / Tesseract | Considers correlations better independent matching | Check operation/factory DEM, windows and deadline | No assumed accuracy multiplier |
| LCD / AlphaQubit 2 | Power hardware adaptive and neural approaches | There are access restrictions, backend, memory-vs-operation and clock | Including: other persons LER / latency not framed |
| Denser planar surface code, May 2026 | Lesser storage/patch padding | Possible NN implementation at suitable: of the right direction embedding; yoking and full transport require verification | Not divide the whole car by reported encoding-rate gain |
| Modern rotation synthesis / catalysis | Lower T demand either depth On account ancillas / mixtures | Needed actual angles, precision and complete resource accounting | T demand Goodbye. 4.8M; candidate with potentially large system effects |

### Primary sources for these decisions

- [Distance-tuned distillation, Table 1 and error analysis](https://arxiv.org/html/1905.06903).
- [GSJ cultivation](https://arxiv.org/html/2409.17595) and [Official model GSJ24Factory](https://learn.microsoft.com/en-us/python/qdk/qdk.qre.models.gsj24factory?view=qsharp-py). The library model does not mean that any requested of the library is not required p_out available.
- [Efficient cultivation with lattice surgery](https://arxiv.org/html/2510.24615v2): More accurate T-output Cannot be replaced by a result S-state proxy.
- [Constant-depth gauging cultivation, Table 1](https://arxiv.org/html/2603.05429): to p=0.1%, d_f=5 reported proxy P_L=(3.2±0.4)×10⁻¹⁰ and success 4%; d_f=7 success 0.01%, P_L not measured. These are not finished statistics accepted T after full escape/delivery.
- [High-rate cultivation](https://journals.aps.org/prxquantum/abstract/10.1103/p8tw-6kq9), [fold-transversal cultivation](https://journals.aps.org/prxquantum/abstract/10.1103/gpvl-lg4c) and [Public code of the last](https://github.com/kaavyas99/MSC_foldedH).
- [Recursive distillation](https://arxiv.org/html/2603.05409): a small area does not per se give quality, retry cost and appropriate output distance.
- [BB factories](https://arxiv.org/abs/2602.20546), [constant-overhead distillation](https://www.nature.com/articles/s41567-025-03026-0).
- [FlowRouter](https://arxiv.org/html/2609.23756), [PureMagic](https://arxiv.org/html/2512.06484), [PureMagic repository](https://github.com/BQSKit/PureMagic), [TopoLS repository](https://github.com/tqec/TopoLS), [TQEC](https://github.com/tqec/tqec). Public availability FlowRouter implementation Unconfirmed; publication available; published and/or.
- [Correlated PyMatching](https://github.com/oscarhiggott/PyMatching), [BeliefMatching](https://github.com/oscarhiggott/BeliefMatching), [Tesseract](https://github.com/quantumlib/tesseract-decoder), [LCD](https://arxiv.org/html/2411.10343v2), [AlphaQubit 2](https://arxiv.org/html/2512.07737v2).
- [Denser planar surface code](https://arxiv.org/html/2605.30455), [continuous rotations: full surface-code costs](https://arxiv.org/abs/2508.06236), [small-angle synthesis, 2026](https://arxiv.org/html/2605.31544).

## 3. Replacement of factories: real-life recalculated candidates

**Old component:** historical estimator, 484 factories for batch, Near 16.07M physical qubits in factory region, to idealized runtime 1.14 s. Not to be used as a strong competition.

**Simultaneous published alternative for numerical anchor:** distance-tuned surface-code distillation with small internal ancilla/transfer overhead. Pick the best admitted spacetime point of the tested table configurations below. It's a limited set, not proof of the best. factory protocol in the literature 2026.

| ID | Protocol, p=10⁻³ | Physical qubits / factory, SRC | Code cycles / batch, SRC | Outputs / batch | Output error proxy, SRC | Qubit-cycles / output, CALC |
|---|---|---:|---:|---:|---:|---:|
| M1 — preserves the original T sub-budget | (15-to-1)⁴₁₃,₅,₅ → (20-to-4)₂₇,₁₃,₁₅ | 46 800 | 157 | 4 | 2.6×10⁻¹¹ | 1 836 900 |
| M2 — Redistributes budget with the same total target | (15-to-1)⁶₁₃,₅,₅ → (20-to-4)₂₃,₁₁,₁₃ | 43 300 | 130 | 4 | 1.4×10⁻¹⁰ | 1 407 250 |
| M3 — more accurate, more expensive | (15-to-1)⁶₁₁,₅,₅ → (15-to-1)₂₅,₁₁,₁₁ | 30 700 | 82.5 | 1 | 2.7×10⁻¹² | 2 532 750 |

Source of table parameters: [Litinski, Table 1](https://arxiv.org/html/1905.06903). Here. counts Includes physical measurement ancillas. Four outputs You can't be mistakenly counted as one. Internal transfers included in the layout/error analysis. The table is based on error analysis, not full analysis simulation with present decoder. Mean/retry-aware accounting does not specify p99 delivery deadline. YES. M2 I'll take it. d_X=23 from Table 1; in prose There's a difference. subscript — I don't mix versions.

### Apples-to-apples

Workload, physical p, local-gate family, The time and time of the total target retained. But the same scalar p Doesn't make two error model identical. In addition, old estimator uses another factory reliability/provisioning model. So this is **Recalculations in compatible primitive assumptions**, Not same-dataset performance comparison.

For factories, take source incoherent Pauli resource model. Translation infidelity proxy in error budget Demands its conditions; coherent noise You can't just sum up the same things.. numbers. Correlations between the four outputs retained as batch resource; not assumed four independent, and other and other factors. Bernoulli errors.

Direct cultivation point 2×10⁻⁹ would contribute 4.8M×2×10⁻⁹=0.0096. It's the highest target 0.002. It needs a better published configuration or a full chain of further purification with calculated costs. Just add "another perfect distillation» would be made up ledger.

## 4. Harmonization accuracy model: Why? d=19 not left free

From history ledger

\[
P_{\rm step}(d)=0.03(0.1)^{(d+1)/2}
\]

applicable logical step. The chosen trade item uses another article proxy:

\[
p_{\rm round}(d)=0.1(100p)^{(d+1)/2}.
\]

It's about **one physical code cycle**. They are not only different in units: the coefficients do not match after the correct recalculation.. Bringing Good P_step an old article with a cheaper factory another article and count target proven not.

For the conditional modern ledger Second round-level proxy also to external algorithm/synthesis tiles. This will agree on an arithmetical basis, but not replace operation-level validation: surgery geometry can change prefactors and faults. Strong decoder Doesn't get a fake. accuracy gain.

Prin d=19, about 1,000 external of the world. tiles and C=150k logical steps estimate logical contribution order 0.03 — above target. Prin d=21 Contribution 0.0032 — It's also too big. Prin **d=23**, p_round=10⁻¹³, The scenarios below are arranged in model budget.

Thus distance increased to 23 from-for a more conservative joint accounting. This is **Not proof that the strong decoder I really do d=23**, and not physical deterioration hardware. This is a correction to model inconsistencies. Runtime proxy Now:

\[
t_0=C\,d\,t_{\rm cycle}
=150000\times23\times400\,{\rm ns}
=1.38\,{\rm s}.
\]

## 5. Ancilla / routing allocation: explicitly, rather than treating it as free»

Old 460 main-region positions retained. Additional synthesis space is not allowed to be declared already in these 460.

**TOY sizing assumption, not compiled floorplan:** Reserved to 100 rotation carriers for each instance, Total 200; Add 262 tiles local ancillary/routing capacity. It's working. **462 synthesis-region tiles**. The area is two rounded fast-block allocations for 100 carriers, But used here as sizing proxy. He is **does not prove** throughput 100 simultaneous injections or achievement C=150k. You fast block Provides serial magic consumption; Save historical parallel-synthesis throughput requires separate layout trace. Known fast-block space/time tradeoff described in [A Game of Surface Codes](https://arxiv.org/html/1808.02892).

I'll reserve it for each factory.. **two d=23 external tiles**: staging/egress and local interface. It's another one **TOY allocation**, unpublished guarantee delivery network. Internal trade: of the goods ancillas I do not repeat. Between factories and synthesis region may require long corridors and supplementary inventory; I're going to give them a name. **R tiles**, Not to appoint a fictional routing percentage.

Total external tiles:

\[
N=460+462+2F+R.
\]

Known counts and assumptions differ. Defects, spares, calibration/remapping reserves — Individual S_Q physical-qubit term, unknown for fixed device. You can't think of him as zero. Number anchor Lower R=0, S_Q=0 Only for the separation of the calculated kernel from unknown additives on the ground.

## 6. The factories, throughput and full-size kernel

The factories are placed in two independent units supply pools, to avoid the possibility of two free associations instances. If k outputs It's a problem. c code cycles, mean production interval as at output:

\[
\tau_{\rm output}=\frac{c\,400\,{\rm ns}}{k},\qquad
F=2\left\lceil\frac{(4.8M/2)c\,400\,{\rm ns}}{k\,t_0}\right\rceil.
\]

For M2: τ_output=13 μs, **23 factories / instance**, Total **46**. Theirs mean supply rate Near **3.538M outputs/s**, v. average demand **3.478M/s**. Small mean surplus does not prove absence stochastic starvation. Peak demand, startup, postselection tails, inventory lifetime, output compatibility and p99 require supply trace.

**All digits — CALC as at source inputs Listed TOY allocation assumptions.** d=23, R=0; This is kernel estimates, Not confirmed full-system costs.

| Resource | Old historical snapshot S0 | M1, old T sub-budget | M2, the same total target | M3, more accurate factory output |
|---|---:|---:|---:|---:|
| Workers logical qubits | 200 | 200 | 200 | 200 |
| T demand | 4 800 000 | 4 800 000 | 4 800 000 | 4 800 000 |
| Logical compiled steps | 150 000 | 150 000 | 150 000 | 150 000 |
| Algorithm/synthesis distance | 19 | 23 | 23 | 23 |
| Number of factories | 484 | 56 | 46 | 116 |
| Factory qubits | ≈16 067 880 | 2 620 800 | 1 991 800 | 3 561 200 |
| Main-region qubits | 332 120 | 486 680 | 486 680 | 486 680 |
| Extra synthesis-region qubits | not included | 488 796 | 488 796 | 488 796 |
| Extra egress/interface qubits | not included | 118 496 | 97 336 | 245 456 |
| Total external tiles | 460, incomplete count | 1 034 | 1 014 | 1 154 |
| Calculated Q | ≈16.4M | 3 714 772 | **3 064 612** | 4 782 132 |
| Idealized t₀ | 1.14 s | 1.38 s | **1.38 s** | 1.38 s |
| Physical rounds | 2 850 000 | 3 450 000 | 3 450 000 | 3 450 000 |
| Reserved Q×t₀, qubit·s | ≈18 696 000 | 5 126 385 | **4 229 165** | 6 599 342 |
| Accepted-output quality proxy | selected by the old estimator | 2.6×10⁻¹¹ | 1.4×10⁻¹⁰ | 2.7×10⁻¹² |
| Additional corridors/spares/stalls | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

M2 — smallest modeled quantum-volume configuration **Of these admitted points**, if redistributive sub-budgets with the previous total target. If you have to keep equal sub-budgets literally.., anchor — M1. It's a specific existing alternative to the weak historical factory allocation, Not the announcement SOTA Total FTQC.

**Relationship 18.70M / 4.23M is not honestly established end-to-end gain.** S0 and M2 different fidelity proxies, ancilla coverage and provisioning. It shows the extent of the change resource accounting with known protocol replacements. Measured apples-to-apples improvement for the reference workload not yet available.

### Logical error budget

M1 preserves ε_log=ε_T=ε_syn=0.002/3. For M2 Designated:

| Budget component | Budget M2 | Contribution proxy, CALC |
|---|---:|---:|
| Logical operations/storage outside factories | 0.000533333 | 1 014×150 000×23×10⁻¹³ = **0.000349830** |
| Accepted resource-state errors | 0.000800000 | 4.8M×1.4×10⁻¹⁰ = **0.000672000** |
| Rotation synthesis | 0.000666667 | retained budget, actual trace not checked |
| Amount assigned budgets | **0.002000000** | Amount proxies c synthesis bound **0.001688497** |

Balance model margin Near 0.000311503 is not a free guarantee against any bursts, coherent errors or repair. When these are activated mechanisms I need to count it. circuit-level bound. Errors inside factory source proxy Second time in logical region Not added; count all external tiles protected — conservative area-time proxy.

Conservation ε_syn Holds the previous required approximation quality. Unagreed source counts do not show that a particular newly compiled trace It actually reaches with 4.8M T. The absence of such verification clearly limits ledger.

### Formula for additives not yet evaluated

\[
Q_{\rm allocated}=3\,064\,612+1058R+S_Q,
\]

\[
t_{\rm actual}\geq
\max(C_{\rm trace}\,d\,t_{\rm cycle},\,t_{\rm supply},\,t_{\rm reaction})
\Delta_{\rm startup/tails/repair},
\qquad
V_{\rm reserved}=Q_{\rm allocated}t_{\rm actual}.
\]

Here. 1058=2×23²; C_trace may differ from historical 150k. B t_reaction already included classical dependencies, a Δ must not repeat the same stalls. Supply and routing should be modelled jointly, not by two independent accelerations.

**TOY sensitivity to corridor reserve**, t=t₀, without defects/stalls:

| Additional R tiles | Q | Reserved qubit·s | Total error proxy With previous synthesis bound | Suitability |
|---:|---:|---:|---:|---|
| 0 | 3 064 612 | 4 229 165 | 0.001688497 | Kernel, routing Not confirmed yet |
| 100 | 3 170 412 | 4 375 169 | 0.001722997 | Lower assigned logical budget in proxy |
| 500 | 3 593 612 | 4 959 185 | 0.001860997 | Lower assigned logical budget in proxy |
| 1 000 | 4 122 612 | 5 689 205 | 0.002033497 | **Not going through total target** |

These R not obtained from the router and not plausible confidence interval. They show why extra space I have to evaluate with logical exposure. With more runtime You have to choose again.. distances, factories and budget.

## 7. Compilation and logical transactions: modern candidates without false transfer

### 7.1. Cultivation-aware routing and scheduling

**Old component:** PSSPC snapshot c serial phase-kickback, without overlap consecutives non-Clifford layers and without full synthesis/delivery accounting.

**Strong, Modern Alternatives:** FlowRouter for joint topological Clifford routing / runtime cultivation; public PureMagic for stochastic supply and shared ancillas; TopoLS + TQEC for factory-fed topological compilation/physical verification. Their published advantages do not set the best method for my long-term circuit.

**Apples-to-apples:** Family hardware compatible; output quality, cycle time, actual circuit and latency Not match. FlowRouter uses Gridsynth ε=10⁻³ and another early-FT regime, - while here average per-rotation synthesis allowance Near 1.1×10⁻⁸. Him. published 2.3× volume ratio not applicable 4.23M qubit·s. PureMagic requires suitable cultivated outputs; its mean cultivation-time Cannot be used for a more stringent output quality without new calibration. [FlowRouter evaluation](https://arxiv.org/html/2609.23756), [PureMagic](https://arxiv.org/html/2512.06484).

**Recalculation:** M_T=4.8M and C=150k As long as they are still in place; Q, t, V Re-assessed **UNKNOWN**. After trace:

\[
F'=2\left\lceil\frac{(M_T'/2)\tau_{\rm output}}{t'}\right\rceil,\quad
Q'=2d'^2N_{\rm trace}+F'q_F+S_Q,\quad V'=Q't'.
\]

Ancilla/routing overhead from occupancy trace, Not from published average ratio. Logical budget depends on the time of life and the full geometry patches. Decoder/I/O are counted according to physical measurement trace. External distillation region does not disappear from compiler flag «free magic».

### 7.2. Surface-code operation scheduling and compact operations

**Old component:** fixed d-round macrosteps, serial layer order, approximate main layout.

**Modern alternatives:** TopoLS/FlowRouter for parallel surgery, operation-aware physical lowering TQEC; compact/padding-free surgery and dense storage from Denser Planar Surface Code. [Current planar primitives](https://arxiv.org/html/2605.30455).

**Apples-to-apples:** NN Doesn't stop it by itself hex-style subgraph embedding in a suitable square device. But it's necessary to test couplers, gate/reset schedule, distances and decoder new boundaries. Reported encoding-rate improvement does not save free logical gates: dense qubits must be removed compute patches; ideal outer yoke decoder and transport Not fully validated in this work of the work.

**Recalculation:** numerical anchor leaves 2d²/tile and C=150k. New Q/t/V/T demand/routing — **UNKNOWN** without same-workload lowering. For reduction only only storage region used sensitivity below. Replacement of one check schedule does not allow automatic division surgery time per two: temporal faults and reaction dependencies remaining.

### 7.3. Modern rotation synthesis: an important test that cannot be missed

**Old component:** angle-independent synthesis and historical M=4.8M, internal incompatible with the original description.

**Modern alternatives:** probability-mixture/fallback small-angle synthesis; Hamming-weight phasing / phase-gradient / catalyst approaches For groups of identical angles. The latter can reduce T-count and depth, by spending additional carriers, catalysts, Toffoli/CCZ resources and routing. [Small-angle synthesis](https://arxiv.org/html/2605.31544), [Full surface-code costs rotations](https://arxiv.org/abs/2508.06236).

**Apples-to-apples:** & Save the same fourth-order Trotter circuit, J/g/Δ, scientific precision and error norm. Quasi-probability estimates with additional repetitions — other output contract; not to replace them by one successful circuit run. Probability mixtures Potentially compatible, but need a list angles and synthesis/channel bounds. Cheap CCZ factory does not replace T factory in circuit, whereN CCZ demand equal to zero as long as published recompilation Doesn't set up a new resource mix.

**Recalculation:** actual M_T', CCZ/catalyst demand, new logical depth and ancillary exposure **UNKNOWN**. Number 20 T/rotation of the conflicting snapshot formulas not counted as automatic four-fold reduction demand. B anchor retained 4.8M T; decrease for the next day M_T checked as sensitivity, Not the result of the target group.

## 8. Strong decoder assumptions and classical I/O

**Old component:** scalar logical-error law without measured decoder cost. This is not benchmark And not proof of advantage over static PyMatching.

**Modern competitive recruitment:** tuned correlated PyMatching, BeliefMatching and Tesseract on the basis of a harmonized circuits; LCD c causal leakage telemetry, if available compatible backend; AlphaQubit 2 How neural accuracy/latency frontier. Static/oracle matching retained by diagnostic baselines. Small exact/TN subset stays ceiling. [Public correlated matching Opportunities](https://github.com/oscarhiggott/PyMatching), [AlphaQubit 2](https://arxiv.org/html/2512.07737v2).

For numerical ledger I don't pick the "most powerful" on another's schedule.. No measurements on ours factory/surgery trace, So, **LER, mean/p50/p95/p99 latency and throughput for all baseline and ORCHESTRA = NOT MEASURED**; gaps to static/oracle/best = NOT ESTIMABLE. Full reporting rules stay in [benchmark_protocol.md](benchmark_protocol.md).

Strong decoders shall apply to computational operations, changing boundaries, transfer/measurement faults and factories, Not just d=23 memory. LCD under-1-μs divided-window metric does not prove 400-ss streaming throughput plus full feedback. AQ2 high-accuracy and AQ2-RT — Different configurations; not available accuracy one and latency other. New specialized device not software-only improvement.

**Counting:** quantum kernel stays M2, d=23. Decoder savings not anticipated. Actual classical compute, memory, energy, backend throughput and tails — **UNKNOWN**. Required input rate Can be evaluated:

| Flow | Accountable proxy M2 | Limitation |
|---|---:|---|
| Binary checks for 200 working patches | 200×528 / 400ns = **264 Gb/s** | Without soft readout, control/metadata and exact boundaries |
| All 1 014 external tiles as normal active patches | 1 014×528 / 400ns = **1.33848 Tb/s** | Surgery/synthesis activity Changed; not physical trace |
| External patch-round workload | 1 014 / 400ns = **2.535 billion patch-rounds/s** | Not FLOPS and not single-core capacity |
| Half of the total Q=3.064612M Measure each cycle | **3.830765 Tb/s** | Whole-machine envelope; variable factory layout/active fraction Not verified |
| Storage of All external binary checks for 1.38 s | **230.888 GB** | Streaming Doesn't require you to keep the whole launch; bytes decimal |
| Required accepted T delivery | **3.478M states/s** | Medium, not peak availability |

Each I/O number — CALC/TOY, not measured bandwidth. Decoding factories uses different types of internal distances, So you can't multiply all Q as at d=23 decoder latency. Local filtering/compression can reduce transmission, But you can't lose the information you need. strong decoder. The savings are not equal to the decline quantum qubit-seconds without measured stall.

## 9. What's dominant now

Here I rank **reserved quantum resource kernel M2**, Because monetary total, classical power and availability Not yet specified. The total real price of the whole car cannot be ranked with the same fractions.

Internal factory routing/ancillas already in line 1. The remaining groups do not cross. General critical-path costs time cannot be added to space of the Independent States percentages.

| Rank Under Q×t₀ | Group | Q, CALC | Qubit·s, CALC | Percentage kernel, TOY CALC | What? software can change |
|---:|---|---:|---:|---:|---|
| 1 | T-state factories with internal ancillas/transfer | 1 991 800 | 2 748 684 | **64.99%** | Existing protocol/configuration, output quality allocation, utilisation, demand |
| 2 | Synthesis carriers + their local ancillary capacity | 488 796 | 674 538 | **15.95%** | Synthesis protocol, parallelism, lifetimes, sharing; quality I have to keep it. |
| 3 | Main ancillary/layout region | 275 080 | 379 610 | **8.98%** | Existing compiler, valid routing/measurement order |
| 4 | 200 working data positions | 211 600 | 292 008 | **6.90%** | Decoder-enabled distance, supported denser storage; physical code limits |
| 5 | Explicit external factory interfaces | 97 336 | 134 324 | **3.18%** | Placement / buffering, maintained supply |
| Not specified | Long corridors, inventory, spare/remapping capacity | UNKNOWN | UNKNOWN | UNKNOWN | Measure; may change this order |
| Not specified | Decoding/control/I/O, stalls, cooling, fabrication | UNKNOWN | UNKNOWN | UNKNOWN | May dominate of the country classical cost and runtime |

If costly T layer It'll be much cheaper, share algorithm/synthesis It's bound to grow. Therefore, the conclusion «factory 98%, "All the rest is irrelevant" is no longer appropriate even for this conditional reference.

## 10. Effect 2× in each component of the of the project

**This is sensitivities, neither achieved results nor proposals for new methods.** For space term Q_i Previously on "The Last" quality/throughput/time:

\[
\text{system resource ratio}=
\frac{Q}{Q-Q_i/2}.
\]

Can't multiply the lines with the overlaps components. Factory area reduction and T-count reduction They often save the same thing.. region.

| Which has been conditionally improved in the 2× | Impact on kernel | Material for the entire programme? / limit |
|---|---|---|
| Factory area with the same accepted quality and output rate | Q×t less than in **1.481×**, reduction **32.50%**, CALC | Yes; this is the main single counted space term |
| Factory throughput Same factory area | From-for integer pools 46→24 factories: Near **1.451×** others retained tiles | Yes; t stays 1.38s if logical path Doesn't change; idle/interface counts can change |
| T demand with the same compiled depth / output quality | The same 46→24 factories in mean proxy | Yes, but it's a condition; new synthesis changes depth, ancillas and resource mix |
| All external algorithm/synthesis tiles | **1.212×**, reduction **17.50%** | It's not half the car |
| Only main ancillary/layout region | **1.047×**, reduction **4.49%** | Small system effect, Goodbye. factories Previous |
| Synthesis carriers with local ancillas | **1.087×**, reduction **7.97%** | Could be useful; often changes simultaneously T demand/runtime |
| Only working data footprint | **1.036×**, reduction **3.45%** | Small effect in itself |
| Total external routing/ancilla/interface tiles: 260+262+92 | **1.119×**, reduction **10.60%** | Saved throughput; does not include internal factory routing |
| LER fast decoder | d=21 Still not going through assigned logical budget with one 2× accuracy | No proven quantum-space gain: distance Discrete |
| Decoder execution time | UNKNOWN | Material if he creates stalls/large classical cost; in idealized t₀ its cost None |
| Syndrome-processing compute / transmission bytes | UNKNOWN for total; relevant classical the cost component decreases | Quantum t₀ does not automatically decrease |
| Classical latency at critical chain | UNKNOWN without trace | Need a share serial dependencies; half mean Doesn't guarantee half p99 |
| Logical compiled depth with the previous T demand | Fixed 46 factories Save mean supply time ≈1.357s; instead t₀/2=.69s It's gonna be supply limit | Provides almost no speedup fixed-allocation Launch; .69s mean supply I need it. 92 factories, without tails/delivery overhead |
| Factory-only production latency, if area additional double | Capacity/time tradeoff; not free of charge software gain | I need to compare Q×t, inventory and whole-program floor |
| Physical fidelity / measurement time | Not authorized as automatic software Replacement | You can calibrate supported controls, But you can't think of a new one hardware quality |

For decoder sensitivity use the same modern round-level proxy. Prin d=21 c resized mean-supply pools logical contribution Near 0.0032193; v. assigned budget 0.000533333 I need it. multiplier Near **6.04**, not 2. With the previous one wall time and geometry exposure I need to count it again. It's a conditional estimate, not a test measured advantage Right decoder.

Another limit is that all factories cannot be physically removed free of charge. Formal de-frosting only their calculated region would have been no more than **2.857×** reduction kernel Q×t₀ with the previous external region. It's a mathematical thing cap one space component, **not plausible software-only maximum**. It is not on the ground of the victim runtime/demand changes or gains, affecting other regions.

## 11. Responses to the five main questions

### 1. After modern replacements that dominate?

B admitted distillation scenario — **non-Clifford resource production**, Then synthesis Support space. B execution time Three different leaders possible: logical dependency depth, accepted-resource delivery and classical reaction. Average supply counts They don't prove which one is actually the main one.

There is no reason to claim that this is a permanent world order after any cultivation/rotation improvements. For full contemporary optimum on ours workload is missing compatible supply frontier, complete compiled circuit and measured classical backend.

### 2. What do you think? bottlenecks More. software-addressable?

**Partially:** rotation synthesis, selection existing resource protocol, quality/distance allocation, concurrent delivery, utilisation, valid surgery scheduling and temporary capacity sharing. They change the big one.. resource region, but limited to physical accuracy, geometry, deadlines and accessible observations.

**Mostly at classical Party:** syndrome processing, decoding implementation/dataflow and runtime scheduling. Their actual system significance Depends on backend profile. Only noise estimation or memory decoder improvement does not delete quantum cost million non-Clifford resources.

### 3. Where the biggest plausible remaining software headroom?

Of the calculated regions The largest sensitive term — **magic resource stack**. The most appropriate place for further measurement — **end-to-end compilation of rotations + preparation/delivery**, Because existing methods Change and demand, And depth, ancillas. It's not like it's a saying that it's easier to think of a new factory or anything else 2× after full modern optimum.

Actual remaining headroom after strongest compatible cultivation+distillation/compilation **Not yet quantified**. Proven integration of known methods may be a major economy, but it will be an improvement baseline, Not automatically research novelty.

### 4. Will it? 2× in each component of the system gain?

**No.** 2× in the dominant, or the dominant factory term has a significant impact on kernel; 2× Only in data region Gives you a few percent..; 2× decoder accuracy may not change distance Total; 2× logical-depth reduction may be able to get back to the old one. supply. First, you need to specify which resource The article has improved and what hasn't changed.

Any claimed 2× full-program result has to include accuracy target, occupied qubits, actual runtime/tails, qubit-seconds and classical cost. You can't give away half T count or faster offline compiler for half FTQC cost.

### 5. Where you need a shift scaling, Not just constant factor?

| Limiting the challenge | Why? constant factor Doesn't solve it for long | What to Measure |
|---|---|---|
| **Perimeter delivery** to growing compute region | Boundary supply can grow like √N to area demand ∝N | Accepted states / logical round as a function N, c routing/quality included |
| **Code overhead vs target failure/depth** | For local surface patches n∝d²; d growing with exposure and precision | Required physical Q and volume v. logical qubits/depth to fixed total target |
| **Global classical decoder/control dependency** | Centralized bottleneck can grow faster available local throughput | Queue growth, p99 reaction and watts to fixed hardware/topology |
| **Postselection / cultivation yield more stringent precision** | Large d can drastically reduce yield; faster local checks They don't cancel. rejection | Accepted-output volume and tails v. p_out to fixed p |
| **Serial critical path** | Less gates outside dependency chain Doesn't decrease runtime | Full causal schedule, reaction-limited steps and unavoidable temporal exposure |

Perimeter/area issue already discussed cultivation-aware schedulers; This is **Not a new idea.. ORCHESTRA**. Constant-factor 2× It can still be valuable on fixed 200 qubits. Scaling change needed to maintain the advantage of growth N, depth or accuracy; Not every useful engineering result is required to change asymptotics.

## 12. What is determined and what remains to be measured

**Established:** historical factories — weak reference configuration; modern; modern and so on local resource protocols must be in baseline. Additional synthesis/delivery space and different logical-error Unit materially Change ledger. Conditional M1/M2/M3 calculated in full within the models; numbers are reproduced from the formulas and JSON.

**Not established:** exact full-stack optimum 2026, valid same-workload routed execution, achieved target as at physical operation circuits, no-backlog classical deployment, Real spares and monetary system cost. Therefore, strongest compiler/LCD/AQ2 performance It's not a part of ours workload.

To turn kernel in a fully-fledged modern world on the full-fledged modern world of the world's benchmark reference, I need it. **Assessment of existing methods**, Without developing a new algorithm:

1. Re-establish version-pinned original TFIM circuit, angles and precision; Agree on conflicting counts c actual compilation.
2. Get compatible factory frontier On one circuit-level noise model, including existing cultivation + Next stages Only published/verified chain.
3. Compiling the same circuit Existing and other existing ones and so on.. TopoLS/PureMagic/Available FlowRouter; Insert real supply availability and factory geometry.
4. Remove whole-run occupancy, external corridors, buffer ages, transport errors, startup, stochastic tails and total quality budget.
5. Profile strong decoders as at computational/factory DEM and recorded classical hardware, including measurement-to-action latency and I/O.

**The field of further analysis is conditional:** non-Clifford demand/supply/delivery looks like a bigger software lever than an isolated one memory decoding. But declare maximum software-only or or or software-first breakthrough Until these comparisons are completed, no can be.
