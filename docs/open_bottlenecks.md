# ORCHESTRA: bottlenecks remaining after strong QEC methods

Audit date: 4 October 2026. This builds on the 34 method records in
[prior_art.md](prior_art.md), with additional checks of qLDPC, logical operations,
magic states, and two-dimensional code limits. Literature, theorem, simulation,
and hardware experiment are different evidence levels; this is not my benchmark.

**Conclusion:** strong decoders and adaptive control remove particular costs,
but do not by themselves guarantee inexpensive execution of a long quantum
program. Physical errors, connectivity, logical-operation reliability, reaction
time, hardware resources, and evidence for extremely rare failures remain joint
constraints. Adding AI above the QEC stack does not bypass them.

ORCHESTRA is a research testbed. A **10% LER** improvement can be a useful
intermediate result, not proof of a major advance toward **200+ useful logical
qubits**. This document does not start implementation. STITCH is outside this
workspace and has not been changed. Software headroom, the reference workload,
and permitted representation changes are examined in
[software_headroom.md](software_headroom.md).


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## 1. What exactly is a limitation??

FTQC — Failure-safe quantum calculation: The system protects information during storage and during operations. LER — The probability of a logical error; it is always designed to be specified, for one cycle, experiment, code block or operation..

Short dictionary for reading of the:

- **Syndrome / detectors:** The results of the tests that are looking for traces of errors; this is not a list of errors themselves..
- **Code Distance d:** minimum number of errors in physical cubes that may result in a non-observed logical error. In the actual scheme, error of operations and measurements is also important.
- **Encoding rate:** How many logical qubits are stored on one physical cube of data; auxiliary cubes need to be counted separately.
- **Ancillas:** Auxiliaries for inspection and operations. **Patch / Patch:** Section of the coded cube device.
- **Herald:** measured signal of a certain type of error, e.g. leakage from operating cube levels.
- **Throughput:** How much data is processed per second. **Latency / reaction:** How long do I wait for the answer?.
- **Floor:** residual level of error which does not decrease in the mode expected or other appropriate. **Surrogate:** a convenient measurable indicator instead of a direct target error.
- **Compute:** Classical calculations, e.g. CPU/GPU. More compute — Not the same as more or more than quantum cubes.

| Type | Value | What it takes to get over it?. |
|---|---|---|
| **Proven under conditions** | There is a mathematical boundary for a particular model | Change model conditions or find design within the remaining range |
| **Lack of information information gap information availability and dissemination of information on the basis** | Different hidden errors look the same in available telemetry | Additional observations, permissible verification or narrower assumptions about noise |
| **Physical/architective** | Communications, measurements, time, spares; errors have already damaged condition | Change device, code or physical protocol compute might help you pick a choice |
| **Computation / Engineering** | Shortfall of speed, memory, power or good implementation | Optimization and additional resources can help; their cost must be taken into account |
| **Boundary of evidence of the case** | Outside published test, unknown | New measurements or simulations with uncertainty control |

Last line **does not mean impossible**. For example, "not shown 200 parallel decoded patches" is not equal to "the method cannot work at" a certain number of and a certain degree of pressure 200 The patches». And mathematical asymptotics don't charge a particular machine without a constant and a hardware model..

In the cards below «compute does not correct" means: **simple increase in classical computations with the same code, physical actions and accessible information and information** does not remove the problem. Compute It can still help to develop another schedule, code or device.

## 2. Why? «200 logical qubits" is still not a complete target

At least: number of logical qubits working, program and depth, probability of failure, time of execution, physical platform and resource constraints by the user.. Memory on 200 Cubes, short post-selective experiment and universal machine 200 Cubes — Different Results.

### Figure 1 - Error budget

Let's say **For example only**: 200 logical qubits must be stored a million cycles and memory errors are selected 1% Failure probability. It's working. 200 Millions of opportunities for error. A sufficient conservative condition for combining events:

\[
P(\text{At least one memory failure.})\leq\sum_i P(E_i),\qquad
p_{\rm memory}\leq\frac{0.01}{200\cdot10^6}=5\cdot10^{-11}.
\]

This is **My calculation**, not required by what-or a specific article. This upper limit does not require the independence of events. This is a sufficient condition, not a necessary one; it may be inaccurate when correlates. The frequency of the change in logical parity that is taken from memory shots, Also not automatically equal to the probability of any harmful event in the program. Operations, state preparation and measurement spend parts of the budget and the need for a more efficient and effective system. for the future. For another depth, you'll get another target.. LER.

### Why Wins 10% Not necessarily saving the cubes.

Take a condition model below the threshold: the extension of the code distance 2 reduces LER in \(\Lambda\) once. If decoder improvement is only a constant multiplier 0.9, equivalent change in distance:

\[
\Delta d=\frac{2\ln(1/0.9)}{\ln\Lambda}.
\]

Prin **conditional** \(\Lambda=2\) That's about 0.30. Real permissible distances in a family can be a step 2; Then the required distance will not change at all the distance required. If the system is near the next distance selection line, even 10% can help you move to a smaller code. If the method changes the suppression coefficient itself, the effect can be significantly greater. Therefore, the same resource value of any "minus" cannot be declared 10% LER».

