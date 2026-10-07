# Adversarial compiler baselines: graph-aware ZZ/HWP

Logical audit: 6 October 2026. Native Windows update: **7 October 2026**.

**Result:** the audited Qualtran phase-gradient implementation does not dominate
C4-cover HWP. B saves **9,900 AND**, or **39,600 adaptive 4T**, against an
already strengthened nongraph baseline A. However, the strongest full-program
compiler test remains **UNKNOWN**. Modern Feynman and FastTODD now run on
Windows, but both full Feynman `-ppf` attempts timed out. No system-level victory
has been established. Physical-model refinement remains paused.

## 1. Workload and precision contract

This is the existing **conditional P reconstruction**, not a recovered original
Beverland QIR program: two independent periodic 10-by-10 TFIM instances, 200 data
logical qubits, 400 combined ZZ edges, J=g=1, evolution time 5, timestep 0.25,
and 20 fourth-order Suzuki steps. Merging adjacent equal layers gives **101 X
and 100 ZZ blocks**. No symmetry sector is assumed. The intended operation
preserves the complete quantum output channel, including entangled inputs.

With `R_P(alpha)=exp(-i*alpha*P/2)`, a ZZ layer is, up to global phase,
`exp(i*alpha*cut(z))`. Qualtran requires `exponent=alpha/pi`; passing radians as
its exponent would implement a different operation.

| Family | Angle, radians | Blocks |
|---|---:|---:|
| X_boundary | 0.10362269294859393 | 2 |
| X_common | 0.20724538589718786 | 59 |
| X_mixed | -0.060868078845781784 | 40 |
| ZZ_common | -0.20724538589718786 | 80 |
| ZZ_central | 0.3289815435887514 | 20 |

Provenance: `analysis/results/paper_counts_proxy.structure.json` and `.costs.json`;
reconstruction limitations are in [non_clifford_structure.md](non_clifford_structure.md).
The total execution failure target remains **0.002**, with **0.002/3** allocated
to rotation approximation. This execution budget does not certify the separate
Suzuki/Trotter algorithmic approximation.

All arbitrary rotations use the same Ross-Selinger-based synthesizer, positive
mixture contract, and local full-diamond tolerance:

```
delta = (0.002/3)/1708 = 3.9032006245121e-7
```

Phase-gradient coefficient rounding must fit within the same aggregate budget.
The methods need not have identical actual errors: each must meet the contract.

The mixture's error bound applies to the **averaged quantum channel**. The fixed
compiler branches use seed `20261006`, including synthesis-branch selection and
Clifford twirling. An individual selected branch does not inherit that averaged
bound. Optimizers must preserve its fixed operation; a branch certificate does
not certify the entire randomized protocol.

Historical hardware assumptions remain unchanged: p=1e-3, a 2D nearest-neighbour
superconducting surface-code-like platform, conditional d=29 and 400 ns cycle.
This audit does not turn those assumptions into new physical estimates.

## 2. Implementations and the stronger baseline

