# Adversarial compiler audit — reproducible artifacts

Date: 2026-10-06. Report: [adversarial_compiler_baselines.md](../../docs/adversarial_compiler_baselines.md).

This folder compares existing HWP/phase-gradient/graph-cover circuits. It does not implement a new algorithm or refine the physical model. `TIMEOUT`, host errors, unknown scratch/depth, and missing large-circuit equivalence certificates remain explicit results.

## Runtime and source pins

- Preparation/synthesis/checks: `analysis/.venv/Scripts/python.exe`, pygridsynth 2.0.
- API/optimizer: `analysis/.compiler_venv/Scripts/python.exe`; Qualtran 0.7.0, Cirq 1.7.0, PyZX 0.10.7.
- TopoLS requires PyZX **0.10.6** instead; its wheel is separately extracted in `analysis/sources/compilers/topols_runtime`.
- The historical installation used official wheels and repositories under `analysis/sources/compilers/`. Qualtran source hashes are in `qualtran_resources.json`; Git pins and actual tool availability are in `availability.json`.
- This host blocks newly installed Pandas/rustworkx DLLs. Working compiler commands put extracted pure-Python wheels first and the approved bundled runtime site-packages second; bundled Pandas 3.0.1 is used. This workaround does not alter any compiler algorithm.
- Modern Feynman and FastTODD were built and smoke-tested natively on Windows on 7 October 2026. Full Feynman preprocessing reached the recorded time limits; the full downstream FastTODD stage is pending. See `analysis/native/` and `docs/native_windows_setup.md`. WISQ records its Windows integration error; FlowRouter remains a literature reference.

These are records of a Windows audit, not a portable environment lock for every operating system.

## Run accounting and API checks

From the project root, PowerShell:

```powershell
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/prepare.py
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/verify.py
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/export.py

# Configure PYTHONPATH for the separately installed compiler environment if needed.
analysis\.compiler_venv\Scripts\python.exe analysis/adversarial_compiler/qualtran_probe.py
analysis\.compiler_venv\Scripts\python.exe analysis/adversarial_compiler/gradient_frontier.py
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/gradient_prep.py --frontier
```

`prepare.py` writes only the audit synthesis cache, leaving the previous main cache untouched. It stores all fixed branch/twirl choices in `programs.json.gz`. Synthesis uses the same local full-diamond tolerance for every method. Error bounds belong to the positive mixture channel, **not** each individual sampled branch.

## Bounded actual compiler attempts

```powershell
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/run_jobs.py basic
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/run_jobs.py strong
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/run_jobs.py full
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/run_jobs.py feynman
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/run_jobs.py surgery
```

Each command logs external processes with hard limits. Default workers=2. `strong`/`full` limits are 180 seconds per job, `surgery` 240. These commands can overwrite earlier attempt records; hashes apply to the saved audit snapshot. Run one batch at a time for comparable host load. Timing is compilation wall time, not quantum runtime. TopoLS parameters are identical for A/B but only model free-T unitary-lift blocks.

```powershell
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/tiny_prepare.py
analysis\.compiler_venv\Scripts\python.exe analysis/adversarial_compiler/tiny_optimize.py
analysis\.compiler_venv\Scripts\python.exe analysis/adversarial_compiler/surgery.py wisq
analysis\.venv\Scripts\python.exe analysis/adversarial_compiler/summarize.py
```

Tiny optimizer outputs have exact symbolic ZX certificates. The large completed basic outputs have `certificate=NOT_RUN`. Tiny success does not certify the 200-data-qubit workload. `summarize.py` verifies resource arithmetic and hashes; it does not certify quantum equivalence of large optimized outputs.

## Important files

- `logical_resources.json`: adaptive 4T compute + measured cleanup accounting.
- `export_resources.json`, `circuits/*full.input.qasm`: unitary lifts with **8T per compute/cleanup pair**. Do not compare this raw T cost with the adaptive ledger as if the implementations were identical.
- `circuits/*__ZZ_common__*__full.input.qasm`: historical full PyZX attempt inputs, without the extra lifetime reuse in `export.py`; graph uses 890 wires instead of 882, unchanged T count. All those attempts timed out. They are not the final compact exports.
- `qualtran_resources.json`: actual official API/count/decomposition probe and source hashes.
- `qualtran_frontier.json`: all tested rounding tolerances, weight checks, admissibility, best **tested** setting.
- `gradient_preparation_frontier.json`: paid 23-bit gradient preparation, channel error, T/CCZ vectors; adder scratch/depth unresolved.
- `*_attempts.json`, `logs/`: completed/timeout/error statuses. Missing or empty output is **not** a zero-resource result.
- `tiny_optimizer_results.json`, `verification.json`: completed correctness checks and their scope.
- `audit_summary.json`, `artifact_manifest.json`: aggregated status and file hashes.

The audit has no validated full-program strong-optimizer or lattice-surgery output. Modern native tools are now available; completing these experiments requires sufficient compiler resources and full equivalence checks. No system-level saving is inferred from missing outputs.
