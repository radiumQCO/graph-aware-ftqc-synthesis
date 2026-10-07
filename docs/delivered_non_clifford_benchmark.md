# Delivered non-Clifford operations: A-prime, cultivation, and CCZ

Date: 6 October 2026. No new factory, decoder, or quantum algorithm is proposed.

**The strict three-way physical benchmark is incomplete:**
`INCOMPLETE_NO_THREE_WAY_PHYSICAL_WINNER`. A reproducible resource-model comparison
of A-prime and CCZ exists for the same carry network and a conditional layout.
Cultivation delivery fields remain `null`; unavailable costs are not zero.

The narrow finding is a **2.852-fold reduction in resource-production cost** for
one CCZ versus four T states in the selected published models, for the same
clean AND. This is neither the full FTQC improvement nor a validated delivered
gate error. The conditional P workload is two independent 100-spin periodic
10-by-10 TFIM instances, 200 data logical qubits, Suzuki-4, and 20 steps.
Original Beverland QIR and all original parameters were not recovered.

The selected historical compilation has expected demand **253,374.364 T** and
maximum **253,617 T**. Its **238,388 T = 59,597 clean AND** are Hamming-weight
carries. See [non_clifford_structure.md](non_clifford_structure.md) and
[weight_arithmetic_bottleneck.md](weight_arithmetic_bottleneck.md).


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## 1. What is restored and what is not yet restored

Saved P-Reconstruction from [non_clifford_structure.md](non_clifford_structure.md): **two independent 100-spin TFIM**, 200 data logical qubits; 10×10 periodic lattice in each, Suzuki-4, 20 Steps. Reference QIR Beverland and all reference parameters not restored. It's a conditional reconstruction, not a precise original program.

Existing selected compilation: `hwp_global_joint_batch_in_circuit_tower_mixed_diagonal`. For her, what she expected.. total demand — 253 374,364 T; Maximum — 253 617 T. Of them **238 388 T = 59 597 clean AND** are relevant Hamming-weight carries. [Previous arithmetical audit](weight_arithmetic_bottleneck.md) Checks the network used.

The exact one is restored here **carry-Sub-graph of this renovation**, including its Clifford Environment:

| Operation | Number |
|---|---:|
| H for X basis changes | 40 400 |
| CNOT for weight computation, Network back and back ZZ parity | 757 176 |
| Compute AND | 59 597 |
| Measuring inverse AND, without T | 59 597 |
| Unrecorded in time phase/tower interface | 201 |
| Total records trace | 916 971 |

The layers: 101 X and 100 ZZ. For X weight is considered as a joint 200 bits; for ZZ — weight 400 edge-parity bits. All maintained per-qubit dependencies and borders of non-converting blocks.

**15 229 remaining T And the length of the journey phase/tower circuits deleted replay.** They are not declared free: trace They are standing in clear positions `PHASE_INTERFACE_UNTIMED` and global barriers. So the brought seconds are relevant carry-Sub-graph with missing phase windows; this is not runtime Total programme. Missing windows will change the real demand, Releases and storage.

Trace — exact sequence macros, but not re-established hardware trace with absolute timestamps. The latter build a conditional model of the schedule. SHA-256 compressed reproducible trace: `60bbda761382b5064c5628fd7f167ce5deee875ccaa92eb77d8dca5abd65ed3a`.

## 2. The same exit challenge

Both lines require the same line coherent operation:

\[
|a,b,0\rangle\longmapsto |a,b,a\land b\rangle.
\]

