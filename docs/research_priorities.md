# Research roadmap

Updated: 7 October 2026.

I investigate the resource cost of successfully executed logical non-Clifford operations. The accounting includes preparation, rejected attempts, protection, storage, delivery, injection, correction, classical feedback, and the execution error budget.

The graph-aware compiler track provides verified arithmetic kernels and a matched conditional TFIM workload. Its current result is 9,900 fewer AND operations and 39,600 fewer adaptive T gates than the specified strengthened nongraph baseline. Workspace improves; recorded abstract logical depth increases. Each metric is retained in the ledger.

The next compiler milestone is to complete the matched modern Feynman/FastTODD pipeline with equivalence checks, followed by comparable lattice-surgery compilation. The native tools already run on Windows. Full preprocessing currently reaches the saved time limits, so the strong full-program result is pending.

The supporting resource studies compare known T-state, cultivation, and CCZ implementations through the point of actual use. T states and CCZ states are priced by equivalent implemented operations. Production cost and delivered-operation cost remain separate quantities.

Physical-model refinement is paused. The present scope is compilation, reproducibility, and resource accounting using existing methods. Further work must preserve the output contract, matched workload, and failure target.

See [the compiler audit](adversarial_compiler_baselines.md), [native toolchain notes](native_windows_setup.md), [the factory study](factory_bottleneck.md), and [the delivered-operation study](delivered_non_clifford_benchmark.md).
