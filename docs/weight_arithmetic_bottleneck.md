# The 238,388 T coherent-weight arithmetic bottleneck

Audit date: 5 October 2026. This examines the existing compilation and known
representations; no new algorithm is proposed.

**Finding:** **238,388 T** is not a proved minimum for the TFIM phase circuit.
Calling all of it an artifact of a poor binary adder is also incorrect. The
**197 AND** needed for exact X population weight is optimal within the stated
XOR/AND model. The **397 AND** ZZ counter treats 400 dependent edge parities as
generic independent popcount inputs; its optimality is not established. The
phase-only operation does not require materializing a separate exact weight.

Counts below are implementation checks, explicitly derived formula estimates,
or bounds for stated models. Unknown costs are not zero. T, CCZ, depth, latency,
and ancilla demand are distinct resources. The selected historical line is
`hwp_global_joint_batch_in_circuit_tower_mixed_diagonal`; it was lowest-T among
the evaluated P options, not a global optimum. Later graph-aware and compiler
audits must be consulted before treating this count as the current baseline.


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## 1. Which one?? baseline He's on it.

Reference files: [non_clifford_structure.md](non_clifford_structure.md), [paper_counts_proxy.structure.json](../analysis/results/paper_counts_proxy.structure.json), [paper_counts_proxy.costs.json](../analysis/results/paper_counts_proxy.costs.json).

Line selected `hwp_global_joint_batch_in_circuit_tower_mixed_diagonal` — Minimum T-count **among previously calculated options P**, Not a proven world minimum:

| Composing | T Total batch |
|---|---:|
| Hamming-weight computation | **238 388**, fixed number |
| AND in phase catalyst towers | 6 432 |
| Synthesis seed rotations | 7 242.424448, Mathematical waiting |
| Training catalysts | 1 311.939166, Mathematical waiting |
| Total | **253 374.363614 expected**, maximum branches **253 617** |

238 388 does not include AND Inside phase towers. Current ledger Individual CCZ states not consumed: AND Four T.

The limitations of the previous study remain:

- **200 data logical qubits — two independent systems for the of 100 back.** It's not one connected 200-Back grate. Joint-The block combines equal phases of the two systems.
- P — **paper-count proxy**: two periodic bars of the 10×10, Under 200 edges; 20 Steps Suzuki Fourth order of the country. The periodic boundary is chosen to agree on the number of rotations, not to be restored from the original QIR.
- The numerical angles use the imputed completion `J=g=1`, `dt=0.25`. The original work does not capture all these parameters. This reservation [prior recovery](non_clifford_structure.md) still on.
- Total execution target — 0.002; Selected synthesis budget — 0.000666666667. Evaluation of the synthesis error of the selected line - about 0.000331837 in the previous full channel standard. Physical errors arithmetic, catalysts and routing Not certified; scientific error Suzuki also not automatically activated.
- The previous platform: surface code, Planck connectivity, physical error 10⁻³, cycle 400 ns. Here. **No new routed physical ledger**: one logical primitive is not equal to one such cycle or a certain degree of resistance.

## 2. Precise conversion: X-weight and ZZ-weight

Convention: `R_P(θ)=exp(−iθP/2)`. On the Bit Line `s` The same work Z-rotations have an effect

\[
\prod_{j=1}^{m}R_Z(\theta)|s\rangle
=e^{-im\theta/2}e^{i\theta w(s)}|s\rangle,
\qquad w(s)=\sum_j s_j.
\]

The general phase can be omitted for the uncontrolled circuit. For controlled time evolution She would have demanded separate accounting.

### X: Number of units X eigenbasis

For 200 back `s_j=0/1` The value of the individual X, respectively +1/−1. Therefore,

\[
U_X(\theta)=e^{-i\theta\sum_{j=1}^{200}X_j/2},
\qquad w_X(s)=\sum_{j=1}^{200}s_j.
\]

The current block does of the unit:

1. H at each of the 200 data qubits, translation X eigenbasis a computational base.
2. A precise countable `w_X` 8-day weekend, s 197 temporary work qubits.
3. Phase `exp(iθw_X)` by the weighted output phase and already calculated catalyst tower.
4. Recalculation of all interim data, returning data, etc scratch Zero.
5. H as at data qubits, returning the base.

The counting network itself can change data wires **between compute and uncompute**. Her description is correct —

\[
W_m:|s\rangle|0^{K+b}\rangle
\longmapsto |\widetilde s(s)\rangle|g(s)\rangle|w(s)\rangle,
\quad
W_m^\dagger D_\theta W_m:
|s\rangle|0\rangle\longmapsto e^{i\theta w(s)}|s\rangle|0\rangle.
\]

`g(s)` — interim data; `b=ceil(log₂(m+1))`. The first register does not need to remain unchanged internally and other features of the register. sandwich. It's the recovery that lasts that keeps the quantum full output contract.

### ZZ: Ribs cut

For Z-Line `z` and each rib `(u,v)` specified parity bit

\[
p_{uv}=z_u\oplus z_v,
\qquad
w_{ZZ}(z)=\sum_{(u,v)\in E_1\cup E_2}p_{uv}.
\]

`w_ZZ` — the number of edges whose endpoint spins differ, not the number of one-valued spins. At batch available 400 edges:

