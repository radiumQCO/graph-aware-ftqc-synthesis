# ORCHESTRA: mandatory benchmark protocol

Date: 4 October 2026. This defines future experiments; it does not report a
completed benchmark or authorize implementing ORCHESTRA before the prior-art
decision in [prior_art.md](prior_art.md).

ORCHESTRA is a benchmark/research testbed. Beating static PyMatching alone is
insufficient. The protocol requires strong adaptive and neural competitors,
matched noise/circuit data, accuracy and latency measurements, and honest
reporting of losses and unavailable methods. A 10% LER reduction can be a useful
component result; it does not establish a major reduction in full FTQC cost.
See [open_bottlenecks.md](open_bottlenecks.md) for the wider limitations.


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## What is considered a meaningful result

Victory over static PyMatching Not enough in itself. At least one result required of the target group:

- better than a strong adaptive competition on the same noise and code;
- near near-optimal accuracy at significantly less time a certain degree of accuracy a certain amount of time accuracy at a;
- a clearly better accuracy/latency trade-off at comparable resource cost;
- Resistance to sound non-permanent sounds where strong existing techniques are degrading;
- A proven utility opportunity not available to specific tested competitors.

For the last point, you need capability experiment, Not the general phrase "I have more action to do"». Absence API One competition doesn't prove that everyone isn't able to.

If a strong competition is unavailable, let's say the limit of the comparison is reached. I don't raise the weak. baseline to state of the art And I don't announce a general victory over adaptive methods...

For selector mandatory comparison with tuned simple rules: threshold syndrome weight, confidence gate And the best fixed configuration. A complex model over fixed decoder does not prove necessity learning or joint coordination.

## Mandatory and extended hierarchy

| Role | Settings | What gets | Limitation |
|---|---|---|---|
| Static PyMatching LER | Ordinary MWPM, fixed prior | Circuit topology, nominal/calibration prior, detectors | Mandatory lower step of comparison |
| Static correlated PyMatching | Two-pass correlated matching, fixed prior | Same data plus available correlation model | Mandatory stronger matching baseline |
| Oracle PyMatching LER | Ordinary MWPM c true-rate prior | True probability of the current simulation regime | Unrealistic reference, Individual marking |
| Oracle correlated PyMatching | Correlated matching c true-rate prior | The same true probability and correlation model | Separate line; not replaced ordinary Oracle |
| Strongest adaptive baseline LER | Tuned syndrome-estimated matching; DGR/window techniques; LCD in compatibility | Only authorized causal telemetry | Choice validation and resource constraints |
| LCD | Leakage-unaware / leakage-aware / weighted leakage-aware | General detectors, compatible circuit, Available heralds | Official service/implementation; none imitation-LCD labels |
| BeliefMatching | Harmonized Set BP budgets | Detector data and public/estimated DEM | Conditional adaptation Not equal to education drift |
| Tesseract | Several pre-sets search budgets | Detector data and public/estimated DEM | Not declare exact logical ML without verification |
| Strongest neural baseline LER | AlphaQubit-style baseline; additional Ising/QAdapt with accessibility | Same observations, authorized features | Precise Google model not default |
| Near-optimal reference | Exact logical ML or tested TN | Clearly indicated priors/side information | Only tractable and compatible on the ground datasets |
| My LER | ORCHESTRA + Listed fast decoder | Only authorized telemetry | Account for full controller/shadow/update cost |

