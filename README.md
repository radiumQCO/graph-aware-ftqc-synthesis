# graph-aware-ftqc-synthesis

**Exact graph-cut phase circuits and graph-aware Hamming-weight phasing, with reproducible FTQC compiler benchmarks.**

I study how graph structure can reduce the arithmetic needed to compile non-Clifford quantum operations. This project starts with an exhaustively verified four-cycle identity, builds reversible circuits for square grids, and compares the resulting workload against strengthened Hamming-weight and phase-gradient baselines.

The main workload comparison saves **9,900 temporary AND operations**, equivalent to **39,600 T gates** with the same adaptive 4T implementation. The repository contains the formulas, circuit records, resource ledgers, verification scripts, and compiler-run evidence behind that result.

## Verified results

| Case | Compared implementations | Result |
|---|---|---|
| Four-cycle integer output | Exact binary `cut/2` in the declared XOR/AND model | Two AND operations, with a matching lower bound |
| Four-cycle phase | Exact generic-angle cut phase | One AND and two arbitrary rotations |
| Periodic 10 × 10 grid | Even-aware partial popcount → C4-cover partial counter | 196 → 147 AND; seven rotations in both |
| Two independent 10 × 10 grids | Same comparison, jointly aggregated | 396 → 297 AND per ZZ block |
| Complete reconstructed workload | Even-aware HWP + catalysis tower → C4-cover HWP + the same tower | 61,105 → 51,205 AND; 254,118 → 214,518 sampled adaptive T |

The grid reduction is a **constant-factor arithmetic improvement**: both constructions scale linearly with the number of edges. The workload result is relative to the stated strengthened baseline and resource model.

## The four-cycle identity

For computational-basis bits `A, B, C, D`, define

```text
cut = (A XOR B) + (B XOR C) + (C XOR D) + (D XOR A)

p = A XOR C
q = B XOR D
g = p AND q
r = A XOR B
s = C XOR D XOR g

cut = 2 * (r + s)
```

Here `+` is integer addition. Consequently, phases of angle `2 * theta` on `r` and `s` implement `exp(i * theta * cut)` exactly for every basis input and generic `theta`. The reversible implementation restores the input register and cleans its temporary workspace with measured AND uncomputation.

## Workload and comparison contract

The reference circuit is a **conditional reconstruction** inspired by the TFIM resource-estimation workload of Beverland et al.: two independent periodic 10 × 10 instances, 200 data qubits, 400 ZZ edges, and 20 fourth-order Suzuki steps. Adjacent equal layers are merged into 101 X blocks and 100 ZZ blocks. The exact original QIR was not recovered; the reconstruction and its provenance are recorded in the analysis artifacts.

The execution failure target is `0.002`, with `0.002 / 3` allocated to rotation approximation. All compared methods use the same synthesis contract. Probability-mixture error bounds apply to the averaged channel; individual exported branches have their own equivalence contract. Suzuki approximation is accounted for separately from execution failure.

Adaptive temporary-AND circuits and fixed unitary compiler exports have separate ledgers. A temporary AND costs 4T with measured cleanup; replacing that cleanup by a unitary inverse gives 8T per pair. CCZ counts are alternative resource accounting, not an extra charge on top of the T implementation.

## Compiler audit

| Baseline or tool | Recorded result |
|---|---|
| Qualtran `HammingWeightPhasing` | Completed logical accounting under the matched contract |
| Qualtran `HammingWeightPhasingViaPhaseGradient` | Fewer synthesized rotations; more Toffoli/CCZ arithmetic; resource trade-off |
| PyZX basic optimization | Completed representative blocks; graph arithmetic saving retained in the counted T resources |
| PyZX strong TODD | Recorded workload attempts reached their time limits |
| Modern Feynman + FastTODD | Native Windows builds and equivalence-checked smoke tests completed; full Feynman preprocessing reached 240 s; downstream full FastTODD stage remains pending |
| TopoLS | Recorded matched attempts reached their time limits |
| WISQ/DASCOT | Recorded Windows integration issue; no comparable full output |
| FlowRouter | Literature reference; no runnable official benchmark recorded |

Full-program strong-optimizer and lattice-surgery comparisons are open benchmark tasks. Logical depth is also reported: the graph-aware circuit saves AND resources and workspace, while its recorded abstract logical depth is higher than baseline A.

## Quick start

The core graph-cut verification uses **Python 3.10+ and the standard library only**. From the repository root:

```bash
python analysis/graph_cut_phase/toy_c4.py
python analysis/graph_cut_phase/verify_quantum.py
python analysis/graph_cut_phase/verify_artifacts.py
python analysis/adversarial_compiler/verify.py
```

These checks cover the C4 truth table and exhaustive XOR/AND search, quantum amplitudes and cleanup branches, saved circuit hashes and resource counts, and the matched 200-qubit arithmetic kernels. GitHub Actions runs these same checks.

To regenerate the scaling circuits and report:

```bash
python analysis/graph_cut_phase/scaling.py
python analysis/graph_cut_phase/report.py
python analysis/graph_cut_phase/verify_artifacts.py
```

The broader compilation and factory analyses have additional dependencies and pinned external tools; see the documentation below. Downloaded third-party sources, installed toolchains, environments, and local caches are intentionally kept outside the published snapshot.

## Repository guide

- [`docs/graph_cut_phase_synthesis.md`](docs/graph_cut_phase_synthesis.md): identities, restricted minimum-AND proofs, circuits, scaling, and resource accounting.
- [`docs/adversarial_compiler_baselines.md`](docs/adversarial_compiler_baselines.md): matched Qualtran, PyZX, Feynman/FastTODD, and lattice-surgery audit.
- [`analysis/graph_cut_phase/`](analysis/graph_cut_phase/): standard-library verification, explicit reversible circuits, and saved results.
- [`analysis/adversarial_compiler/`](analysis/adversarial_compiler/): fixed branches, Clifford+T exports, source pins, and compiler-run records.
- [`docs/native_windows_setup.md`](docs/native_windows_setup.md): native compiler versions, build notes, and completed checks.
- [`docs/reproducibility.md`](docs/reproducibility.md): publication provenance, dependencies, and accounting boundaries.
- [`docs/`](docs/): supporting research notes on workload reconstruction, integer-weight arithmetic, non-Clifford resources, and FTQC cost.

## Authorship and AI assistance

I set the research questions, scope, and benchmark requirements. **The analysis code was written by AI (OpenAI Codex) under my direction**, with AI assistance in the documentation and investigation. Verification scripts and saved artifacts are included so that the results can be checked independently.

## License and references

Project-authored code and documentation are licensed under the **[Apache License 2.0](LICENSE)**. Third-party software and publications retain their respective licenses; this repository records their source references and pins rather than redistributing installed toolchains.

Key references include [Beverland et al., *Assessing requirements to scale to practical quantum advantage*](https://arxiv.org/abs/2211.07629), [Gidney, *Halving the cost of quantum addition*](https://arxiv.org/abs/1709.06648), [Qualtran Hamming-weight phasing](https://qualtran.readthedocs.io/en/latest/bloqs/rotations/hamming_weight_phasing.html), [Feynman](https://github.com/meamy/feynman), [FastTODD](https://github.com/VivienVandaele/quantum-circuit-optimization), and [PyZX](https://github.com/zxcalc/pyzx). Detailed citations accompany the individual reports.
