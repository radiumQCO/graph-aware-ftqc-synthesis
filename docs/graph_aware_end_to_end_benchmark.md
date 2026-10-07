# Graph-aware ZZ: conditional full-program benchmark

Date: 6 October 2026. No new factory protocol or decoder is developed here.

**Conditional result:** the reduction **396 to 297 AND** per ZZ block survives
the modeled catalysis tower, rotation synthesis, catalyst startup, and delivery
accounting. Balanced resource-model replay changes runtime from **11.584 to
10.219 s**, a calculated **-11.78%**. The fixed allocated area does not decrease.
This is not a measured physical FTQC advantage: critical physical interfaces
remain **UNKNOWN**, and the final status is **D**.

Percentages are calculations from stored results using `(B-A)/A`; times and
qubit-seconds are conditional model outputs. The prior carry-only replay is not
the new baseline. The same conditional P workload is used: two independent
periodic 10-by-10 TFIM instances, 200 data logical qubits, Suzuki-4, 20 steps,
J=g=1, timestep 0.25, and evolution time 5. Original QIR and all paper parameters
were not recovered. See the later
[adversarial compiler audit](adversarial_compiler_baselines.md): deeper physical
validation is paused pending strong matched compiler evidence.


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## 1. What is preserved and what is restored and the rest

Source: [graph_cut_phase_synthesis.md](graph_cut_phase_synthesis.md), [delivered_non_clifford_benchmark.md](delivered_non_clifford_benchmark.md), [factory_bottleneck.md](factory_bottleneck.md), [non_clifford_structure.md](non_clifford_structure.md), [weight_arithmetic_bottleneck.md](weight_arithmetic_bottleneck.md), [modern_ftqc_ledger.md](modern_ftqc_ledger.md). Data and gate strings Read from the ancients JSON; synthesis budget and the angles were not counted as more accurate.

Workload P stays **conditional reconstruction**: two independent periodic 10×10 TFIM, 200 working logical qubits, Suzuki-4, 20 steps, J=g=1, Δt=0.25, evolution time 5. Reference Beverland QIR and all parameters paper run not restored. It's the same. P-workload, Not the exact reproduction of the historical programme.

Stayed 101 X and 100 ZZ blocks. Inside X weight is considered as a joint 200 bits; Inside ZZ — cut two torus graphs, 400 edges. Not used symmetry sectors, not removed noncommuting layers, does not overuse weight over X/ZZ basis changes. Row-major graph labels Clearly translated into former ones snake labels for both configurations. It's a renaming circuit targets, not free physical SWAP.

**A:** verified balanced even-aware partial arithmetic, 396 AND/ZZ. **B:** verified C4-cover arithmetic, 297 AND/ZZ. X counter unchanged in both lines. He's the same published-counter implementation; joint global optimum compilation/placement Not approved.

For 201 `PHASE_INTERFACE_UNTIMED` Now there's a full logical gate trace: arithmetic → 8 level in-circuit tower → measurement-assisted cleanup. Re-established 40 catalyst preparations, 201 seed rotation, their real cached Clifford+T strings, twirls, basis changes and inverse circuits. At HWP and tower clean-target AND in both lines **Same old admitted CCZ injection**. It's obviously the same resource substitution; I don't mix CCZ count c T count.

## 2. Precise phase completion and her test

