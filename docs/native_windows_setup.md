# Native Windows compiler setup and verification

Date: 7 October 2026. This is an environment and compiler-validation update,
covering the recorded toolchain builds and compiler checks.

**Linux/WSL is not required for the installed Feynman and FastTODD tools.**
Both were built from the official pinned sources and run on this Windows
host. The full A/B optimization result remains a separate question.

## Installed components

The recorded installations were project-local under `analysis/native/`. No global PATH,
registry setting, or Windows security policy was changed by the setup scripts.
Native Haskell executables still require execution outside the restricted tool
sandbox on this host; this is distinct from needing Linux.

| Component | Installed version or source commit | Location |
|---|---|---|
| GHC | 9.4.8, official Windows bindist | `ghc-9.4.8-x86_64-unknown-mingw32/` |
| Cabal | 3.10.3.0 | `bin/cabal.exe` |
| Rust | 1.90.0, `x86_64-pc-windows-gnu` | `cargo/` and `rustup/` |
| Feynman optimizer | `d2c382a2ab43a40a87f12f4255645bbb55f704f8` | `bin/feynopt.exe` |
| Feynman verifier | same source commit | `bin/feynver.exe` |
| FastTODD | `231e6fe9f92d5bb1ebf7459c2a9233f5e74d148e` | `fasttodd-target/release/quantum_circuit_optimization.exe` |

Sources: [official GHC downloads](https://downloads.haskell.org/~ghc/9.4.8/),
[official Cabal downloads](https://downloads.haskell.org/~cabal/cabal-install-3.10.3.0/),
[Feynman repository](https://github.com/meamy/feynman),
[FastTODD repository](https://github.com/VivienVandaele/quantum-circuit-optimization).
Feynman's package version remains `0.1.0.0`; the source commit and executable
hash distinguish this modern build from the historical 2019 release binary.
The modern build accepts `-ppf`.

The GHC archive is 307,598,296 bytes and has SHA-256
`c4a767218551210521c78ddb51bfb309b0e336eef21eba1cc076f3bc0cc99a00`.
The Cabal archive is 15,667,375 bytes and has SHA-256
`b651ca732998eba5c0e54f4329c147664a7fb3fe3e74eac890c31647ce1e179a`.
Both were checked against their official checksum files. Cabal uses HTTPS
Hackage with its signed package-index verification enabled.

## Build details affecting reproducibility

Rust uses the GNU Windows target and the available LLVM `dlltool`, so this
build does not require Visual Studio. The latest compatible `ahash` resolution
failed on this toolchain through `getrandom`'s raw Windows DLL imports. Pinning
`ahash` to the author-declared compatible version **0.8.11** succeeded. The
generated `Cargo.lock` records the dependency resolution; optimizer source and
`Cargo.toml` were not modified.

Feynman was additionally linked with `-rtsopts` to allow a heap cap. A temporary
executable-only Cabal flag patch added `-rtsopts -fforce-recomp`; the original
Cabal file was restored afterward. No optimization algorithm was changed.
`run.py haskell-rts` reproduces this temporary patch and restoration. Ordinary
command-line flag changes alone initially left Cabal's cached executable
unchanged; that unsuccessful attempt must not be mistaken for the relink.

## Completed smoke checks

The two-wire control contains `T a; T a; CNOT a b; T b; T-dagger b; CNOT a b`.

| Check | Result | Evidence |
|---|---|---|
| Modern Feynman `-ppf -verify` | 4 T to 0 T; verified | `logs/feynman_ppf_smoke.log` |
| Official FastTODD | 4 T to 0 T | `logs/fasttodd_smoke.log` |
| Feynman verifier on FastTODD control output | Equal | `logs/fasttodd_smoke_equivalence.log` |
| Rebuilt Feynman with `+RTS -M3G -RTS` | same verified control result | memory-cap smoke invocation |

These establish that the programs work. They do not establish an A/B advantage.

## A necessary output-contract check

The official FastTODD CLI gadgetizes internal Hadamards. Its `.qc` output
contains added ancillas but no explicit measurement/feed-forward instruction
stream. A separate one-qubit control, `T; H; T`, was optimized and its complete
two-wire output simulated for both computational-basis inputs.

Projecting the added ancilla onto zero gives the desired operation multiplied
by `1/sqrt(2)`, with numerical residual below `2.60e-16`; the probability outside
the clean-zero ancilla sector is `1/2` for either input. Thus this raw output is
**not** a deterministic clean-ancilla unitary replacement. This is a small
numerical diagnostic, not a symbolic certificate for the full workload. It is
consistent with a postselected Hadamard gadget and does not refute FastTODD's
optimization method.

To compare deterministic implementations, the gadget measurement outcomes,
corrections, dependency order, and resources must be explicitly accounted for,
or optimization must be restricted to blocks with an appropriate contract.
Comparing only the emitted T count would skip this requirement. Reproducible
evidence: `benchmark/internal_h_contract.json` and `audit.py gadget-check`.

## Full-branch attempts and limits

The existing fixed branches were converted losslessly from QASM to DotQC. The
rotation strings, sampling seed, synthesis budget, and gates were not changed.
There are 200 arbitrary data inputs; other inputs are clean zero and all
original wires remain outputs. Hashes and gate counts are recorded in
`benchmark/input_manifest.json`.

| Fixed unitary branch | Wires | Input T count |
|---|---:|---:|
| A: even-aware counter plus catalysis tower | 1,082 | 498,538 |
| B: C4-cover counter plus the same tower | 882 | 419,338 |

These exports pay **8 T per AND compute/inverse pair**, rather than the adaptive
4 T accounting. Their 79,200 T difference is not a 79,200 T adaptive saving.

Modern Feynman `-ppf` is attempted under matched **240-second timeout and 3 GiB
managed-heap cap**. The heap cap is not a whole-process memory limit. Timeout
and shared host load are not comparative compiler speed measurements. A timeout
without a circuit provides neither an optimized T count nor an equivalence
certificate. Per-branch outcomes are in `benchmark/*__ppf.json`.

Full `-ppf` plus FastTODD is not certified by the smoke tests. If polynomial
folding produces no full output, the downstream pipeline remains unfinished.
Physical refinement remains paused; no new factory, noise, or qubit-second
estimates were generated during this setup.

Recorded outcomes: both full branches timed out at 240 seconds, and matched
representative `ZZ_common` blocks also timed out at 90 seconds. No optimized
T count was obtained for any of these four attempts. Historical compiler
artifacts were independently hash-checked: **163 files, zero mismatches**.
`toolchain_manifest.json` identifies the installed binaries and source commits.
These integrity checks do not turn a timeout into a compiler result.

## Reproduction

Use an available Python interpreter; the Windows `python` application alias may
point to the Microsoft Store rather than an installed interpreter. Commands
below assume a real Python interpreter is already on PATH:

```powershell
python analysis/native/run.py versions
python analysis/native/run.py smoke
python analysis/native/prepare_inputs.py
python analysis/native/audit.py gadget-check
python analysis/native/audit.py even_tower
python analysis/native/audit.py graph_tower
```

Some native commands require the same unsandboxed execution permission used
during setup. No further Windows security-policy changes are part of this
setup. The official binaries are already installed; repeating downloads is
unnecessary.

## Published snapshot

The executable installations are excluded from GitHub. Source pins, build runners, small control circuits, benchmark records, and binary hashes are included. Rebuild or install the tools locally before rerunning native jobs.
