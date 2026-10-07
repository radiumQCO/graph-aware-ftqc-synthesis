# Matched graph-aware whole-logical-workload benchmark

Run from the workspace root, using the existing main analysis environment:

```powershell
analysis/.venv/Scripts/python.exe analysis/graph_aware_end_to_end/run.py --concurrent
analysis/.venv/Scripts/python.exe analysis/graph_aware_end_to_end/verify.py
analysis/.venv/Scripts/python.exe analysis/graph_aware_end_to_end/report.py
```

The main replay uses only the standard library and cached input artifacts.
Verification additionally uses existing NumPy and mpmath. It does not download
papers, resynthesize rotations, rerun factory parameter searches, or modify old
results. `--resume` skips completed identical configuration keys; rerun without
it after changing the implementation. A complete replay takes a few minutes.

- `workload.py`: expands all 201 phase windows and startup; imports existing
  verified graph arithmetic and the original X counter. No new algorithm.
- `scheduler.py`: same placement, corridors, finite buffers, injection,
  branch-resolved corrections, Pauli tracking and list policies in both A/B.
- `run.py`: three list priorities per circuit, switching sensitivity,
  conservative corrections, and explicit additional concurrent-small-T case.
- `verify.py`: all 65,536 weight/catalyst basis combinations for an 8-level
  tower, graph mapping, counter checks, CCZ branches, frame identities,
  selected synthesis ensembles and completed-run accounting.
- `report.py`: renders the English report from the result artifacts.
- `workloads.json.gz`: deterministic full logical gate trace, including
  sampled synthesis branches/twirls. Contains no untimed phase placeholders.
- `results.json`: logical counts, conditional timing/volume and known gaps.
- `verification.json`: independent checks and their explicit scope.

Primary resource model: one shared factory region time-multiplexes the old
tuned A′ T source and the unchanged tuned CCZ source, since they do not fit
concurrently in 64,000 physical qubits. Its switching time is UNKNOWN physically;
0/29/290-cycle values are sensitivity assumptions, not measurements.

The separately labeled concurrent comparison instead uses the already audited
7,782-qubit small T source, three copies, plus the same 35,062-qubit CCZ source.
58,408 physical qubits fit the unchanged area capacity. This is a different,
explicit existing factory operating choice, never mixed into primary numbers.
Area compatibility is not a validated factory-shape embedding.

**This is a complete conditional P logical workload, but an incomplete physical
FTQC benchmark.** Factory cold start, physical output bridges, injection landing
sites, physical reset/feedback tails, shared circuit noise, decoder performance,
and actual whole-program failure probability remain unvalidated. Null fields
and status D must not be changed into zero-cost or physical-success claims.