Current interfaces are checked in primary sources: [PyMatching correlations](https://github.com/oscarhiggott/PyMatching/blob/master/src/pymatching/matching.py), [BeliefMatching](https://github.com/oscarhiggott/BeliefMatching), [Tesseract](https://github.com/quantumlib/tesseract-decoder). For leakage: [Official Deltakit workflow](https://deltakit-docs.riverlane.com/en/latest/guide/decoding.html).

You can't declare one decoder The strongest one in advance of another article. For the main output, I'll see the strongest validation-selected competitor, budget authorized. Show all options implemented and accuracy/latency/resource frontier. The best result already selected for test, allowed as clearly stated descriptive comparison; formal conclusion must take into account this multiple choice.

## Rules Oracle

Oracle Gets True **Noise test/parameters**, Not realized faults, Correct recovery, future observations or reply to logical failure. True-rate adaptation access to the true and leakage state — different information privileges. The latter is allowed only as a separate, clearly named oracle-state option.

For mixed/temporal noise/time noise:/ sound/simulent noise/ sound/ weights are derived from the current fully-defined model rather than from the average a certain level of change in the model. and other factors. and/or p. Schedule, error support and logical mapping retained. If the noise is not adequately expressed in graphlike DEM, I're recording the appendix; it's not called the full model. leakage/correlation.

Oracle Shows the reserve of perfect model knowledge **selected matching implementation**. It's not a strict mathematical ceiling for all of us. matching strategies: graph approximation, degeneracy and limited heuristic They can leave a reserve. Individual end-samples can also change order LER. Global accuracy ceiling requires optimal logical-class inference with the same input data.

Construction/updating cost oracle graph separately from decoding, Even if such costs are not realistic deployment scenario.

## The same data and protection from hidden truth

For each experiment Save manifest:

- code family, distance, X/Z basis, cycles/window, boundary protocol and detector ordering;
- noiseless topology/schedule hash, nominal decoder model And the true simulator model with separate access rights;
- simulator/decoder/library versions and commit hashes, decomposition rules, seeds and noise trajectory ID;
- number shots, observed logical failures, split, Available heralds/soft readout and the time of their availability;
- CPU/GPU/FPGA model, memory, threads, precision, batching, warmup and timing scope.

For fixed quantum circuits All decoders One saved set detector events, logical labels and side information. One seed Without stored arrays, doesn't guarantee the same samples when modified simulator version or batch size.

Simulator noisy circuit can contain the true probabilities. So, normal decoder/controller does not automatically receive it. For decode, pass topology c nominal either causal estimated probabilities; true-noise circuit only stored at generator/evaluator and Oracle. This also applies to of the country circuit, to Deltakit: The server should not accidentally turn LCD baseline in oracle.

Available in experiment leakage heralds You can give them all who support them decoders. Missing support is recorded as capability limitation. Comparison of different input-information classes to be marked separately. You can't give ORCHESTRA hidden physical rates, a adaptive baseline — only syndrome.

Online logical labels actual and actual of the country and actual. and/or hidden faults Only sees evaluator. Decoder outputs/confidence available controller; error decoder On this. shot cannot be used for online promotion or model update. Offline training/validation labels Authorized and clearly described.

I're following a causal order: train → validation → frozen test trajectories. Test-time estimator can be updated for past undecided events according to a predetermined algorithm. Future test blocks and logical labels prohibited. Data for Choice candidate and its verifications are divided.

If the physical pattern changes, schedule or remapping, old syndrome dataset is no longer a general counter-fact test. Then let's compare policies in one simulator family with the same distributions/exogenous drift traces and correct modelling of actions. General random numbers allowed with correct coupling, but does not mean the same faults after change circuit. Cost transport/gates/idle and new detectors included. These results are separated from the results decoder-only Phase 1.

## LCD: Feasibility test

Up to the numerical comparison required:

1. Confirm authorized Deltakit access, SDK version and available LCD mode.
2. Check that API Accepts the correct pattern, same detector batch, logical observables and leakage flags without model/border change, etc. and control system for the purpose of the model/borders.
3. Set which probabilities uses a server: nominal, estimated either true; Last configuration name Oracle LCD.
4. Check for support for cause block updates. One offline batch limit the conclusion accuracy by this regime.
5. Measure client end-to-end latency separate from available and other than available. server compute time; absence server timing & N/a.

Documentation describes cloud LCDecoder and token requirement, Not a free local FPGA implementation. [LCDecoder API](https://deltakit.riverlane.com/api/docs/_build/generated/deltakit.decode.LCDecoder.html), [authentication](https://deltakit-docs.riverlane.com/en/stable/guide/authentication.html).

If it is not possible to keep the same noise/circuit/input information, record `NOT_COMPARABLE` with a specific cause. Others LCD paper numbers remaining literature context And never enter «Gap to best competitor».

## Neural baseline: requirements for implementation

Official name of the homemade model: **AlphaQubit-style baseline**. Not «Google AlphaQubit reproduction» and not «AlphaQubit 2», if not reproduced architecture/training/checkpoints and validation.

After audit decision selected by the strongest available recurrent/transformer option in the budget. Architectural ideas: condition retained between QEC rounds; spatial mixing/attention; coordinate/type embeddings; temporal recurrence; logical output correct processing final measurements. Full model design Not approved now. [AlphaQubit methods](https://arxiv.org/html/2310.05900), [modern AQ2](https://arxiv.org/html/2512.07737v2).

Compare several reasonable sizes/number of layers and training seeds Independent Expert validation. Set Settings, training shots, noise mixture, rounds curriculum, hardware hours and convergence evidence. A small, untrained model is not strong neural baseline. Available flags/analogue features must be consistent with the data.

Inference measured without gradient, with agreed precision and sync accelerator. Separate latency batch=1, streaming/block latency and throughput to batching. Training, retraining, model transfer and startup cost Reports. If resources do not allow learning a competitive model, line neural stays `NOT_RUN — insufficient validated training`, a Total SOTA conclusion limited.

Ising/QAdapt — additional modern neural competitors, But they can't be signed like AlphaQubit-style, if architecture is different. For QAdapt Check online training-label requirements and full play: public bundle contains inference patch/checkpoints, Not full training pipeline. [Ising repository](https://github.com/NVIDIA/Ising-Decoding), [QAdapt release](https://huggingface.co/Qhub-AI/QAdapt).

## Near-optimal / exact reference

Exact logical maximum-likelihood decoder Selects logical class with maximum **Total** The probability of all compatible faults this class. The most likely separate chain of errors is another task.

The total over-shot is exponential in number mechanisms: small distance Doesn't guarantee tractability for long circuit-level experiment. Before launch, estimate state/memorial and introduce limit. I don't cut high-weight faults Silent and not called the slit-over exact.

For TN - I're gonna get it. representation, contraction order, bond/truncation settings And check convergence budget and where possible coincidence with total over-reaction. Close TN is reference, Not certified ceiling. If priors, noise support or available side information Different, different ceilings, too... [BSV](https://arxiv.org/abs/1405.4883), [circuit-level TN implementation](https://github.com/ChriPiv/tndecoder3d), [CUDA-Q TensorNetworkDecoder](https://nvidia.github.io/cudaq-qec/examples_rst/qec/decoders.html).

Code-capacity d=3 exact calculation may be used as a separate sanity/reference Objective. You can't compare it LER c d=5 circuit-level result or count accuracy ceiling Basic test. Main TN/exact subset shall have the same scheme, and noise model For all those who are compared to him methods.

## Accuracy and statistics of the world's largest economies

For fixed-length experiment Main value:

`LER_shot = number_of_failed_shots / number_of_valid_shots`.

Shot is considered wrong if the decoder misproved at least one required logical observable. Showing More per-observable errors. X/Z basis The results are published separately, then a distinct association is clearly defined.

Can't be shared LER_shot as at rounds And no explanation to call it. per-cycle LER. Prin stationary independent logical parity flips and correct model used:

`P_fail(R) = (1 - (1 - 2 * epsilon)^R) / 2`.

Parameter epsilon Better to estimate severals durations with account taken preparation/measurement. For nonstationary noise It's like that. constant-rate Interpretation not guaranteed: first publication errors on fixed windows and trajectory, time after drift event and recovery phase.

Each assessment contains fails/shots and 95% interval. Zero errors observed does not mean LER=0 precision: Show upper limit. Timeouts, decoding failures and invalid outputs Into system-failure accounting; They can't be thrown out for the sake of low-lying LER. If timeout Completed valid fallback decoder, Include his final error and time.

Comparison by the same shots — paired: Keep where only wins A And that's it. B. For independent stationary shots That's right paired tests/bootstrap. For drift and stateful adaptation using independent trajectories and block/trajectory bootstrap; You can't count all dependents shots independent.

The main test is selected independently pilot/power analysis and then I'll see it through. If required adaptive stopping, I're going to determine statistically correct in advance. sequential procedure; Normal fixed-N interval After stopping, a beautiful result is not acceptable. I don't stop alone decoder before the others after a good number of mistakes.

Report contains different training/controller seeds and variation Under drift seeds. Precise near-optimal solver Also tested on a sample; its expected optimumity does not prohibit random losers on a small one sample.

## Delay, throughput expenditure

For **each** ♪ I're publishing the method ♪:

- mean latency;
- p50;
- p95;
- p99;
- throughput with units shots/s And wherein is right, cycles/s.

It is mandatory to indicate what is measured: latency one complete shot, response after the last syndrome, batch request or streaming block. For decoder-only timing The interval is from the available prepared input Before ready logical output. End-to-end timing Includes transfers, queueing and preprocessing. Quantum acquisition duration issued separately.

You can't be confused anymore `batch_time / batch_size` c per-shot latency. This value can be printed as amortized time, but percentile is considered real latency samples selected unit. `shots / total_wall_time` ♪ Gives me ♪ throughput; in parallel run It's not equal to the back mean latency. GPU timing requires synchronization, CPU — monotonous clock.

I declare warmup/JIT, cache state, number of timing samples, batching, thread count, frequency/power policy and precision. For meaningful p99 sufficient samples; Short smoke-test does not confirm latency tails.

Controller/estimator/shadow Working at full capacity resource cap, I think the competitors. The report is in..:

- time decoding, feature extraction, estimation and graph/model update;
- Duration pause to promotion and probability deadline miss;
- update frequency, adaptation delay/recovery time, queue/backlog;
- peak memory, CPU core-seconds, GPU hours, threads and hardware cost class;
- training/initial compilation/startup, their frequency and amortized cost;
- cost mapping/transport/gates/idle for future physical action.

Parallel shadow Work can reduce waiting but consume resources and can interfere. and the public fast path. Amortized update time does not replace the measurement of pauses, and p99 in the presence of updates.

Hardware paper numbers and cloud requests Not mixed into one speed table. Several tables can be shown timing scopes, with the main on the ground system comparison has an agreed scope. Support throughput >1 MHz does not prove latency <1 μm.

## Gap: Clear definitions

For reference `B` and ORCHESTRA `O`:

`Gap_abs(B) = LER_B - LER_O`.

`Gap_rel_percent(B) = 100 * (LER_B - LER_O) / LER_B`.

Positive gap means less LER y ORCHESTRA; Negative - Absent by precision. I'll rule it out:

- Gap to Static;
- Gap to Oracle;
- Gap to best competing decoder.

I're publishing both numbers, both numbers intervals and identity reference. If LER_B equal to or missing, relative gap = `N/A`, Not endless winnings. Zero errors show uncertainty bounds absolute difference. For lack of statistics verdict — `INCONCLUSIVE`.

Best competing decoder for deployment The output is selected among **not-oracle** comparable methods, which are contained in a given resource/latency budget. You can show it separately best accuracy without such restriction, expensive references. Oracle and exact reference Never disappear from the report; their comparisons are their own labels.

Latency/resource advantages shown separately: negative LER gap You can't hide it beautiful throughput. Let's just say that I have a fair conclusion about tradeoff, if it is confirmed that this compromise is useful for the pre-defined limitation the compromise.

## Mandatory template for each report

**Below the template, not results.** All lines remain visible if no method is used. For `NOT_RUN`, `UNAVAILABLE`, `NOT_COMPARABLE` and `FAILED` specified cause. Published Others' numbers don't fill the void.

`dataset_id / circuit_hash / noise_model_id / information_class / hardware / timing_scope / frozen_resource_budget`.

| Required result | Decoder/configuration | Status/reason | Fails/shots | LER + 95% interval | Mean latency | p50 | p95 | p99 | Throughput |
|---|---|---|---|---|---|---|---|---|---|
| Static PyMatching LER | ordinary fixed prior | NOT_RUN | — | — | — | — | — | — | — |
| Oracle PyMatching LER | true-rate ordinary | NOT_RUN | — | — | — | — | — | — | — |
| Strongest adaptive baseline LER | named validation-selected method | NOT_RUN | — | — | — | — | — | — | — |
| Strongest neural baseline LER | named validated model | NOT_RUN | — | — | — | — | — | — | — |
| My LER | ORCHESTRA + fast decoder | NOT_IMPLEMENTED | — | — | — | — | — | — | — |
| Correlated PyMatching | fixed prior | NOT_RUN | — | — | — | — | — | — | — |
| Oracle correlated PyMatching | true-rate correlated | NOT_RUN | — | — | — | — | — | — | — |
| LCD weighted leakage-aware | official execution | ACCESS_NOT_VERIFIED | — | — | — | — | — | — | — |
| Near-optimal reference | exact / converged TN | NOT_RUN | — | — | — | — | — | — | — |

After table mandatory `Gap to Static`, `Gap to Oracle`, `Gap to best competing decoder`, in each case absolute, relative and interval; missing input → `N/A — reason`.

A verdict is written in plain language: «ORCHESTRA loses X Under LER On this. dataset», «Better on the delay, but worse on the LER», «Statistics is not enough" or a precise limited claim of victory. Contains coverage/compatibility gaps, training budget, full controller cost violations deadlines. The term "failure" is only permitted with a pre-selected criterion of meaningful result.

## Status after this audit

No implementation ORCHESTRA, datasets, trained neural baseline or numerical comparative runs. LCD access, local decoder builds, accelerator availability and tractable exact subset Not yet verified. These are the work that has been noted for the future.. benchmark, Not the permit to frame the weak competitor.

The next scientific step is independent pilot and freezing narrow Phase-1 experiment from prior_art.md. Broad architecture implementation remains postponed to the decision on this hypothesis.
