# Graph-cut phase synthesis: exact identities and resource scaling

Date: 6 October 2026. Publication edition: 7 October 2026.

## Results

The C4 cut value has an exact two-AND binary representation. The required phase has a more compact one-AND representation with two generic-angle rotations. A square-grid C4 cover reduces the tested periodic 10-by-10 arithmetic from 196 to 147 AND while retaining seven rotations. Both grid constructions have linear edge-count scaling.

The comparison includes an even-parity-aware partial counter, rather than only a generic full binary popcount. Every computational-basis input is preserved. The construction assumes neither a symmetry sector nor postselection.

## Exact C4 integer representation

For bits A, B, C, D:

\[
\operatorname{cut}=(A\oplus B)+(B\oplus C)+(C\oplus D)+(D\oplus A).
\]

Here `+` denotes integer addition. Define

\[
p=A\oplus C,\quad q=B\oplus D,\quad r=A\oplus B,\quad g=pq,
\]
\[
\ell=p\oplus q\oplus g,\qquad h=r(1\oplus\ell).
\]

Then `cut / 2 = ell + 2*h`. If either opposite pair differs, the cut has two edges. Otherwise, the cut is zero or four according to `r`.

| ABCD | cut | Low bit ell | High bit h | Phase bit r | Phase bit s |
|---|---:|---:|---:|---:|---:|
| 0000 | 0 | 0 | 0 | 0 | 0 |
| 0001 | 2 | 1 | 0 | 0 | 1 |
| 0010 | 2 | 1 | 0 | 0 | 1 |
| 0011 | 2 | 1 | 0 | 0 | 1 |
| 0100 | 2 | 1 | 0 | 1 | 0 |
| 0101 | 4 | 0 | 1 | 1 | 1 |
| 0110 | 2 | 1 | 0 | 1 | 0 |
| 0111 | 2 | 1 | 0 | 1 | 0 |
| 1000 | 2 | 1 | 0 | 1 | 0 |
| 1001 | 2 | 1 | 0 | 1 | 0 |
| 1010 | 4 | 0 | 1 | 1 | 1 |
| 1011 | 2 | 1 | 0 | 1 | 0 |
| 1100 | 2 | 1 | 0 | 0 | 1 |
| 1101 | 2 | 1 | 0 | 0 | 1 |
| 1110 | 2 | 1 | 0 | 0 | 1 |
| 1111 | 0 | 0 | 0 | 0 | 0 |


The high binary bit has algebraic normal form

\[
h=AC\oplus BD\oplus ABC\oplus ABD\oplus ACD\oplus BCD.
\]

Its degree is three. One AND of affine input functions has degree at most two, and subsequent XOR/NOT gates do not increase the degree. Two AND gates are therefore necessary and sufficient for these binary output bits in the declared XOR/AND model.

The exhaustive search enumerates all 32 affine functions and 35 nonlinear first-AND cosets. It finds no one-AND binary solution and 96 two-AND witnesses. This is a restricted Boolean-circuit minimum, rather than a minimum over arbitrary quantum gates, resource states, or measurements.

## Exact phase-only representation

Define

\[
s=C\oplus D\oplus[(A\oplus C)(B\oplus D)].
\]

The identity

\[
\boxed{\operatorname{cut}=2(r+s)}
\]

holds for all sixteen inputs. Applying `P(2*theta)` to each predicate implements the required `exp(i*theta*cut)` for generic real theta. No angle specialization is used.

With zero AND gates, predicates are affine. The cut has four distinct nonconstant edge characters in its real Fourier expansion; a parity phase supplies one such character. A zero-AND parity-phase implementation therefore uses at least four generic theta-dependent rotations. Direct edge phases achieve that count. The one-AND construction reduces it to two rotations, while the strengthened even-aware partial counter also matches this C4 resource vector.

## Reversible implementation

The compact phase circuit uses one clean ancilla g and an in-place linear basis change:

1. Apply `CNOT B -> D`, `CNOT A -> C`, and `CNOT A -> B`. The data wires now hold `[A, r, p, q]`.
2. Compute `g = p AND q` into the clean ancilla.
3. Apply `CNOT B -> g`, `CNOT C -> g`, and `CNOT D -> g`, producing `s = g XOR r XOR p XOR q`.
4. Apply `P(2*theta)` on B and g.
5. Reverse the three CNOTs into g, restoring its AND value.
6. Measure g in the X basis, apply `CZ(p,q)` conditioned on outcome one, and reset g.
7. Reverse the initial three CNOTs, restoring the original data basis.

This uses one temporary AND, twelve explicit CNOTs outside its gadget, one clean ancilla, two arbitrary rotations, and one measurement/conditional-CZ cleanup. The temporary-AND computation costs 4T; its measured cleanup costs no additional T. A CCZ-state implementation is an alternative resource accounting. Arbitrary rotations are accounted for separately.

The binary circuit adds a clean h ancilla, computes the second AND, phases ell and h at the appropriate weights, and reverses the two computations. Explicit gate lists and depth calculations for both circuits are retained in the circuit archive.

## Scaling comparison

The following table uses the recorded even-aware balanced partial counter and the corresponding graph construction. C4 uses its compact circuit; longer cycles use the fan plus partial aggregation; grids use edge-disjoint C4 faces and partial aggregation. These are implementation comparisons at equal generic-phase requirements.

