# Graph-cut phase audit

Python 3.10 or newer; standard library only. Run from the project root:

```powershell
python analysis/graph_cut_phase/toy_c4.py
python analysis/graph_cut_phase/verify_quantum.py
python analysis/graph_cut_phase/scaling.py
python analysis/graph_cut_phase/report.py
python analysis/graph_cut_phase/verify_artifacts.py
```

Python 3.10+ is sufficient; no package installation is required for these checks.

1. `toy_c4.py` verifies all 16 C4 inputs, computes ANFs, exhaustively searches
   affine-input XOR/AND circuits and two-predicate phase representations.
2. `verify_quantum.py` independently expands the 4T gadgets into actual complex
   amplitudes and projective cleanup branches. Generic-angle phases remain ideal.
3. `circuits.py` contains explicit reversible gate lists and arithmetic ledgers.
   It distinguishes binary counters from partial carry-save phase representations.
4. `scaling.py` first requires a successful C4 result. It checks every input for
   cycles and grids with at most 16 vertices. Larger grids are covered by the
   exact local-identity/edge-partition/adder proof plus implementation samples.
5. `report.py` writes `docs/graph_cut_phase_synthesis.md` from the results.
6. `verify_artifacts.py` checks saved circuit counts, depths, extremal inputs,
   reference-graph relabelling, archive hashes and document links.

Gate records are `[kind, targets]`, with an additional integer coefficient for
`P`: its angle is coefficient × theta. `AND` is a clean-target temporary AND;
`M_AND` is its X-measurement/CZ-corrected cleanup. `AND_ZERO` records a proved
zero product for auditing and has no implemented gate or resource cost.

Resource counts exclude synthesis of generic angles, resource factories and
injection/delivery workspace. Depth is an abstract logical circuit depth with
all-to-all interactions, not a measured hardware time. Claimed minima are
restricted Boolean-circuit minima; larger graph phase minima remain unknown.
