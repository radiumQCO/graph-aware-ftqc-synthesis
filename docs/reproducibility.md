# Reproducibility and publication provenance

## Core checks

The graph-cut suite and the independent compiler arithmetic checks require Python 3.10 or newer and its standard library. The root README lists the verification commands. The archived scaling suite contains 120 explicit circuits; its verifier checks recorded resource counts, depths, extremal inputs, graph relabeling, and hashes. Tiny circuits additionally have exhaustive basis and quantum-amplitude checks.

Larger-grid correctness follows from the local identity, edge-disjoint partition, and reversible arithmetic construction, supplemented by the implementation checks. The repository reports exhaustive and sampled cases separately.

## Extended analysis environments

`analysis/requirements.txt` records the main analysis environment. `analysis/factory_requirements.txt` records the separate factory-analysis environment. The compiler audit records Qualtran 0.7.0, Cirq 1.7.0, and PyZX 0.10.7; the historical TopoLS integration uses PyZX 0.10.6. These are recorded environments, rather than a single cross-platform dependency lock.

External repositories and wheels can be retrieved through the source-fetch scripts and recorded URLs. They are not included in this release. Native Windows compiler instructions and exact source commits appear in [native_windows_setup.md](native_windows_setup.md). Installed compiler executables and runtime distributions remain local.

## Historical artifacts and hashes

This release retains the numerical results, circuit traces, and bounded compiler-run records from the research snapshot. Machine-specific paths in public metadata are replaced with repository-relative paths or environment placeholders. Documentation is edited for publication. No physical experiment is rerun by this packaging step.

`publication_provenance.json` records original workspace hashes and published hashes for normalized files. `publication_manifest.json` records the final release files. The compiler artifact manifest is refreshed for the published bytes; earlier execution status and numerical outcomes remain historical results. Original circuit archives and synthesis branches retain their recorded content.

Script runs may rewrite deterministic verification reports. Historical timing records are not fresh timing measurements on the reader's machine. Failed or empty compiler outputs retain their failure status and are not counted as optimized zero-cost circuits.

## Resource boundaries

- Temporary-AND ledgers charge 4T computation plus measured Clifford cleanup. Unitary exports charge the corresponding unitary inverse separately.
- CCZ demand is an alternative implementation ledger and is not added to the T cost of the same operation.
- Generic-angle rotations require explicit synthesis. Mixture-channel approximation bounds and fixed-branch equivalence certificates have different scopes.
- Logical ASAP depth assumes the stated interaction and gate-duration model. Surface-code scheduling, factory delivery, and noisy whole-program reliability require separate accounting.
- Supporting background notes preserve the historical workload and resource investigations; numerical JSON artifacts and primary references are the detailed evidence for their claims.

## Attribution

The project uses and credits the published methods cited in its reports, including Hamming-weight arithmetic, temporary logical AND, rotation synthesis, catalysis, phase gradients, and generic Clifford+T optimization. Downloaded upstream implementations retain their own licenses. Apache 2.0 covers the project-authored material in this repository.
