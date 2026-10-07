# Magic-state factories: the remaining cost by stage

Audit date: 6 October 2026. This studies existing protocols; no new factory,
decoder, or controller is proposed.

**Finding:** in tuned two-level distillation, the main cost is protected
Pauli-product measurements, internal transport, and maintaining protected patches
during those operations. The selected geometric accounting is approximately
**39% L1 / 35% L2 / 26% internal paths and ancillas**, a calculation from this
model rather than a hardware measurement. Cultivation depends strongly on reuse:
escape and waiting for acceptance dominate active-use accounting, while rejected
early attempts matter more when the entire region stays reserved.

The historical **65%** factory share used **4.8 million T** and cannot be carried
over after recompilation. A state at the factory boundary is not automatically
a successfully delivered logical gate. The subsequent
[delivery benchmark](delivered_non_clifford_benchmark.md) remains physically
incomplete; cultivation delivery was not measured. Remaining error budget is
headroom, not an observed delivery error.

The workload remains the conditional reconstruction of two independent 100-spin
TFIM instances, **200 data logical qubits**, rather than a recovered original
Beverland QIR circuit. See [non_clifford_structure.md](non_clifford_structure.md).


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## 1. What exactly is holding constant?

The original task is conditional P-reconstruction of two independent 100-spin TFIM, Total **200 logical qubits**. It is not a related task. 200 spins and not restored original QIR Beverland. The parameters and limitations of recovery are described in [non_clifford_structure.md](non_clifford_structure.md).

I're using the existing compilation `hwp_global_joint_batch_in_circuit_tower_mixed_diagonal`, without change in quantum algorithm:

| Value | Value |
|---|---:|
| Expected T-demand | 253 374,364 |
| Maximum of the branches considered | **253 617** |
| Hamming-weight carries | 238 388 T |
| Consumption CCZ in this compilation of the data on | **0** |
| Additional logical qubits before factories/routing | to 891 |
| Purpose of total error | **0,002** |
| Budget synthesis | 0,002/3 |
| Selected budget faulty magic states + of additional shipments | **0,002/3** |
| Other operations/memorials | 0,002/3 |

Three-part budget split — **my conservative condition of comparison**, Not theorem and not the result of the optimization. Unused stock synthesis I don't re-spill. Budget below applies to the additional error of the factory resource and its path to use; the overall error of computational Clifford Other transactions and the transaction is recorded in the remaining.

Consequently,, proxy-claim for one delivery status:

\[
p_{T,\mathrm{delivered}}\leq\frac{0.002/3}{253617}
=2.628635567\cdot10^{-9}.
\]

This is union-bound accounting for stochastic logical-fault proxies. Independence of different exits union bound not required. **Infidelity Arbitrary coherent status is not per se equal diamond error T-gate:** without model noise/twirling/teleportation These numbers don't prove complete channel-error contract.

Hardware Keep: immediate neighbours 2D grid, surface-code-like superconducting stack, circuit noise scale **p=10⁻³**. Contingent normal SC-cycle — **400 ns**, gate — 50 ns, measurement — 100 ns from the previous ledger. Lower clocks different sources do not automatically consider the same. Leakage, bursts and drift not included in published numerical points.

## 2. Selection and strength of evidence

Three detailed existing implementations selected and other relevant measures. and/or and/or and/or to be tested:

1. **A: distance-tuned 15→1 / 20→4**, Fast surface-code option.
2. **B: small-footprint 15→1 / 15→1**, other point trade-off area/time.
3. **C: GSJ cultivation d₁=5 → grafted matchable d₂=15**, Prospective candidate with a conditional rating T-quality.

A and B using one family of published surface-code constructions, But different distillation blocks and schedules. They're not three independently best algorithms. This is **Strong, compatible and quantifiable candidates. and access to the public. for the public. for the public for the public**, Not proven world optimum all works 2026 year.

Historical year A/B Doesn't make them weak. They need the right ones. distances, output fidelity and routing. Modern alternatives are further tested in §8. If the new job doesn't publish the full path to the proper quality state on this hardware, Her promise doesn't replace the one being tested baseline.

### Original published operating points