Used existing generalized phase-catalysis building block and in-circuit tower, Us described [Sun et al., Fig. 2–4](https://arxiv.org/pdf/2409.04587). For clean target t and catalyst c=P(φ)|+⟩ one level is the following gate-level completion after normal Clifford cancellations:

```text
CNOT(y,c)
CNOT(x,y)
AND(y,c,t)
CNOT(x,t)
P(2φ) on t                 # recursively supplied by the next tower level
CNOT(x,t)
measured inverse AND(y,c,t) # X readout, outcome-controlled CZ, reset
CNOT(x,c)
CNOT(x,y)
```

Reference x,y Rehabilitate, catalyst Returned. Basis — `x+y+c = (x XOR y XOR c) + 2 majority(x,y,c)`. State of operation prefix target contains relevant majority. Primary phase catalyst and doubled seed phase Gives you the right ones. P(φ) as at x,y. Recursive composition gives you eight required weighted phases of one seed, 8 AND and eight measured inverses; one unused partner Back to |0⟩. It's a restoration of a known scheme, not a proposed new mechanism.

Separate check over-take **65,536** of the 8 combinations weight bits and eight catalyst basis components: whole phase identity Exactly.., garbage targets Peeled, catalyst mapping is a biography for each input. This is composite evidence for superpositions; no statement is made statevector simulation as at 200 qubits. Additional implemented 518 mapped graph checks and 331 X-counter checks; used by previous exhaustive/proof results graph audit.

Synthesis remains the same **positive mixed-diagonal averaged-channel contract**. For 38 selected unique mixtures independently multiplied gate matrices and verified channel bound. All 241 random synthesis branches/twirls equal in A/B. At perfect angles A/B implement one unitary up to global phase. With real approximate strings guaranteed old averaged-channel diamond bound **0.000331836952**, not each selected accuracy, etc. and other factors. and/or other relevant factors. random branch. These two guarantees cannot be combined into an "compiled" statement noisy The program is accurate».

## 3. Complete logical counts

| Meteric, full program | A | B | CALC change |
| --- | --- | --- | --- |
| X AND | 19 897 | 19 897 | +0.00% |
| ZZ AND | 39 600 | 29 700 | -25.00% |
| Tower AND | 1 608 | 1 608 | +0.00% |
| Total compute AND | 61 105 | 51 205 | -16.20% |
| CCZ demand | 61 105 | 51 205 | -16.20% |
| T: sampled synthesis trace | 8 552 | 8 552 | +0.00% |
| T: expected synthesis demand | 8 554.364 | 8 554.364 | +0.00% |
| T: synthesis branch maximum | 8 797 | 8 797 | +0.00% |
| Weighted arbitrary-angle phases | 1 608 | 1 608 | +0.00% |
| Synthesized arbitrary-rotation calls | 241 | 241 | +0.00% |
| Of them seed calls | 201 | 201 | +0.00% |
| Catalyst preparations | 40 | 40 | +0.00% |
| Peak compilation ancillas, conservative allocation | 882 | 682 | -22.68% |
| Peak compilation logical Q, including data | 1 082 | 882 | -18.48% |

8 552 T — one reproducible choice random branches, Not a reduction in mathematical expectations 8 554.364. Retained worst-branch demand 8 797 T. T-state demand Considers seed synthesis and catalyst preparation; 1 608 tower AND paid CCZ, So they were the former ones. 6 432 T not added second time.

Full arithmetic/tower CNOT count: **761,624 → 562,224**, -26.18%. Shared tower completion contains 48 CNOT on the window. From basis changes the former 40 400 H; additional H into the synthesis/catalyst preparation and injection.

Optional 4T-only logical reference, **without new physical replay**: A = 252 974.364 expected T, B = 213 374.364 expected T. This is `4×total_AND + synthesis_T`; primary comparison uses CCZ and T as miscellaneous resources. Historical 4.8M T and old ≈253k T are not current physical baseline.

## 4. Total hardware fixture and the problem of two types factories

Retained p-scale=10⁻³, planar nearest-neighbour surface-code-like platform, d=29, 400 ns ordinary cycle, 50 ns physical gate and 100 ns physical readout. **Full physical noise model and physical reset timing None.** For logical reset The old one is the same.. d-cycle allowance; It's not restored. duration Physical reset. Feedback allowance — 25 cycles = 10 μs, without measured decoder p99.

Grid and routes: 36×32 logical sites, 73×65 tiles Corridors, tile proxy=2d²=1 682 physical Q; 1 091 compilation/data slots + 12 finite buffer slots. Factory area capacity=64 000 physical Q. Both rows use the same coordinates and rectilinear routing rule; intersecting corridor cells Not at the same time, not booked. Total reserved fixture = **8 045 090 physical Q**. It's spacious accounting fixture, not optimal chip for 200 logical qubits.

Main resource-model configuration Saves old tuned sources from [pinned Litinski implementation](https://github.com/litinski/magicstates/tree/8fffa48c2e45d3bb0634559fce6b7b5b45f96966/Python):

| Source | Q | Expected cycles/accepted batch | Batch | Produced-state error proxy |
| --- | --- | --- | --- | --- |
| CCZ, previous admitted point | 35 062 | 52.004607 | 1 CCZ | 2.329194e−9 |
| A′, previous tuned T point | 39 976 | 130.066523 | 4 T | 7.915757e−10 |

**75 038 > 64 000:** At the same time these two of the factories not even in the area. Therefore, primary model uses one region (c) In turn, c 402 source-mode changes. Real reconfiguration/cold-start price **UNKNOWN**. Values 0/29/290 cycles - under - clearly marked sensitivity, Not developed protocol; zero point is optimistic scheduling limit and doesn't mean zero-cost physical operation. Price accepted output and Medium-sized retries already included in source cadence, repeated retry multiplier not added.

For verification without source-mode switching built **Individual** matched configuration: the same CCZ factory + three before audited small 15→1/15→1 T factories. One is in 7 782 Q, has 468.459384 expected cycles/T and proxy 6.076100e−10. Total **58 408 Q ≤ 64 000**. It's a distinctly different operating choice for T, applied equally to A/B; Her numbers don't mix with primary A′. Physical embedding factory shapes and cold pipeline fill Under-still not restored.

Buffers divided equally: 6 slots for CCZ (two three-qubit outputs) and 6 for T. Accepted outputs They're going straight to reserved full-distance buffers past d-cycle **unverified growth allowance**. For concurrent configuration Standard end-use prefetch, one batch to be determined source In the devastation inventory. Any produced surplus paid, stored and dropped at drain. Ways, endpoint injection geometry, output bridge fidelity remaining physical UNKNOWNs.

## 5. Corrections: compulsory work and old conservative artifact

Normal CCZ teleportation outcome m=(ma,mb,mc) requires CZ(b,t)^ma, CZ(a,t)^mb, CZ(a,b)^mc and linear Z updates c coefficients mb·mc, ma·mc, ma·mb. For perfect equiprobable branches Average — **1.5 physical CZ/CCZ**, Not always three; inverse AND requires CZ c probability 1/2. All 64 basis/outcome injection cases Checked, error 0.

Primary replay Performing the Right CZ, Doesn't write them down for free Pauli frame. Linear Z updates monitored through Clifford gates: H, S/S†, CNOT, CZ. Before each AND, inverse AND and T nonzero Pauli frame Physical materialize; End output frame Purified. It's a conventional limited frame tracking, not free passage through any non-Clifford gate. 44 matrix identities Checked up to phase. Random correction outcomes tied to source-operation indices: Unchanged X/startup/phase parts use the same outcomes in A/B and at different scheduler priorities.

Additional conservative replay Reserved all three CZ and linear Z after each CCZ, inverse CZ after each cleanup. It shows the influence of the past worst-branch artifact. **AutoCCZ not set up free.** [AutoCCZ construction](https://arxiv.org/html/1905.08916) It's moving corrections in delayed-choice resource with additional routing qubits and their storage/adaptive readout. Training is required and embedding; previous ordinary-CCZ source doesn't give these costs automatically. I can't take the general, either Clifford frame through arbitrary measures and other persons or groups or groups of persons who are involved in the conduct of public service AND No new payments, and so on. to pay for new corrections.

## 6. Same scheduler objectives

Normal used dependency-list heuristics General block/phase barriers. Resource policy Prefers short ready Clifford route; depth policy — larger remaining critical-path rank; balanced policy Combines rank and route length. First, it is taken into account operand release time. No policy is globally optimal. That's three identical for A/B schedule objectives On one placement; new circuit synthesis None.

| Objective, primary τswitch=29 | A runtime, s | B runtime, s | CALC Δruntime | A active Qs | B active Qs | CALC Δactive |
| --- | --- | --- | --- | --- | --- | --- |
| resource | 11.730 | 10.387 | -11.44% | 16 792 876.231 | 12 370 472.830 | -26.33% |
| depth | 11.531 | 10.212 | -11.44% | 16 558 895.036 | 12 198 131.441 | -26.33% |
| balanced | 11.584 | 10.219 | -11.78% | 16 645 591.937 | 12 204 752.194 | -26.68% |

If each side is allowed to choose the fastest of these three replays, received **11.531 → 10.212 s**, -11.44%. Prin fixed reserved area minimum reserved Qs The minimum is runtime. You can't just give these politicians away for proven Pareto optimum; others not investigated placements and valid surgery schedulers.

## 7. Full A/B Table, primary balanced model

| Meteric | A | B | CALC change |
| --- | --- | --- | --- |
| Reserved/allocated peak physical Q fixture | 8 045 090 | 8 045 090 | +0.00% |
| Peak active factory Q allowance | 39 976 | 39 976 | +0.00% |
| Factory area capacity | 64 000 | 64 000 | +0.00% |
| Finite resource buffer logical Q | 12 | 12 | +0.00% |
| Observed peak output reservation logical Q | 9 | 9 | +0.00% |
| Conservative application logical Q + buffer capacity | 1 094 | 894 | -18.28% |
| Logical readout count | 252 972 | 213 372 | -15.65% |
| Feedback wait events | 130 762 | 110 962 | -15.14% |
| Deferred Pauli materializations | 104 634 | 88 207 | -15.70% |
| Logical unit-gate depth of injection replay | 224 135 | 209 600 | -6.48% |
| Conditional SC-cycle duration | 28 960 242.021 | 25 548 365.209 | -11.78% |
| Conditional runtime, s | 11.584 | 10.219 | -11.78% |
| Conditional active Qs | 16 645 591.937 | 12 204 752.194 | -26.68% |
| Conditional reserved Qs | 93 195 101.393 | 82 215 558.984 | -11.78% |
| Conditional corridor volume, Qs | 1 138 467.008 | 907 527.997 | -20.29% |
| Physical-noise sensitivity proxy | 1.580169e-04 | 1.336843e-04 | -15.40% |
| Synthesis diamond bound | 3.318370e-04 | 3.318370e-04 | +0.00% |
| Arithmetic sum proxy + synthesis, NOT failure probability | 4.898538e-04 | 4.655212e-04 | -4.97% |
| Clifford endpoint operation volume, patchcycles | 134 844 809 | 104 611 178 | -22.42% |
| Total peak logical Q including internal factory ancillas | UNKNOWN | UNKNOWN | — |
| Validated actual physical peak occupancy | UNKNOWN | UNKNOWN | — |
| Validated full-program physical failure probability | UNKNOWN | UNKNOWN | — |
| Actual classical decoder compute | UNKNOWN | UNKNOWN | — |
| Actual total classical I/O | UNKNOWN | UNKNOWN | — |

Logical depth in this table on the table of the table — per-wire unit-duration gate depth completed injection/correction trace, c finite-buffer reuse and barriers; factory production duration and real SC-operation durations excluded. This is not minimal circuit depth. Previous 4T unit-gadget ZZ depths **430 → 448** are valid for their own gate set; They don't predict SC runtime after another CCZ injection and routing. You can't compare these two depth units as one number.

Reserved Qs = total fixed area × runtime. Active ledger contains data/catalyst holding, lifetime arithmetic workspace, tower scratch, occupied corridors, output inventory and intrinsic factory work. Endpoint gate volume It's already inside held patches, So, second time to active ledger not added. They don't add up either. reserved Qs. Landing sites and source shapes not fully integrated, therefore active volume and is conditional, holding data while waiting enabled.

### Resource waits and throughput

| Resource | Request → delivery, μs | A | B | CALC change |
| --- | --- | --- | --- | --- |
| CCZ | mean | 360.334 | 261.337 | -27.47% |
| CCZ | p50 | 310.000 | 184.000 | -40.65% |
| CCZ | p95 | 865.604 | 645.764 | -25.40% |
| CCZ | p99 | 1 020.402 | 766.802 | -24.85% |
| CCZ | max | 1 402.006 | 1 035.606 | -26.13% |
| T | mean | 253.126 | 253.126 | -0.00% |
| T | p50 | 23.200 | 23.200 | +0.00% |
| T | p95 | 1 480.266 | 1 480.266 | +0.00% |
| T | p99 | 1 491.866 | 1 491.866 | +0.00% |
| T | max | 1 515.066 | 1 515.066 | +0.00% |

CCZ consumption throughput full program: 5274.904 → 5010.595 CCZ/s, CALC -5.01%. Less throughput demand may be accompanied by a smaller runtime: less resources required and the number of persons required to participate in the process for the purpose of the project. T demand throughput: 738.253 → 836.844 T/s, CALC +13.35%. Percentiles — distribution requests in one seeded replay c expected factory cadence, **not stochastic factory/decoder latency tails**.

## 8. Waterfall: Where he goes saving

| Transition | Full-program CALC | Limitation |
| --- | --- | --- |
| 99 AND/ZZ × 100 layers | −9 900 compute AND; −9 900 inverse AND | Exact logical count |
| CCZ production | −9 900 CCZ; T synthesis unchanged | 61 105 → 51 205 CCZ: -16.20% |
| Intrinsic CCZ factory work | 514 845.606 accepted-cadence cycles saved; 7 220.607 Qs saved | Source equations; not runtime saving by itself |
| Delivery/injection | −29 700 resource halves, −29 700 injection CX/readouts | Actual route/landing volume is layout-dependent |
| Cleanup/feedback | −9 900 inverse readouts; −19 800 feedback events | Events may overlap; not 19 800 serial waits |
| Clifford network | −199 400 arithmetic CNOT | C4 predicates included; no hidden extra XOR network |
| Corrections, ideal expectation | −14 850 CCZ CZ; −4 950 inverse CZ | Primary replay uses actual seeded branch counts |
| Unrouted 4T ZZ depth | +18 unit-gate layers/ZZ block | A trade-off; paid by full CCZ routing replay, not subtracted as SC cycles |
| Primary net conditional runtime | 11.584 → 10.219 s, -11.78% | Whole P logical trace; physical result UNKNOWN |
| Net reserved physical Q | 8 045 090 → 8 045 090 | Same fixture; smaller workspace does not shrink the chip automatically |

| Nonoverlapping active-ledger component | A Qs | B Qs | B−A Qs | CALC change |
| --- | --- | --- | --- | --- |
| data_memory | 3 896 890.166 | 3 437 788.023 | -459 102.144 | -11.78% |
| catalyst_memory | 779 378.033 | 687 557.605 | -91 820.429 | -11.78% |
| arithmetic_workspace_lifetime | 10 687 826.588 | 7 049 388.460 | -3 638 438.128 | -34.04% |
| tower_scratch_lifetime | 19 926.036 | 19 870.489 | -55.547 | -0.28% |
| reserved_output_inventory_lifetime | 73 791.825 | 60 527.949 | -13 263.876 | -17.97% |
| busy_routing_corridors | 1 138 467.008 | 907 527.997 | -230 939.012 | -20.29% |
| factory_intrinsic | 49 013.835 | 41 793.228 | -7 220.607 | -14.73% |
| factory_mode_switch_allowance | 298.445 | 298.445 | 0.000 | +0.00% |

25% saving applicable ZZ AND, Not the whole program. Doesn't change 19 897 X AND, 1 608 tower AND, rotation programs, catalyst preparation and baseline X/ZZ basis changes. Full CCZ demand decrease approximately by 16.2%. Runtime further defined dependency chains, corridor conflicts and phase windows. Therefore, 1 per cent arithmetic saving doesn't turn into the same percentage runtime saving.

In this spacious place conditional layout Main active savings in **lifetime arithmetic workspace**: 200 fewer allocated ZZ ancillas and shorter length of blocks. Intrinsic factory work — Just a little bit of it.. active ledger. Old «65% factories» were treated differently of the child historical kernel; They do not apply here. It's localizing bottleneck not all possible optimal on the ground FTQC machine.

| Sequential whole-block contribution | A s | B s | CALC change |
| --- | --- | --- | --- |
| startup | 0.051 | 0.051 | +0.00% |
| X | 4.793 | 4.794 | +0.02% |
| ZZ | 6.740 | 5.374 | -20.26% |

Amount block intervals plus final frame flush/drain ♪ Gives me ♪ runtime. A slight difference in unaltered X blocks may arise from buffer/factory availability since previous ZZ block; gate/rotation/outcome choices these X blocks same.

The price of the re-turn was separately checked phase wires in the same layout. Lower **Only clearly recorded CNOT**, without resource delivery and outcome-controlled CZ: number and corridor volume independent of scheduler order.

| Stage | A CNOT | B CNOT | A CNOT-corridor Qs | B CNOT-corridor Qs | CALC Δroutes |
| --- | --- | --- | --- | --- | --- |
| X_compute | 99 788 | 99 788 | 55 713.685 | 55 713.685 | +0.00% |
| X_phase | 4 848 | 4 848 | 5 325.153 | 5 325.153 | +0.00% |
| X_cleanup | 99 788 | 99 788 | 55 713.685 | 55 713.685 | +0.00% |
| ZZ_compute | 276 200 | 176 500 | 261 239.359 | 205 105.637 | -21.49% |
| ZZ_phase | 4 800 | 4 800 | 5 118.178 | 4 812.242 | -5.98% |
| ZZ_cleanup | 276 200 | 176 500 | 261 239.359 | 205 105.637 | -21.49% |

In this placement Additional fine for manifest phase CNOT not found: ZZ phase CNOT-corridor volume change to -5.98% with the same CNOT and the same angles. It's not a common property of anyone placement. He's already in the general routing ledger; Second time not added to net improvement. Full delivery/CZ-route The difference is in results.json and primary active-component table.

## 9. Sensitivity and feasible-area cross-check

| Matched existing-source configuration | A conditional s | B conditional s | CALC change |
| --- | --- | --- | --- |
| A′ time-mux, τ=0, sampled_frame | 11.581 | 10.216 | -11.78% |
| A′ time-mux, τ=29, sampled_frame | 11.584 | 10.219 | -11.78% |
| A′ time-mux, τ=290, sampled_frame | 11.619 | 10.251 | -11.77% |
| A′ time-mux, τ=29, conservative | 13.183 | 11.397 | -13.55% |
| CCZ + 3 small T, resource | 12.122 | 10.780 | -11.07% |
| CCZ + 3 small T, depth | 11.924 | 10.608 | -11.04% |
| CCZ + 3 small T, balanced | 11.977 | 10.612 | -11.39% |

B concurrent balanced cross-check active Qs = 17 112 834.212 → 12 612 209.041, -26.30%; fixed physical Q unchanged. Source-mode changes = 0 **Because there's no switch**, Not because they're declared free... Source T outputs: 8553 in A/B, including 1 Unused outputs. It's separate factory operating choice, no reason to change primary reliability numbers.

The benefits of conditional models does not disappear after the former all-CZ conservative artifact or after a separate matched factory-area cross-check. But τ=290 not worst-case bound for unknown physical reconfiguration. These sensitivities does not cover arbitrary growth/layout/correlated-noise costs. In general unknown serial overhead U relative runtime saving change as `(tA−tB)/(tA+U)`; to configuration-dependent overhead unknown even the real sign physical savings.

## 10. Error contract, decoding and I/O

Total execution target retained **0.002**: synthesis, extra magic/delivery and other logical operations Under 0.002/3. Distance policy same, d=29; Not reduced distance y B, to artificially increase savings. No line announced certified passing target.

| Level of evidence | Status |
| --- | --- |
| Ideal graph-cut phase / X phase / tower | Exact identity + compositional verification, for all inputs; no symmetry-sector restriction |
| Approximate compiled average channel | Previous certified synthesis bound; Equal precision budget |
| Logical resource counts | Full reproducible trace, without untimed phase windows |
| Physical noise proxy | Source state-error proxies + toy memory/gate/growth allowances |
| Validated common circuit-level failure probability | UNKNOWN; Not measured |

Proxy uses the old one.. toy law pL(d)=0.1×(100p)^((d+1)/2), p=10⁻³. Memory waiting included. Growth allowance uses output dx=21, Although real source patch anisotropic dx=21,dz=9: **dx alone does not certify transition**. Overlapping memory/gate allowances and produced-state infidelity does not automatically give whole-channel diamond bound. Amount proxy+synthesis Table — sensitivity accounting, not the physical probability of failure. Correlated bursts, leakage, stochastic retry tails and decoder failures not added by fictional zeros.

| Mandatory decoder metric | Value |
| --- | --- |
| Static PyMatching LER | NOT MEASURED |
| Oracle PyMatching LER | NOT MEASURED |
| Strongest adaptive baseline LER | NOT MEASURED |
| Strongest neural baseline LER | NOT MEASURED |
| My LER | No new decoder; NOT MEASURED |
| Gap to Static / Oracle / best competitor | UNKNOWN |
| Decoder mean / p50 / p95 / p99 / throughput | UNKNOWN; 10 μs — allowance, not benchmark |

Classical I/O also not measured. **TOY binary-check floor** for 200 d29 data patches: `200×(29²−1)/400ns = 420 Gb/s`, Same in A/B; additional workspace, surgery, factories, soft readout and control metadata not included. For all 1 103 reserved logical slots the same toy patch formula ♪ Gives me ♪ 2.3163 Tb/s, Not tested whole-machine flow. CPU/GPU/FPGA cost, actual strong-decoder queues and total I/O remaining UNKNOWN.

## 11. What else is in the way of a strict? physical benchmark

| Missing component | What is already counted | What exactly is missing |
| --- | --- | --- |
| Physical factories/startup | Expected accepted cadence, retries, intrinsic volume, finite inventory, final drain | Factory-shape embedding, cold pipeline fill, time-mux reconfiguration circuit |
| Factory output → d29 | Same d-cycle allowance and explicit sensitivity error | Validated anisotropic-to-ordinary-SC growth/escape circuit, time and fidelity |
| Delivery/injection landing | Corridor conflicts and logical injection/corrections | Landing-site occupancy, merge/boundary schedule and full physical faults |
| Ordinary logical operations/reset | Same d/2d allowances | Physical H/S/reset gadgets under common clock/channel |
| Classical controller/decoder | 25-cycle reaction allowance and event counts | Measured backend throughput/tails on actual surgery/factory DEM |
| Reliability | Separate source/output/memory sensitivity terms | One shared physical noise model, strong decoder and validated delivered/full-run failure |

The answers to the main question are therefore divided: **non-Clifford demand — proven less; full conditional logical-model runtime/volume — less than; secured physical capacity — same; present physical cost and failure probability — Goodbye. UNKNOWN.** New algorithm search and novelty audit not conducted.

## 12. Reproduction

[README and teams](../analysis/graph_aware_end_to_end/README.md), [workload builder](../analysis/graph_aware_end_to_end/workload.py), [scheduler](../analysis/graph_aware_end_to_end/scheduler.py), [run script](../analysis/graph_aware_end_to_end/run.py), [verification](../analysis/graph_aware_end_to_end/verify.py), [results](../analysis/graph_aware_end_to_end/results.json), [verification results](../analysis/graph_aware_end_to_end/verification.json), [compressed full logical traces](../analysis/graph_aware_end_to_end/workloads.json.gz).

```powershell
analysis/.venv/Scripts/python.exe analysis/graph_aware_end_to_end/run.py --concurrent
analysis/.venv/Scripts/python.exe analysis/graph_aware_end_to_end/verify.py
analysis/.venv/Scripts/python.exe analysis/graph_aware_end_to_end/report.py
```

Full logical trace SHA-256: `de29f1eb3bfe952f3770f7998bdc9c9bfc8102d0aeeb789740793692be50fe2b`. Input hashes in results/trace manifest. Checked 7 input hashes That's all. 18 replay rows. Results checks Not substitute for missing physical-noise validation.

## Final status

D. Benchmark remains incomplete because critical physical components are missing
