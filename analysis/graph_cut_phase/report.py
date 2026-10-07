"""Render the graph-cut report from verified numerical artifacts."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
toy = json.loads((HERE / 'c4_results.json').read_text(encoding='utf-8'))
result = json.loads((HERE / 'scaling_results.json').read_text(encoding='utf-8'))
quantum = json.loads((HERE / 'quantum_verification.json').read_text(encoding='utf-8'))

md = r"""# Graph-cut phase synthesis: exact identities and resource scaling

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
"""
for row in toy['truth_table']:
    md += f"| {row['ABCD']} | {row['cut']} | {row['half_low']} | {row['half_high']} | {row['r']} | {row['s']} |\n"

md += r"""

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
"""
for case in result['cases']:
    methods = {m['name']: m for m in case['methods']}
    if 'generic_balanced_partial' not in methods:
        continue
    graph_name = ('C4_compact_phase' if case['case'] == 'C4' else
                  'cycle_fan_partial' if case['case'].startswith('C') else
                  'plaquette_balanced_partial')
    if graph_name not in methods:
        continue
    a, b = methods['generic_balanced_partial'], methods[graph_name]
    md += (f"| {case['case']} | {a['AND_compute']} | {b['AND_compute']} | "
           f"{a['rotation_count']} / {b['rotation_count']} | "
           f"{a['clean_ancillas_excluding_magic_injection']} / {b['clean_ancillas_excluding_magic_injection']} | "
           f"{a['cleanup_X_measurements']} / {b['cleanup_X_measurements']} | "
           f"{a['expanded_logical_depth']} / {b['expanded_logical_depth']} |\n")

md += r"""

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

"""
md += (f"The independent quantum verifier checks **{quantum['expanded_C4_basis_angle_measurement_branch_cases']}** "
       f"basis/angle/measurement-branch cases, with maximum statevector error "
       f"`{quantum['maximum_full_statevector_error']:.3g}`. Its CCZ injection check covers "
       f"**{quantum['CCZ_injection_basis_branch_cases']}** basis/branch cases with zero phase error.\n\n")
md += r"""
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
"""
(HERE.parents[1] / 'docs/graph_cut_phase_synthesis.md').write_text(md, encoding='utf-8', newline='\n')
print('Wrote docs/graph_cut_phase_synthesis.md')
