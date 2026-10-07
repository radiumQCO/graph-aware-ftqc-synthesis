# ORCHESTRA: prior-art audit

Audit date: 4 October 2026. Status: pre-implementation research audit.

**Decision:** ORCHESTRA is a benchmark/research testbed. The broad architecture
is not claimed as a fundamental breakthrough. The **10% LER** Phase-1 hypothesis
is a possible component test, not proof of an architectural leap. No ORCHESTRA
implementation, model training, or comparative decoder run was performed in
this audit.

The proposal is control above QEC, with a fast decoding path and slower updates
from accumulated telemetry. Adaptive weights, syndrome-based noise estimation,
decoder selection, telemetry learning, remapping, and fast/slow hierarchies
already exist in related forms. Especially close work includes
[Google RL control](https://www.nature.com/articles/s41586-026-10759-2),
[ReloQate](https://arxiv.org/html/2603.00837),
[CaliQEC](https://cseweb.ucsd.edu/~tullsen/isca_caliqec.pdf),
[Q3DE](https://arxiv.org/html/2501.00331), and
[Surf-Deformer](https://arxiv.org/html/2405.06941).

Not locating an exact match to the full feature list is not proof of novelty.
A concrete coordination mechanism, causal evaluation, guarantee, or matched
measured improvement would be required. See
[open_bottlenecks.md](open_bottlenecks.md) before defining another research target.


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## Main conclusion

**The broad idea already has a close realization.** Adaptive weights, syndrome-based noise estimation, decoder selection, and telemetry-based learning cannot be claimed as new QEC, transport of a logical qubit or separation of rapid decoded and slow setting. Especially close.. Google RL control, ReloQate, CaliQEC, Q3DE and Surf-Deformer. They're already connecting several levels of the system... [Google RL control](https://www.nature.com/articles/s41586-026-10759-2), [ReloQate](https://arxiv.org/html/2603.00837), [CaliQEC](https://cseweb.ucsd.edu/~tullsen/isca_caliqec.pdf), [Q3DE](https://arxiv.org/html/2501.00331), [Surf-Deformer](https://arxiv.org/html/2405.06941).

Completely match all the options listed ORCHESTRA No reference is made to the sources tested. This is **Not proof of newness**: The list of desired functions does not yet define the new method. A possible research question is whether joint, causal management of several solutions gives precedence over well-defined individual controllers with the same time and resource limits...

Recommendation: **not to build a new general «QEC orchestrator» as a declared breakthrough**. First check narrow hypotheses from the section Phase 1. If the benefits are limited to already known noise or decoder switching, the result should be called replication or engineering integration...

## How to Read Audit

- **LER** — Probability of logical error. Less is better.. Error for one experiment and error for one cycle - different values.
- **Latency** — response time; **throughput** — How many cycles or experiments are processed per second. A quick handling of large packs does not guarantee a short waiting for a separate response.
- **DEM** — A model of what errors cause what events of detectors and changes in logical result.
- **Herald** — A signal that is actually available, e.g. measured leakage indication a certain number of signals. It's not a hidden truth of the simulation.
- **N/a** — No comparable value established in the verified material. It's not zero..
- «Code not found" means there is no confirmed public artifact in the search, not proof that it is nowhere.
- **Runtime** — During work; **offline** — before launch or on pre-collection data or; **prior** — Initial assessment of error probability and other factors.. **Hotspot** — small area with increased noise. **p99** — Delay in which the 99% measured replies.

All numbers lower — the authors' results in the **their own conditions**, Not the competition table with ORCHESTRA. Sources: original articles, copyrights and official documentation. No promotional numbers used for ranking. Audit is not a complete systematic review of all literature or patents.

## Responses to five research questions

### 1. Which parts ORCHESTRA already exists?

| Part of the plan | Existing approaches on the ground | Conclusion |
|---|---|---|
| Assessment of local and measuring noise from syndrome history | Spitz; DEM estimation; Bhardwaj; Takou | Monitoring and evaluation is not new and evaluation a new approach to |
| Updating weights matching | DGR; adaptive assessments; Google decoder steering | Do not announce new |
| Adaptation to measured leakage signals | LCD and weighted leakage-aware LCD | A Direct and Serious Predator |
| Neural Fastway | AlphaQubit 1/2; Ising; QAdapt | Not a new class of decision |
| Decoder selection or cascade | Neural ensemble; Harmony; Libra | Choice, ensemble and confidence gate already exists |
| Physical event management training QEC | Kelly; Google RL control; self-calibration theory | There are experimental and theoretical implementations |
| Change in the recovery of syndromes | Adaptive Syndrome Extraction; AlphaSyndrome; FastSched | Discourage online-Adaptation and pre-start design |
| Transport and recalibration of logical patch | ReloQate; CaliQEC | Systemic, inter-level adaptation already in place |
| Response to code change and location defects | Q3DE; Surf-Deformer | Inter-level management already exists for the future |
| Active/shadow and screening of the candidate on | Known principle of model management and development and other relevant information | Not new by itself QEC-The idea; does not resolve the evaluation of alternatives automatically |

The basis for the table is shown in the cards below. For active/shadow The engineering finding is made here, not a statement of precision found QEC-Protocol.

### 2. Which will only be a gradual combination of known works?

One layer of telemetry that connects the assessment DEM, Weight settings and configuration selection, first integration. Adding a neurosnet or a slower controller doesn't change this conclusion. The addition of patches does not provide newness either: comparison with ReloQate/CaliQEC, including the cost of movement and calibration.

Two levels are convenient, but already seen as a fast decoder with periodic settings, a precoder with a global decoder and a small ensemble with a more expensive second passage. A new one may be a specific coordination algorithm, a guarantee, a method of causal evaluation or a measured gain rather than the name of the architecture by the user..

### 3. Is there really a non-verified hypothesis?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

**Candidates, not confirmed new:** Can a controller without any hidden noise and online-The log error mark is shared between selecting the noise assessment window, the frequency of the update and the decoder configuration in order to improve. LER limited to p99 Delays and full cost of calculations?

The test did not check this combination of causal access to data, the same budget and separate control options by the user. the data in the same way.. There are already very close solutions for parts of it. The experiment should therefore demonstrate the added value of coordination in relation to the independent combination of these decisions. If she's not there, the hypothesis is Phase 1 Not confirmed.

The broader issue of joint decoder, transport and scheduling remains a separate future experiment. Phase 1 below it doesn't prove it.

### 4. Which competition is the most powerful and how accessible?

There is no single strongest decoder without a sound, code, equipment and budget.

| Conditions | Mandatory, serious competition | Practical accessibility and other measures to ensure that the public is able to use it. to do so. for the public |
|---|---|---|
| Pauli circuit noise, Local CPU | Correlated PyMatching, BeliefMatching, Tesseract multiple search budgets | There are public applications; the installation and speed on this computer is not yet checked |
| Drift and heterogeneity | Assessment of syndrome + correlated matching; DGR; window techniques Bhardwaj | DGR/window techniques may require an honest implementation under article |
| Measured leakage signals | Weighted leakage-aware LCD | Official Deltakit API with authentication; access and the same scheme shall be checked and a safety net |
| Neural methods | AlphaQubit 2 as a scientific reference point; practical AlphaQubit-style baseline; Ising/QAdapt as additional candidates | Full official weights AlphaQubit Not confirmed; Ising has public code and access to weights with conditions; QAdapt published inference bundle |
| Small code, accuracy control | Exact logical ML; circuit-level tensor networks | Explicit value exact; public tndecoder3d; GPU-option CUDA-Q requires separate verification |
| Physical control | Google RL control; ReloQate; CaliQEC; Q3DE/Surf-Deformer | Not all are ready local libraries; CaliQEC publishes artifact |

**For Phase 1 a reasonable strength local:** adaptive syndrome-estimated correlated PyMatching + BeliefMatching + Tesseract. The main adaptive competition must be well-established separately. This is a working recommendation based on the available interfaces rather than the already measured ratings. Correlated matching fixed prior You can't be given the opportunity to adapt to temporarily changing noise.

LCD You can't replace your own Union-Find and sign the result «LCD». Local API-client is not a local hardware LCD. If access is not confirmed, line LCD is absent with cause; no victory is announced.

### 5. What a narrow, rebuttable experience to be the first to experience?

**Hypotheses H1:** Joint noise assessment control and decoder configuration will reduce LER minimum per 10% a relatively better adaptive competition, largely a test, with the same limit p99 delays and budget CPU/Memory. Threshold 10% — Proposed pre-encumbrance project, not the number of article.

Lock rotated surface-code memory, distance 5, both logical frameworks and 25 Cycles for Experiment. Distances 3 and 7 are separate inspections. Local experiments change Pauli/Measurement probability: Slow drift, steps and spatial hotspot. Correlated separate checks shall be performed Pauli-fixed permissible mechanisms DEM support. Leaks are a separate set only after the general test leakage simulator/API. Inside the first set, probability is fixed to one experiment; it simulates drift between experiments rather than random continuous calculation.

After independent pilot, I'll record the numerical noise ranges, drift scales, delay limits and test scope. I don't use the basic test to get them to work. Rapid artificial regime change should be called stress-Retroactivity requires links to published hardware tracks.

Actions Phase 1: Select from a small pre-tested set of window settings/assessment frequency and configuration matching/BP/search. New measurement scheme, stabilizers, code and physical transfer are not input. Each configuration has the same input data and a certain logical result format.

The controller uses only the previous telemetry; the settings for the next block are published after the evaluation of the current unit.. Only the true probability is obtained Oracle; True logical errors only get the valuer. Offline train/validation may have simulation marks, but test controller Can't see them..

| Option | What you need |
|---|---|
| Static ordinary and static correlated matching | Show normal and stronger fixed priors |
| Oracle ordinary and Oracle correlated matching | Segregate the benefits of noise knowledge from other improvements |
| Best single adaptive decoder | Main specialized competition |
| Only change in noise model sound sound noise | Check whether one evaluation is responsible for the gain |
| Select configuration only | Check the benefits of switching separately |
| Independent evaluator and selector | Check whether joint coordination is needed |
| Joint controller | Candidates ORCHESTRA Phase 1 |
| Strongest available neural baseline | Check neural accuracy/latency tradeoff |
| Exact/TN compatible small sub-set | Assess remaining reserve of accuracy |

Total offline grid search Under validation Mandatory: The controller should not gain advantage simply because competitors were ill-tuned. I need the same stream of events, a causal order, independent drift seeds and full cost of training, updates and shadow-calculation.

I also need a simple threshold.. selector by number of detectors activated and separate threshold available confidence-Statistics. Complex controller must justify the advantage over such cheap rules. Recent work on qLDPC shows that learned selection may fall to one threshold; it is still copyrighted preprint with a different code, not a general negative result, not negative overall result. [Adaptive decoder selection](https://zenodo.org/records/21466148).

Prior to launch, it is necessary to confirm that the configurations have different useful features the following accuracy/latency tradeoffs: if one is dominant in all modes, selector no meaningful task. This pilot is not used as a final test H1.

H1 Only confirmed by a selected basic metric, sufficient statistics and advantage over a strong adaptive competition aisle **and** independent combination. For 10% upper limit of the relationship trust interval LER should be lower 0.90. If the gain is less, unstable or disappears after accounting for expenses - claimed H1 Not confirmed. If I lose, I write it straight. Lack of statistics means uncertain result, not victory or proven loss.

Detailed rules for data, delays, confidence intervals and reports and data points to be kept up to date. data and data to be maintained and reported on by the Secretariat: [benchmark_protocol.md](benchmark_protocol.md).

## Methods cards

Each card captures the idea, entry, action/time scale, noise/code, accuracy, delay, scale/equipment, publicity and proximity by the user. by the user. ORCHESTRA. «The difference" describes the hypothesis of the project: there is no difference achieved yet.

### 01. Static / Oracle / Correlated PyMatching

- **The idea and the entrances:** MWPM by count DEM and detector events; correlated matching Additional uses decompressable errors correlations.
- **Actions and Time:** Normal static prior fixed; correlated matching — Conditional second passage; Oracle in my protocol gets a true probability of noise for renewal prior.
- **Noise and code:** graphlike/decomposable DEM, surface/repetition and other compatible tasks; arbitrary correlated leakage does not automatically appear.
- **Accuracy and delay:** matching does not add up all logical class errors. Comparable LER/p99 Not yet measured for project.
- **Scale/equipment:** C++/Python as at CPU; cost depends on the number of events, graph and correlations.
- **Publicity:** [PyMatching source/API](https://github.com/oscarhiggott/PyMatching/blob/master/src/pymatching/matching.py); `enable_correlations=True` required for construction and decoding.
- **Similarity:** Re-update weights - Existing function/take. ORCHESTRA should prove the usefulness of coordination over this instrument.

### 02. Local Clustering Decoder — LCD

- **The idea and the entrances:** distribution based on Union-Find; Detector events, graph and runtime heralds.
- **Actions and Time:** adaptivity engine Applys the precalculated local changes to the graph for measured leakages; updates are made near rapid decoded.
- **Noise and code:** rotated surface code, circuit noise leaks, relaxation and patch wiggling.
- **Accuracy:** in leakage-dominated Adaptation improves the design of the author model suppression factor; It's not proof of the same winning on another noise.
- **Delay:** less than 1 μs/cycle before d=17 — The window decoded time divided by the number of cycles. Time adaptivity engine Not separately measured.
- **Scale/equipment:** coarse-grained FPGA, resources d²; It's not a result of normal CPU.
- **Publicity:** [Article LCD, v2](https://arxiv.org/html/2411.10343v2); access through Deltakit considered separately.
- **Similarity:** Fast decoder plus adaptive engine already exists. Replacement heralds on another telemetry doesn't prove a new method by itself.

### 03. Deltakit: official route to LCD and Collision Clustering

- **The idea and the entrances:** SDK Sends circuit and detector batch; LCD Also accepts leakage flags. Yes weighted leakage-aware regime.
- **Actions and Time:** decode batch in the cloud; adaptive changes on LCD Inside service. Public high-level The interface does not confirm the control of the arbitrary slow controller or. continuous streaming.
- **Noise and code:** compatible surface-code circuits; leakage through Deltakit tooling, Not automatically through upstream Stim.
- **Accuracy/delay:** local comparable N/A. Network/API latency and FPGA decoder time separately recorded.
- **Scale/equipment:** Local Python-client and external service; offline compilation maps can be expensive...
- **Publicity:** SDK Open; LC/CC proprietary cloud features require token. [Authentication](https://deltakit-docs.riverlane.com/en/stable/guide/authentication.html), [LCDecoder API](https://deltakit.riverlane.com/api/docs/_build/generated/deltakit.decode.LCDecoder.html), [leakage workflow](https://deltakit-docs.riverlane.com/en/latest/guide/decoding.html).
- **Similarity:** Real possibility of a strong comparison; access/quotts/transfer of the same data not yet verified.

### 04. Collision Clustering — CC

- **The idea and the entrances:** Growth and merger of clusters of events; re-utilization of computing hubs to save hardware resources.
- **Actions and Time:** correction of each decoding window; Common drift control or remapping is not the main contribution on the basis of the information provided by the secretariat.
- **Noise and code:** rotated surface code, as described by the authors circuit-level depolarizing noise.
- **Accuracy:** Close Union-Find; threshold Near 0.78% That's the noise... Extrapolation very small LER Not equal to the measured errors.
- **Delay:** Table FPGA Gives you around 0.81 μs/cycle under d=21 and p=0.1%; normalized by d Cycles. ASIC — project evaluations, separate from FPGA measurements.
- **Scale/equipment:** FPGA/ASIC; small serial computation engine, growing memory and time.
- **Publicity:** [Article CC](https://arxiv.org/html/2309.05558); proprietary CC available through Deltakit, public FPGA RTL not confirmed.
- **Similarity:** candidate for a quick route, not a reason to declare a new one controller.

### 05. AlphaQubit 1

- **The idea and the entrances:** recurrent transformer; state per stabilizer, spatial attention/convolution, Measurement history and available additional readout features.
- **Actions and Time:** Update on cycles; simulation and simulation training finetuning on experimental data. It's not universal online-Code management.
- **Noise and code:** surface code, SI1000 And a bigger noise with leakage, crosstalk, soft readout; Sycamore d=3/5, simulation before d=11.
- **Accuracy:** better than the strong authors considered decoders in relevant cases of the relevant items datasets; do not transfer them LER To my circuits.
- **Delay:** Initial version insufficient for 1 μm superconducting cycle; compute-per-round does not equal the time of receipt of the final reply.
- **Scale/equipment:** Acceleration, significant education; spatial attention :: Accrued with number of stabilizers, recurrence limits the growth of memory over time.
- **Publicity:** Official full weight/pre-implementation not confirmed in audit. [Nature paper](https://www.nature.com/articles/s41586-024-08148-8), [methods/preprint](https://arxiv.org/html/2310.05900).
- **Informal code:** Found [community AlphaQubit-style repository](https://github.com/overshiki/alphaqubit-reproduce), the author notes the lack of a connection to Google/DeepMind. README reviewed; quality, training And a coincidence with paper Not checked here. It's a candidate for further testing, not an exact reproduction.
- **Similarity:** neural fast path Known; my possible controller He's above him.

### 06. AlphaQubit 2 / AQ2-RT

- **The idea and the entrances:** more scalable on the ground spatiotemporal neural architecture, temporal compression and recurrence; stabilizer history.
- **Actions and Time:** streaming inference; offline training/curriculum; not general runtime selector Physical politician of the population.
- **Noise and code:** surface and colour codes; realistic circuit noise and Willow data; full model shown before d=23.
- **Accuracy:** strong accuracy/throughput Results on modern competitors on the basis of the results of the competition; RT-The version changes accuracy for speed.
- **Delay:** Application for processing <1 μs/cycle before surface d=11 and colour d=9 as at Trillium TPU. Final latency — other value, may be significantly higher; QPU communication not fully activated.
- **Scale/equipment:** TPU; Long streams limited memory; large on the ground training costs does not delete.
- **Publicity:** Exact official model/weight not confirmed. [AQ2, v2](https://arxiv.org/html/2512.07737v2).
- **Similarity:** Mandatory modern orientation; homemade small transformer not equal AQ2.

### 07. BeliefMatching

- **The idea and the entrances:** belief propagation a more complete error model, then matching with updated probabilities; detector syndrome and DEM.
- **Actions and Time:** Conditional adaptation to each syndrome; number BP iterations ♪ Sets up ♪ ♪. Long-term drift study not automatically built.
- **Noise and code:** circuit-level surface-code noise c hyperedge correlations; compatible Stim DEM.
- **Accuracy/delay:** Improves the correlation; ours LER/tails n/a. Public version uses parallel BP schedule, Different from more accurate serial of the article.
- **Scale/equipment:** CPU, BP iterations add value before matching.
- **Publicity:** [author repository](https://github.com/oscarhiggott/BeliefMatching), Installation `beliefmatching`, input circuit/DEM.
- **Similarity:** «assess and transfer the probability matching» already exists. ORCHESTRA must be comparable to tuned BP, Not just plain MWPM.

### 08. Tesseract

- **The idea and the entrances:** search-based decoder Under DEM, Considers hyperedges; limited search for probable error pattern.
- **Actions and Time:** beam/search budget and ordering Change accuracy/latency; These are natural pre-tested configurations for selector.
- **Noise and code:** different stabilizer-code DEM, surface/colour/qLDPC and supported logical protocols.
- **Accuracy/delay:** High-precision competitors; do not declare competition; competition; competition exact logical ML. Most-likely error and most likely logical class different. Ours timing/LER N/a.
- **Scale/equipment:** C++/Python CPU, cost depends heavily on difficulty syndrome and limitations of search; tails are important.
- **Publicity:** [official repository](https://github.com/quantumlib/tesseract-decoder), [paper](https://arxiv.org/html/2503.10988); Accepted pre-generated detection events/DEM.
- **Similarity:** prepared by a strong alternative on the ground decoder and a well-adjusted accuracy/latency tradeoff.

### 09. Spitz et al.: adaptive weight estimator

- **The idea and the entrances:** Probability graph edges of steam statistics detector events without access to physical noise oracle.
- **Actions and Time:** Regular reassessment weights a more slow history window than decoding cycle.
- **Noise and code:** graph-compatible surface/repetition setting; Demonstration time-dependent noise as at repetition code.
- **Accuracy:** helps with sufficient statistics; too fast drift is not evaluated; too fast drift is not evaluated.
- **Delay:** decoder timing percentiles n/a; significant delay in statistical accumulation, etc.
- **Scale/equipment:** classical pair statistics; The choice of a window limits the frequency sensitivity.
- **Publicity:** [Article 2017/2018](https://arxiv.org/abs/1712.02360); confirmed ready author package Unreconciled in audit.
- **Similarity:** noise estimation → weights on two scales of time existed well before ORCHESTRA.

### 10. DGR — Decoding Graph Re-weighting

- **The idea and the entrances:** Considers selected decoder edges and their joint appearances rates/correlations from decoder history.
- **Actions and Time:** periodic alignment reweighting and conditional second matching pass; heuristic or neural reweighter.
- **Noise and code:** drift/mismatch, correlated Pauli noise, surface and honeycomb; phenomenological/circuit settings.
- **Accuracy:** significant gain over mismatch baseline under article under article 3 on the ground of the substance of the goods; decoder-derived estimates may inherit errors of the original decoder.
- **Delay:** for my N/A data; take into account tracers, Re-evaluation, second passage and graph updates.
- **Scale/equipment:** CPU and possible separate classical processing; pair tracking needs memory, selection limits costs.
- **Publicity:** [DGR, v3](https://arxiv.org/html/2311.16214v3); confirmed official reproducibility repository not found.
- **Similarity:** One of the most direct predecessors Phase 1. The Simplified Realization DGR-style, Not by exact reproduction.

### 11. Bhardwaj et al.: Adaptive Estimation of Drifting Noise

- **The idea and the entrances:** syndrome-only estimation c sliding, iterative and overlapping/relative windows for multiple drift frequencies.
- **Actions and Time:** Updates noise estimates and decoder priors Accumulated history; window sets the delay and filtering of drift.
- **Noise and code:** time-dependent Pauli, phenomenological and circuit-level surface-code simulations.
- **Accuracy:** estimated-model decoding Approaching ground-truth-model decoding in the regimes studied and improving on static prior.
- **Delay:** ours compute/tail metrics n/a; adaptation not instantaneous from-Statistical Window.
- **Scale/equipment:** Classic window processing; complexity depends on the mechanisms and windows being tracked and the other groups the windows.
- **Publicity:** [preprint/methods](https://arxiv.org/html/2511.09491), [journal publication](https://journals.aps.org/prxquantum/abstract/10.1103/z1hc-nqw5); Ready public package Not confirmed.
- **Similarity:** even adaptive/window combination cannot automatically be considered new.

### 12. Blume-Kohout / Young: DEM estimation

- **The idea and the entrances:** Statistics detector histories and their parity allow for assessment probabilities DEM events or aggregates or aggregates.
- **Actions and Time:** Recovers noise model of the many cycles; decoder-free estimation, Not a new fast decoder.
- **Noise and code:** independent DEM mechanisms with fixed signature; applicability is determined by the model and not only by the code name.
- **Accuracy:** identifiability and accuracy priors; Universal number LER does not state.
- **Delay:** estimation/inference percentiles N/a.
- **Scale/equipment:** Total number of individuals, number of and/or other factors. detector bits; sparse/aggregated options are more practical but limited to statistics.
- **Publicity:** [Article](https://arxiv.org/html/2504.14643); official package Not confirmed.
- **Similarity:** Simple firing rates do not reveal arbitrary physical patterns; ORCHESTRA shall take into account unidentifiable parameters and uncertainty.

### 13. Takou et al.: Logical error estimation from syndrome data

- **The idea and the entrances:** Assesses DEM event rates for experimental syndromes at support.
- **Actions and Time:** prior estimation Under dataset without supervised fitting to logical labels; then decode.
- **Noise and code:** surface-code memory as at Willow and IBM; Supported reference DEM, measurement/gate noise and correlations.
- **Accuracy:** Authors report typical improvements logical error probability order 5–10% Concerning device-informed priors; That's not my data.
- **Delay:** matched per-shot and adaptation tails N/a.
- **Scale/equipment:** classical statistics plus and other factors. matching; sampling cost important in rare errors.
- **Publicity:** [Article](https://arxiv.org/html/2606.11496v2); public experimental data Used; ready author package Not confirmed.
- **Similarity:** A strong competition for "without" hidden noise online logical labels». Support for errors cannot be assumed to be automatically learned with rates.

### 14. Kelly et al.: in-situ calibration

- **The idea and the entrances:** error-detection outcomes are the setting signal single/two-qubit gates.
- **Actions and Time:** physical control parameters adjusted during re-entry error detection; Slower cycles of statistics QEC.
- **Noise and code:** superconducting nine-qubit repetition experiment, injected frequency drift.
- **Accuracy:** Shows suppression of drift; not universal surface-code LER Table.
- **Delay:** Full decoder p50/p99 N/a; calibration response requires many measurements.
- **Scale/equipment:** parallel local calibration physical device; declared local scalability does not mean zero total value.
- **Publicity:** [Author article of the author 2016](https://arxiv.org/abs/1603.03082); ready calibration control library Not confirmed.
- **Similarity:** Training of the Directorate of Public Administration and other factors. and and so forth. and the public QEC telemetry Existence before the present neural decoder architectures.

### 15. Google: Reinforcement learning control of QEC

- **The idea and the entrances:** detector rates and sparse factor structure binding QEC telemetry with physical controls; decoder steering Supplements loop.
- **Actions and Time:** policy-gradient calibration/steering Under epochs, Not the big one NN for each physical event. There's a joint physical/decoder settings.
- **Noise and code:** Willow surface/colour memory and injected drift; scaling simulations to surface d=15.
- **Accuracy:** The authors submit 3.5-multiple stabilization with decoder steering in their drift experiment.
- **Delay:** calibration epochs and real-time decoding different; end-to-end percentiles for ORCHESTRA N/a.
- **Scale/equipment:** superconducting processor and classical management, thousands control parameters; The experiment cannot be repeated by one PyMatching.
- **Publicity:** [Nature 2026](https://www.nature.com/articles/s41586-026-10759-2), [supplement](https://arxiv.org/html/2511.08493), [experimental data](https://zenodo.org/records/17566522); Total ready-to-run hardware controller Not confirmed.
- **Similarity:** very high. B supplement decoder steering uses LER estimates and notes the difficulty of transferring scalable real-time setting. It's a specific border, not a lack of cross-layer prior art.

### 16. Provably Efficient Self-Calibrating Quantum Fault Tolerance

- **The idea and the entrances:** syndrome detection rate She is the speaker surrogate objective for analog calibration with conditions control-induced noise.
- **Actions and Time:** online optimization Under epochs, including drift; not arbitrary optimization of any QEC Policy.
- **Noise and code:** under review control errors, qLDPC and Simulated neutral-atom/Clifford settings.
- **Accuracy:** theoretical conditions of convergence and simulations; not a universal guarantee of minimization LER Under firing rate.
- **Delay:** per-decoder latency N/a; convergence/sample cost depends on the required accuracy.
- **Scale/equipment:** code locality can produce distance-independent convergence with preconditions; data processing remains.
- **Publicity:** [preprint 2026](https://arxiv.org/html/2608.05686); Ready controller package Not confirmed.
- **Similarity:** online telemetry-based calibration and some of its safeguards have been studied; it cannot be assumed that the reduction of the the state of the environment is a major cause of concern. on the ground firing rate Always improves any logical task.

### 17. Neural ensemble decoding

- **The idea and the entrances:** neural selector Under syndrome Selects decoder, Whose name is this? pattern It's better...
- **Actions and Time:** Select for a specific syndrome after offline training.
- **Noise and code:** surface code, depolarizing setting; MWPM and HDRG ensemble.
- **Accuracy:** improving relative to individual members ensemble in the article; advantages depend on the addition of errors between decoders.
- **Delay:** ours latency tails N/a; selector and caused by: decoder Together, the price is determined.
- **Scale/equipment:** Classical ML plus set decoders; Increase in recruitment not free.
- **Publicity:** [Article 2019](https://arxiv.org/abs/1905.02345); Officially ready selector package Not confirmed.
- **Similarity:** «Select decoder "A known idea. Slow block-level selection may be an engineering variation, not a new principle.

### 18. Harmony / harmonization

- **The idea and the entrances:** ensemble MWPM variants c perturbations; syndrome, priors and agreement on decisions.
- **Actions and Time:** small ensemble - He's a servicer cases; Low consent triggers a higher-value level.
- **Noise and code:** repetition/surface benchmarks, phenomenological and circuit-level noise.
- **Accuracy:** Approaching ML reference with sufficient ensemble size; confidence — empirical risk signal.
- **Delay:** accuracy/cost tradeoff exist; my percentiles N/a; branch to complex cases affects tails.
- **Scale/equipment:** CPU parallelism, value of membership ensemble; layered scheme reduces average flow.
- **Publicity:** [Article](https://arxiv.org/html/2401.12434); specific independent author library Not confirmed.
- **Similarity:** quick/slow decoding cascade and confidence-based escalation already exists; do not confuse ORCHESTRA slow adaptation across epochs.

### 19. Libra / matching synthesis

- **The idea and the entrances:** Collects the best local error assignment from ensemble correlated MWPM solutions; syndrome, DEM and alternative approaches matchings.
- **Actions and Time:** conditional ensemble/search For the Undead cases, not general physical controller.
- **Noise and code:** circuit-level correlated surface-code memory.
- **Accuracy:** The author reports about 10% improvement suppression factor in a researched study setting; not 10% universal reduction LER.
- **Delay:** ours metrics N/a; ensemble and synthesis Increase costs, conditional use reduces average.
- **Scale/equipment:** local synthesis and CPU parallel ensemble; cost depends on the size ensemble and complex cases.
- **Publicity:** [Article](https://arxiv.org/abs/2408.12135); AQ2 describes Libra How in-house decoder, ready public implementation Not confirmed.
- **Similarity:** ensemble coordination already investigated; separately to prove the benefits adaptation to drift.

### 20. NVIDIA Ising predecoder

- **The idea and the entrances:** local neural predecoder Under spatiotemporal detector tensor; Residual syndrome ♪ He's passing on ♪ global decoder.
- **Actions and Time:** neural inference plus PyMatching for surface / Chromobius for colour; training separately.
- **Noise and code:** & Flat circuit-level noise; surface and colour code with supported representation.
- **Accuracy/delay:** ours LER/tails n/a; account for and NN, and processing residual, and global backend.
- **Scale/equipment:** GPU/Torch, Local receptive field, CPU/backend and device transfers.
- **Publicity:** [official code](https://github.com/NVIDIA/Ising-Decoding); published model options, access pretrained weights requires entry/compliance. The car access was not checked.
- **Similarity:** «small learned fast stage above matching» already operational. Ising should not be renamed on the ground AlphaQubit-style transformer.

### 21. QAdapt

- **The idea and the entrances:** local neural corrections, heterogeneous spatiotemporal features and continual adaptation; residual It's normal global decoder.
- **Actions and Time:** sequential noise-task adaptation c regularization, Then inference. Not to be proven unlabeled online control Just by word of word adaptive.
- **Noise and code:** rotated surface memory, synthetic OOD noise and Willow evaluation; Not all leakage/logical-operation regimes Checked.
- **Accuracy:** paper He tells you the winnings of his neural baseline; Notes the absence of LER confidence intervals and total per-component end-to-end timing.
- **Delay:** backend residual latency not equal latency complete pipeline.
- **Scale/equipment:** Torch/GPU plus Ising-compatible backend.
- **Publicity:** [paper](https://arxiv.org/html/2607.28422), [author checkpoint bundle](https://huggingface.co/Qhub-AI/QAdapt); patch/inference configs and weights available, training code/intermediate models in bundle not available; required Ising revision.
- **Similarity:** Strong direct predecessor to adaptive neural-plus-global Ways; explore train-label requirements before comparison online adaptation.

### 22. Adaptive Syndrome Extraction

- **The idea and the entrances:** inner-code detection He's picking which ones. outer stabilizers measure.
- **Actions and Time:** measurement circuits changes during extraction realizablesed flags.
- **Noise and code:** [[4,2,2]]-concatenated hypergraph product codes, Supported circuit noise/settings; Not directly surface-MWPM apples-to-apples comparison.
- **Accuracy:** Authors show lower LER and reduction CNOT/qubit overhead in the examples studied.
- **Delay:** Total p99 decoder/controller n/a; yes cycle/gate resource tradeoff.
- **Scale/equipment:** requires feedforward and to be permitted adaptive FT gadgets; You can't just miss arbitrary checks.
- **Publicity:** [paper](https://arxiv.org/html/2502.14835), [author code/data](https://github.com/noahberthusen/adaptive_qec).
- **Similarity:** runtime The choice of measurements already exists with the mathematical design of the code. ORCHESTRA must choose the tested gadgets, Not invent stabilizers.

### 23. AlphaSyndrome

- **The idea and the entrances:** MCTS Looking for execution order syndrome-measurement circuit Under stabilizers, dependencies and noise/decoder evaluation.
- **Actions and Time:** changes gate schedule before execution; this compilation-time search, Not proven online-Drift controller.
- **Noise and code:** several QEC families, noisy syndrome circuits, including surface and qLDPC settings.
- **Accuracy:** optimizes LER, Not just circuit depth; the results depends on decoder and gate ordering.
- **Delay:** search time and quantum cycle duration separate from inference latency; ours p99 N/a.
- **Scale/equipment:** Classical search and and simulations; search space growing with circuit size.
- **Publicity:** [paper](https://arxiv.org/html/2601.12509v2), [author repository](https://github.com/acasta-yhliu/asyndrome), MIT artifact.
- **Similarity:** hardware/noise-aware scheduling Known. Selection of pre-qualified schedules A drift may require new experience, but not a new baseline scheduler.

### 24. Reinforcement Learning for Syndrome Extraction / FastSched

- **The idea and the entrances:** RL and importance sampling Search extraction schedules Low logical error probability.
- **Actions and Time:** Trainee search before execution, not an automatic continuous replacement policy stabilizers.
- **Noise and code:** extraction circuits different sizes, surface-code examples.
- **Accuracy:** The authors compare it to AlphaSyndrome/PropHunt; Benefits are related benchmarks.
- **Delay:** training/search cost not equal online latency; matched p99 N/a.
- **Scale/equipment:** Classical RL training and simulated/importance-sampled evaluation; rare logical errors It's difficult scoring.
- **Publicity:** [preprint September 2026](https://arxiv.org/html/2609.12020) Recalls [Anonymous Author artifact](https://anonymous.4open.science/r/FastSched-B5FE/). Reference found; contents and reproducibility of launch are not checked here.
- **Similarity:** It's important to keep up with the new one. prior art Under scheduling, but Phase 1 does not include this action space.

### 25. CaliQEC

- **The idea and the entrances:** hardware calibration needs, drift characteristics, surface patch geometry and current logical operations.
- **Actions and Time:** Selects/insulated qubits for calibration, Supports the protection of the logical state through code deformation/enlargement and planning.
- **Noise and code:** surface-code fault-tolerant computation under drift; hardware and and and and and and and the other two and simulation assumptions.
- **Accuracy:** analyse retry risk and spacetime overhead, Not just solitary decoder LER.
- **Delay:** operation/runtime overhead and calibration duration Important; Single, one-stop prim. decoder p99 N/a.
- **Scale/equipment:** additional qubits and the possibility of calibration/change patch; simulation start on CPU.
- **Publicity:** [ISCA 2025 paper](https://cseweb.ucsd.edu/~tullsen/isca_caliqec.pdf), [public artifact](https://zenodo.org/records/15104546); paper indicates Python/Stim and MIT artifact. The archive page was not downloaded through a research tool, the contents were not checked; accessibility was confirmed by a statement in the of the document. artifact appendix, not by local launch.
- **Similarity:** very high for calibration + mapping/policy control. Without these comparisons, you can't say new cross-layer stack.

### 26. ReloQate

- **The idea and the entrances:** detector fire-rate history → conservative prediction logical risk; calibrated patch availability.
- **Actions and Time:** threshold breach start remapping to a healthy one tile and recalibration released; monitoring, prediction, relocation different delays.
- **Noise and code:** drift/bursts in surface-code patch architecture; Models linked to hardware tracks.
- **Accuracy:** reduces stay above the permissible logical risk in analysed scenarios not universal decoder winner.
- **Delay:** remap/calibration cycles taken into account; decoder inference percentiles N/a.
- **Scale/equipment:** spare tiles/routing space, valid logical transport and calibration capability.
- **Publicity:** [paper, v2](https://arxiv.org/html/2603.00837v2); Official ready-to-run public implementation Not confirmed.
- **Similarity:** almost a direct match to telemetry → mapping/calibration part ORCHESTRA. Free renaming physical indices does not reproduce such remap.

### 27. Q3DE

- **The idea and the entrances:** syndrome anomaly detection signals multi-bit burst; integration detection, deformation and decoding response.
- **Actions and Time:** event-driven enhanced protection and and and and and and and the public re-decoding c rollback After detection burst.
- **Noise and code:** surface-code architecture, cosmic-ray-like correlated bursts.
- **Accuracy:** systemic reduction of vulnerability to on the ground burst in the authors models; not ranking LER v. LCD on another noise model.
- **Delay:** detection delay, rollback and deformation cost significant; comparable on the ground decoder p99 N/a.
- **Scale/equipment:** additional spatial-resources and on the ground hardware-control support.
- **Publicity:** [Authorized text](https://arxiv.org/html/2501.00331); [University page of authors](https://kyushu-u.elsevierpure.com/en/publications/q3de-a-fault-tolerant-quantum-computer-architecture-for-multi-bit/) Reaffirms MICRO 2022. ArXiv upload 2024/2025 Not the date of origin of the idea; public reproduction package Not confirmed.
- **Similarity:** early apparent cross-layer adaptive QEC system. «Joint management" with no specific distinction is covered.

### 28. Surf-Deformer

- **The idea and the entrances:** defect information, surface patch layout and requirements logical operations; Correct set gauge/deformation primitives.
- **Actions and Time:** Defects Management, adaptive enlargement and layout optimization when modified hardware quality.
- **Noise and code:** static/dynamic surface-code defects, drift/burst scenarios.
- **Accuracy:** improves end-to-end program failure and qubit efficiency on the means under consideration; it is not comparable on the way in which it is considered per-cycle LER rating.
- **Delay:** deformation/routing time and communication throughput, Single decoder p99 N/a.
- **Scale/equipment:** grid resources and runtime control permissible transformations.
- **Publicity:** [MICRO 2024 paper, v3](https://arxiv.org/html/2405.06941v3); Ready author repository Not confirmed.
- **Similarity:** Joint settings code policy and placement already studied. ORCHESTRA must not repeat it as a new general principle.

### 29. Hardware-aware compilation + lightweight QED co-design

- **The idea and the entrances:** circuit, connectivity, calibrated noise profile; Joint optimization mapping, SWAP insertion and places syndrome checks.
- **Actions and Time:** compiler search plus learned scheduler, predominantly before execution.
- **Noise and code:** early fault-tolerance and lightweight error-detection codes c postselection; It's not a full-fledged long-term. surface-code QEC.
- **Accuracy:** evaluated algorithm success probability c postselection; do not use it instead unconditional logical error rate.
- **Delay:** compilation/scheduler time and quantum program time; ours inference tails N/a.
- **Scale/equipment:** Small circuits, CPU optimization, GPU density-matrix simulations.
- **Publicity:** [preprint](https://arxiv.org/abs/2606.07666), [author repository](https://github.com/Sumitchongder/quantum-hw-aware-pipeline); Results were not independently reproduced.
- **Similarity:** joint mapping/scheduling design There is already a different regime QED Doesn't make it straight decoder comparator.

### 30. Tensor-network decoding: BSV / qecsim

- **The idea and the entrances:** summation of probability errors in logical equivalence classes Through tensor contraction; syndrome and noise model.
- **Actions and Time:** Selects logical class for each syndrome; oracle priors or evaluated priors — Different information regimes.
- **Noise and code:** planar surface code; tractable exact cases and approximate general-noise TN. qecsim MPS routines Not automatically circuit-level leakage decoder.
- **Accuracy:** accurate summation gives ML in the specified model; truncated contraction only approximation.
- **Delay:** For my cases N/a; bond dimension manages value/precision.
- **Scale/equipment:** exact generally exponential; TN approximation requires convergence checks.
- **Publicity:** [Bravyi–Suchara–Vargo paper](https://arxiv.org/abs/1405.4883), [qecsim](https://github.com/qecsim/qecsim).
- **Similarity:** reference for small and medium-sized subset, Not the main fast track and not proven ceiling to approximation.

### 31. Tensor Network Decoding Beyond 2D

- **The idea and the entrances:** contracting higher-dimensional networks, including spacetime circuit noise; syndrome and model factors.
- **Actions and Time:** approximate logical probability computation; increase contraction budget The stability shall be checked.
- **Noise and code:** 3D surface code and rotated surface code c circuit-level noise; specific implemented models.
- **Accuracy:** improves matching as at studied circuits; approximate TN not count exact without verification.
- **Delay:** ours mean/tails n/a; not to be moved timing between contraction settings.
- **Scale/equipment:** rapidly growing contraction cost/memory; Julia, ITensors and Python dependencies.
- **Publicity:** [paper](https://arxiv.org/html/2310.10722), [author tndecoder3d](https://github.com/ChriPiv/tndecoder3d).
- **Similarity:** most relevant public circuit-level accuracy reference among the audited TN implementations; not automatically compatible with arbitrary leakage.

### 32. Optimal adaptation to local noise

- **The idea and the entrances:** syndrome and local process-matrix noise description; TN near-optimal recovery with intentionally distorted priors.
- **Actions and Time:** Examines what adaptation parameters are really important; not telemetry-driven live controller.
- **Noise and code:** surface code, single-qubit local noise, coherence/bias/inhomogeneity.
- **Accuracy:** allows the loss from incorrect parameters to be assessed relative to near-optimal recovery in the study class.
- **Delay:** realtime decoder percentiles N/a.
- **Scale/equipment:** TN contraction, cost depends on representation/bond budget; Not all circuit correlations in local model.
- **Publicity:** [Article](https://arxiv.org/html/2403.08706); The final public package is not confirmed in this audit.
- **Similarity:** provides a useful test on whether adapting a specific parameter to its cost is worth. It's not justified to adapt all at the same time without such analysis.

### 33. CUDA-Q QEC TensorNetworkDecoder

- **The idea and the entrances:** GPU tensor contraction for ML reference; documentation shows circuit-level problem from Stim circuit.
- **Actions and Time:** Imagining correction Under syndrome/model, not general slow controller.
- **Noise and code:** Supported parity-check/DEM problems and shown surface-code circuits; arbitrary leakage support Not confirmed.
- **Accuracy:** The official example describes exact maximum-likelihood decoding. Before use as logical-class ceiling I need to check that the interface and mode actually add up the right classes and don't notice the model.
- **Delay:** project-specific mean/p99 N/a; GPU transfers and compilation Take into account.
- **Scale/equipment:** NVIDIA GPU/CUDA runtime, High contraction complexity; Available equipment is not confirmed here.
- **Publicity:** [Official documentation](https://nvidia.github.io/cudaq-qec/examples_rst/qec/decoders.html).
- **Similarity:** candidate reference in technical compatibility, not any authorization to declare tensor result best.

### 34. Adaptive decoder selection: Checking the simple threshold

- **The idea and the entrances:** selection decoder Under syndrome; Check if a full history/nirson is needed instead of the number of people who worked checks.
- **Actions and Time:** DQN or simple threshold Switch decoder for the task; not joint physical control.
- **Noise and code:** considered qLDPC/HGP simulations, of which [[625,25]]; Not direct surface-code experiment.
- **Accuracy:** The author states that. of the author tuned threshold comparable or better learned policy in these circumstances, although learned policy Better. fixed decoder. It's a limited result. author preprint, Unestablished universal law.
- **Delay:** comparable accuracy/cost constraints; measured load can change the order of value decoders, ours p99 N/a.
- **Scale/equipment:** classical decoder runs and DQN training; threshold It's almost cheaper..
- **Publicity:** [Author Zenodo record, July 2026](https://zenodo.org/records/21466148) contains paper; reproducible public code package Not confirmed.
- **Similarity:** Direct warning.. and other measures. and/or Phase 1: Win fixed decoder Not enough, comparison with tuned Simple selectors.

## What exactly is checked in the repository

Reviewed public source/API PyMatching and README/Interfaces BeliefMatching, Tesseract, Deltakit and its component repositories, Ising, QAdapt release, AlphaSyndrome, tndecoder3d and qecsim. This checks declared capabilities and integration points; it is not independent algorithm certification. No code was installed, launched or reproduced; large training runs not implemented.

References to `stable`, `latest`, `main` and `master` contents may change. Before the future experiment You need to record the versions/commit hashes. For LCD/AQ2 The cards shall indicate the tested arXiv versions. Presented QAdapt release instruction tied to Ising commit `33acb152e403bc189f2effdb07f1a87b34c745f1`, Not arbitrary latest checkout. [QAdapt release instructions](https://huggingface.co/Qhub-AI/QAdapt).

## Practical testing Deltakit to the future benchmark

Documentation confirms the approval batch interface, But real server call Not implemented. The authentication, quotas, versions and transmission of the required scheme will have to be verified. Token should not be included in the repository or report. [Official authentication](https://deltakit-docs.riverlane.com/en/stable/guide/authentication.html).

Future adapter must serve **the same** Saved detector batch and circuit; leakage flags must be issued in the same form to all compatible leakage-aware decoders. Showed in guide interface — `LCDecoder(..., parameters={"weighted": True})` and `decode_batch_to_logical_flip(detectors, leakage)`. Before implementation recheck signature on a recorded SDK version. [LCDecoder API](https://deltakit.riverlane.com/api/docs/_build/generated/deltakit.decode.LCDecoder.html), [official guide](https://deltakit-docs.riverlane.com/en/latest/guide/decoding.html).

If only the service is accepted batch And doesn't change the cause prior between blocks, You can compare accuracy on the same dataset, but it cannot be said that the equivalent streaming controller. SDK installation, server availability and FPGA hardware latency — Three different checks. Cloud batch time Cannot be given for hardware delay LCD.

## Bound active/shadow

On a fixed scheme shadow decoder may evaluate alternative decoder outputs The same story.. He doesn't get online logical truth. Disagreement or high confidence doesn't prove that one decoder Right. For offline Checks need separate train/validation labels or valid model-based estimates with uncertainty assessment.

Shadow Cannot verify otherwise physical mapping or schedule Just by re-coded old events: another scheme would change events and mistakes. New simulations required/valid counterfactual model or separate hardware trials. Promotion threshold, replay budget, rollback and maintenance Pauli frame must be determined before on the ground deployment. This is a future research work, a non-enforceable guarantee.

## Decision after audit

1. Do not duplicate adaptive MWPM, decoder ensemble or total telemetry-driven controller under the statement of a new basic idea.
2. Save them as mandatory competitors/components, with honest reproduction names.
3. First, conduct the described limited test of joint management and independent combination.
4. Only a positive, sustainable outcome justifies further development cross-layer coordination. He doesn't prove his ability to work mapping/scheduling or continuous QPU control.
5. No wins, numerical LER or latency ORCHESTRA No such document is declared.