**Qualtran HWP:** the official pinned installed API, **Qualtran 0.7.0 / Cirq 1.7.0**,
its call graphs, and its three-to-two Hamming-weight network were inspected.
The logical emitter follows that network; it is not a successful direct Cirq
export of the complete composite bloq. Stock HWC uses `n-popcount(n)` clean AND:
**197 for X and 397 for ZZ**, plus 400 edge-parity ancillas for ZZ.
[HWP documentation](https://qualtran.readthedocs.io/en/latest/bloqs/rotations/hamming_weight_phasing.html),
[HWC implementation](https://github.com/quantumlib/Qualtran/blob/main/qualtran/bloqs/arithmetic/hamming_weight.py).
Installed wheel files were inspected and hashed; `main/latest` URLs are explanatory
references, not reproducibility pins.

**A, `even_tower`:** an even-aware balanced partial ZZ counter uses **396 AND**
and eight nonzero weighted phases, rather than stock HWP's nine. It uses the
same existing binary-angle catalysis tower as B. A is deliberately stronger
than literal stock Qualtran.

**B, `graph_tower`:** the same X counter and catalysis tower, with C4-cover ZZ
arithmetic requiring **297 AND** per ZZ block. A direct-phase graph row is also
retained to separate graph arithmetic from known catalysis. Both counters
implement the integer phase exactly; GF(2) rank is not substituted for weight.

**Qualtran phase-gradient:** the audited path is
`HammingWeightPhasingViaPhaseGradient`, `phase_oracle`, QVR, and the actual signed
shifted additions in `AddScaledValIntoPhaseReg`. The official `AddIntoPhaseGrad`
call graph charges `phase_bitsize-2` Toffoli for an uncontrolled addition.
These are implementation counts, not lower bounds for all phase-gradient circuits.
[Phase-gradient implementation](https://github.com/quantumlib/Qualtran/blob/main/qualtran/bloqs/rotations/phase_gradient.py).

## 3. Logical resources

Clean AND uses a 4T temporary-AND computation with T-free measured cleanup.
CCZ is an alternative resource accounting, not an additional charge for the
same operation. `sampled` refers to the fixed branch; `expected` to the mixture.

| Method | Arbitrary synthesis calls | Clean AND | Additional Toffoli | Synthesis T: sampled / expected | Adaptive total T: sampled / expected | Workspace ancillas |
|---|---:|---:|---:|---:|---:|---:|
| Stock Qualtran HWP | 1,708 | 59,597 | 0 | 69,246 / 69,191.222 | 307,634 / 307,579.222 | 806 |
| Stock HWC, zero ZZ phase removed | 1,608 | 59,597 | 0 | 65,202 / 65,165.959 | 303,590 / 303,553.959 | 806 |
| Graph, direct weighted phases | 1,608 | 49,597 | 0 | 65,202 / 65,165.959 | 263,590 / 263,553.959 | 597 |
| A: even-aware counter + tower | 241 | 61,105 | 0 | 9,698 / 9,726.161 | 254,118 / 254,146.161 | 882 |
| B: C4-cover counter + tower | 241 | 51,205 | 0 | 9,698 / 9,726.161 | 214,518 / 214,546.161 | 682 |
| Qualtran phase-gradient, tested 23-bit setting | 20 + 1 exact T-dagger | 59,597 | 53,172 | 843 / 829.074 | Not a 4T-AND-only calculation | 829 + UNKNOWN adder scratch |

The phase-gradient additions require general Toffoli, not proven clean temporary
AND. Charging their standalone exact 7T implementation gives **611,435 sampled T**;
this is a resource conversion, not a completed circuit export. Even an optimistic,
unimplemented 4T charge for each extra Toffoli gives **451,919 T**.

| Alternative CCZ accounting | CCZ demand | Additional sampled synthesis T |
|---|---:|---:|
| A + tower | 61,105 | 9,698 |
| B + tower | 51,205 | 9,698 |
| Qualtran phase-gradient, 23 bits | 112,769 | 843 |

Relative to B, phase-gradient saves **8,855 synthesis T** and adds **61,564 CCZ**.
It is a trade-off, not Pareto dominance. A physical CCZ-to-T price was not
re-estimated here.

Tower startup costs are included: **201 seeds + 40 catalyst preparations = 241
synthesis calls**. Its 1,608 weighted-phase uses add 1,608 AND, already included
above. Five banks reserve 17 slots each: all 85 slots are charged, including
40 catalyst qubits. Workspace counts exclude factories, delivery buffers,
and surface-code routing corridors. Lifetime improvements must be applied to
all methods on the same terms.

The stronger A-to-B saving is **(396-297)*100 = 9,900 AND = 39,600 adaptive T**.
Stock-to-graph direct saves 100 AND per ZZ block because A already removes one
of stock HWP's unnecessary operations. Earlier A estimates near 252,974 T used
looser separate seed/catalyst tolerances and are not mixed into this comparison.

### Depth and feedback

| Method | Serial-block ASAP depth | T depth | Cleanup measurements / conditional CZ | Macro CNOT |
|---|---:|---:|---:|---:|
| Stock HWP | 466,448 | 40,027 | 59,597 | 757,176 |
| Stock, zero phase removed | 466,462 | 40,020 | 59,597 | 757,176 |
| Graph direct | 218,562 | 22,120 | 49,597 | 552,576 |
| A + tower | 223,130 | 21,731 | 61,105 | 761,624 |
| B + tower | 224,930 | 22,231 | 51,205 | 562,224 |
| Qualtran phase-gradient | UNKNOWN | UNKNOWN | 59,597 HWC cleanups; other details UNKNOWN | UNKNOWN |

These are unrouted unit-cost logical schedules, not QEC cycles or optimal depths.
Each block finishes before the next. Cleanup includes H, measurement, conditional
CZ, and reset; dependencies are included but physical feedback latency is not.
Macro CNOT excludes CNOT inside 4T gadgets. Additional T/CCZ injection measurements
are not counted here. **B loses to A by 1,800 depth and 500 T-depth units.**

## 4. Phase-gradient precision and export limitations

The initial conservative setting used 25 gradient bits, 2,713 additions, and
62,399 Toffoli. The subsequent sweep used
`eps_factor=1,2,3,4,5,6,8,12,16`. Each family was checked on **all X weights
0 through 200 and all even ZZ weights 0 through 400**, conservatively including
potentially unreachable weights. Actual shifted additions were checked against
scaled multiplication modulo `2^b`.

After removing global phase, the small-spread diagonal-channel diamond distance
is `2*sin((max(phi)-min(phi))/2)`. Block bounds are composed. Rounding checks use
double precision, rather than certified interval arithmetic; synthesis records
use high precision. The passing setting's margin exceeds floating-point roundoff.

| Gradient bits | Toffoli | Full-workload rounding diamond bound | Passes with preparation? |
|---|---:|---:|---|
| 25 | 62,399 | 0.0001412351 | yes |
| 24 | 57,442 | 0.000300026 | yes |
| 23 | 53,172 | 0.0006303412 | yes |
| 22 | 47,800 | 0.0013446619 | no |
| 21 | 44,289 | 0.0025418251 | no |

The tested 23-bit option uses **2,532 additions**, 20 preparation rotations, and
one exact T-dagger. Preparation bound **0.00000379035** gives total bound
**0.00063413159 < 0.00066666667**. B's corresponding bound is **0.00005259026**.
Both pass, although B is more accurate. The gradient is prepared once and reused;
its preparation error is not independently recharged for every use. Physical
corruption and propagation through reusable resources were not simulated.

**Gate export remains incomplete:** the installed Qualtran `AddIntoPhaseGrad`
has a resource call graph and classical semantics but no complete gate
implementation. `cirq.decompose` returned
`ValueError: Undecomposed leaf AddIntoPhaseGrad(...)`. Depth, scratch, and the full
measurement/feedback schedule remain unknown. Twenty-three bits is the best
**tested** API setting, not a proved globally optimal phase-gradient realization.

## 5. Fixed Clifford+T inputs

Arbitrary rotations were replaced by the actual fixed synthesized strings under
the common contract. Measured cleanup was replaced by the adjoint of the same
4T unitary gadget, giving **8T per compute/inverse pair**. Standard unitary
optimizers cannot consume adaptive measurement/reset as ordinary unitary gates.

The export preserves the ideal clean-input isometry. With sampled synthesis it
is not automatically the same averaged channel as the measured protocol; the
mixture contract remains a separate requirement.

| Fixed full branch | Wires including workspace | Input T | ASAP depth |
|---|---:|---:|---:|
| Stock HWP | 1,006 | 546,022 | 593,493 |
| A + tower | 1,082 | 498,538 | 278,548 |
| B + tower | 882 | 419,338 | 283,348 |

Clean workspace is reused across X/ZZ blocks; data wires are unchanged. Exports,
seed records, and hashes are retained. The unitary A-minus-B difference is
**79,200 T**, not an adaptive saving of that size.

Historical full PyZX attempts used the earlier slot labels: A had 1,082 wires,
B had 890 rather than 882, with unchanged T demand. Those are separate retained
inputs. Native Feynman uses the compact 1,082/882-wire exports.

## 6. Generic optimization results

[PyZX](https://github.com/zxcalc/pyzx) **0.10.7** was used for basic optimization,
`full_optimize` including phase-polynomial TODD, and phase teleportation followed
by basic optimization. [API documentation](https://pyzx.readthedocs.io/en/latest/api.html).

| Attempt | Coverage | Outcome |
|---|---|---|
| Basic optimization | 3 methods, 5 representative angle families | all 15 completed; T unchanged |
| TODD / teleportation on ZZ_common | 3 methods, 2 passes; 180 s | all 6 TIMEOUT |
| Full 201-block program | A/B, 3 passes; 180 s | all 6 TIMEOUT |
| Tiny C4 controls | generic/compact, 3 passes | all 6 completed; exact ZX certificates |

Representative ZZ_common input/output T: **A 3,271 to 3,271; B 2,479 to 2,479**.
Other resources changed:

| Branch | Depth before / after | T depth before / after | CNOT before / after |
|---|---:|---:|---:|
| A | 678 / 645 | 91 / 128 | 10,420 / 10,927 |
| B | 726 / 565 | 101 / 119 | 7,238 / 7,867 |

These representative results are not multiplied into a full-program claim.
Large basic outputs have hashes, but their independent equivalence certificate
is `NOT_RUN`. Unchanged T count is not a correctness certificate. Tiny C4
controls use different synthesis strings, 93 and 90 input T; neither was
reduced by the three passes. They do not settle the large-workload comparison.

### Modern Feynman and FastTODD: 7 October update

| Official source | Pinned commit | Native status |
|---|---|---|
| [Feynman](https://github.com/meamy/feynman) | `d2c382a2ab43a40a87f12f4255645bbb55f704f8` | built; modern `-ppf` runs |
| [FastTODD](https://github.com/VivienVandaele/quantum-circuit-optimization) | `231e6fe9f92d5bb1ebf7459c2a9233f5e74d148e` | built; official CLI runs |

The earlier missing-toolchain limitation has been resolved natively on Windows.
No Linux installation is needed. Details, dependency pinning, hashes, and smoke
checks are in [native_windows_setup.md](native_windows_setup.md).

A tiny 4T control becomes 0T under both tools; Feynman verifies both results.
The matched **full-program `-ppf` attempts each timed out at 240 seconds**, under
`+RTS -M3G -RTS`: A elapsed 240.464 s, B 240.166 s. No optimized circuit or
optimized T count was obtained. Shared load and timeout are not a compiler-speed
comparison. Downstream full-program FastTODD was **NOT_RUN** because no full
PPF output existed.

Matched representative `ZZ_common` blocks were also attempted with modern PPF
under the same heap cap and a 90-second limit: both **TIMEOUT**, with no output
circuit. These are recorded separately and do not replace the full-program
test. No block result was extrapolated across the workload.

A separate internal-H control exposes a necessary contract check: raw official
FastTODD gadget output implements the intended operation **after projection**
of an added ancilla, with factor `1/sqrt(2)`, rather than as a clean-ancilla
unitary. Measurements/corrections must be accounted for before claiming a
matched deterministic implementation. This is a diagnostic of the exported
representation, not evidence that the FastTODD method is incorrect.

Evidence: `analysis/native/benchmark/*__ppf.json`,
`input_manifest.json`, `internal_h_contract.json`, and native logs.
The 2019 Feynman Windows fallback lacked modern `-ppf` and previously failed
with `WinError 623 / IllegalSystemDLLRelocation`; it is not used as a substitute
for the modern tool.

## 7. Lattice-surgery compiler checks

**[TopoLS](https://github.com/tqec/TopoLS)**, commit
`78aab0ef1326bdf2041b519708f28741162f45c4`, required PyZX 0.10.6. Matched complete
ZZ_common A/B blocks were attempted before and after basic optimization.
Parameters: block size 20, zx/dir optimization 1, spread 0, seeds (17,1),
MCTS 10 iterations, time_bound 0.02, move 6, length 32, backtrack 0.
All four attempts timed out at 240 s before `prepare_graph` returned. No circuit
volume was produced. Even a completed result in this mode would be a free-T
unitary-block topological proxy, not a cultivation-aware adaptive system ledger.
[TopoLS paper](https://arxiv.org/abs/2601.23109).

**[DASCOT/WISQ](https://github.com/qqq-wisc/wisq)**, commit
`97c12a5e22cf16e37288c60a0a5735c58c6fe8ca`: direct routing API was inspected
separately from the Java optimizer. Historical import was blocked by Windows
Application Control, and the unmodified router uses `SIGALRM/alarm`, absent from
Windows Python. Those attempts provided no matched result. WISQ was not rerun
in the native Feynman/FastTODD setup update. No replacement router was invented.
[DASCOT paper](https://qqq-wisc.github.io/files/oopsla25.pdf).

**[FlowRouter](https://arxiv.org/html/2609.23756v1), literature-only:** the audited
20 September 2026 preprint combines maximum-flow Clifford-layer routing with
runtime cultivation on free patches, including postselection and classical
correction waits. Official runnable code was not located during the recorded
search; this does not prove no code exists. No FlowRouter result was produced
on this workload. Headline results on another distance/layout are not transferred
to d=29 or this CCZ-heavy adaptive demand trace.

## 8. Correctness evidence and limits

Recorded checks include 602 HWC weight/cleanup tests for n=200/400; 503 mapped
graph tests including constant and checkerboard inputs; local C4 identities and
compositional proof in [graph_cut_phase_synthesis.md](graph_cut_phase_synthesis.md);
eight basis cases for unitary gadget/inverse with maximum residual 2.78e-16;
phase-gradient shifted-addition/weight checks for every family and tested
precision; six exact small ZX certificates; and resource/hash assertions for
all 15 completed basic input/output pairs.

These validate source arithmetic and accounting. They do not certify large
optimized outputs, physical fault tolerance, or the total execution target.
Scripts and historical results are in
[analysis/adversarial_compiler/](../analysis/adversarial_compiler/README.md).
Key artifacts include `logical_resources.json`, `qualtran_resources.json`,
`qualtran_frontier.json`, `gradient_preparation_frontier.json`,
`export_resources.json`, `audit_summary.json`, and `artifact_manifest.json`.
Historical summaries remain historical; native results are stored separately.
Empty failed output files are not interpreted as zero-T circuits.

## 9. Answers and stopping rule

**A. Does phase-gradient HWP beat graph-aware HWP outright?** Not in the audited
pinned implementation: it saves synthesis T but uses substantially more
AND/Toffoli/CCZ arithmetic. Twenty-three bits is the best tested passing setting.
This is not a universal optimality proof against all phase-gradient circuits.

**B. Does a strong Clifford+T optimizer remove the advantage? UNKNOWN.** Basic
passes did not reduce T. Strong large PyZX attempts and both modern full PPF
attempts timed out. Native installation and tiny smoke tests do not answer B.
The full PPF-plus-FastTODD pipeline has no certified output.

**C. Does a modern lattice-surgery compiler preserve a system-level advantage?
UNKNOWN.** No matched complete output accounts for adaptive feedback, cultivation,
and delivered T/CCZ cost.

No existing method has demonstrated dominance under the complete matched
contract. That is not evidence of my victory. Physical validation stays paused.
The remaining required evidence is a completed and verified strong full-branch
optimization, a complete phase-gradient gate export with scratch/depth/feedback
accounting, and a matched surgery result. Randomized compilation must also
preserve the averaged-channel contract. The justified claim remains a reduction
in the specified logical AND demand, not novelty or a breakthrough.