For rotated surface-code memory with individual measuring cubes used \(2d^2-1\) physical cubes per patch. For **chosen at random** d=25 and 200 The patch is. 249 800 Cubes only for memory. This is not an assessment of the right d for example above. It does not contain routerization, operations, state factories and reserves. The patch formula is given, for example, in [work LCD, II.1](https://arxiv.org/html/2411.10343v2).

**Useful System Meteric:** Minimum cost of a given programme with a defined probability of success. Count physical cubes, time, cube-seconds, classical resources, communications and energy consumption; not conceal them in one arbitrary score. Decoder reports keep all mandatory metrics from [of the Protocol](benchmark_protocol.md).

## 3. Four key examples

### AlphaQubit 2: Why can't you just increase the code??

Full AQ2 Shows surface-code LER Near \(7.3\cdot10^{-11}\) as at d=23 in **simulations SI1000, p=0.15%, 120 Cycles**. Full version on d=23 process about one cycle per 30 μm. Option AQ2-RT reaches throughput <1 μs/cycle before d=11 surface and d=9 colour. At d=23 RT-The alternative is faster, but the authors explicitly note that there is insufficient precision.. These are different modes of accuracy and speed. [AQ2, §3–4 and A.7](https://arxiv.org/html/2512.07737v2)

Hence, "very low" of the "nil" is a LER "The actual time is already shown" cannot be added to the statement that both characteristics are achieved simultaneously on a large code. Spatial attention It connects a lot stabilizer representations; normal total attention Under m The audit is of a square value m. It's an analysis of an operation, not a theory of the impossibility of a more effective neuronet. The increase in the number of patches adds model condition, data transfer and accelerator competition.

More compute can improve learning, inference and parallelism and parallelism. It does not reduce the number of physical errors in a fixed pattern or create missing data on a new noise type. Long series checks and changes in the force of the noise studied are useful but do not prove resistance to any drift, leak and damaged connections by the user.. Also memory decoder does not confirm the validity of the entire logical framework. **Balance of compromise:** Accuracy, reaction and price of accelerators; separate boundary of evidence - large code plus many patches plus full computing workload.

### LCD: what remains after <1 μm

LCD already adapted the graph for heralded leakage. In the article, time of windows of the world. the world's most important features of the world's world. on d×d×d divided by d; So the meth is received <1 μs/Rund to d=17. Time adaptivity engine was not measured, but streaming latency identified as further work on the ground. FPGA routing Limiting frequency at size growth. The case study is a flexible version — unweighted; Adding weights requires resources. [LCD, II.2–III and IV](https://arxiv.org/html/2411.10343v2)

The main system limitation remains with the perfect throughput: The physical dimensions, their reliability, the transmission of the result and, where necessary, the conditional effect need to be measured... Herald must actually detect the leak and arrive in time; the decoder does not make the signal perfect. Classic acceleration does not replace missing acceleration herald and does not restore the arbitrary condition already lost.

Expenditure FPGA under one patch is not equal to the cost of the entire machine. Cannot linearly multiply published percentage LUT as at 200 and get ready configuration: check location, memory, input-output, simultaneous load and reserve. It's an engineering question, not a proven ban. **Balance of compromise:** Accuracy and universality of adaptation against resources; then physical cycles and end-to-end reaction become the next limitation.

### qLDPC: Why good? overhead The memory doesn't automatically give you cheap 200 qubits

qLDPC — code family with diluted checks; it is not one code or decoder. Good families can have tall. encoding rate. Sparse graph does not mean short geometric links on a two-dimensional chip.

B BB-Example [[144,12,12]] data and check qubits Give 288 physical cubes to remember 12 logical. Research requires a certain amount of connectivity, including long-distance communications and considering their implementation. Simple repetition 17 blocks give **arithmetic** 204 logical / 4896 physical memory cubes, but does not prove target reliability, transaction performance and the ability to build such a device. You can't compare this number with surface-code number at another LER and workload. [BB memory, Fig. 1 and hardware requirements](https://arxiv.org/html/2308.07915)

High rate One end code also does not guarantee that the family will maintain the same family if the required distance is increased. rate. You can't take the asymptotics of the good ones.. qLDPC-families on any particular BB-code. For example, Tour de gross separate discussion of a family with a fixed number of logical qubits and its two-dimensional limit, rather than adopting the same scaling All qLDPC. [Tour de gross, §5](https://arxiv.org/html/2506.03094)

There are already serious computational schemes: [gauging logical operators](https://arxiv.org/html/2410.02213), [High-Rate Surgery](https://arxiv.org/abs/2510.08523), as well as recent theoretical improvements [September 2026](https://arxiv.org/abs/2609.26973). Therefore, the claim «qLDPC "Career" is obsolete. But the result is sparse gadget and its asymptotics do not automatically confirm low hardware constants, convenient positioning and the cost of arbitrary software.

A very illustrative example — **Tour de gross**: Full modular project with instructions, compilation and resource assessment and a high-level project with guidelines. The authors estimate about as little as physical cubes as possible, but more than as much as the time of implementation relative to the review. the number of cubes. the number of cubes.. surface-code architectures; reducing runtime overhead is one of their open problems. It's the result of a specific comparison, not the property of all qLDPC. [Tour de gross, §4–5](https://arxiv.org/html/2506.03094)

More classical of the same compute doesn't create quality long-distance couplers, does not correct transport errors or accelerate a specified physical operation. For atom arrays The re-seat of the atoms can achieve the necessary connectivity, but its cost is part of the physical protocol. [Reconfigurable atom arrays](https://arxiv.org/html/2308.08648)

**Balance of compromise:** close storage against the cost of communication, the transaction, measurement, decoding and the delivery of the computational resources. Strong new schemes reduce this price; question: does the final device and the selected programme still have savings with full budget errors?.

### Google RL control: Why Adaptation Doesn't FTQC

Work already connects physical management with decoder steering. Her. supplement Notes: Physical management uses surrogate from detector rates, a decoder steering — evaluation LER, which is difficult to scale directly on realtime setting. It is a particular problem of access to the purpose of the training, not lack of an idea cross-layer control. [Google RL, main text and and supplement](https://arxiv.org/html/2511.08493)

The controller can hold good operating parameters. He doesn't make the maximum of himself.. fidelity equal to one, does not eliminate all noise in the environment and does not provide lost connections. Evaluation of response in epochs — not instantaneous correction of one dangerous burst. The "nature" detection events» Nor does it guarantee "smaller logical errors" in all noise models.

Strong controller remains limited to observation, measurement and permissible action. The more parameters and interactions it optimizes, the more important it is the cost of verification and the causal evaluation of the result. **Balance of compromise:** Response speed, statistical certainty and price of change; working calibration does not replace code overhead, Programme logical operations and resource budget.

## 4. General restrictions not belonging to the same decoder

### 4.1. Information limit for decode

With a fixed scheme and accessible information I The best choice of logical class L has a conditional probability of error

\[
r^*(I)=1-\max_L P(L\mid I).
\]

It's a consequence of choosing the most likely class. If several logical classes remain likely after all the observations, even unlimited compute Doesn't. r* Zero. The exact summation of classes is discussed in [BSV](https://arxiv.org/abs/1405.4883); near-optimal recovery and sensitivity to noise description - in [on the work of the local noise](https://arxiv.org/html/2403.08706).

A mistake equivalent to a non-trivial logical operator may not change stabilizer syndrome. So alone detector rates do not identify the arbitrary probability of such errors. It's an exemplar, not a statement that any real noise contains an unknown global operator. Parameter-recovery methods may exist for a restricted class of local noise; that class must be stated explicitly. [DEM estimation](https://arxiv.org/html/2504.14643)

**Investigation for the platform:** First, measure how much of the loss is caused by a failed decoder, which is the wrong model, and which remains even at the exact end of the equation.. decoder in the same model. True-rate Oracle PyMatching shows only the benefits of perfect weights inside matching; It's not an information limit..

### 4.2. Locality and number of physical cubes

For 2D codes with geometrically local switch checks and the limits in the theorem are fulfilled \(kd^2=O(n)\). Here. k — Number of logical qubits, n — physical, d — distance. The constant depends on the locality and size of the local state space. It's the real border that the best matching or RL-The controller doesn't cancel. [Bravyi–Poulin–Terhal](https://arxiv.org/abs/0909.5200)

You can't apply it without conditions to everyone qLDPC, subsystem, dynamic or non-local design. A way out of the baseline could be cost-effective, but then the price of a new link and protocol should be considered. BPT — The code boundary in the model, not the exact price floor of any FTQC-machine.

### 4.3. Rapid adaptation against statistics of the statistical system

The already known adaptive methods are limited to the rate of information accumulation, not just the time of the optimist. [Spitz et al.](https://arxiv.org/abs/1712.02360), [Bhardwaj et al.](https://arxiv.org/html/2511.09491)

For W independent Bernoulli-rare event with probability of p relative standard error of estimate \(1/\sqrt{Wp}\). Like when p=0.001 for a relative standard error 10% About required 100 000 Effective observation **one parameter estimated**. This is an analytical illustration, not measured time of a particular estimator. The sharing of detectors helps in the overall noise structure; correlations reduce the effective number of independent data..

Long window reduces the noise of the grade, but lags behind the drift. Short is faster to react, but wrong more often. Compute Helps process statistics; it does not measure the past state of the device. Stranger burst Could damage the condition before a reliable estimate comes up. If an early physical signal exists, its use changes this task — that's why heralded leakage important.

### 4.4. Rare and correlate physical failures

Willow-The research found rare correlated bursts, Limitations **repetition-code** Results: approximately one event per hour in the device studied. It's not a universal frequency and it's not proven floor Any surface/qLDPC code. But the example shows why extrapolating independent noise can miss a significant part of the failure. [Willow, ultralow-error repetition memory](https://www.nature.com/articles/s41586-024-08449-y)

A perfect decoder can use footprints burst, where sufficient information is stored. It cannot guarantee recovery from arbitrary damage that exceeds the protection of the code. Physical suppression, early detection, additional protection or acceptable recovery required. Q3DE and Surf-Deformer Some of these measures are already under consideration; delays in detection and final reserves remain..

### 4.5. Throughput, latency and physical reaction times

Throughput Answers the question: "About the flow?». Latency — «When the answer is ready?». The final result may be required before the next conditional logical operation. Windows and batching Increase throughput, But waiting for a window can slow down the reaction. Documents [LCD](https://arxiv.org/html/2411.10343v2) and [AQ2](https://arxiv.org/html/2512.07737v2) The same concepts.

Memory c Pauli frame does not require immediate physical correction by everyone syndrome. Required deadline Depends on subsequent action; rule "any". decoder "Observation for one physical cycle" is too harsh. At the same time, the average throughput does not prove compliance deadline for feedforward.

For 200 Patch d=25, one binary stabilizer outcome for cycle and cycle verification 1 μm **Unpackaged** The flow is \(200(25^2-1)/10^{-6}\approx1.25\cdot10^{11}\) Bit/s, about 125 Gbit/s. This is my imputed estimate; no soft readout, metadata and other transactions of the data on. Compressive and local processing can reduce transfer. Flow size does not prove impossible, but does input-conclusion part of the study.

The final response time includes measurement, delivery, line, decode, update frame and conditional enforcement. Accelerating one kernel does not reduce all other parts. Check p99 violations deadline when the load is mixed, not just the time of the empty GPU kernel.

### 4.6. Memory, logical operations and magic states

The program requires operations between protected cubes. Code distortion, lattice surgery, operations qLDPC and other permissible schemes spend space, time and their budgets on errors. Cost depends on the code and platform; rule cannot be universally passed O(d) One cycle surgery-protocol on all architectures. [Gauging](https://arxiv.org/html/2410.02213), [High-Rate Surgery](https://arxiv.org/abs/2510.08523), [Tour de gross](https://arxiv.org/html/2506.03094)

In architectures with resource injection for non-Clifford Operations need to be sufficiently clean magic states and their timely delivery. You can't automatically count old giants factories the need to remain: **magic state cultivation** The cost of the treatment reviewed has already significantly decreased. But they stay postselection/retries, Transport to large security code, storage, feedback and production speed. The job itself has seen a rapid increase in post-cation costs, with a desire for greater fault distances. [Cultivation](https://arxiv.org/html/2409.17595), [copyright code](https://github.com/Strilanc/magic-state-cultivation)

Not all approaches are required to use the same factories; There are other ways to implement non-Clifford operations. The right question is, how much is it??. **selected universal set of operations** with the accuracy given, including preparation and delivery of resources, not only 200 Memory sites.

### 4.7. Checking order errors 10⁻¹⁰

Zero mistakes in N Independent tests give an approximate 95%-Upper boundary 3/N the probability of error for the test. That's the limit 5×10⁻¹¹, About required 6×10¹⁰ Test. This is binomial-calculation, not mandatory number of normal Monte Carlo shots for each study. If tests and drifts are dependent, a simple formula is not applicable the test.

Importance sampling and other methods of rare events can dramatically reduce the cost of verification **in the specified model**, if the weight is correctly taken into account, support and uncertainty. A large simulation does not prove the model of the device correctly. Quick search for the best schedule Inaccuracy scoring can also choose statistical noise instead of improvement. AQ2, FastSched and work with the tensor networks show different ways to work with this price; none exempts from physical noise compliance checks.

### 4.8. Causal valuation and final reserve

Shadow decoder can honestly compare different decoders on the same stream. Shadow mapping/scheduling controller Doesn't see what syndrome would have happened after **other physical circuit**. Separate experiments or proven model of counter-acting are needed. Existing CaliQEC, ReloQate, Q3DE and Surf-Deformer includes physical changes; free replacement of indices does not reproduce.

Moving takes a healthy place, a way, and a time; calibration takes part of the resource out of normal mode; the extension takes place in adjacent cells. If damage covers all the spare areas, choosing the best of them is not the solution. It is a conditional limitation on available resources, not a statement that remapping useless.

## 5. All 34 of the method: what remains after each

The numbers match [prior_art.md](prior_art.md). «Price" below is the reason the result of the method is not yet a cost-effective one FTQC. That's not a rating LER: number of different models not compared. For implementation availability, noise published by the performance see. Basic cards.

### 01. Static / Oracle / Correlated PyMatching

- **Scale:** MWPM Decides matching-The problem; correlations and amounts of probabilities of different equivalent errors are only partially presented by this model.
- **Price:** best choice in matching may still be different from the most likely logical class; large code and physical operations a certain degree of speed-I'm still needed...
- **Compute Doesn't fix it.:** Lack of distinguishable observations and insufficient physical protection. True-rate Oracle improves priors, Not knowing the error that was realized.
- **Compromise:** speed and compact graph against completeness noise model / decoding objective. [PyMatching API and source](https://github.com/oscarhiggott/PyMatching/blob/master/src/pymatching/matching.py)

### 02. Local Clustering Decoder

- **Scale:** FPGA placement/routing, resources and the relationship between processing elements; Multi-pat load requires separate verification.
- **Price:** Fast clustering does not cancel the hardware cycles and the price of protected transactions.
- **Compute Doesn't fix it.:** missing or late heralds Arbitrary loss of logical information.
- **Compromise:** leakage-aware accuracy / weights / flexibility against resources and reactions. Details of the time measured cm. §3, Not count <1 mx full QPU round trip. [LCD](https://arxiv.org/html/2411.10343v2)

### 03. Deltakit And the cloud LCD/CC

- **Scale:** Access to cloud service, limits, limits and other measures. and/or and/or other measures. for the public to use of cloud service API and compatibility of circuits/telemetry - practical limitations of reproducibility.
- **Price:** batch cloud comparison Doesn't confirm a cheap built-in realtime system.
- **Compute Doesn't fix it.:** Lack of local proprietary hardware implementation or inaccessible entry for a particular scheme; no more client resources open closed interface.
- **Compromise:** convenience of the official API against the control of implementation and end-to-end latency. It's a restriction on access, not a physical limit LCD. [LCDecoder](https://deltakit.riverlane.com/api/docs/_build/generated/deltakit.decode.LCDecoder.html), [authentication](https://deltakit-docs.riverlane.com/en/stable/guide/authentication.html)

### 04. Collision Clustering

- **Scale:** The consistent separation of hardware resources saves the future of the system logic, But growth clusters and data increases work.
- **Price:** Quick decision clustering not equivalent ML and does not remove the remaining costs FTQC.
- **Compute Doesn't fix it.:** Information limits syndrome and physical noise. ASIC timing estimates Not equal to the measurement of the complete machine.
- **Compromise:** Equipment area, time and accuracy; rare, complex syndromes important for deadlines. [CC](https://arxiv.org/html/2309.05558)

### 05. AlphaQubit 1

- **Scale:** Training, recurrent state and spatial mixing; original version does not reach the required superconducting throughput.
- **Price:** Strong accuracy requires learning resources/inference And doesn't provide logical transactions.
- **Compute Doesn't fix it.:** Incorrect noise class and lack of information. More training samples one distribution does not guarantee transfer to another.
- **Compromise:** Rich soft/leakage inputs and accuracy against model speed/access. AQ2 The border is already making significant progress; shortcomings AQ1 You can't attribute the whole neural area. [AQ1](https://arxiv.org/html/2310.05900)

### 06. AlphaQubit 2 / AQ2-RT

- **Scale:** inference and teaching of the big patches, spatial attention and parallel flows.
- **Price:** large low error full-The alternative and the small fast RT-The alternative takes up different points of compromise.
- **Compute Doesn't fix it.:** physical noise, invisible logical events and unconfirmed model of the device.
- **Compromise:** accuracy / throughput / reaction / accelerator cost; detailed checked bounds are in §3. Open audit scaling does not constitute proven impossibility. [AQ2](https://arxiv.org/html/2512.07737v2)

### 07. BeliefMatching

- **Scale:** belief propagation with cycles and additional on the cycle box matching passes; depends on the number of iterations.
- **Price:** Improved processing circuit correlations does not provide a general guarantee of precision logical ML.
- **Compute Doesn't fix it.:** unidentifiable noise and information missing from the graph. More BP-Iterations do not guarantee the correct resemblance to loopy graph.
- **Compromise:** iteration budget, accuracy and latency tails; selected BP schedule is important. [Work](https://arxiv.org/abs/2203.04948), [code](https://github.com/oscarhiggott/BeliefMatching)

### 08. Tesseract

- **Scale:** A*-Searching for the high-value, difficult syndromes; The search restriction changes accuracy.
- **Price:** near-optimal the results may cost too much time or resources for the given flow.
- **Compute Doesn't fix it.:** The distinction "the most likely fault set» and "amount of probability logical class», and physical uncertainty.
- **Compromise:** depth/wide of search versus latency, especially tail; malfunctions should be measured when budget is exhausted. [Work](https://arxiv.org/html/2503.10988), [code](https://github.com/quantumlib/tesseract-decoder)

### 09. Spitz: adaptive weight estimator

- **Scale:** sufficient statistics local rates shall accumulate faster than a significant drift.
- **Price:** Good prior does not replace the large code distance and full-scale operations.
- **Compute Doesn't fix it.:** unknown parameters indistinguishable by available syndrome correlations; future measurements cannot be obtained in advance.
- **Compromise:** window length versus reaction speed and dispersion weights. [Spitz et al.](https://arxiv.org/abs/1712.02360)

### 10. DGR

- **Scale:** tracking decoder edges and co-occurrences requires data/memorials; errors of the original decoder impact on evaluations.
- **Price:** reweighting and additional passageways cost resources, while the gains over mismatched prior does not prove the winnings over a strong adaptive method.
- **Compute Doesn't fix it.:** The uncertainty of the hidden faults Under decoder output. The wrong decisions themselves can be polluting feedback.
- **Compromise:** Details correlations, sample window and the cost of adaptation. [DGR](https://arxiv.org/html/2311.16214v3)

### 11. Adaptive Estimation of Drifting Noise

- **Scale:** multi-speed drift requires suitable windows and sufficient observations on parameters.
- **Price:** approach true-model decoding does not reduce a physical error per se.
- **Compute Doesn't fix it.:** Statistical delay and noise emission per identifiable model.
- **Compromise:** tracking bandwidth against accuracy of the estimate; drift profiles Does not guarantee any abrupt change. [Bhardwaj et al.](https://arxiv.org/html/2511.09491)

### 12. DEM estimation — Blume-Kohout / Young

- **Scale:** full model for detector parities road; sparse/aggregate submissions limit the number of parameters.
- **Price:** The evaluated probability model has yet to be decoded and confirmed on the device.
- **Compute Doesn't fix it.:** The same observed signatures mechanisms And the invisible logical-only faults without additional preconditions on the ground.
- **Compromise:** wealth model support, identifiability and sample cost. [Work](https://arxiv.org/html/2504.14643)

### 13. Logical error estimation from syndrome data — Takou et al.

- **Scale:** Acquainted support reference model remains a prerequisite; rates may be evaluated without supervised logical labels.
- **Price:** improved prior Doesn't confirm anything small LER and doesn't solve the whole program.
- **Compute Doesn't fix it.:** no new fault mechanism in the model; fitting known rates does not equal discovery All errors.
- **Compromise:** sample cost and model assumptions against convenience syndrome-only estimates. [Work](https://arxiv.org/html/2606.11496v2)

### 14. In-situ calibration — Kelly et al.

- **Scale:** local calibration requires measurements and accessible physical knobs; Some parameters interact.
- **Price:** retention of the optimum operating point does not intrinsic noise zero.
- **Compute Doesn't fix it.:** hardware fidelity floor and actions the device does not support.
- **Compromise:** calibration exploration, noise and speed drift tracking. Demonstration at repetition code is not equal to the guarantee of full FTQC. [Kelly et al.](https://arxiv.org/abs/1603.03082)

### 15. Google RL control

- **Scale:** greater controls and interactions, surrogate reliability, Cost of collection reward.
- **Price:** A stabilized device still requires codes, operations and hardware budget.
- **Compute Doesn't fix it.:** missing online logical truth, Physical limitations and damage before reaction.
- **Compromise:** detection surrogate v. Real logical objective; decoder steering c LER estimates has a separate scaling problem. More detailed §3. [Google RL](https://arxiv.org/html/2511.08493)

### 16. Provably Efficient Self-Calibrating Quantum Fault Tolerance

- **Scale:** The guarantee is based on a given class control-induced noise properties objective, including local optimization conditions.
- **Price:** effective convergence does not mean zero samples, infrastructure and physical errors.
- **Compute Doesn't fix it.:** Violation of the theorem preconditions. Surrogate not universal certificate LER against Arbitrary Detention actions.
- **Compromise:** the force of the guarantee against the latitude of the noise/control models; distance-independent convergence not equal to the constant totals of the machine. [Preprint](https://arxiv.org/html/2608.05686)

### 17. Neural ensemble decoder selection

- **Scale:** Learning to choose requires information on what decoder was right; the cost of the band is rising with the candidates.
- **Price:** selector only useful for complementary errors available decoders.
- **Compute Doesn't fix it.:** a situation where all candidates make the same mistakes; no online truth Only because there are their answers...
- **Compromise:** Decision price / additional launch against gain selection. [Neural ensemble](https://arxiv.org/abs/1905.02345)

### 18. Harmony / harmonization

- **Scale:** Many perturbed matching runs; Complex syndromes They need more ensemble budget.
- **Price:** confidence and accuracy may be improved at the cost of cumulative work or tail latency.
- **Compute Doesn't fix it.:** A certain general error caused by a wrong model or a common blind zone.
- **Compromise:** agreement / Early stop against rare errors; consensus You have to calibrate, not count as proof correctness. [Harmony](https://arxiv.org/html/2401.12434)

### 19. Libra / matching synthesis

- **Scale:** ensemble solutions and synthesis of improved on the ground corrections Work; approximated search is not general exact-ML guarantee.
- **Price:** Increase error suppression should be evaluated at the required distance, operations and or a certain degree of severity. on the ground compute.
- **Compute Doesn't fix it.:** Information ceiling or systematically incorrect noise model.
- **Compromise:** synthesis budget against accuracy and time; private success does not justify independent multipliers of benefits from others decoders. [Libra](https://arxiv.org/abs/2408.12135)

### 20. NVIDIA Ising predecoder

- **Scale:** Local neural predecoding plus global global and residual decoding, device transfers and deployment backend.
- **Price:** Local speed stage does not remove rare large or globally mixed errors.
- **Compute Doesn't fix it.:** Insufficient accessible context of a fixed local stage; Enclosure global stage It's already changing architecture and costs.
- **Compromise:** Size/complicity residual against price NN and data communication. Check All Way. [Official repository](https://github.com/NVIDIA/Ising-Decoding), [work](https://arxiv.org/abs/2604.12841)

### 21. QAdapt

- **Scale:** continual learning should maintain past regimes and respond to new ones with limited memory and data.
- **Price:** sustainability in sequences studied tasks does not guarantee the safety of the new drift mechanism.
- **Compute Doesn't fix it.:** indistinguishable by selected telemetry and missing labels.
- **Compromise:** plasticity v. forgetting, updates v. runtime budget; pilot CPU latency does not replace the complete hardware path. [QAdapt](https://arxiv.org/html/2607.28422), [inference artifacts](https://huggingface.co/Qhub-AI/QAdapt)

### 22. Adaptive Syndrome Extraction

- **Scale:** allowed specific fault-tolerant adaptive gadgets c flags and feedback.
- **Price:** savings checks/gates may require additional stages, ancillas and reactions.
- **Compute Doesn't fix it.:** non-removable lifting of checks where errors no longer observed or distributed without control.
- **Compromise:** Measurement against protection and on the ground latency; proven design in one code family not automatically reset. [Work](https://arxiv.org/html/2502.14835), [code](https://github.com/noahberthusen/adaptive_qec)

### 23. AlphaSyndrome

- **Scale:** space allowed gate schedules, dependence and expensive noisy scoring.
- **Price:** offline The best scheme is still being executed on a real device with gate/measurement errors.
- **Compute Doesn't fix it.:** Physical conflicts of the links used and the results that cannot be obtained without the proper measurement.
- **Compromise:** depth, idle errors and hook-error propagation; less than circuit depth not always means less LER. [Work](https://arxiv.org/html/2601.12509v2), [code](https://github.com/acasta-yhliu/asyndrome)

### 24. FastSched

- **Scale:** RL schedule search and assessment of rare logical failures; importance sampling only works when the model/weight is correct.
- **Price:** A strong win at a certain point of the right to be a member of the public extraction benchmark does not demonstrate acceleration of the long program.
- **Compute Doesn't fix it.:** mismatch between scoring model and the device; ideal boundaries / one noisy round doesn't represent all repeated computation.
- **Compromise:** price/fidelity: of the goods scoring C. Anti-search scope; separate check of the re-cycle transfer of the detected diagram. [Preprint](https://arxiv.org/html/2609.12020)

### 25. CaliQEC

- **Scale:** protected calibration requires space, isolation/enlargement and Harmonization with the logical workload.
- **Price:** additional geometry and calibration time spend resources even if large ones are prevented. drift loss.
- **Compute Doesn't fix it.:** insufficient physical stock and minimum duration to be given calibration protocol.
- **Compromise:** Frequency of calibration versus cube availability, additional noise exposure and programme time. [ISCA paper](https://cseweb.ucsd.edu/~tullsen/isca_caliqec.pdf)

### 26. ReloQate

- **Scale:** detector-fire-rate predictor must be carried to real species drift; I need healthy ones.. spare tiles routes.
- **Price:** relocation, recalibration and reserve geometry with value.
- **Compute Doesn't fix it.:** No healthy place; DFR does not define arbitrary logical risk Absolutely..
- **Compromise:** early safety remap v. false alarms and reserve consumption; correctness fitted risk bound Outside the trained scenarios, requires verification. [ReloQate](https://arxiv.org/html/2603.00837v2)

### 27. Q3DE

- **Scale:** Detection burst, the extension of protection and rollback requires time/space and access to history.
- **Price:** rare accidents can cause large reserves or delay the program and the public and the public..
- **Compute Doesn't fix it.:** damage that has already destroyed the visible logical information, or burst, over existing reserve.
- **Compromise:** sensitivity detector v. false positives, detection delay value recovery. Correlated malfunctions require system metrics, not just average LER. [Q3DE](https://arxiv.org/html/2501.00331)

### 28. Surf-Deformer

- **Scale:** permissible geometry around defects, distance preservation and conflicts of neighbouring countries and the conflicts between patches.
- **Price:** Defects and Defects on the ground enlargement They can eat routing capacity, additional cubicles and time of operations.
- **Compute Doesn't fix it.:** Lack of physically protected position on the damaged device.
- **Compromise:** utilisation and density protection and ability to carry out operations; improved layout Doesn't guarantee unlimited defect tolerance. [Surf-Deformer](https://arxiv.org/html/2405.06941v3)

### 29. Hardware-aware QED compilation

- **Scale:** Search mapping/schedule assessment of small and medium-sized noisy circuits; selected work uses detection/postselection.
- **Price:** High condition fidelity may be accompanied by a low acceptance rate a low-level launch rate.
- **Compute Doesn't fix it.:** Loss of successful start-ups with fixed detection protocol and physical value SWAP/idle.
- **Compromise:** accepted accuracy v. unconditional success / retries / runtime. You can't give up this regime for proven long-term fault-tolerant QEC programme. [Work](https://arxiv.org/abs/2606.07666), [code](https://github.com/Sumitchongder/quantum-hw-aware-pipeline)

### 30. BSV / qecsim tensor networks

- **Scale:** Yes tractable exact cases; The general noise needs expensive contraction either approximation limited bond dimension.
- **Price:** achievement ML in a given model may be too expensive for realtime And still doesn't take off. LER.
- **Compute Doesn't fix it.:** Infidel physical model and syndrome ambiguity.
- **Compromise:** contraction accuracy time/memorials; TN convergence Not automatically certified ceiling. Do Not Declare All BSV cases exponential. [BSV](https://arxiv.org/abs/1405.4883), [qecsim](https://github.com/qecsim/qecsim)

### 31. Tensor Network Decoding Beyond 2D

- **Scale:** circuit noise Creates a more complex spacetime network; width contraction and truncation important.
- **Price:** proximity optimal accuracy may require memory/times that are difficult to scale on many streams and time required by the current system. and the current situation and the current. to be able to scale on many flows.
- **Compute Doesn't fix it.:** physical information limit or missing model factors.
- **Compromise:** quality approximation against resources and the possibility of confirming convergence; large bond budget is not self-evident of accuracy. [Work](https://arxiv.org/html/2310.10722), [code](https://github.com/ChriPiv/tndecoder3d)

### 32. Optimal adaptation to local noise

- **Scale:** recovery is calculated for a given local process description; circuit correlations may lie outside this description.
- **Price:** The best value under the local model doesn't confirm end-to-end Optimum of device.
- **Compute Doesn't fix it.:** Non-observed/unwritten channels and limited physical and knobs.
- **Compromise:** accuracy knowledge of noise against value characterization and recovery; first to understand what parameters really affect LER. [Work](https://arxiv.org/html/2403.08706)

### 33. CUDA-Q QEC TensorNetworkDecoder

- **Scale:** GPU memory, contraction plan, Supported submission decoder problem and transfers.
- **Price:** The accelerator reduces some computational costs; ML Mode doesn't mean cheap ML for any large scheme.
- **Compute Doesn't fix it.:** Wrong Purpose — For example, fault-set likelihood Instead of the appropriate grade amount, and unsupported noise.
- **Compromise:** exactness / Model / size of problem against hardware costs. Before use as ceiling check semantics and selected modes. [Official documentation](https://nvidia.github.io/cudaq-qec/examples_rst/qec/decoders.html)

### 34. Adaptive decoder selection / simple threshold

- **Scale:** learned selection Maybe more expensive tuned threshold; The cost of candidates depends on the actual workload.
- **Price:** gain relative to one fixed decoder doesn't mean the benefit of a relatively heavy cheap selector.
- **Compute Doesn't fix it.:** Lack of useful additional information and recruitment of candidates with the same mistakes.
- **Compromise:** sophistication policy cost and carrying capacity. Limited output author preprint — useful control, Not the theory of uselessness neural selection. [Authored record](https://zenodo.org/records/21466148)

## 6. Supplements to the original. 34 work

| Technology/source | Which is already filming | What remains | Status of the border |
|---|---|---|---|
| [BB qLDPC memory](https://arxiv.org/html/2308.07915) | Large overhead in the examples examined | Connectivity, finite-size logical risk, Operations and manufacturing | Simulation/hardware project; not prohibited |
| [Reconfigurable atom arrays](https://arxiv.org/html/2308.08648) | Feasibility of realizing non-local sparse connectivity displacement | Time/quality transport, operations, finite constants | Physical background and design |
| [Localized Statistics Decoding — LSD](https://www.nature.com/articles/s41467-025-63214-7) | Global price matrix elimination in BP+OSD, especially in small clusters | Largest-cluster work, number BP iterations, accuracy And the load of the evil noise | Algorithmic compromise; not all qLDPC decoders ♪ Just as slow ♪ ♪ |
| [Gauging logical operators](https://arxiv.org/html/2410.02213) | Too expensive some of the previous measurement gadgets | Ancillas, connectivity and implementation of a specific logical framework and execution | Improved proven design; hardware price to be treated separately |
| [High-Rate Surgery](https://arxiv.org/abs/2510.08523) | Low capacity of target logical measurements | Implementation auxiliary graph and value of specific workload | Design and numerical examples; not finished universal machine |
| [Near-optimal high-rate surgery](https://arxiv.org/abs/2609.26973) | Theoretical size of the world sparse measurement gadgets | Constants, noise, schedule and hardware | Fresh theoretical preprint; checked abstract, Not reproduced all proof |
| [Tour de gross](https://arxiv.org/html/2506.03094) | No related programming/resource model for BB | Space–time tradeoff, Inter-moduular operations and equipment. and equipment and equipment. and and | Full architectural analysis and simulation, not deployed machine |
| [Magic state cultivation](https://arxiv.org/html/2409.17595) | Part of the high price of quality T states | Retry/acceptance, escape, storage, throughput and noise assumptions | Specific schemes/stimulations; not universal price of all non-Clifford gates |
| [Willow below threshold](https://www.nature.com/articles/s41586-024-08449-y) | Experimental demonstration of the suppression of the growth error surface code | Long workload, many logical qubits, rare correlated faults | Experiment; repetition-code floor not to be universally tolerated |
| [BPT bound](https://arxiv.org/abs/0909.5200) | Explains the limit encoding at geometric location | For improvement asymptotics You have to get out of the way, then pay for the new architecture | Proven boundary only in the model |

For LSD Local, and so on factorization, which reduces the price relative to global OSD. Therefore, «qLDPC Mandatoryly requires cubic full-matrix decoding each cycle» wrong. But the benefits depend on the cluster statistics and available parallelism; The average time on a low independent noise does not certify deadlines to burst. [LSD, algorithm / complexity](https://www.nature.com/articles/s41467-025-63214-7)

## 7. What limitations are more important to verify for my purpose

This is **verification procedures**, Not a list of new untested inventions. No item per se is declared a free area without prior art.

| Question | Why Important of the world 200+ qubits | What should be measured | Which will deny the importance of my own workload |
|---|---|---|---|
| How many mistakes remain even with the best compatible decoder? | Shows the limit of purely software improvements decoding | Static, Oracle, strong adaptive/neural and exact/near-optimal subset on one model | My journey is close reference, a resource target remains unattainable: seek an existing rather than a new decoder |
| Whether the benefits are still available code family during calculation of the data? | Memory overhead may not coincide with compute overhead | One programme, the same failure budget; qubits/time/connectivity/factories/ancillas | Memory wins disappear after surgery or requires unreachable connections |
| Are rare physical dominant bursts? | They can destroy independent extraction | Long hardware traces / Audited burst model; frequency, size, logical damage, detection delay | In the selected device and horizon Their ultimate assessment is a neglected contribution |
| Can I learn before noise changes??..? | Too slow an evaluation makes adaptive useless at a dangerous moment | Effective sample rate, response time, uncertainty, faults during reaction | Tuned Simple estimator Reaction is fast enough; complex coordination does not generate resource benefits |
| Which limits reaction With many patches? | A quick single kernel doesn't guarantee a quick core feedforward | Combined load, dataflow, p99, deadline violations, classical power | Decoder It's already a small part of the world. critical path; His acceleration does not accelerate the program |
| Is there a reserve for calibration / remapping / deformation? | Adaptation spends space and time | Reserve, probability of simultaneous damage, transport/recalibration costs | The best. fixed allocation Gives the same reliability cheaper or the supply too expensive |
| Whether the real purpose of management is being tested the target of the management the actual purpose? | Surrogate can improve without improving the programme | Separate validation, errors predictions, actions with cause assessment | For this action/noise class surrogate - It's already accurate enough; controller No need. |

## 8. How to distinguish useful improvement from architectural leap

Old H1 c 10%-Reduction LER still possible **quality test of individual components**, Not the main objective of the project. Victory only over static PyMatching Not considered a success. The loss of a relatively strong competition must be clearly identified.

For a big step to the cheap one. FTQC The results are needed on a pre-defined software and hardware model failure budget a significant decrease in full resources or a substantial increase in reliable transactions with the same resources a significant increase in the number of transactions performed. How much improvement is enough, I have to figure out before the experiment; here is the arbitrary figure.: «breakthrough» not appointed.

Check multiple sizes and different realistic modes to distinguish a constant multiplier from a change scaling or error suppression. Show full interlayer transport price: e.g. less data qubits at the expense of a large number links, less than LER at the expense of the huge accelerator pool or less gates On long-term feedback may be reasonable solutions, but not free savings.

You can't multiply the best winnings of the various articles baseline, noise, hardware preconditions and already accounted for optimizations may cross. Comparison qLDPC and surface should be responsible for one programme task, and decoder comparison — use compatible, identical on the same side circuits/datasets, As required [benchmark protocol](benchmark_protocol.md).

## 9. Decision before next job

1. **ORCHESTRA Leave the research platform.** Do not make a new appearance telemetry, weights, selection or general fast/slow hierarchy.
2. **Do not choose architecture from a list of familiar functions.** First select a specific limitation, show its contribution to the cost of the calculated calculation and verify the strongest available solution.
3. **Do not make the lack of publication proof of newness.** The new mechanism will require a separate, targeted audit, including work outside these 34 cards.
4. **Do not start implementation under this task.** A map of limitations has been prepared... It does not prove the existence of a fundamental mechanism found.

The most meaningful challenge for the platform now is to share four causes of loss: **not ideal decoding, Lack of noise information, physical/code limitations and cost of logical calculation**. Then you can see where the new mechanism can really change the resource picture and where it can only improve the already good component.

Simple explanation: First, understand where the system loses credibility and resources. If the state is already broken by a non-observed error, smarter decoder He won't return it.. If decoder It's almost optimal, it's better to investigate a physical protocol or a transaction. If the main time is spent on communication and measurement, acceleration of neurosnet can only change the program time slightly.

## 10. The limits of this document

- All 34 The original audit cards are presented in §5. New sources are given in of the country §6 and related sections.
- Analysis is not an exhaustive review of all QEC-architecture, bosonic codes, erasure-based devices, photonics or all qLDPC families. It does not set the absolute lower price limit FTQC.
- The published indicators are context-specific. There's no inter-line decoder rating and no one's here. LER/latency measurements.
- No system is installed, trained or launched. Access to cloud LCD Not checked; new theoretical works not reproduced; new theoretical works not reproduced and so on and so on..
- The open restriction may be partially decided by a new method or other device or other device. or other device or other type of device.. The selection of a separate research target will require updating the test rather than treating it as a permanent map..