| Candidates | Distances | Physical qubits, ancillas included | Cycles adopted by the batch | Exits | Published output-error proxy |
|---|---|---:|---:|---:|---:|
| A | L1=(13,5,5), 6 Clusters; L2=(23,11,13) | 43 300 | 130 | 4 T | 1,4×10⁻¹⁰ / T |
| B | L1=(9,5,5); L2=(21,9,11) | 7 780 | 469 | 1 T | 6,1×10⁻¹⁰ |
| C | d₁=5, d₂=15 | see. circuit audit below | 25 measurement-rounds Under surviving path | 1 candidate | ≈2×10⁻⁹, conditional T estimate |

A/B: [Litinski, Table 1, §§3–6](https://arxiv.org/html/1905.06903v3). C: [GSJ cultivation](https://arxiv.org/html/2409.17595), numerical limitations and erratum as discussed below. Noise scale same, **Full circuit/noise/decoder models different**; rating accuracy between the articles is not apples-to-apples benchmark.

Next, all fractions, fractions and amounts — **My calculations** from fixed sources, not new ones measurements physical hardware.

## 3. A: two-tier 15→1 / 20→4

### 3.1 Full route and condition that every step of the road

Public calculation functions: [onelevel15to1.py](https://github.com/litinski/magicstates/blob/8fffa48c2e45d3bb0634559fce6b7b5b45f96966/Python/onelevel15to1.py) and [twolevel20to4.py](https://github.com/litinski/magicstates/blob/8fffa48c2e45d3bb0634559fce6b7b5b45f96966/Python/twolevel20to4.py). Lower numerical evaluation uses these operations, not the other one. factory.

| Step | Resource and duration | T/CCZ | Check, retry and error proxy | Purpose |
|---|---|---|---|---|
| Raw input | Physical faulty-T measurements Inside L1; Individual high-distance injection pipeline not added | 15 noisy T-equivalent rotations as at L1 try; 0 CCZ | Errors physical gates The source model | Add non-Clifford a resource Clifford preparation Doesn't create |
| L1 | 6 parallel blocks; 2 594 physical Q Total 15 564; 30 cycles Try | 15 raw Unit; 20 adopted by the L1 outputs necessary for L2 batch | p_reject,L1=0,04705749; ≈31,481 cycles/accepted output Unit; pl1=1,86425×10⁻⁶ | Squeeze raw faults, Before the darling L2 uses them |
| L1 checks/postselection | 4 logical X-check qubits On the block, already inside footprint and time | Supplementary high-quality T no | All four checks must accept; attempt to otherwise throw | Check syndromes Finds dangerous input-fault patterns |
| Internal transfer/auto-correction | 10 530 Q by a certain lower break-up; t_L1=13 cycles | L1 T Expenditure on Pauli rotation L2 | Transport/storage/gadget channels included in model | Deliver and apply rotation with the right measurement-dependent correction |
| L2 20→4 | 7 persistent logical qubits: 4 outputs + 3 checks; Region 17 250 physical Q; 10×13=130 cycles to L2 retry correction | 20 adopted by the L1 T / batch, 0 CCZ | p_reject,L2=0,000112843; ≈130,01467 cycles/accepted batch | Second error-detection layer plus protected output |
| L2 check/output | 3 logical X checks; acceptance of all exits of the same batch | New T no | p_out=1,44275×10⁻¹⁰/T, proxy Model | Dissipate Accepted batch from the Deviated |
| Output consumption | There is already a closure with late/follow-up steps; storage while consuming included in the source | 4 adopted by the T They're going to the program | It's not a free state to be delivered anywhere.. chip | Release output patches, not to use rejected resource |
| Additional external storage/delivery | **Not defined without layout and demand trace** | Unknown, untraceable 0 | Individual residual error and congestion budget | Put the fortunes where and where they are needed |

The public model includes average retries; Again multiply it qubitcycles as at `1/(1-p_reject)` You can't. Feed-forward and remote external delivery may add costs beyond the published overlapped schedule.

Number raw resources: Without repetition **20×15/4=75** during the weekend T. C p_reject Both stages are given **78,7125 raw T-equivalents/output** in demand-matched count. Continuously employed L1 When overfilling buffers may produce more: this account does not simulate discarded surplus. Raw physical T-equivalent Doesn't mean expensive protected T.

### 3.2 Reproducible break-up

Formulas pinned code Give **43 344 Q**; Table 1 round to 43 300. The text of the article once appears d_X2=21 at numbers operating point d_X2=23; used Table 1 and corresponding code parameters, not mixed.

Identify non-overlapping geometric categories:

\[
Q_1=6\cdot2[(13+4\cdot5)3\cdot13+2\cdot5]=15564,
\]
\[
Q_2=2(4\cdot23+3\cdot11)3\cdot23=17250,
\]
\[
Q_{\mathrm{transfer}}=43344-Q_1-Q_2=10530.
\]

The latter category includes connecting lanes L1 and additional ancilla/buffering Figure 2 -. This is **Internal**, not chip-wide routing cost.

With a permanently reserved area for each region and the environment and the environment.:

| Category | Q | Q×cycles/output | Percentage factory volume, My calculation |
|---|---:|---:|---:|
| L1 cores | 15 564 | 505 887 | **35,91%** |
| L2 core | 17 250 | 560 688 | **39,80%** |
| Internal transfer/ancillas | 10 530 | 342 264 | **24,29%** |
| Total | **43 344** | **1 408 839** | **100%** |

«Re-evaluation syndrome checks» — Not category four: they're being executed inside all three. Split footprint-time as at mutually exclusive «checks», «gate», «memory» No definition accounting policy You can't.

In these formulas, the measurement physical ancillas already included. For SC-Regional factor 2 About to divide qubits as at data and measurement ancillas. Persistent logical check qubits — separate concept; they cannot be added to physical Q.

### 3.3 Specific expensive operation

L2 He does. **20 logical Pauli-product π/8 rotations**, Two-flow service resources. Each uses fault-tolerant Joint measurement with resource on the resource qubit; logical measurement requires multiple physical syndrome extraction, Not just one reliable physical measurement.

On this one. operating point:

\[
t_{L1}=\max\left(d_{m2},\frac{6d_m}{(1-r_1)(n_{L1}/2)}\right)
=\max(13,10.494)=13.
\]

**Bottleneck throughput — Duration protected measurement, Not a deficiency raw T.** Double speed L1 with unchanged L2 measurement It won't speed up the exit. Remove L2 checks — change error-detection contract. There are known ways to do it otherwise in §8; There is no guaranteed removal of value without replacement of the security mechanism.

### 3.4 The current task of the current protocol: A′

Reference A destined for a more stringent produced quality. To prevent her from being deliberately dispersed, she's checked **36 Existing parameter combinations**: L1 fixed (13,5,5); d_X2∈{19,21,23}, d_Z2∈{7,9,11}, d_m2∈{11,13}, n_L1∈{4,6}. Circuit/protocol Doesn't change.

For that. scan I're obviously giving you a further condition: produced error ≤ half per-delivered-state budget; the second half at least stays for the extra delivery faults. This is my reservation rule, Not the result of the article. Passed 8 Points. Minimum intrinsic volume Among them:

| Value | A′, Best in limited scan |
|---|---:|
| L1 / Number of blocks | (13,5,5) / 6 |
| L2 | **(21,9,13)** |
| Physical qubits | **39 976** |
| Expected cycles/accepted batch from 4 T | **130,06652** |
| Produced output-error proxy | **7,91576×10⁻¹⁰ / T** |
| L2 rejection | 0,000511452 |
| Qcycles/output | **1 299 885** |
| Additional error reserve/output | **1,83706×10⁻⁹** |

Non-transverse regions of the same formula..:

| Region | Q | Qcycles/output | Percentage A′ |
|---|---:|---:|---:|
| L1 cores | 15 564 | 506 089 | **38,93%** |
| L2 core | 13 986 | 454 778 | **34,99%** |
| Transfer/ancillas | 10 426 | 339 018 | **26,08%** |

Intrinsic volume below the reference A as at **7,73%**, My calculation. Largest region Now L1, but throughput still limiting L2 protected measurement: t_L1=13. **A′ — Current strongest quantitative T-only reference this limited audit**; not worldwide/global optimum and not fully routed delivered-gate simulation. A solution with more permission produced error, Other L1 distances or other delivery allocation may be different.

## 4. B: small 15→1 / 15→1

Source: [smallfootprint.py](https://github.com/litinski/magicstates/blob/8fffa48c2e45d3bb0634559fce6b7b5b45f96966/Python/smallfootprint.py). Same hardware class, Other organization concurrency.

| Step | Q / cycles / resources | Error and retries | Condition |
|---|---|---|---|
| Raw + L1 | One L1 core 1 586 physical Q; 15 raw T-equivalent rotations, 30 cycles/attempt | Reject=0,03626784; ≈31,129 cycles adopted by the L1 | Get Interim T |
| L1 check | 4 logical X checks already included L1 | pl1=8,24086×10⁻⁵ before next processing | Catch input faults; Low distance cheaper, but output Worse A |
| Transfer/ancillas | 1 408 Q; 11 cycles transport + 11 cycles Pauli-product measurement as at L2 rotation | Transport/storage channels taken into account | Sustaining one consecutively L2 stream |
| L2 | 4 788 Q; 5 persistent logical qubits: 1 output + 4 check qubits; **15 rotations** | t_L1=max(22,31,129)=31,129 cycles | Resuscitate Resource Error |
| L2 postselection | Inside the same area of | Reject=0,00325465; 468,459 cycles/accepted T; p_out=6,07610×10⁻¹⁰ | Accept only past checks output |
| Protected consumption | Storage/consumption model already included | Not separately full-chip delivery | Free exit without loss protection |
| External buffer/delivery | Undefined | Residual error and time apart | Need physical route to the consumer |

Pinned formula ♪ Gives me ♪ **7 782 Q**. Round Table — 7 780; literal geometric descriptions may differ from one another boundary terms. For shares, use one formula of the reference:

| Region | Q | Qcycles/output | Percentage reserved factory volume |
|---|---:|---:|---:|
| L1 | 1 586 | 742 977 | **20,38%** |
| L2 | 4 788 | 2 242 984 | **61,53%** |
| Transfer/ancillas | 1 408 | 659 591 | **18,09%** |
| Total | **7 782** | **3 645 551** | **100%** |

Without repetitions 225 raw T-equivalents/output; with two retry probabilities — **234,230**. CCZ not consumed.

Here. **L1 supply Limit throughput**: One cheap L1 It takes time for each of them. 15 inputs, But protected L2 occupied and awaiting. Transport + joint measurement occupied by 330 cycles scheduled windows to retries; Near 137 cycles remaining supply waiting. These are temporary windows, not separate interest qubitcycles: L1 and L2 working simultaneously.

The price of a smaller area — **≈2,59× greater intrinsic Qcycles/T**, than the original A. For one factory instance footprint about to 5,57 less than, but output cadence much worse. «Less qubits» does not mean "a cheaper programme».

## 5. C: cultivation — review of the public scheme

Secure [Official repository GSJ](https://github.com/Strilanc/magic-state-cultivation/tree/871e68ff6df2f75190b1bfd6351459d1b5a037e3); circuit builder — [`_integration.py`](https://github.com/Strilanc/magic-state-cultivation/blob/871e68ff6df2f75190b1bfd6351459d1b5a037e3/src/cultiv/_construction/_integration.py), reference lifetime accounting — [`make_lifetime_plot.py`](https://github.com/Strilanc/magic-state-cultivation/blob/871e68ff6df2f75190b1bfd6351459d1b5a037e3/src/cultiv/make_lifetime_plot.py).

Started **S-proxy** circuit dcolor=5, dsurface=15, r_growing=5, r_end=10, unitary injection, uniform depolarizing p=0,001. **1 024 000** attempts, seeded Stim 1.14.0. I only take the moment of early rejection; not measuring order error 10⁻⁹.

### 5.1 What the Scheme Makes

| Phase | surviving-path rounds | Activated physical Q | Raw T-equivalent gates On full attempt | What provides |
|---|---:|---:|---:|---|
| Injection | 1 | 13 | 1 | Add physical non-Clifford state Small code |
| Cultivation/checks/growth | 8 | 14–42 | 52 | To be resolved magic eigenstate c flags; growth to d=5 and stabilization |
| Graft stabilization | 5 | 462 | 0 | Increase protection to the large patch before removal color region |
| Matchable transition | 1 | 463 | 0 | Make it late decoding tractable for matching construction |
| Wait for complementary gap | 10 | 463 | 0 | Get a decision if you're reliable enough candidate |
| External growth/storage/gate delivery | Not published for this exact complete contract | Undefined | Undefined | Apply T to the program without the possibility of rolling it back |

Full surviving path: **53 raw T-equivalent physical gates**, **14 839 CX pairs**, **3 795 physical measurements**. It's a scheme account, not a number expensive logical T states. B S-proxy location physical T I should be.. S/S†. CCZ No need.. Measurement/workspace qubits included in peak **463**; Computer logical ancillas Programme not added.

Check magic value uses forward/reverse parity checking, including flags. After cultivation state is not considered to be normal surface-code d=15: This is matchable grafted construction. Unable to complete state, intermediate state and error performed T-gate — different values.

### 5.2 Ours expected cost, with regard to abandoned attempts

For round k Measured survival **Before** implementation: s_k. Rejected at the end round Trying to pay for it anyway round.

\[
V_{\mathrm{active}}=\frac{\sum_k q_k s_k}{a},\qquad
V_{\mathrm{fixed}}=\frac{463\sum_k s_k}{a}.
\]

Lock **a=0,01** — published approximate yield for targeted d=5 operating point. Ours early-postselection sample ♪ Gives me ♪ **0,053118** to final gap decision; this value **does not replace** a. After cultivation stage in this particular of the S circuit survives 0,187208. I don't announce these early figures as a playback.. T-quality or definitely matching to a separate ungrown point of article on the article.

Received:

| Phase | Active Qrounds/accepted output | Percentage active cost | If all cell 463 Q reserved | Percentage fixed-cell cost |
|---|---:|---:|---:|---:|
| Injection | 1 300 | **1,90%** | 46 300 | **14,24%** |
| Cultivation | 14 160 | **20,72%** | 225 860 | **69,47%** |
| Graft stabilization | 25 657 | **37,54%** | 25 712 | **7,91%** |
| Matchable transition | 2 641 | **3,86%** | 2 641 | **0,81%** |
| Gap waiting | 24 594 | **35,98%** | 24 594 | **7,56%** |
| **Total** | **68 351** | **100%** | **325 107** | **100%** |

This is **ours Monte Carlo cost calculations for published on the public of the public S-proxy**, Contingent per a=1%. Percentages not in general FTQC cost. They're using measurement-round units; rounds different number gate layers.

The shares are rounded; this is sampled cost profile, Not exact constants. Indeterminate yield with required real-T quality and errors packing/timing model More significant than the indicated arithmetic accuracy.

B active Model escape + transition + wait = **77,38%**. B fixed-cell models injection + cultivation = **83,71%**. The physical space organization changes the answer to the question "what dominates"».

**Active volume The plan includes the rapid release/reuse of the site. and the public. and the public.**, Which is not proven packing scheduler. Fixed-cell volume assumes the entire region cannot be reused by other attempts before this attempt finishes. These are two clear ones. accounting scenarios, not strict lower/upper limits of any factory: additional buffers, fences and reset/decision latency can make more value.

Average paid approximately **2 395 raw T-equivalent gates/accepted output** in eager-rejection Model. Take `53×100=5300` It would be wrong for her: many shots to be dropped T gates. The number of attempts, tails latency and sufficient buffer for steady throughput Not yet determined.

Ideal terminal MPP/stabilizer/observable readout used only as simulation boundary and **not paid as physical training**; Last real syndrome round retained. This is different from direct copying of the author's integral plot with two last amended survival entries. The new table is therefore separate and other measures. transparent calculation, not a statement of exact reproduction of their drawing.

### 5.3 Compatibility: where the evidence ends

Published T estimate **2×10⁻⁹** pass produced-state proxy budget:

\[
253617\cdot2\cdot10^{-9}=0.000507234 < 0.002/3.
\]

For an additional error delivery There's only one thing left. **6,286×10⁻¹⁰ as at output**. For old ones. 4,8 million T same produced quality I wouldn't have passed budget.

YES. C three restrictions:

1. d=5 T-quality evaluated through S-proxy and conjectured conversion; full T simulation d=5 My audit is not implemented.
2. GSJ §2.6 contains erratum on 6-cube signs on the side of the stabilizers to transversal H_XY. S-cost audit does not confirm the correction of the actual T circuit.
3. Paper endpoint does not include consumption/gate teleportation; Late grafted patch not equal normal SC d=15. Po published idle-quality The results just hold him and count him for a long time ready-for-use You can't.

Source of these restrictions: [GSJ §§2.6, 3.2–3.3](https://arxiv.org/html/2409.17595). **C — conditional comparison candidate, Not past full 200-qubit delivered-gate contract winner.** A/B also have model-based quality, not hardware demonstration, But their protected consumption I think he's in the equations.

### 5.4 You can't be sneaking down decoder wait

Reference C assumes **10 μs** complementary-gap latency, submitted by the rounds. With my conditional 400 ns normal SC-cycle 10 rounds — 4 μs, Not 10 μs. In addition, cultivation rounds A different number gate layers.

Therefore, **Not multiplied C volume as at 400 ns for direct comparison with A/B**. Net clock toy: if real wait stays 10 μs, a late rounds actual 400 ns, I need it. 25 wait rounds instead 10. With the same measured survival That would add **≈36 891 Qrounds/output**; retention of the previous p_out after additional rounds not proved. Number — sensitivity calculation, not compatible operating point.

Exact Meaning bottleneck: after high growth to ~463 qubits The factory holds candidate and fulfils syndrome rounds, Until he has a credible decision to adopt. Accelerating the classical solution helps this section, but **Doesn't eliminate itself quantum protection or his error budget**. It's a factory condition for the suitability of exit; new decoder/controller architecture Not developed here.

## 6. Full delivery and cost of the entire programme

For reference A/B, with a conditional normal SC-cycle=400 ns:

| Resource | A | B |
|---|---:|---:|
| Expected accepted-batch time | 52,006 μs / 4 outputs | 187,384 μs / output |
| Average output interval to steady schedule | 13,001 μs | 187,384 μs |
| Intrinsic volume / delivered-to-factory-boundary T | 0,563535 Q·s | 1,458220 Q·s |
| Work for 253 617 T | **142 922 Q·s** | **369 829 Q·s** |
| Product N×p_out proxy | 3,65907×10⁻⁵ | 1,54100×10⁻⁴ |

For a set **A′**: ≈52,027 μs as at 4 adopted by the T, Average interval ≈13,007 μs; intrinsic volume **0,519954 Q·s/T**, Total demand **131 869 Q·s**. Exactly. A′, Not the original A, should be used in the subsequent on the subject T-only sizing.

It's the work of fully loaded factories, **not runtime Programme**. Not included factory idle time After exhaustion demand, startup/drain, external buffer, chip-wide routing and stalls Computer qubits. Physical qubits and runtime You can't get the whole program by sharing this volume to the old 1,38 s: old schedule was related to another compilation.

For a job runtime τ and perfect steady demand required average throughput Only gives optimistic sizing:

\[
F\ge\left\lceil\frac{N_T\tau_{cycle}}{\tau}\,
\frac{C_{batch}}{n_{out}}\right\rceil.
\]

Piki demand and retries requires additional sizing. CCZ outputs may borrow more delivery lanes, than T. The replacement of the factory does not guarantee its accessibility states It is in moments of dependence logical operations.

For delivery accounting You need to add separate **growth bridge, route, queue storage, final injection measurement, classical feedback**. If part consumption already included in source equations, It can't be paid for twice.. Unknown value recorded unknown, not 0.

Illustration error reserve, **toy SC memory model**:

\[
p_L(d)=0.1(100p)^{(d+1)/2},\quad p=0.001.
\]

Then.. d=19/21/23 ♪ Gives me ♪ 10⁻¹¹/10⁻¹²/10⁻¹³ per proxy cycle. For additional storage n cycles estimate n p_L(d) shall be placed in on the ground residual budget. This is not fidelity validation grafted→normal conversion, not estimate leakage and not theorem o hardware. You transition I need to check separately...

## 7. Which transactions are mandatory and which are dependent on implementation

| Dear part | What condition protects | You can get it in a known other way? | What can't be promised honestly |
|---|---|---|---|
| Non-Clifford raw input | A Marriage stabilizer operations | Distillation, cultivation, resource-state gadgets, Other codes | Get magic state of one Clifford operations free of charge |
| Error detection L1/L2 | Do Not Miss input-fault patterns | Other published codes/protocols; cultivation instead logical distillation | Remove checks without change fidelity contract |
| Repeated syndrome/joint measurements | Squeeze noisy-measurement ambiguity and logical faults | Other FT measurement schedules/codes | That one physical shot replaces protected logical measurement |
| High-distance output protection | Save quality after last check | Distance tuning, Other escape geometry | That perfect acceptance cures faults, what happened after him |
| Internal transfer/auto-correction | Pass state And properly processed measurement outcomes | Known compact/twist gadgets and concurrent schedules | That giving up correction automatically retains the required gate |
| Postselection/retries | Better quality is conditional quality quality quality control quality control measures accepted output | Published early rejection, different acceptance thresholds | Change threshold and hold output error permanent without verification |
| External storage/delivery | Feasibility for irreversible programme delivery | Known routing/buffering/code-growth constructions | Move retry after the use of the condition in the arbitrary programme |
| Whole-cell reservation | Capacity isolation, absence collision | Packing/reuse Existing circuit stages | Achieve active-area integral without layout and latency constraints |

**There's no proof that it is.. 43k Q, 130 cycles or 99% rejection fundamentally inevitable.** But some conditions are creation magic, Transport error protection, correct non-Clifford gate — Mandatory. Unlimited compute does not delete physical noise, limited local, and so on. connectivity and finite-time measurements.

For selected topological operations, normal cost pattern Q≈d² and a time of order protected d rounds ♪ Gives me ♪ Q×time≈d³. This is scaling Specific implementation family, Not the lower limit of all fault-tolerant architectures.

## 8. Testing modern literature: What already solves part of the problem

| Existing alternative | Confirmed utility | Why not declare a complete replacement for ours?? baseline |
|---|---|---|
| **MSC-LS, v2 Aug 2026** | NN square grid; cultivation escape in rotated SC Through lattice surgery; early rejection | Presented T-quality ≈3×10⁻⁶ to p=10⁻³,dcolor=3: **Not going through** 2,63×10⁻⁹ target. Reduction cost in their regime Cannot be carried over d5 |
| **Recursive surface-code distillation, Mar 2026** | Compact 3-tile recursion; includes different measurement/check schedules | Preliminary analysis; I need specific operating distances and input errors. Prin p=10⁻³ working, but not enough to take output distance normal SC. Low asymptotic proportional-quality threshold does not mean that the method is fully inoperable |
| **Low Spatial Cost CCZ, Jun 2026** | Compact Pauli-rotation/twisted-measurement representation, less area reference CCZ layout | Time and total spacetime Dependent on pipelining; paper does not publish full-fledged p=10⁻³ circuit-level supplied-and-delivered T operating point. Comparison with another old CCZ geometry does not prove superiority over tuned A |
| **Zero-level CCZ, May 2026** | Small physical Preparatory block for CCZ | Number qubits small block is not worth protected usable CCZ after growth and delivery; appropriate full contract I need to check. |
| **CCZ→2T catalysis** | Existing resource conversion | Needed CCZ supply, protected catalyst, Account correlated errors/catalyst contamination and conversion/delivery; 1 CCZ not equal 2 free of charge T |
| Other transversal/fold-transversal architectures | Sometimes they cut back preparation/gadget overhead | I need to check it out separately connectivity and threshold; Not change the fixed hardware Invisible |

Sources: [MSC-LS paper](https://arxiv.org/pdf/2510.24615v2), [public MSC-LS implementation](https://github.com/yutakahirano/msc-ls/), [recursive distillation](https://arxiv.org/html/2603.05409), [compact CCZ factory](https://arxiv.org/html/2606.24170v1), [zero-level CCZ](https://arxiv.org/abs/2605.21867), [catalyzed conversion](https://arxiv.org/html/1812.01238).

**Early rejection, resource-state substitution, compact ancillas and distance tuning already exists.** They're not a new idea ORCHESTRA. A more recent date does not replace a full-scale test cost/error path.

### CCZ as separate existing compilation comparison

Current workload Pays 59 597 HWP AND Four T each. Known Toffoli/CCZ-state injection may replace this compute resource as at **59 597 CCZ**, Left measurement-assisted inverse and injection overhead; see. [weight_arithmetic_bottleneck.md, §8](weight_arithmetic_bottleneck.md).

At a comparable published point 15→1 / 8→CCZ: Q=47 000, cycles=60, p_out=5,2×10⁻¹¹, volume=2,82 million Qcycles/CCZ. For a set A′ four T They're going to be ≈5,200 million Qcycles. This is **Existing conditional resource-type comparison**, Not new protocol. Full gate/route/error contract Not yet counted. I're not replacing 238 388 T as at 59 597 «T» And not write it down as savings achieved.

## 9. What exactly is to be tested next - without inventing the method

The next check shall select one existing one circuit and count **Successful delivery T/CCZ gate**, Not just the state at the edge factory:

1. Secure Physical noise model and gate timings, including reset/readout, then use them for all candidates.
2. For A/B expand the limited number of cases already completed distance/concurrency scan Real delivery allocation; Select parameters for the current error reserve, rather than under 4,8 million T.
3. For C Check real T circuit/erratum and append Existing growth/storage/consumption circuit. Cost-only S proxy does not complete this inspection.
4. Every attempt to write down Q(t), Real time, reasons rejection, consumed resources, accepted output error, time-to-ready. For rare error I need it. enumeration/validated analytical model or the corresponding volume sampling.
5. On fixed layout Comparison whole-cell reservation and permissible reuse. Count reset latency and latency decision; do not release the area until the signal is received reject.
6. Give the same one T-demand trace my existing compilation; count idle factory area, queueing, stalls data qubits, delivered failure budget.

For final factory benchmark I need it. expected/mean cost, p50/p95/p99 ready latency, throughput and delivered-gate quality. **The current document does not measure steady-state factory latency or decoder benchmark:** circuit rounds and average analytical cadence not issued for these measurements.

## 10. Answer to the main question

**In a mood-set conventional A′ Honey fault-tolerance operation — protected Pauli-product measurement plus content of protected distillation regions and domestic resource paths.** L1≈39%, L2≈35%, paths/ancillas≈26% intrinsic reserved volume. These geometric regions are comparable; they cannot be separated from syndrome checks in an independent diagram without double counting. Raw-input purity after L1 It's good enough: throughput crawl into a measuring window L2.

**B cultivation C Main active-area bottleneck — exit into sufficiently protected and decoded code plus waiting acceptance.** With full section secured bottleneck Moves to Many discarded early attempts. This dependence on reservation/reuse — real research uncertainty, not a solution found.

Thus, there is a specific subject for further audit: **How much it costs to retain and transfer non-Clifford resource with required reliability, including unsuccessful attempts and physical space that cannot be immediately re-used**. I didn't prove that this one cost I have located the conditions that make it. None breakthrough, No new method declared.

## Reproduction

Files:

- [`analysis/fetch_factory_sources.py`](../analysis/fetch_factory_sources.py): public code snapshots, commit pins, SHA-256 manifest.
- [`analysis/factory_audit.py`](../analysis/factory_audit.py): the same published channel equations, region ledger, S-proxy early-rejection cost sampling.
- [`analysis/results/factory_audit.json`](../analysis/results/factory_audit.json): quantitative results and data, layer/stage costs, error proxies.
- [`analysis/results/factory_gsj_d5_s_proxy.stim`](../analysis/results/factory_gsj_d5_s_proxy.stim): Exact semplicate.
- [`analysis/factory_requirements.txt`](../analysis/factory_requirements.txt): separate environment of old Stim versions; does not replace dependence synthesis analysis.

Start after loading of source and installation factory dependencies in a separate environment:

```powershell
analysis/.factory_venv/Scripts/python.exe analysis/factory_audit.py --scan --cultivation
```

NumPy adapter changes only numerical linear algebra instead mpmath; quantum operation order/noise channels retained. Primitive I gave you the cricket. max difference **9,81×10⁻¹⁸**. Pinned M2 source contains debugging `breakpoint()`: Only this stop shall be disabled when starting. Output errors — double-precision model estimates rounding to several significant numbers not accurate certified bounds.

Cultivation cost sample excludes ideal terminal readout and takes into account the cost round pending decision on rejection. Seed=20261006, shots=1 024 000. Full T-quality d5, external delivery and physical whole-program schedule Not Verified. Available documents on synthesis/QEC not rewritten as these imputed results.