| Graph | Baseline AND | Graph AND / CCZ | Rotations baseline / graph | Ancillas baseline / graph | Cleanup measurements baseline / graph | Abstract expanded depth baseline / graph |
|---|---:|---:|---:|---:|---:|---:|
| C4 | 1 | 1 | 2 / 2 | 6 / 1 | 1 / 1 | 24 / 22 |
| C6 | 3 | 3 | 2 / 2 | 10 / 8 | 3 / 3 | 53 / 58 |
| C8 | 4 | 4 | 3 / 3 | 13 / 11 | 4 / 4 | 65 / 62 |
| C10 | 6 | 6 | 3 / 3 | 17 / 15 | 6 / 6 | 77 / 98 |
| open_2x2 | 1 | 1 | 2 / 2 | 6 / 4 | 1 / 1 | 24 / 21 |
| open_2x3 | 4 | 3 | 3 / 3 | 11 / 9 | 4 / 3 | 59 / 61 |
| open_3x3 | 10 | 8 | 4 / 4 | 22 / 18 | 10 / 8 | 93 / 94 |
| open_3x4 | 12 | 9 | 5 / 5 | 29 / 23 | 12 / 9 | 104 / 119 |
| open_4x4 | 22 | 17 | 5 / 5 | 46 / 36 | 22 / 17 | 135 / 144 |
| torus_4x4 | 26 | 19 | 5 / 5 | 59 / 43 | 26 / 19 | 129 / 139 |
| torus_6x6 | 67 | 50 | 6 / 6 | 140 / 104 | 67 / 50 | 194 / 210 |
| torus_8x8 | 120 | 89 | 7 / 7 | 249 / 185 | 120 / 89 | 285 / 299 |
| torus_10x10 | 196 | 147 | 7 / 7 | 397 / 297 | 196 / 147 | 346 / 379 |
| two_torus_10x10 | 396 | 297 | 8 / 8 | 797 / 597 | 396 / 297 | 430 / 448 |


Each listed graph AND can alternatively be charged as one CCZ resource. Its adaptive 4T charge is four times the AND count; measured cleanup adds no T. Replacing cleanup with the recorded unitary inverse adds its separate cost. The table excludes arbitrary-angle synthesis and magic-state injection workspace.

C6, C8, and C10 do not improve on the strengthened counter at equal rotation counts. Direct fan phases can reduce arithmetic further at the price of more rotations. On an even square torus, checkerboard faces partition the edges into C4 blocks. Each block replaces four edge bits by two predicates of weight two with one local AND; the aggregation network then processes fewer inputs. Both final costs remain Theta(E), with a constant-factor saving for the covered grid family.

For two independent 10-by-10 tori, the partial counters use 396 and 297 AND respectively. Repeating the matched ZZ block 100 times saves 9,900 AND. Under common adaptive 4T accounting, that is 39,600 T. The complete workload audit includes X arithmetic, catalysts, startup, rotation synthesis, workspace, and depth separately.

## Verification and evidence

The scripts use Python 3.10 or newer and its standard library:

```bash
python analysis/graph_cut_phase/toy_c4.py
python analysis/graph_cut_phase/verify_quantum.py
python analysis/graph_cut_phase/scaling.py
python analysis/graph_cut_phase/report.py
python analysis/graph_cut_phase/verify_artifacts.py
```

The C4 formulas are checked on all sixteen assignments. Cycles and grid cases with at most sixteen vertices receive exhaustive basis checks. Larger cases use the exact local identity, edge partition, and arithmetic proof with sampled implementation checks. Stored-circuit verification independently recomputes resource counts and depths.

The independent quantum verifier checks **288** basis/angle/measurement-branch cases, with maximum statevector error `2e-16`. Its CCZ injection check covers **64** basis/branch cases with zero phase error.


Primary artifacts:

- [C4 search and truth table](../analysis/graph_cut_phase/c4_results.json).
- [Explicit reversible circuit implementation](../analysis/graph_cut_phase/circuits.py).
- [Scaling resource ledger](../analysis/graph_cut_phase/scaling_results.json).
- [Stored circuit archive](../analysis/graph_cut_phase/circuits.json.gz).
- [Quantum verification](../analysis/graph_cut_phase/quantum_verification.json).
- [Independent artifact verification](../analysis/graph_cut_phase/artifact_verification.json).
- [Matched compiler audit](adversarial_compiler_baselines.md).

Depth uses all-to-all logical interactions and the stated gadget schedule, rather than measured surface-code runtime. Measured cleanup assumes the explicit outcome-conditioned correction. Factories, physical routing, feed-forward latency, noisy reliability, and full-program generic optimization have separate ledgers and benchmark statuses.

## Known circuit context

The arithmetic uses existing temporary-AND, full-adder, carry-save, and Hamming-weight techniques. Relevant references include [Gidney's temporary logical AND](https://arxiv.org/abs/1709.06648), [Qualtran Hamming-weight phasing](https://qualtran.readthedocs.io/en/latest/bloqs/rotations/hamming_weight_phasing.html), and [Boyar and Peralta on multiplicative complexity](https://www.nist.gov/publications/tight-bounds-multiplicative-complexity-symmetric-functions). The comparison isolates the effect of exploiting the graph-cut identity within those techniques.

## Classification

**A. real scalable reduction found** — for the tested square-grid family, graph-aware arithmetic uses fewer AND/CCZ/fixed-4T resources than the specified even-aware full and partial counters, with exact phases and the same rotation budget. The saving is a constant-factor implementation result. Global circuit optimality, novelty, and end-to-end FTQC benefit are not established.