T-The option uses the existing four-T temporary AND and measuring inverse. CCZ-Option — existing CCZ-state injection, H as at target before/after and the same inverse. It's a replacement. resource type in a known gadget; 59 597 CCZ You can't write it down like 59 597 T. Basis: [temporary AND](https://arxiv.org/html/1709.06648), [Toffoli resource injection](https://arxiv.org/html/1212.5069).

Independent ideal test CCZ injection Checked everything 8 measurement outcomes × 8 basis amplitudes: maximum deviation **0**. Four Checks-T AND and measured inverse gives a deviation less 10⁻¹⁴. Linearity extends these tests to superpositions. **They don't check physical noise or delivery.**

## 3. General condition hardware/layout fixture

Saved platform assumptions: **2D nearest-neighbour surface-code-like hardware**, p-scale=10⁻³, Normal SC-cycle=400 ns. Total computation distance in this calculation — **d=29**. Choice distance is not a certificate total failure probability.

| Parameter | Same value |
|---|---:|
| Workers logical data | 200 |
| Reservedl logical slots, including 891 compilation ancillas | 1 091 |
| Additional final output buffer | 12 logical-qubit slots |
| Grid logical sites | 36×32 |
| Logical sites + Corridors | 73×65 tiles |
| Conditional footprint tile | 2d² = 1 682 physical Q |
| Separate capacity for factories | 64 000 physical Q |
| Full fixed area fixture | **8 045 090 physical Q** |
| Classical feedback allowance | 25 cycles = 10 μs |

This is **new, clear, intentionally spacious fixture for verification accounting**, not restored chip, not recommended layout and not optimal evaluation 200-logical FTQC. Corydor tiles Reserved for all execution time. Internal shapes no plants invested in physical grid: only checked area capacity. One area A′ or one selected CCZ factory. You can't give up this one area-verification for physical packing.

Each logical slot The two lines use the same coordinates the same. the same. Rectilinear routes They walk along free corridors, conflicting cells are not allowed to occupy simultaneously. of the. CCZ ♪ I'm gonna give you three ♪ resource halves, T — one. Normal dependency-list scheduler changes order only disjoint macros; policy one for two lines, global optimum not stated.

Timing allowances: route/CX=2d cycles, H/S/injection/reset≈d cycles. CCZ injection Includes three CX, measurements, feedback and conservatively reserves all three possible and conservatively reserve CZ fixups and Z corrections. It's the top schedule branch corrections, not minimum implementation [AutoCCZ](https://arxiv.org/html/1905.08916). For T Also expected correction feedback. Better known frame/auto-correction implementations here not declared executed.

**Growth/delivery — logical allowances, not complete physical circuits.** All accepted batch outputs immediately to the pre-selected full-distance buffer; They're not exposed until they ask... At bridge selected d cycles. Fidelity anisotropic factory output → ordinary SC not checked, bottleneck entry-port/merge geometry Physically unverified. Not called these d cycles priced conversion.

## 4. Settings of existing factories under the same AND-Objective

Used pinned public channel/cost equations from [Litinski repository](https://github.com/litinski/magicstates/tree/8fffa48c2e45d3bb0634559fce6b7b5b45f96966/Python). I don't compare the tune T factory with known excess CCZ factory from the old table.

| Value | A′: 15→1 / 20→4 | 15→1 / 8→CCZ |
|---|---:|---:|
| L1 (dX,dZ,dM), Number of blocks | (13,5,5), 6 | (13,5,5), 6 |
| L2 (dX,dZ,dM) | (21,9,13) | (21,9,13) |
| Physical Q as at factory | 39976 | 35062 |
| The Entrances accepted batch | 4 T | 1 CCZ |
| Expected cycles / accepted batch | 130.067 | 52.005 |
| Produced-state error proxy | 7.916e-10 / T | 2.329e-09 / CCZ |
| Qcycles resources AND | 5 199 539.314 | 1 823 385.518 |
| Intrinsic Qseconds All 59 597 AND resources | 123 950.778 | 43 467.323 |

A′ taken from previous restricted 36-point scan. CCZ retuning Checks 54 point point L1 fixed; minimum selected intrinsic volume among those passing through produced-state proxy allowance. It's not global optimum. Published average acceptance/retries already included in cadence — Repeat by retry factor You can't.

Source models already contains part output storage/overlapped consumption. Here, external delivery is added as a separate conservative allowance; without one physical The diagrams cannot be fully checked and excluded overlap. Therefore, the amount is not being paid for the exact end-to-end factory cost.

One. AND Initially selected 4×(0,002/3)/253 617 = **1,051454×10⁻⁸** extra-resource error allowance. Half of this value is used as CCZ produced-state cut-off. It's the same output-task budget, although different resources have different errors.

## 5. Results matched resource-model replay

**All numbers below are my calculations in the given fixture, Not physical measurements.** Subsequent gate Operations are not guaranteed success in real noise.

| Meteric carry-Sub-graphs | A′ + 4T AND | CCZ AND | Cultivation |
|---|---:|---:|---|
| AND completed in the model | 59 597 | 59 597 | unknown |
| Resources | 238 388 T | 59 597 CCZ | unknown delivery |
| Runtime, s | 19.489 | 15.530 | null |
| Reserved physical Q | 8 045 090 | 8 045 090 | null |
| Reserved qubit-seconds | 156 787 105.634 | 124 938 282.910 | null |
| Throughput, AND/s | 3 058.053 | 3 837.601 | null |
| Maximum batch-output reservation, logical Q | 12 | 9 | null |
| Measured delivered-gate error | null | null | null |

AND service latency — elapsed interval between readiness operands and the end of the macro in the schedule; some target preparations May occur in advance. These intervals overlap: not equal to program runtime.

| AND service, μs | Mean | p50 | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|
| A′ + 4T | 361.452 | 344.800 | 575.200 | 689.600 | 2 620.000 |
| CCZ | 220.270 | 193.202 | 307.602 | 319.202 | 2 504.000 |
| Cultivation | null | null | null | null | null |

| Resource request → end of route, μs | Mean | p50 | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|
| A′ + 4T | 11 807.890 | 46.400 | 77 008.400 | 99 995.600 | 105 402.800 |
| CCZ | 82.608 | 55.602 | 170.002 | 181.602 | 2 366.400 |
| Cultivation | null | null | null | null | null |

It's distribution **for one determinist replay**, not experimental latency distributions and not p99 stochastic retries. Long request intervals including occupied corridors and waiting operands; They are not "time of manufacture of one". T». Producer uses expected cadence, And the rare burst stalls/retry tails Not yet.. sampled.

Relationship model-runtime A′/CCZ = **1.255**. It depends heavily on location, macro list policy, buffer policy and missing phase windows. Proclaiming it of the world CCZ Total requested benchmark You can't.

## 6. Where they're spent active qubit-seconds

Reserved Qseconds The above include all fixed area and simple area. In the following table, separate operation-volume ledger: Q×time Realized model operations on the sites in question on the ground of; holding data memory It's not possible. Idle resource buffers are separately considered busy operations. I don't fold this one. ledger c reserved Qseconds.

| Area | A′ + 4T, Qs | CCZ, Qs |
|---|---:|---:|
| Normal Clifford operations and their routes | 1 290 119.918 | 671 443.472 |
| External resource delivery paths | 611 657.155 | 347 054.729 |
| CCZ Clifford fixups | 0.000 | 230 182.309 |
| Internal factory production | 123 950.778 | 43 467.323 |
| Idle full-distance resource buffers | 239 205.841 | 8 032.804 |
| Final injection operations | 9 302.472 | 17 442.135 |
| Feedback reservation | 11 026.637 | 9 021.794 |
| Measured inverse fixups | 20 186.639 | 20 186.639 |
| Growth allowance | 4 651.236 | 3 488.427 |
| Low-distance idle storage | 0.000 | 0.000 |
| Amount operation-volume ledger | 2 310 100.675 | 1 350 319.630 |

In this CCZ replay **Normal Clifford operations/paths, external delivery and CCZ fixups greater intrinsic factory production**. This localizes the next dimension in this fixture: A logical network and protected routes, not just the production of a resource. This arrangement cannot be carried over to optimally packed chip or full workload No phase.

Share of factories in total FTQC-The program is now unknown. Previous «65%» was a share of another, a historical one kernel. No line here confirms that factories are actually occupied 65% modern end-to-end hardware volume.

## 7. Errors: What is assessed and not proven

Total program target retained **0,002**: synthesis / extra magic+delivery / other logical operations Under 0,002/3. Full maximum T-demand it's a problem. delivered-T allowance **2,6286356×10⁻⁹**. For carry-Sub-graph used relevant part of resource; not misspent phase budget again.

Supplementary sensitivity model: pL(d)=0,1×(100p)^((d+1)/2), p=0,001; ordinary d29 ♪ Gives me ♪ 10⁻¹⁶ per proxy cycle. For bridge used output dX=21. **At the source anisotropic patches (dX=21,dZ=9): one dX Doesn't describe everything faults.** Real bridge/gate error may be significantly different. Overlapping memory/operation allowances also do not constitute a severe breakup of the physical fault channel.

| Proxy-Amount | A′ + 4T | CCZ |
|---|---:|---:|
| Factory-output contribution | 1.887e-04 | 1.388e-04 |
| Growth allowance | 6.913e-06 | 5.185e-06 |
| Data memory | 5.316e-06 | 4.236e-06 |
| Routes / gates | 2.887e-07 | 1.925e-07 |
| Protected resource residence | 3.822e-08 | 4.233e-09 |
| Low-distance residence | 0.000e+00 | 0.000e+00 |
| Total sensitivity proxy | 2.013e-04 | 1.484e-04 |

**Passing a proxy Doesn't mean passing failure target.** State infidelity Not automatically gate diamond error; physical noise/decoder/growth fidelity Not measured. Fields measured LER and validated full-program contract remaining null/false. Number logical cycles to full error budget Cannot be certified from this table.

Because it's factory audit, decoder baselines It wasn't done here. To make sure that no measurement is made clear:

| Required decoder metric | Value |
|---|---|
| Static PyMatching LER | Not measured |
| Oracle PyMatching LER | Not measured |
| Strongest adaptive baseline LER | Not measured |
| Strongest neural baseline LER | Not measured |
| My LER | own decoder No; not measured: not measured |
| Gap to Static / Oracle / best competitor | not calculated without comparable LER |

Classical decoder compute and actual I/O not benchmarked; 10 μs — fixed assumption latency, Not achieved decoder p99. Shadow/LCD/neural claims not added.

## 8. Why? cultivation retained outside delivered comparison

Published GSJ d5 quality estimate Near **2×10⁻⁹** applicable to specified cultivation construction/noise and relies on proxy/conjecture for full T-quality; see. [GSJ assumptions/errata](https://arxiv.org/html/2409.17595). My previous one.. public-code replay measured early-rejection **cost**, not rare T-gate errors. It's not a routine test 10⁻⁹ sampling-million shots.

Mandatory non-compliance interfaces:

1. Real-T d5 validation with account taken errata.
2. Grafted accepted output → total ordinary surface-code patch with verified fidelity.
3. Storage, routing and final T injection under general circuit noise and decoder.
4. Acceptance-decision timing Total 400 ns clock: 10 μs Meaning 25 ordinary cycles, Not 10.

Produced-state proxy leaves 2,6286356×10⁻⁹ − 2×10⁻⁹ = **6,286356×10⁻¹⁰ / T** as at extra delivery. It's a small reserve **Not yet measured as spent**. It cannot be said that cultivation Not going through target or that she wins: unknown delivery fields — `null`, Status `NOT_ADMITTED_TO_DELIVERED_GATE_COMPARISON`.

## 9. What outcome is already suitable for decision?

**CCZ resource substitution deserves full physical Comparison:** cheap clean AND not required to be paid for four separate T resources. It's famous. compilation/resource choice, Not a new idea... Settings CCZ factory under the same heading AND error allowance It was cheaper than four settings T Current source equations.

**The largest remaining area cannot be honestly declared as found for the entire system.** Limited replay This is protected Clifford/path/delivery work. For cultivation Question-still in bridge/storage/acceptance-to-consumption; It can't be ranked by delivered cost Without these interfaces. Not yet included in the core programme physical phase/tower schedules.

A specific controlled entry will not be required for a full launch, but will require a new algorithm: complete, complete and complete. circuit/demand trace; physical factory + growth + consumption circuits for all three candidates; embedding Total NN layout; Single noise model with the same reset/readout/idle channels; controller and decoder timings. Their absence — The Cause incomplete status, Not the computational victory of a single method.

## 10. Reproducibility and verification

- [Replay and CCZ parameter scan](../analysis/delivered_benchmark.py).
- [Number of results and status](../analysis/results/delivered_benchmark.json).
- [Same fixture](../analysis/results/common_delivery_fixture.json).
- [Precision compressed carry trace](../analysis/results/carry_demand_trace.json.gz).
- [Pinned source hashes](../analysis/sources/factories/manifest.json), old [factory audit](factory_bottleneck.md).
- [Separate factory environment](../analysis/factory_requirements.txt).

```powershell
analysis/.factory_venv/Scripts/python.exe analysis/delivered_benchmark.py
analysis/.factory_venv/Scripts/python.exe analysis/report_delivered_benchmark.py
analysis/.factory_venv/Scripts/python.exe analysis/verify_delivered_benchmark.py
```

Checked demand counts, inverse counts, corridor validity, Limited buffer reservation, and ideal CCZ injection. Additional integrity/equivalence checks written in [delivered_verification.json](../analysis/results/delivered_verification.json). This is model and entry checks; full physical fidelity/retry-tail validation Not declared.
