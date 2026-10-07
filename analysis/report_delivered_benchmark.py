"""Render the bounded-scope factory delivery audit from its computed results."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results/delivered_benchmark.json').read_text())
t,c=r['resource_model_rows']; cf=r['ccz_factory_scan']['best']
fa=json.loads((ROOT/'results/factory_audit.json').read_text())
a=fa['distillation']['best_within_limited_scan']
def n(x):return f'{x:,.3f}'.replace(',',' ')
def lat(row,key):
    v=row[key]
    return ' | '.join(n(v[k]) for k in ('mean','p50','p95','p99','max'))
active_t=sum(t['intrinsic_component_qubitseconds'].values())
active_c=sum(c['intrinsic_component_qubitseconds'].values())
production_ratio=4*a['qubitcycles_per_output']/cf['qubitcycles_per_output']
runtime_ratio=t['runtime_seconds']/c['runtime_seconds']
md=f'''# Delivery non-Clifford operations: A′, cultivation and CCZ

Date: **6 October 2026**. New factory, decoder or quantum algorithm not proposed.

**Strict Triangular benchmark has not yet been completed.** Status: `{r['strict_benchmark_status']}`. There\'s a reproducible comparison **Resource models** A′ and CCZ per carry-network and one contingent site. Cultivation was not assigned invented delivery values: its end-to-end Fields retained `null`.

Narrow, confirmed result: for the same pure AND-Production of one transaction CCZ Standing in **{production_ratio:.3f} less than**, than production of four T, in selected published models. It\'s not even a value-of-all ratio. FTQC-and no confirmation of the reliability of the delivery gate.

## 1. What is restored and what is not yet restored

Saved P-Reconstruction from [non_clifford_structure.md](non_clifford_structure.md): **two independent 100-spin TFIM**, 200 data logical qubits; 10×10 periodic lattice in each, Suzuki-4, 20 Steps. Reference QIR Beverland and all reference parameters not restored. It\'s a conditional reconstruction, not a precise original program.

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

Trace — exact sequence macros, but not re-established hardware trace with absolute timestamps. The latter build a conditional model of the schedule. SHA-256 compressed reproducible trace: `{r['trace']['trace_sha256']}`.

## 2. The same exit challenge

Both lines require the same line coherent operation:

\\[
|a,b,0\\rangle\\longmapsto |a,b,a\\land b\\rangle.
\\]

T-The option uses the existing four-T temporary AND and measuring inverse. CCZ-Option — existing CCZ-state injection, H as at target before/after and the same inverse. It\'s a replacement. resource type in a known gadget; 59 597 CCZ You can\'t write it down like 59 597 T. Basis: [temporary AND](https://arxiv.org/html/1709.06648), [Toffoli resource injection](https://arxiv.org/html/1212.5069).

Independent ideal test CCZ injection Checked everything 8 measurement outcomes × 8 basis amplitudes: maximum deviation **0**. Four Checks-T AND and measured inverse gives a deviation less 10⁻¹⁴. Linearity extends these tests to superpositions. **They don\'t check physical noise or delivery.**

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

This is **new, clear, intentionally spacious fixture for verification accounting**, not restored chip, not recommended layout and not optimal evaluation 200-logical FTQC. Corydor tiles Reserved for all execution time. Internal shapes no plants invested in physical grid: only checked area capacity. One area A′ or one selected CCZ factory. You can\'t give up this one area-verification for physical packing.

Each logical slot The two lines use the same coordinates the same. the same. Rectilinear routes They walk along free corridors, conflicting cells are not allowed to occupy simultaneously. of the. CCZ ♪ I\'m gonna give you three ♪ resource halves, T — one. Normal dependency-list scheduler changes order only disjoint macros; policy one for two lines, global optimum not stated.

Timing allowances: route/CX=2d cycles, H/S/injection/reset≈d cycles. CCZ injection Includes three CX, measurements, feedback and conservatively reserves all three possible and conservatively reserve CZ fixups and Z corrections. It\'s the top schedule branch corrections, not minimum implementation [AutoCCZ](https://arxiv.org/html/1905.08916). For T Also expected correction feedback. Better known frame/auto-correction implementations here not declared executed.

**Growth/delivery — logical allowances, not complete physical circuits.** All accepted batch outputs immediately to the pre-selected full-distance buffer; They\'re not exposed until they ask... At bridge selected d cycles. Fidelity anisotropic factory output → ordinary SC not checked, bottleneck entry-port/merge geometry Physically unverified. Not called these d cycles priced conversion.

## 4. Settings of existing factories under the same AND-Objective

Used pinned public channel/cost equations from [Litinski repository](https://github.com/litinski/magicstates/tree/8fffa48c2e45d3bb0634559fce6b7b5b45f96966/Python). I don\'t compare the tune T factory with known excess CCZ factory from the old table.

| Value | A′: 15→1 / 20→4 | 15→1 / 8→CCZ |
|---|---:|---:|
| L1 (dX,dZ,dM), Number of blocks | (13,5,5), 6 | (13,5,5), 6 |
| L2 (dX,dZ,dM) | (21,9,13) | (21,9,13) |
| Physical Q as at factory | {a['qubits']} | {cf['qubits']} |
| The Entrances accepted batch | 4 T | 1 CCZ |
| Expected cycles / accepted batch | {n(a['expected_cycles_per_accepted_batch'])} | {n(cf['cycles_per_accepted_batch'])} |
| Produced-state error proxy | {a['output_error_proxy']:.3e} / T | {cf['output_error_proxy']:.3e} / CCZ |
| Qcycles resources AND | {n(4*a['qubitcycles_per_output'])} | {n(cf['qubitcycles_per_output'])} |
| Intrinsic Qseconds All 59 597 AND resources | {n(t['intrinsic_component_qubitseconds']['factory_intrinsic'])} | {n(c['intrinsic_component_qubitseconds']['factory_intrinsic'])} |

A′ taken from previous restricted 36-point scan. CCZ retuning Checks 54 point point L1 fixed; minimum selected intrinsic volume among those passing through produced-state proxy allowance. It\'s not global optimum. Published average acceptance/retries already included in cadence — Repeat by retry factor You can\'t.

Source models already contains part output storage/overlapped consumption. Here, external delivery is added as a separate conservative allowance; without one physical The diagrams cannot be fully checked and excluded overlap. Therefore, the amount is not being paid for the exact end-to-end factory cost.

One. AND Initially selected 4×(0,002/3)/253 617 = **1,051454×10⁻⁸** extra-resource error allowance. Half of this value is used as CCZ produced-state cut-off. It\'s the same output-task budget, although different resources have different errors.

## 5. Results matched resource-model replay

**All numbers below are my calculations in the given fixture, Not physical measurements.** Subsequent gate Operations are not guaranteed success in real noise.

| Meteric carry-Sub-graphs | A′ + 4T AND | CCZ AND | Cultivation |
|---|---:|---:|---|
| AND completed in the model | 59 597 | 59 597 | unknown |
| Resources | 238 388 T | 59 597 CCZ | unknown delivery |
| Runtime, s | {n(t['runtime_seconds'])} | {n(c['runtime_seconds'])} | null |
| Reserved physical Q | 8 045 090 | 8 045 090 | null |
| Reserved qubit-seconds | {n(t['reserved_qubitseconds'])} | {n(c['reserved_qubitseconds'])} | null |
| Throughput, AND/s | {n(t['throughput_AND_per_second'])} | {n(c['throughput_AND_per_second'])} | null |
| Maximum batch-output reservation, logical Q | {t['peak_reserved_output_buffer_qubits']} | {c['peak_reserved_output_buffer_qubits']} | null |
| Measured delivered-gate error | null | null | null |

AND service latency — elapsed interval between readiness operands and the end of the macro in the schedule; some target preparations May occur in advance. These intervals overlap: not equal to program runtime.

| AND service, μs | Mean | p50 | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|
| A′ + 4T | {lat(t,'AND_service_latency_us')} |
| CCZ | {lat(c,'AND_service_latency_us')} |
| Cultivation | null | null | null | null | null |

| Resource request → end of route, μs | Mean | p50 | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|
| A′ + 4T | {lat(t,'resource_request_to_ready_us')} |
| CCZ | {lat(c,'resource_request_to_ready_us')} |
| Cultivation | null | null | null | null | null |

It\'s distribution **for one determinist replay**, not experimental latency distributions and not p99 stochastic retries. Long request intervals including occupied corridors and waiting operands; They are not \"time of manufacture of one\". T». Producer uses expected cadence, And the rare burst stalls/retry tails Not yet.. sampled.

Relationship model-runtime A′/CCZ = **{runtime_ratio:.3f}**. It depends heavily on location, macro list policy, buffer policy and missing phase windows. Proclaiming it of the world CCZ Total requested benchmark You can\'t.

## 6. Where they\'re spent active qubit-seconds

Reserved Qseconds The above include all fixed area and simple area. In the following table, separate operation-volume ledger: Q×time Realized model operations on the sites in question on the ground of; holding data memory It\'s not possible. Idle resource buffers are separately considered busy operations. I don\'t fold this one. ledger c reserved Qseconds.

| Area | A′ + 4T, Qs | CCZ, Qs |
|---|---:|---:|
'''
labels=[('logical_ops','Normal Clifford operations and their routes'),('resource_delivery','External resource delivery paths'),('ccz_Clifford_fixup','CCZ Clifford fixups'),('factory_intrinsic','Internal factory production'),('protected_resource_idle_storage','Idle full-distance resource buffers'),('final_injection','Final injection operations'),('classical_wait','Feedback reservation'),('measured_inverse_fixup','Measured inverse fixups'),('output_growth_proxy','Growth allowance'),('low_distance_storage','Low-distance idle storage')]
for key,label in labels:
    md+=f"| {label} | {n(t['intrinsic_component_qubitseconds'].get(key,0))} | {n(c['intrinsic_component_qubitseconds'].get(key,0))} |\n"
md+=f'''| Amount operation-volume ledger | {n(active_t)} | {n(active_c)} |

In this CCZ replay **Normal Clifford operations/paths, external delivery and CCZ fixups greater intrinsic factory production**. This localizes the next dimension in this fixture: A logical network and protected routes, not just the production of a resource. This arrangement cannot be carried over to optimally packed chip or full workload No phase.

Share of factories in total FTQC-The program is now unknown. Previous «65%» was a share of another, a historical one kernel. No line here confirms that factories are actually occupied 65% modern end-to-end hardware volume.

## 7. Errors: What is assessed and not proven

Total program target retained **0,002**: synthesis / extra magic+delivery / other logical operations Under 0,002/3. Full maximum T-demand it\'s a problem. delivered-T allowance **2,6286356×10⁻⁹**. For carry-Sub-graph used relevant part of resource; not misspent phase budget again.

Supplementary sensitivity model: pL(d)=0,1×(100p)^((d+1)/2), p=0,001; ordinary d29 ♪ Gives me ♪ 10⁻¹⁶ per proxy cycle. For bridge used output dX=21. **At the source anisotropic patches (dX=21,dZ=9): one dX Doesn\'t describe everything faults.** Real bridge/gate error may be significantly different. Overlapping memory/operation allowances also do not constitute a severe breakup of the physical fault channel.

| Proxy-Amount | A′ + 4T | CCZ |
|---|---:|---:|
| Factory-output contribution | {t['error_components']['factory_output']:.3e} | {c['error_components']['factory_output']:.3e} |
| Growth allowance | {t['error_components']['output_growth_proxy']:.3e} | {c['error_components']['output_growth_proxy']:.3e} |
| Data memory | {t['error_components']['data_memory']:.3e} | {c['error_components']['data_memory']:.3e} |
| Routes / gates | {t['error_components']['route_and_gate']:.3e} | {c['error_components']['route_and_gate']:.3e} |
| Protected resource residence | {t['error_components']['protected_resource_buffer']:.3e} | {c['error_components']['protected_resource_buffer']:.3e} |
| Low-distance residence | {t['error_components']['low_distance_buffer']:.3e} | {c['error_components']['low_distance_buffer']:.3e} |
| Total sensitivity proxy | {t['error_union_proxy']:.3e} | {c['error_union_proxy']:.3e} |

**Passing a proxy Doesn\'t mean passing failure target.** State infidelity Not automatically gate diamond error; physical noise/decoder/growth fidelity Not measured. Fields measured LER and validated full-program contract remaining null/false. Number logical cycles to full error budget Cannot be certified from this table.

Because it\'s factory audit, decoder baselines It wasn\'t done here. To make sure that no measurement is made clear:

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

Published GSJ d5 quality estimate Near **2×10⁻⁹** applicable to specified cultivation construction/noise and relies on proxy/conjecture for full T-quality; see. [GSJ assumptions/errata](https://arxiv.org/html/2409.17595). My previous one.. public-code replay measured early-rejection **cost**, not rare T-gate errors. It\'s not a routine test 10⁻⁹ sampling-million shots.

Mandatory non-compliance interfaces:

1. Real-T d5 validation with account taken errata.
2. Grafted accepted output → total ordinary surface-code patch with verified fidelity.
3. Storage, routing and final T injection under general circuit noise and decoder.
4. Acceptance-decision timing Total 400 ns clock: 10 μs Meaning 25 ordinary cycles, Not 10.

Produced-state proxy leaves 2,6286356×10⁻⁹ − 2×10⁻⁹ = **6,286356×10⁻¹⁰ / T** as at extra delivery. It\'s a small reserve **Not yet measured as spent**. It cannot be said that cultivation Not going through target or that she wins: unknown delivery fields — `null`, Status `NOT_ADMITTED_TO_DELIVERED_GATE_COMPARISON`.

## 9. What outcome is already suitable for decision?

**CCZ resource substitution deserves full physical Comparison:** cheap clean AND not required to be paid for four separate T resources. It\'s famous. compilation/resource choice, Not a new idea... Settings CCZ factory under the same heading AND error allowance It was cheaper than four settings T Current source equations.

**The largest remaining area cannot be honestly declared as found for the entire system.** Limited replay This is protected Clifford/path/delivery work. For cultivation Question-still in bridge/storage/acceptance-to-consumption; It can\'t be ranked by delivered cost Without these interfaces. Not yet included in the core programme physical phase/tower schedules.

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
'''
(ROOT.parent/'docs/delivered_non_clifford_benchmark.md').write_text(md,encoding='utf8')
print('Wrote docs/delivered_non_clifford_benchmark.md')