\[
U_{ZZ}(\theta)|z\rangle
=e^{-i400\theta/2}e^{i\theta w_{ZZ}(z)}|z\rangle.
\]

Existing implementation:

1. Select 400 Net parity carriers. For each rib, two of the two ribs CNOT Record `z_u XOR z_v` in carrier.
2. Count Normal Hamming weight these 400 carriers: 397 temporary work qubits and 9 output qubits.
3. Apply Weight Phase.
4. Implement inverse popcount; carriers again contains the original edge parities.
5. Reverse CNOT Clear carriers.

All vertices have a degree 4. Therefore, `w_ZZ` Always even: `sum_edges p_uv mod 2 = sum_vertices degree(v) z_v mod 2 = 0`. The first step in the selected line is already missing: **8 phases**, double base angle. But the math still stands out 9 output qubits And does **397 AND**. The pass of a permanent phase is not equivalent to a reduction in the counting network a certain degree of speed.

## 3. One transfer and full count

### What Makes an Existing 3-to-2 counter

B [Qualtran HammingWeightCompute](https://github.com/quantumlib/Qualtran/blob/main/qualtran/bloqs/arithmetic/hamming_weight.py) used 3-to-2 counter with one clean-target AND. My script is replicating its sequence, not proposing a new one:

```text
CNOT(a,b)
CNOT(a,c)
AND(b,c,t)       # t starts in 0
CNOT(a,b)
CNOT(a,t)
CNOT(b,c)
```

Independent review of the truth table gives

\[
(a,b,c,0)\mapsto(a,b,\ s=a\oplus b\oplus c,\ h=\operatorname{majority}(a,b,c)),
\qquad a+b+c=s+2h.
\]

The non-linearity is here alone:

\[
h=a\oplus[(a\oplus b)(a\oplus c)].
\]

AND target First store the work, then after CNOT — carry. Prin inverse CNOT First, they return the right ones controls and raw AND target, then the measurement shall be carried out uncompute. **You can't just measure accumulated weight or arbitrary carry and declare it safe purifying.**

For AND published [clean-target 4-T gadget and its measured inverse](https://github.com/quantumlib/Qualtran/blob/main/qualtran/bloqs/mcmt/and_bloq.py): compute uses 4 T; inverse — H, measurement, contingent CZ, reset, without T. This is isometry Net target, Not arbitrary three-beat Toffoli for 4 T without additional conditions.

### How many transfers in each binary column

In the current network inside the column, the three are connected in a sequence, then carries are moved to the next column. This is **It's already compression.. 3-to-2**, but with a long chain of sums inside the column. This is not 200/400 independent bulk into full binary battery.

\[
K(m)=\sum_{r\ge1}\lfloor m/2^r\rfloor=m-\operatorname{popcount}(m).
\]

| Weight column | Carry creations for X, m=200 | Carry creations for ZZ, m=400 |
|---|---:|---:|
| 1 → 2 | 100 | 200 |
| 2 → 4 | 50 | 100 |
| 4 → 8 | 25 | 50 |
| 8 → 16 | 12 | 25 |
| 16 → 32 | 6 | 12 |
| 32 → 64 | 3 | 6 |
| 64 → 128 | 1 | 3 |
| 128 → 256 | 0 | 1 |
| 256 → 512 | — | 0 |
| **Total** | **197** | **397** |

For X This is 192 full-adder-like counters and 5 half-adder-like counters Third entry 0. For ZZ — 391 and 6. In both cases, one counter Creates one AND And it costs four. T. Some work wires subsequently used as inputs to others counters; Not everyone always keeps the original value carry.

### Recalculation by Suzuki layers

After the association of neighbouring countries already completed X half-steps in 20 Suzuki steps remaining **101 X block and 100 ZZ blocks**. Count circuit does not depend on the value or the symbol of the angle.

| Family | Blocks | AND/carry creations | Carry uncomputations | T compute | T uncompute |
|---|---:|---:|---:|---:|---:|
| X_boundary | 2 | 394 | 394 | 1 576 | 0 |
| X_common | 59 | 11 623 | 11 623 | 46 492 | 0 |
| X_mixed | 40 | 7 880 | 7 880 | 31 520 | 0 |
| **All X** | **101** | **19 897** | **19 897** | **79 588** | **0** |
| ZZ_common | 80 | 31 760 | 31 760 | 127 040 | 0 |
| ZZ_central | 20 | 7 940 | 7 940 | 31 760 | 0 |
| **All ZZ** | **100** | **39 700** | **39 700** | **158 800** | **0** |
| **Batch** | **201** | **59 597** | **59 597** | **238 388** | **0** |

Okay.,

\[
T_{\rm carry}=4[101(200-3)+100(400-3)]=238\,388.
\]

This is **59 597 calculations AND plus 59 597 Repurification**, Not 119 194 T-paying Toffoli. Inverse requires 59 597 and before 59 597 Nominal CZ; zero price T does not mean zero time or classical connection.

### Ancillas, Clifford gates and depth

| Resource | One X block | One ZZ block |
|---|---:|---:|
| Nonlinear work targets | 197 | 397 |
| Output weight bits, selected | 8 | 9, of which LSB permanent |
| Additional edge-parity carriers | 0 | 400 |
| **Scratch without towers/routing/factories** | **205** | **806** |
| CNOT in counter macros, compute | 988 | 1 988 |
| The same CNOT in inverse | 988 | 1 988 |
| CNOT Inside 4-T ANDs | 1 182 | 2 382 |
| Measuring inverse AND | 197 | 397 |
| Outer basis/parity operations | 400 H | 1 600 CNOT, Both sides |
| Compute T-depth, dependency schedule | 107 | 208 |
| Compute primitive depth | 968 | 1 879 |
| Inverse primitive depth | 536 | 1 042 |

For all of it. batch outer operations — **40 400 H** for X and **160 000 CNOT** for ZZ. Formula macro CNOT count — `5K+popcount(m)` as at compute And the same amount as inverse; AND-internal CNOTs counted separately.

Carry-only T-depth c block barriers: `101×107 + 100×208 = 31 607`. Compute+inverse primitive depth: `101×1504 + 100×2921 = 444 004`, without outer operations and phase middle. For size 200/400 selected schedule assumes arbitrary logical connectivity And the single time of the primitives/feedback. Enclosure outer sizing bounds ♪ Gives me ♪ 445 806, but **It's not a time on a double-tube surface-code device**.

The full old line gives T-depth 43 620 and primitive sizing depth 521 278 with phases and startup. Peak additional logical qubits — **891 = 806 + 40 catalysts + 45 tower scratch**, I mean, 1 091 with 200 data qubits, Before routing, supply and factories. Ancillas Reuse between blocks: Cannot fold 201 peak allocations as simultaneous qubits.

## 4. What really is limited to math

### Important Known Lower Border

Boyar and Peralta proven accurate **multiplicative complexity** Hamming weight:

\[
c_\land(H_m)=m-\operatorname{popcount}(m).
\]

That's a minimum number AND for receipt **All binary bits of exact weight arbitrary: of the two bits m-Bit line** scheme above XOR, AND and constants. See. [Original technical report, Theorem 2](https://www.cs.yale.edu/publications/techreports/tr1260.pdf) and [publication NIST](https://www.nist.gov/publications/exact-multiplicative-complexity-hamming-weight-function).

**Investigation for current X-the contract issued here:** 197 AND — at least one fresh unrestricted X-popcount oracle in this model of the. Changing a line chain to a tree can reduce depth; simply switching XOR/AND calculation will not reduce the number AND below 197 under the same contract. It's not proof that everything X-Phase block requires 788 T, and not the lower limit of the total quantum. and/or. and/or circuit.

The differences are significant:

- Theorem counts Boolean AND, Not magic states, not T-depth and not qubit-seconds.
- It does not cover arbitrary quantum, etc Fourier/phase circuits, catalysts, Global compilation and near phase output.
- Bordering by 101 blocks are a selected architecture **fresh compute → phase → uncompute**. Theorem doesn't prove that any equivalent full-program circuit I have to re-compense all these oracles.

### Why? 397 for ZZ is not the same lower boundary

400 edge parities owned by cut space Count. Theirs GF(2) rank — **198**, Under 99 for each contact 100-Top system. XOR The ribs of any cycle shall be zero. Therefore, unrestricted 400-bit Hamming-weight lower bound Not applicable directly `w_ZZ(z)`.

You can get a weaker but honest border. Record everything white vertices Two two-deck bars in zero; let's leave 100 black vertices arbitrary. Then..

\[
w_{ZZ}(z)=4\operatorname{popcount}(z_{\rm black}).
\]

The shift of the weekend bits to two positions gives you exact 100-bit popcount. Consequently,, **Any XOR/AND circuit accurate cut weight requires minimum `100−popcount(100)=97` AND**. This is the application of a famous theorem to a subset of entrances, not a new algorithm.

For one ZZ The block is now known from this audit:

\[
97\ \le c_\land(w_{ZZ})\ \le397.
\]

The gap **is not the savings found**: effective implementation of the Convention on the ground of the 97 AND It's not known here.. Recalculation of four T as at AND I would. 38 800–158 800 T as at 100 fresh ZZ oracles **selected gadget-Model**. It's not a universal quantum T bound.

### How many different weights to distinguish

X-weight 201 possible significance, 0…200. A minimum is required to record all values in orthogonal states **8 output qubits**.

For joint ZZ-graph exact mass of weights:

\[
\{0,4,6,8,\ldots,396,400\},
\]

I mean, **199 values**; None 2 and 398, And all the odd ones. Verification and evidence:

1. Each border is even of the two sides. Non-zero cut one toroid grate contains a minimum of four ribs of the top. If there are both rows and columns, each direction contributes at least two; if there is only one direction, at least one direction. 20. Therefore, joint cut 2 Unable.
2. XOR c checkerboard changes each edge parity, translation `w` in `400−w`; Therefore, 398 Also impossible.
3. Choice of any number black vertices ♪ Gives me ♪ `0,4,…,400`. One neighbor black-white pair ♪ Gives me ♪ 6; Enclosure black vertices outside of four neighbours white vertex or Arbitrary black vertices Second bars of the second grate `6+4k`, `0≤k≤96`. Checkerboard complements Add 394. Together, all the remaining even weights. The script checks specific witnesses each value.

So, it's, **8 qubits — lower boundary orthogonal record and for ZZ**; 9 bit current number entry - known zero LSB, Not the necessary information. But a smaller number of values doesn't in itself prove the cheap calculation of their code...

**For phase-only I'm sorry, I'm sorry.. output-register borders are not mandatory at all.** Phase `exp(iθw)` may be applied without materialized weight. For ours generic The angles of different weight phases do not match exactly, but quantum circuit Does not have to write them into separate orthogonal labels. The requirement for precision of phases remains; AND lower bound accurate Boolean oracle Not automatically moved.

## 5. Comparison of known perceptions and implementations

Tables `m=200` for X, `m=400` for ZZ; `b=ceil(log₂(m+1))`; `K=m−popcount(m)`. The cost of the phase is taken into account in addition, unless clearly stated otherwise. For ZZ You also need to get edge parities or to comply phase gates directly on the ribs. Number marked **upper bound** — resources of a particular known simple design, not the best result of all compilers.

### 5.1 Summary table

| A known approach | Non-Clifford cost | Ancillas | Depth without routing | Locality | What happens? | In alternate X/ZZ |
|---|---|---|---|---|---|---|
| **Current column popcount** | K temporary AND, 4K T; inverse 0 T. X: 197/788; ZZ: 397/1588 | K+b; ZZ More. m parity carriers | Measured: T-depth 107/208, compute+inverse primitives 1504/2921 | Global linkages aggregation, Not here. routed | Binary exact weight, Then phase | Total count in each block |
| **Ripple-carry binary accumulator** | For m consecutives additions Lineline lead price O(mb); options cleanup Changed coefficient. Precise textbook bounds below | Compact accumulator O(b); Maintaining the whole story O(mb) | O(mb) ripple, Sometimes it's worse in literal multi-control version | Local chain counter, But each input I'm gonna meet her. | Binary exact weight | Does not eliminate update between blocks |
| **Recursive tree adders / carry-lookahead** | Exact XOR/AND tree can reach K AND; Does not have to reduce T concerning the current K. Lookahead usually adds work/operations For the depth | O(m) intermediate storage; detailed peak Depends on cleanup | Ripple Inside the tree of O(log²m); lookahead/carry-save O(log m) with sufficient workspace/connectivity | The tree's inter-unit; 2D routing separately | Exact binary partial/final weights | Helps the depth of the block, doesn't X/ZZ commuting |
| **Carry-save / redundant integer** | Q 3-to-2 counters → Q AND → 4Q T in the same gadget-Model; Q depends on the format to which the | O(m) active/history storage Typical | Compression O(log m); final carry propagation separately | Links between weighted columns; I need it. routing/fanout resources | Several weighted rows or final exact weight | Phase can be read from of the child redundant rows; After another base, they don't automatically retain meaning |
| **Unary / thermometer** | No "free conversion": accurate thermometer map X requires ≥K Boolean AND. Phase cost depends on reading labels | m thermometer bits or m+1 one-hot bits, plus conversion history | Depends. conversion network; The format does not set the depth itself | Usually global conversion; phase ports distributed | Exact weight in long label | Growth workspace and the need for compatible basis updates remaining |
| **Reversible sorting / popcount networks** | One each history flag as at comparator; specific bitonic upper bound below. Good popcount networks do not have to sort | O(m) y compressor networks; O(m log²m) flags simple sorting network | Bitonic O(log²m) comparator layers; compressor O(log m) | Longer pairs bitonic; NN sorting More expensive | Sorted thermometer either binary popcount | Does not eliminate recoherent processing |
| **Fourier/QFT addition** | No explicit Boolean carries, but O(mb+b²) controlled phase gates; arbitrary rotations I'm gonna pay you.., exact FT T-count not specified by this gate count | b output/counter bits for literal counter; fanout Adds workspace | Literal shared counter O(mb+b²); known parallel constructions Faster | Each input related to counter; QFT Also requires linkages | Exact weight in perfect arbitrary-rotation Models; Nearer FT synthesis | Demands compute/inverse each cluster; phase precision new load |
| **Direct phase accumulation / phase kickback / catalysis** | Direct: m rotations, **0 carry AND**. Kickback: price addition+gradient preparation. Towers: AND+catalysts+seed synthesis | Direct almost without arithmetic ancillas; gradient/catalysts They have their memories. | Direct Phases can go parallel; shared gradient/adders They're creating bottleneck | Direct X lockel; direct ZZ on ribs. Shared resources require delivery | Only the right one. phase; Weight may not be recorded | Direct The blocks are executed without and other features. weight cache; noncommutation retained |
| **Graph-specific cut representations** | Edge parities Clifford; exact cut-weight non-linean. Ours proven Boolean interval 97…397 AND; A perfect best graph circuit not established | Depends. edge carriers, aggregation selected by the graph encoding | No measured graph-specific optimum depth P | You can use a graphal structure, but toroidal wrap edges and joint aggregation I need to route | Cut weight or just phase | Cycle constraints retained; total cut changes at X evolution |

### 5.2 Ripple: baseline He's not paying for the full.. counter After each bit

Normal accumulator Imagining `A ← A + s_j` for each input bit. [Cuccaro et al.](https://arxiv.org/abs/quant-ph/0410184) Give low-ancilla ripple addition; [Gidney](https://arxiv.org/abs/1709.06648) uses temporary AND, 4n+O(1) T for addition and measured cleanup. So compare the current pattern to the historical cost ripple and you can't announce the winnings of a new idea.

**Leading assessment for existing and other relevant bodies or agencies. compact-addition A way, not accurate backend count:** Supplement source bit zero to zero b-bit addend, implement m in-place additions and then they inverses after phase. It's working. `8mb+O(m)` T If applicable 4b+O(1) addition gadget, O(b) scratch plus source/carry workspace, O(mb) serial depth. Lead members — 12 800 T as at X block and 28 800 as at ZZ block, much higher than the present 788/1588; endpoint constants not counted.

For reproducible **accurate upper bound Simple textbook of construction** can be used controlled increments: bit k counter Switch multi-controlled X from input bit and k lower counter bits; clean-ancilla ladder has `2k−1` normal Toffoli. Switches from the senior bat to the youngest. It's standard. [multi-control decomposition](https://arxiv.org/abs/quant-ph/9503016), not proposed new compilation.

| Literal compute → phase → inverse | X, m=200,b=8 | ZZ, m=400,b=9 |
|---|---:|---:|
| Toffoli forward: m(b−1)² | 9 800 | 25 600 |
| Forward + inverse Toffoli | 19 600 | 51 200 |
| 7-T unitary upper bound | 137 200 T | 358 400 T |
| Counter + reusable ladder workspace | 14 qubits | 16 qubits |

Here. inverse paid in full Toffoli: It's not known to be the strongest. ripple option. The table shows ancilla/depth trade-off, Not a worthy competition lowest-T HWP. You can save carry history and use zero-T inverse, But it's different.. memory trade-off; You can't take the minimum at the same time scratch compact accumulator free of charge inverse a saved history.

### 5.3 Trees and carry-save: depth benefits are not equal to non-linearity removal

Recursive exact-weight constructions, carry-save arithmetic and [carry-lookahead adders](https://arxiv.org/abs/quant-ph/0406142) — known ways to change depth/space trade-off. [Quantum Carry-Save Arithmetic](https://arxiv.org/abs/quant-ph/9808061) Postponement of distribution carry, using redundant weighted rows.

Transition tree/Wallace network Removes the Long ripple dependency **inside column**, but numbers 197/397 does not automatically become smaller. The current scheme already uses identity `a+b+c=s+2h`; Rename identity «carry-save representation» doesn't create new savings.

For redundant representation `w=Σ_j 2^j Σ_r y_(r,j)` The phase is actually spread into the phases of the individual phase weighted bits. You don't have to materialize the final one binary counter. But then they're paid. **all remaining weighted-bit phases**, Not just b binary output phases. Number compressors Q, Residual phases, catalysts, precision and inverse must be taken into account together. Value Q=0 allowed: reference input bits already uncompressed weighted representation. It's just a regular thing. direct rotations, Not free weight.

You can't declare it all 238 388 T cost one final carry-propagating adder: these T distributed throughout reduction network, from 100/200 counters in the youngest column.

### 5.4 Unary and sorting

Thermometer label `u_j=[w≥j]`, `j=1…m`, Keeps w single bits; one-hot label stores one active bit from m+1. They're different formats. Simple phase on thermometer — m Same rotations; phase on one-hot — m+1 different conditional phases. Cheap phase recording doesn't make cheap coherent conversion arbitrary input string.

For exact thermometer output each binary weight bit I'm getting it. XOR selected thermometer bits: `b_k = XOR_(r≥1) u_(r·2^k)`. Therefore, if thermometer received by scheme XOR/AND, known X-popcount lower bound **197 AND It still applies**. This is a border conclusion, not a new scheme. If you calculate label Through quantum phases, theorem Not applicable, but their cost should be treated separately.

Standard reversible sorting network preserves flag each exchange; erasing these flags No recovery input Breaks reversibility. This approach is described by y [Beals et al., reversible sorting](https://arxiv.org/html/1207.2307). For a simple binary comparator: flag calculated by Toffoli from `a AND NOT b`, Then Fredkin in compliance conditional swap. Fredkin = one Toffoli + two CNOT. Forward — two Toffoli, inverse — two. Full application 7-T unitary decomposition ♪ Gives me ♪ 28 T as at compare→phase→uncompare; phase as at sorted bits payable in addition.

**Calculation for non-optimized padded bitonic network:** to `p=2^ceil(log₂m)`, `l=log₂p`, number comparators `p·l(l+1)/4`, depth `l(l+1)/2` comparator layers.

| Resource | X, padded p=256 | ZZ, padded p=512 |
|---|---:|---:|
| Comparators forward | 4 608 | 11 520 |
| Comparator layers forward | 36 | 45 |
| History flags | 4 608 | 11 520 |
| Padding qubits | 56 | 112 |
| Forward+inverse Toffoli | 18 432 | 46 080 |
| 7-T upper bound as at sorting sandwich | 129 024 T | 322 560 T |
| Clean flag 4 T, inverse flag 0 T, Fredkin 7 T each side | 82 944 T | 207 360 T |
| C measurement-assisted 4-T Toffoli for Fredkin each side | 55 296 T | 138 240 T |

The last line uses the existing one [4-T measurement-assisted Toffoli Jones](https://arxiv.org/abs/1212.5069): `4 T flag + 4 T swap + 4 T reverse swap + 0 T flag inverse`. She demands helper ancillas, measurement and feedback: for a fully parallel comparator layer may be reserved until p/2 helpers Over history flags and padding. This is accounting upper limit of the standard network with other published gadgets, Not a new one launched sorting compilation. Even this stronger model doesn't compete here with 788/1588 carry T Unit.

Constant propagation and specialized comparators may further reduce these upper bounds; They're not done here. Depth 36/45 — **not** primitive/T-depth, a Number of levels comparators. Unary representation not inherently logarithmic-depth or inherently low-T: I need a specific one converter implementation.

### 5.5 QFT: Transport replaced by controlled phases

[Draper Fourier addition](https://arxiv.org/abs/quant-ph/0008033) It's moving integer addition in phase basis. For literal Hamming counter: Start with Fourier state zero b-bit counter, add each input bit Through b controlled phases, do inverse QFT. Compute uses `mb+b(b−1)/2` controlled phase gates:

| Controlled phases, compute only | X, b=8 | ZZ, b=9 |
|---|---:|---:|
| Total | 1 628 | 3 636 |
| CZ, exact Clifford | 200 | 400 |
| Controlled-S | 207 | 408 |
| Smaller-angle controlled phases | 1 221 | 2 828 |

For phase sandwich after diagonal phase required reverse counter circuit: These numbers are doubling. Controlled-S has a standard 3-T implementation. For the rest of you. `CP(φ)` Standard degradation - two CNOT and three `Rz(±φ/2)` with relevant accounting global phase. Theirs T-count — function FT synthesis precision; She's. **Not equal to zero just because AND gates None**. Price middle phase Also remains.

Perfect dyadic Fourier rotations Give exact binary weight; their nearest Clifford+T synthesis needs a new error allocation and verification of the complete compute→phase→inverse channel. You can't reschedule the old one synthesis budget Only for middle and count Fourier arithmetic accurate. There's no number winnings announced here QFT: FT-compiled by error target No line. [Ross–Selinger](https://arxiv.org/abs/1403.2975) provides specific deterministic rotation synthesis, Not free of charge arbitrary rotations.

Checked and fresh depth results: [Zi et al., August 2026](https://arxiv.org/html/2608.04627). They give all-to-all standard HWC c O(log m) depth/sublinear workspace, standard 2D with optimum Θ(√m) depth and O(log²m) ancillas, and constant-depth dynamic options with large and other options and and so on ancilla allocations and nonlocal classical feedforward. **Theirs elementary-gate model Allows arbitrary rotations; paper He's just leaving.. fault-tolerant T-count/T-depth Open.** They are therefore important known alternatives to depth but not already measured low-T replacement ours 197/397 AND.

[Rethinasamy–LaBorde–Wilde, Hamming-weight projections](https://arxiv.org/html/2404.07151) used controlled phases/QFT and coherence Inside fixed-weight subspaces. Final measurement weight register For ours phase sandwich unacceptable: it would destroy coherence between the balance. Coherent pre-measurement circuit can be considered as existing Fourier alternative, with account taken of him rotations, workspace, inverse and errors; published projection latency Can't be moved like FT latency ours circuit.

### 5.6 Direct phase, gradient and catalysts

**Existing counter-example of necessity carry:** apply reference single-spin X rotations and edge ZZ rotations Directly. None integer weight Not materialized; carry AND count equal to zero. Previously compiled deterministic P It's worth it **5 108 200 T**: 1 708 200 T as at X, 3 400 000 T as at ZZ. Logical ancillas No count, but magic-state supply/routing remaining. It's much more expensive than the present measured baseline, Although it is the article that is completely deleted integer carries.

Only proven by this means of the country: **Availability carry term Not necessarily**. Not proven: the same phase can be obtained cheaper 253 374 T or bypass precision cost.

Phase-gradient kickback Acting phase through controlled/modular addition in gradient state: He's moving accuracy to the preparation of the resource and arithmetic, not canceling it.. Catalyst/tower techniques Reuse prepared phase states, But they do.. nonlinear operations and seed rotations; [Sun–Koczor](https://arxiv.org/abs/2508.06236) taken into account space/time such continuous-rotation approaches. Ours counted tower already included in the original baseline: «Add catalysts» is not an unused economy.

Also checked out.. circuit optimization work [AlphaTensor-Quantum](https://arxiv.org/pdf/2402.14396): as at Hamming-weight/adder It restores the complexity of existing examples measured-uncompute constructions Concerning naive unitary circuits. It's not the source of another automatic double win.. **after** how measured uncompute already used.

### 5.7 Graph-specific cut weight: which applies to the specific P

There are three different tasks: to calculate Boolean edge parities, Identify **integer** sum, apply phase this sum. Parities change CNOT-based linear coordinates; integer cut size Doesn't become XOR-linear from that renaming.

Standard graph identity:

\[
w_{ZZ}(z)=\sum_v d_v z_v-2\sum_{(u,v)\in E}z_uz_v
=4\sum_v z_v-2\sum_{(u,v)\in E}z_uz_v.
\]

It shows the existing vertex/edge-phase submission of the same Ising/QUBO function. Direct application of the source rib phase has already been implemented without separate cut counter. For calculation exact integer sum needs to be taken into account on the ground carries or other non-liner operations; classical efficient cut evaluation not unitary quantum oracle free of charge.

Known graph-aware choices Includes edge coloring/matching groups, CNOT parity networks and HWP Same edge phases. [Official Ising/HWP example Quantinuum](https://docs.quantinuum.com/guppy/algorithms/examples/hamiltonian_simulation/trotter_hamming_weight_phasing.html) Shows disjoint brick-wall groups and in-place parity targets. This is open-chain commuting Ising example, **not** ours toroidal TFIM; Its results are not compared to the number P.

Previously calculated **P matching-HWP+towers+mixture** The whole program is worth it 296 355.97 expected T, maximum 298 532, additional qubits 350. It's more expensive. joint-global Under T, but uses less scratch. B separate-instance global version HWP arithmetic I should be.. **235 976 T**, less than joint **238 388**: joint aggregation savings phases/startup, Not by themselves. carry ANDs. That's a good option 264 705.9987 expected T; its previous depth bounds also less joint. So, it's, lowest-T point Doesn't guarantee the best runtime/qubit-seconds.

Toroidic cycle promises, even cut, degree 4 and bipartiteness They actually give you entry restrictions. But among the sources tested **no validated exact graph-specific cut-weight implementation for this P**, with clearly less complete T/CCZ price, same error contract and routed overhead. The absence of such a result in this audit does not prove that it does not exist. From lower bound 97 Cannot obtain a finished design on 97 AND.

Graphic abbreviations changing Hamiltonian, sparsification with another scientific error, MaxCut heuristics or native analogue Ising evolution on another physical platform, not moved here.

## 6. Why weights are counted and what is known reuse

Generic X evolution changes Z cut-weight superposition. ZZ evolution, In turn, it does. X-population superposition. For the top of the rib of the surface of the ribs `[X_j,Z_jZ_k]≠0`. So keep the old full weight register across the opposite layer and use it as a new exact weight It's not possible: it's going to be linked to the old base, not the meaning of the new one observable.

It's a limitation. **semantics stale cache**, Not proof that any possible circuit has to comply 101+100 full calculation. A compatible global, and so forth. to keep the world's energy compilation/representation might have a different structure; it is not developed here; it is not developed here..

There are some simple known exceptions that shouldn't be hidden.:

- Edge parities satisfactory cycle constraints in each Z-basis slice; cut parity permanent zero.
- Global `Π_j X_j` Each system switches with TFIM Hamiltonian. Consequently,, **X-population parity** retained, although complete X-population count not retained.
- Fixed known symmetry sector can change oracle promise. But the old one is full..-channel contract does not allow without verification to replace entry by one sector: e.g., Z-basis zero state is not known X-parity eigenstate.
- Neighbors are the same.-generator blocks I'm done. fused. You can't count that winning again.

For all submissions in section 5 possibility of performing each individual block retained. None unary label, None carry-save rows, None Fourier counter They don't make you do it on your own. X and ZZ commute. Joint aggregation two independent instances requires additional inter-relationship-instance logical interactions; It's a consequence of choice joint implementation, Not the property of the original product workload.

## 7. Where does every part of the price come from??.

| Reason | What is justified of the country | What part of the current 238 388 T to which the relevant provisions apply |
|---|---|---|
| **I need to distinguish the weight/phase** | Exact orthogonal weight record requires 8 bits for X and 8 for ZZ. Generic phases and specified accuracy require non-Clifford precision resources with gate set | Does not give a numerical lower T bound; I'll take it. storage bound Doesn't require carry network |
| **Non-linearity exact binary X weight** | 197 AND necessary/sufficient in XOR/AND on the Transport of Dangerous Goods fresh unrestricted input | Explains 19 897 X AND selected 101 fresh oracles; with 4-T conversion This is 79 588 T. Not universal phase/full-program bound |
| **Non-linearity exact graph cut** | Promise-specific restriction ♪ Gives me ♪ ≥97 AND; current unrestricted HW400 uses 397 | Price 158 800 T Upper; lower 397 You can't say for cut-space input |
| **Reverse and Delete garbage** | Scratch must be cleaned or kept compatible coherent encoding; measuring weight not allowed | **0 T as at carry inverse already achieved**; 59 597 measurements, feedback and lifetime paid for by other resources |
| **Binary carry propagation** | I need it in this one. exact integer network; influence dependency depth. XOR/AND lower bound X not tied to one particular ripple ordering | All 59 597 AND produce carries, But theirs count not equal to the price of one final carry chain. Tree changes depth, does not guarantee less count |
| **Locality** | On fixed 2D platform aggregation, wrapped edges, magic-state delivery Have spatial/communication cost | **None routing T in 238 388 not added.** Routing — uncalculated supplement; Clifford SWAP Doesn't consume T, But it increases time, mistakes, and space |
| **Re-evaluation basis changes** | H changes the base; opposite layers does not retain full weight | 40 400 H They're going to be 0 T in perfect Clifford Model. T repeated from-for fresh oracle strategy, Not from-For myself H |
| **Ours implementation choice** | General HW400 for dependent edge inputs; 400 parity carriers; linear column chains; separate banks; joint aggregation | These are real possible sources representation/depth/space overhead, But they're all freaking out. T Savings not yet measured |

Prin bounded-fanin unitary gates exact population-count output has a global dependency: minimum logarithmic-depth light cone to unrestricted connectivity. B strictly local 2D measurement-free model is the case square-root propagation barrier; dynamic circuits c nonlocal classical feedforward other conditions. These locality bounds are relevant **materialized aggregation**, not directly from local phases. They cannot be justified by a binding instrument global counter for phase task.

## 8. T, CCZ and physical cost: No change in units without notice

For the same carry network possible different resource accounting conventions:

| Implementation network | Carry non-Clifford demand as at batch | Limitation |
|---|---:|---|
| Current clean AND compute + measured inverse | **238 388 T**, 0 CCZ | 59 597 AND; inverse requires measurement/feedforward |
| Coherent adjoint each 4-T clean AND gadget | 476 776 T, How straightforward implementation | 8 T as at sandwich; Not the optimum of everything coherent Network |
| Normal 7-T Toffoli forward and inverse | 834 358 T, straightforward upper bound | 14 T as at counter sandwich; The historically weak option |
| CCZ/Toffoli-state injection compute + measured inverse | **59 597 CCZ**, plus injection Clifford/ancilla/feedback cost | Not 0 physical cost and not equivalent 59 597 T |

Measurement-assisted [Toffoli constructions Jones](https://arxiv.org/abs/1212.5069) and clean AND gadgets other factor relative to the total unitary Toffoli decomposition. Ours coefficient 4 He's already using this modern resource model. Price/fidelity factories CCZ and T Different; best factory You have to compare it to the same. total failure target. Simple replacement ledger label not software breakthrough.

Conditional toy conclusion: if required fresh exact XOR/AND weight oracles and pay for every one of them AND Data four-T gadget, borders **not less than 118 388 T** (`4[101×197+100×97]`), against current 238 388. This is **boundary within pre-limited architecture**, Not a promise to save 120 000 T and not lower bound for all TFIM phase circuit. No design reaching this border is received here.

## 9. Verification and reproducibility

New [weight_arithmetic_audit.py](../analysis/weight_arithmetic_audit.py) reading existing P artifacts, Selects lowest-T And it creates [weight_arithmetic_audit.json](../analysis/results/weight_arithmetic_audit.json). [hwp_schedule.py](../analysis/hwp_schedule.py) supplemented by exports of the same on the same date macro network; numerical schedule Not changed.

```powershell
.\analysis\.venv\Scripts\python.exe analysis/weight_arithmetic_audit.py
.\analysis\.venv\Scripts\python.exe analysis/verify_analysis.py
```

Checked:

- **9 820 basis cases**: all rows for dimensions 1…12; every attainable standard of living population count and 512 random strings for 200 and 400 inputs. In each case, correct binary weight, Acceptable AND targets to inverse and the reconstruction of all inputs/scratch.
- Independent amplitude Audit of published four-T AND: All four clean-control basis inputs and eight measuring lamps inverse branches. Maximum deviation around **1.67×10⁻¹⁶**. Linearity and the same branch factor Confirm retention superpositions this gadget.
- Specific graph-cut witnesses All **199** permissible joint cut weights.
- Amounts families, columns, X/ZZ and total 238 388; textbook comparator/increment/Fourier gate-count formulas.

These are tests ideal arithmetic and accounting, **not** 200-qubit noisy simulation, not full catalyst-tower gate verification and not physical routing benchmark. Unlike checking one phase identity, check macro network takes into account the change inputs Inside compute and their return.

## 10. Final question

**Which part of the remaining 238,388 T is unavoidable, and which is a
representation artifact?**

No unconditional numerical lower bound on the entire TFIM phase circuit is
established here. Known direct-phase circuits can avoid the carries, but the
previous evaluated option increased total demand to 5,108,200 T. Removing a
carry network is therefore not automatically a cost reduction.

Within the narrower class of fresh exact XOR/AND weight computations:

1. **X:** 197 AND per block is optimal. The current 79,588 T for X cannot all be
   blamed on choosing ripple rather than tree addition. The four-T conversion,
   repeated recomputation, and requirement to materialize weight depend on the
   selected architecture.
2. **ZZ:** 397 AND per block is a generic popcount upper bound, not a proved
   graph-input minimum. The checked lower bound is 97 AND. The current
   **158,800 T** ZZ allocation is the larger uncertain arithmetic component;
   this audit alone does not establish how much can be removed.
3. **Uncomputation:** the additional T charge is already zero. Measurement,
   feedback, ancilla lifetime, and depth remain; there is no second hidden
   238,388 T cleanup charge.
4. **Representation:** binary output, reduction order, 400 edge-parity wires,
   joint aggregation, and fresh recomputation are implementation choices.
   Known alternatives must be compared on full phase cost, not carry count alone.
5. **Circuit contract:** coherent phase, specified accuracy, alternating
   noncommuting layers, and fixed hardware compatibility must be preserved.
   None establishes this implementation's carry count as a universal lower bound.

The audit separates optimal Boolean X popcount, unproved graph-cut popcount,
and the weaker phase-only contract. Full T/CCZ demand, workspace, routed depth,
and error accounting are needed to quantify headroom. See the subsequent
[graph-cut audit](graph_cut_phase_synthesis.md) and
[adversarial compiler audit](adversarial_compiler_baselines.md) before using these
historical counts as the current baseline. No novelty is claimed.
