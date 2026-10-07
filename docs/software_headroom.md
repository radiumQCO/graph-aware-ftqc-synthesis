# Software headroom in total FTQC cost

Date: 4 October 2026. This is a research assessment using
[prior_art.md](prior_art.md), [open_bottlenecks.md](open_bottlenecks.md), and primary
resource-estimation sources. No new algorithm or completed benchmark is claimed.

**Answer:** meaningful software headroom exists in compilation, space usage,
resource preparation/delivery, and classical processing. Available evidence does
not establish one maximum plausible improvement for a modern **200-logical-qubit**
machine. A real critical path, noise model, strong baseline, and complete cost
ledger are needed. Published results and explicitly labeled toy calculations
are kept separate.

The historical snapshot below is not a complete modern resource estimate.
[modern_ftqc_ledger.md](modern_ftqc_ledger.md) revisits factories, scheduling,
decoder assumptions, missing ancillas, and source arithmetic discrepancies.
[non_clifford_structure.md](non_clifford_structure.md) further replaces **4.8M T**
as a modern synthesis baseline. The paper and archived Q# example have different
counts; conditional recompilation savings do not transfer directly to total cost.

Software-only means fixed physical qubits, couplers/topology, primitive
operations, speed/fidelity/noise constraints, and classical hardware/I/O. Buying
accelerators or adding long-range couplers is a hardware change.


Language note (7 October 2026): the abstract was copyedited; the older body
prose is an English translation draft. Numerical artifacts and primary references accompany these background research notes.

## 1. What does this mean?? SOFTWARE ONLY

Locking physical cubes available couplers and their topology, Acceptable measurements/reset/control primitives, Speed limits, physical noise mechanisms and quality limits aisle. I also fix the classical equipment and its available equipment. I/O. I don't buy a new one. FPGA/TPU and don't add long-range quantum ties for the claim software gain.

Allowed to select existing correct protocols, codes, locations and other relevant data and the use of the data to determine the data and the data., decoder configurations, data reporting and support parameters data and parameters data control pulses. When changing physical actions, they need to be re-evaluated for their mistakes and costs. «Hardware fixed» does not mean that waveform Not calibrated; means that its improvement is limited to those actually supported controls and the device. A specific, severe case - to record more circuit, code and distribution faults: Then only classical processing and decoding are available.

Four values:

- **Mounted machine:** manufactured cubes on the side of the road, wiring and electronics. Software Doesn't reduce the number of cubes already manufactured.
- **Programme resource employed:** peak number of cubes used and time. The spaces are available for other work.
- **Cube-seconds:** Work on the employed resource over time; for the variable load, the integrated output of the employed cubes. B ledger I believe in the following: reserved capacity × runtime.
- **Full value:** includes classical computations, transmission, power, learning, testing, repetition and simple. It's not equal to one koupite-seconds; the monetary price was not estimated here.

Therefore, "less of the required cubes in the same platform" can be a useful design result. That doesn't mean the existing chip is automatically cheaper.

### Classes

| Grade | Meaning |
|---|---|
| **A — mostly software-addressable** | Substantive work — classical processing/choice; reserve dependent on implementation and hardware capacity |
| **B — partially software-addressable** | Software The cost of the project is affected but significant physical/code requirements remain |
| **C — mostly physical / architectural** | The main residual is determined by the device, the coherence and the permissible physical protocols |
| **D — information-theoretically limited** | The available observations may lack information; more compute It won't make it better |

Non-exclusive classes: e.g. implementation decoder — A, improving it accuracy — B, a Residual hepaticity of the syndrome — D. The table identifies the main class and the secondary limit. D Doesn't mean that any decoder I'm already at the top of my head. The mathematical complexity is also not equal to the information limit.

## 2. Which components can influence the outcome

| Component | Basic | Additional limit | Potential relevance to the entire programme |
|---|---|---|---|
| Decoding accuracy | **B** | D: Indistinguishable logical classes | High if it can be reduced distance in a substantial part of the machine; otherwise, it may hardly change resource demand |
| Decoding latency | **A** | C: hardware deadline / dataflow | High only when hit by a critical chain or a large classical cost |
| Syndrome processing | **A** | C/D: bandwidth and sufficient information | Can determine the price of the whole classical infrastructure; quantum gain Unknown |
| Noise estimation | **B** | D: identifiability / sample rate | Cuts the price mismatch And the reserve for uncertainty; does not remove the physical noise itself |
| Adaptive calibration | **B** | C/D: control floor / observational | Could affect you right away distance and factory quality, where quality was limited to the corrected drift |
| Mapping / routing | **B** | C: topology / physical transport | The importance of expensive movements, conflict operations and routing area |
| Syndrome extraction scheduling | **B** | C: conflicts / gate propagation | Impact on quantum cycle, idle errors and distance; The effect is related to other layers |
| QEC code choice | **B** | C: a consistent and consistent relationship gadgets | Could change resources very much if another family is actually executed on the same one hardware |
| Logical operations | **B** | C/D: measurement / FT protection | Often More important memory-only Optimization; possible significant; possible significant and other factors. and/or and/or and/or other relevant factors space–time tradeoffs |
| qLDPC connectivity | **C** | The necessary connections may not be available | Software Doesn't create couplers; Emulation is paid for by time, ancillas And by the mistakes |
| Magic-state production / delivery | **B** | C: preparation, postselection, transport | May dominate of the country T-intensive challenges; not universal or modern architecture. and the environment |
| Physical gate fidelity | **C** | B: bounded control calibration | Software Corrects miscalibration, But not any intrinsic noise |
| Measurement fidelity | **C** | B: signal processing / calibration | Readout software may help; missing signal is still |
| Leakage / correlated bursts | **C** | B/D: heralds, response, lost information | Can determine residual failure and reserve; effect depends on the specific device |
| Communication / I/O | **C** | A: packing / placement / compression | Software reduces the transfer and unnecessary movement, but not the physical capacity of the channel |
| Spare-qubit / remapping overhead | **B** | C: stock and valid routes | You can use the reserve better; you can't eliminate the need for the reserve for the intended reserve.. fault model |

«The Strongest Known" means **Strong published candidates for the relevant regime**, Not one universal winner. The numbering of the selection requires the same task and. budget. Static PyMatching Not appointed by the main modern competition...

## 3. One review per component and other relevant measures for each component and in particular for the purpose of ensuring that the required level of the project is maintained

### 01. Decoding accuracy — B, residual limit D

1. **Resource:** larger distance, more physical cubes and cycles; additional computations decoder.
2. **Strong Solutions:** AQ2, Libra, Tesseract, correlated/adaptive matching, BeliefMatching; exact/near-optimal references in compatible small tasks. LCD important when available leakage herald. [AQ2](https://arxiv.org/html/2512.07737v2), [BeliefMatching](https://arxiv.org/abs/2203.04948), [LCD](https://arxiv.org/html/2411.10343v2)
3. **Balance:** Nearer inference, imperfect prior and mixed mistakes even if correct. and mixed errors prior.
4. **Software:** Yes, until the best choice is made. recovery with the same observations. No change in physical action.
5. **TOTAL:** Over-calculated distance, factory protection and runtime; improvement LER is not equal to the same reduction in cost a certain degree of decline. Total §7 reduction only algorithm-region d=19→17 It saves about **0.40%** complete peak quantum allocation; is a imputation, not a measured calculation. residual headroom.
6. **Limit:** Bayes error for fixed observations; true-rate Oracle matching isn't that ceiling.
7. **Measurement:** accuracy frontier Strong decoders per noise/circuit datasets, then repeated resource optimization with one failure budget. For operations They need their real models, not just theirs. memory.

### 02. Decoding latency — A with a restraint

1. **Resource:** CPU/GPU/FPGA Time, memory, energy; turn and quantum stalls Before feedforward.
2. **Strong Solutions:** LCD/CC, optimized matching and AQ2-RT in the modes shown. Cloud LCD does not reproduce latency FPGA. [LCD](https://arxiv.org/html/2411.10343v2), [CC](https://arxiv.org/html/2309.05558), [AQ2](https://arxiv.org/html/2512.07737v2)
3. **Balance:** Introduction-Conclusion, window wait, Rounds, difficult samples and the joint load of several patches.
4. **Software:** Yeah, same. backend; additional accelerator It's not clean anymore software improvement.
5. **TOTAL:** not more than stalls plus savings in classical resources. YES. reference estimator decoder stalls not taken into account: acceleration decoder Doesn't diminish it's already idealized runtime; real system share stalls unknown.
6. **Limit:** Time of measurement and mandatory operations; critical-path dependencies. Faster throughput not equal faster reaction.
7. **Measurement:** trace all phases under full load, p50/p95/p99, deadline misses, queue stability and additional programme time; separately and extra time offline compile/startup.

### 03. Syndrome processing — A

1. **Resource:** Processing measurement records, detector parities, soft readout, buffers, memory traffic.
2. **Strong Solutions:** compiled detector models, streaming processing, hardware decoder dataflows; new composable EDEMs for supported stabilizer circuits. [Stim](https://github.com/quantumlib/Stim), [EDEM](https://research.nvidia.com/publication/2026-09_composing-detector-error-models)
3. **Balance:** many flows, operation boundaries, causal bookkeeping and cost of delivery of information.
4. **Software:** Yes: exclusion of unnecessary work, packing and correct calculation. Loss of useful soft information It can make things worse. LER.
5. **TOTAL:** can significantly change classical footprint; quantum runtime — Only when removed dataflow bottleneck. Classical value share for ledger unpublished, unknown.
6. **Limit:** Minimum necessary information and existing bandwidth/compute capacity; Arbitrary compression without verification does not retain inference.
7. **Measurement:** bytes/events, memory bandwidth, cycles/event and losses accuracy at each data form, then complete multi-patch trace.

### 04. Noise estimation — B with limit D

1. **Resource:** monitoring, statistical windows, model storage/update; distance margin from-for inaccurate priors.
2. **Strong Solutions:** syndrome-only DEM fitting, multi-speed estimators and DGR-style methods. [Spitz](https://arxiv.org/abs/1712.02360), [Bhardwaj](https://arxiv.org/html/2511.09491), [DEM estimation](https://arxiv.org/html/2504.14643), [Takou](https://arxiv.org/html/2606.11496v2)
3. **Balance:** statistical lag, hidden mechanisms, errors outside model support and feedback bias.
4. **Software:** Partly; data can be better used but cannot be obtained instantly.
5. **TOTAL:** limited by price prior mismatch and the reserve for uncertainty. If estimated and true-model decoders I're close, big estimator-only No resource. No universal percentage established.
6. **Limit:** identifiability and number of effective observations; logical errors without detector signature not recovered from firing rates without preconditions.
7. **Measurement:** causal estimated-prior vs true-prior frontier for different drift rates; latency value updates; Recalculation without leakage hidden simulator truth.

### 05. Adaptive calibration — B

1. **Resource:** calibration shots, control compute, Inability time, reserve geometry and noise margin.
2. **Strong Solutions:** Google RL physical/decoder steering, in-situ calibration, CaliQEC and self-calibration with proven conditions. [Google RL](https://arxiv.org/html/2511.08493), [CaliQEC](https://cseweb.ucsd.edu/~tullsen/isca_caliqec.pdf), [self-calibration](https://arxiv.org/html/2608.05686)
3. **Balance:** hardware optimum, Statistics objective, safe actions and errors during reaction.
4. **Software:** Yes, if current fidelity limited by the corrected setup or drift; fixed physical noise floors remaining.
5. **TOTAL:** Potentially affects many components directly through effective noise, but only when measured calibration gap. You cannot use the transition between two different hardware error-rate rows Source as software-only advantage.
6. **Limit:** Available controls, intrinsic decoherence, observational properties and sample rate. Reduction detector surrogate Not always certifying a decrease program failure.
7. **Measurement:** on one device compare the strong conventional and adaptive calibration, including downtime, shots, resources and independent capacity-building validation logical gates/factories.

### 06. Mapping / routing — B

1. **Resource:** ancillary space, SWAP/transport, surgery volume, idle time, Conflict paths.
2. **Strong Solutions:** lattice-surgery resource compilers, dependency-aware compilation, MQT-QECC, fresh FlowRouter; ReloQate/Surf-Deformer for a changing hardware. [MQT](https://arxiv.org/abs/2504.10591), [resource compiler](https://arxiv.org/abs/2506.04620), [FlowRouter](https://arxiv.org/html/2609.23756)
3. **Balance:** dependency depth, graph cuts/congestion, physical performance and stochastic resource availability.
4. **Software:** Yes, in accessible topology; new quantum links — Architectural change.
5. **TOTAL:** ♪ I've got a lot of good news ♪ spacetime volumes Specific circuits; e.g. FlowRouter He's telling me. **2.3×** geometric-mean improvement in cultivation-aware d=13 benchmark. It's not a projection for ours 200-qubit workload And not to test it. target failure.
6. **Limit:** The necessary transmission of quantum information, track capacity and permissible abbreviation or a lack of precision. and FT gadgets. Improvement mapping can increase other costs.
7. **Measurement:** one logical circuit, one topology and error budget; compare modern compilers c ancillas/factories, actual cycle counts and peak space.

### 07. Syndrome extraction scheduling — B

1. **Resource:** cycle duration, idle errors, gate conflicts, propagation of faults, ancillas.
2. **Strong Solutions:** validated code circuits, AlphaSyndrome, FastSched and adaptive extraction in supported families. [AlphaSyndrome](https://arxiv.org/html/2601.12509v2), [FastSched](https://arxiv.org/html/2609.12020), [adaptive extraction](https://arxiv.org/html/2502.14835)
3. **Balance:** measurement/reset time, coupling conflicts protection from torture and other faults during extraction.
4. **Software:** in part; order can be optimized, physical duration primitive Can't be declared zero.
5. **TOTAL:** Through cycle time and noise suppression all active codes. You can't multiply separately improvement scheduler and decoder, If they use the same effect.
6. **Limit:** dependencies and fault tolerance; Arbitrary skipping checks Changes the task and may lose protection.
7. **Measurement:** as at fixed primitive durations/noise Comparison of Strong valid schedules Under repeated-cycle/gate performance, including decoder cost and looking for a scheme.

### 08. QEC code choice — B, Often architectural limit C

1. **Resource:** qubits/logical, time checks, decoder compute, operations and connectivity.
2. **Strong Solutions:** mature surface/colour constructions, BB and other qLDPC, compatible FT operation schemes. There is no single best family. [BB](https://arxiv.org/html/2308.07915), [gauging](https://arxiv.org/html/2410.02213), [High-Rate Surgery](https://arxiv.org/abs/2510.08523)
3. **Balance:** finite-size performance, Real circuits and the dearest logical operations / Communications.
4. **Software:** The choice of another code can only be made if it can be run on fixed lines hardware; The time of emulation of connections is paid for.
5. **TOTAL:** potentially large effect, but only full compilation ledger on one platform. qLDPC memory rate is not in itself a programme evaluation and the body of the programme..
6. **Limit:** geometry, FT requirements Information protection; BPT Acting in the context of its own 2D-local conditions. [BPT](https://arxiv.org/abs/0909.5200)
7. **Measurement:** one programme/target, All effectively compatible code families; physical transactions: of the day, connectivity, factories and classical cost included.

### 09. Logical operations — B

1. **Resource:** surgery/gauge ancillas, measurement rounds, distance Protection on the ground, feedforward, errors as at boundaries.
2. **Strong Solutions:** optimized lattice surgery, gauging, high-rate surgery and full programming models I think Tour de gross. [Litinski](https://arxiv.org/html/1808.02892), [gauging](https://arxiv.org/html/2410.02213), [Tour de gross](https://arxiv.org/html/2506.03094)
3. **Balance:** actual protected measurement and transport; memory decoder accuracy does not certify accuracy all operations.
4. **Software:** can choose and comb the existing cheaper gadgets; The benefits depend on the available primitives.
5. **TOTAL:** Maybe it's bigger if operations determine depth/area. Tour de gross He's showing it himself tradeoff: less than space may be accompanied by a large runtime; That's not the total price. qLDPC.
6. **Limit:** required information flow, Protection during operation, physical speed and logical dependencies.
7. **Measurement:** verified gate-level noisy circuits and full workload trace; count failures/cost each instruction, including non-Clifford path.

### 10. qLDPC connectivity — C

1. **Resource:** long distance couplers, crossovers, buses; either SWAPs, transport, entanglement generation and ancillary space for emulation.
2. **Strong Solutions:** BB connectivity layouts, reconfigurable atom arrays and modular qLDPC architectures. [BB](https://arxiv.org/html/2308.07915), [atom arrays](https://arxiv.org/html/2308.08648), [Tour de gross](https://arxiv.org/html/2506.03094)
3. **Balance:** quality physical performance of the right interactions the right interaction the right person.
4. **Software:** improves embedding/schedule; doesn't create missing persons. couplers. Atom movement let's just say hardware, The one that can already do it..
5. **TOTAL:** The benefits of a lower cost of emulation may be possible, but it is not set for ours fixed 2D-transmon Model. You can't count all qLDPC qubit economy in software headroom.
6. **Limit:** topology/cut capacity, physical errors and duration Communications.
7. **Measurement:** implement resource/noise accounting Every one of you edge as at **Ibid.** primitive graph; Comparison of the final programme, not abstract [[n,k,d]].

### 11. Magic-state production / delivery — B

1. **Resource:** factories, accepted-state quality, retries, buffers, transfer and consumer stalls.
2. **Strong Solutions:** distance-tuned distillation, cultivation, optimized factories and cultivation-aware runtime scheduling. [Distillation](https://arxiv.org/html/1905.06903), [cultivation](https://arxiv.org/html/2409.17595), [FlowRouter](https://arxiv.org/html/2609.23756)
3. **Balance:** A sufficient condition quality, stochastic rejection, escape/storage and delivery to logical operation.
4. **Software:** significant impact on protocol/configuration/utilisation, if hardware Supports the necessary action; underlying preparation noise stays.
5. **TOTAL:** in T-intensive tasks can dominate. However historical reference §4 is not the most powerful of the times factory baseline. Sensitivity §7 shows the price of the intended improvement, not proves its availability.
6. **Limit:** nonzero physical preparation/protection cost and required output error; You can't replace it free of charge T-resource normal Pauli frame.
7. **Measurement:** best compatible published factory protocols with one input noise and output-error target; accepted outputs/s, qubit-seconds/output, transport, retries and the whole programme.

### 12. Physical gate fidelity — C limited part B

1. **Resource:** code distance, Re-protection and factory overhead.
2. **Strong Solutions:** hardware engineering and device-specific calibration/control, including in-situ/RL tuning. [Google RL](https://arxiv.org/html/2511.08493)
3. **Balance:** The optimally adjusted device still has intrinsic noise and unwanted interactions.
4. **Software:** Corrects the available miscalibration, pulse/crosstalk scheduling; does not guarantee the improvement of the physical ceiling.
5. **TOTAL:** High sensitivity possible through noise exponent, but the size of the corrected gap for reference device unknown. Fixed p It doesn't decrease in the calculations for software Winning.
6. **Limit:** supported control bandwidth, coherence and real noise mechanisms; noise floor not necessarily fundamental to other equipment.
7. **Measurement:** measured gap current→best-supported controls On one device and its impact on the QEC operations, Not just isolated gate benchmark.

### 13. Measurement fidelity — C

1. **Resource:** repeated rounds, wrong syndromes/heralds, longer measurement windows and decoding work.
2. **Strong Solutions:** calibrated readout/reset, Optimal handling of the available signal and soft-information decoding; AQ1/AQ2 show the value of rich data. [AQ1](https://arxiv.org/html/2310.05900), [AQ2](https://arxiv.org/html/2512.07737v2)
3. **Balance:** overlap signal distributions, finite integration time and state errors during measurement.
4. **Software:** may improve the classification/use of the same signal but not return data detector did not distinguish.
5. **TOTAL:** Through measurement-limited cycle and effective logical noise; without error/time curve unknown.
6. **Limit:** visibility readout, detector bandwidth and back-action.
7. **Measurement:** hard vs soft readout with one physical measurement procedure; software decision cost, logical failures and time dependence integration.

### 14. Leakage / correlated bursts — C c B/D

1. **Resource:** reset/mitigation, reserve qubits, enlargement, risk margin, rollback and lost programmes.
2. **Strong Solutions:** leakage-aware LCD plus physical suppression; Q3DE/Surf-Deformer for researched burst/defect scenarios. [LCD](https://arxiv.org/html/2411.10343v2), [Q3DE](https://arxiv.org/html/2501.00331), [Surf-Deformer](https://arxiv.org/html/2405.06941v3)
3. **Balance:** missed/delayed heralds, damage before reaction and bursts Better protection.
4. **Software:** uses side information and existing controls; does not restore arbitrarily destroyed logical information.
5. **TOTAL:** May significantly decrease risk margin/retries in the dominant mechanism; cannot be carried published leakage savings on another noise.
6. **Limit:** observability, Available reset/transport actions and limit of correction of code.
7. **Measurement:** same-circuit leakage traces with the same heralds for all; frequency and; frequency and:: logical damage bursts, failures during reaction, Reserve and full expected cost/success.

### 15. Communication / I/O — C with programme part A

1. **Resource:** readout channels, network bandwidth, memory, transfers, latency energy.
2. **Strong Solutions:** Local decoder dataflows, compiled detector processing, packing and streaming; specific best backend Depends on hardware. [LCD](https://arxiv.org/html/2411.10343v2), [Stim](https://github.com/quantumlib/Stim)
3. **Balance:** Physical delivery of required information and synchronisation of conditional actions.
4. **Software:** It reduces the extras.. copies/transfers and selects the processing site; compression requires the preservation of the necessary information.
5. **TOTAL:** may limit feasibility and classical cost. Reference source Doesn't think so; you can't blame the whole calculated bit rate real network traffic.
6. **Limit:** fixed channel capacity; entropy/accuracy data and physical data requirements reaction path.
7. **Measurement:** hardware counters all borders, useful bits vs transmitted bytes, tail delay and program stalls Full load.

### 16. Spare-qubit / remapping overhead — B c C

1. **Resource:** spare- tiles, routes, calibration windows, transport and temporary enlarged codes.
2. **Strong Solutions:** CaliQEC, ReloQate, Surf-Deformer and Q3DE. [CaliQEC](https://cseweb.ucsd.edu/~tullsen/isca_caliqec.pdf), [ReloQate](https://arxiv.org/html/2603.00837v2)
3. **Balance:** Probability of multiple injuries, availability health and the cost of proper transportation.
4. **Software:** Better use the general reserve and choose moment/action, But doesn't cancel the right supply for the set. risk target.
5. **TOTAL:** Depends on distribution defects/drift. B reference ledger additional runtime reserve Not evaluated; zero in the old model is not equal to zero necessity.
6. **Limit:** no healthy place or valid route; The condition is already lost before remap.
7. **Measurement:** The same defect/drift workloads; required reserve at specified total failure, false moves, transport/correction/calibration overhead.

## 4. Specific reference workload

### The published task and my expansion to 200 data qubits

Use quantum-dynamics example from Beverland et al., **Assessing requirements to scale to practical quantum advantage**, Appendix F / Tables 1–5. It's a real logical thing workload cooperation and cooperation non-Clifford rotations, Not memory test. B Appendix F for one copy specified 100 workers spin qubits, fourth-order Trotter, T=20, 230 planar-ISA positions, Near 150 000 logical time steps and 2.4 million T states After synthesis. [Source and context](https://arxiv.org/html/2211.07629)

**Ours reference — calculated batch of two independent tasks in parallel:** 200 logical qubits, 460 ISA positions with ancillary/routing region and 4.8 million T states. It's not a published simulation of one interacting person 200-spin Hamiltonian. Double independent instances is clearly separated from the original result; for one related task, route and depths can change.

Defining target total modeled execution error/failure **≤0.002** as at batch. Two copies with original target 0.001 Amount ≤0.002; Independence is not necessary for the upper boundary of the association. B source error model rotation synthesis enters execution-error budget. It's a closely-defined model of the quality of the computation, not experimentally certified probability all physical failures. Error Trotter physical dynamics and quantity repetitions for scientific research observable checked separately; one batch is not a complete measurement campaign.

Fixed physical platform: **hypothetical superconducting transmon-like nearest-neighbour 2D processor**, gate 50 ss, measurement 100 ss, primitive noise parameter p=10⁻³. These parameters correspond to gate-based ns-row A source, not an existing car for millions of cubic metres. Code family — surface code c planar lattice surgery; d=19 for algorithm region. No additional quantum links.

Reference Table 4 reference uses around 8.2 million physical cubes and 242 factories one copy; about 98% footprint occupied distillation. This is a historical assessment of the first resource estimator, **not strongest 2026 factory baseline**. I use it as a reproducible numerical ledger and diagnostic example. She doesn't prove that a modern machine needs one of these. footprint. [Table 4](https://arxiv.org/html/2211.07629)

### Formulas reference model

For gate-based surface-code row Source:

\[
n(d)=2d^2,\quad \tau(d)=(4t_g+2t_m)d,\quad
P(d)=0.03\left(\frac{p}{0.01}\right)^{(d+1)/2}.
\]

Here. **P(d) applicable logical time step of this model**, Not to one physical syndrome round. These fitted/assumed resource-estimation formulas are not measured universal noise law. Do not frame P(d) alien memory LER without harmonization of units. [Table 5 / Appendix B](https://arxiv.org/html/2211.07629)

Of them **My calculations**: physical cycle proxy 400 ss, logical step 7.6 μm, 2.85 million cycles and runtime 1.14 c/ When C=150 000. Table 4 round runtime to 1.1 c. I'll use it later. 1.14 c so that arithmetic is agreed.

## 5. Resource ledger for batch

Tags: **SRC** — source model; **CALC** — my arithmetic on its parameters; **UNKNOWN** — Data missing. Value rounded 8.2M Save only approximate accuracy. Missing expenditure is not considered free of charge.

| Resource | Value/status | What is included and what is unknown |
|---|---|---|
| Workers logical qubits | 200 — CALC | Two independent recruitments 100 spins |
| Algorithm ISA region | 460 positions — CALC | 200 workers + 260 Others; the latter include auxiliary/layout space, Not 260 additional useful spins |
| Logical depth | C=150 000 time steps — SRC/CALC | Parallel batch has the same depth; this is compiled ISA depth, not number Trotter steps |
| Logical gates/resources | 4.8 million T states; 60 200 rotations prior to synthesis — CALC | CNOT-conjugated ZZ interactions and Clifford operations Also included in the original compilation; complete gate trace It wasn't launched here |
| QEC cycles | 2.85 million — CALC | d=19 physical rounds as at logical step Model |
| Peak physical allocation | Near 16.4 million — CALC | Double historical evaluation; not count existing existing existing status of the current one position hardware |
| Working-data patches | 144 400 physical qubits — CALC | 200×2×19² Under tile model |
| Balance algorithm region | 187 720 physical qubits — CALC | 260×2×19²; They're already coming in. ancillary/routing tiles, do not add |
| Factories and their internal assistance | Near 16.07 million physical qubits — CALC | Diversity total and algorithm region; about 484 factories. Internal distance/ancillas Different; not all factory region d=19 |
| Quantum runtime | 1.14 c — CALC | Idealized estimator execution; decoder stalls, extra calibration/repair and actual launch not measured |
| Reserved qubit-seconds | Near 18.70 million qubit·s — CALC | 16.4M×1.14; This is reservation volume, not measured integral active cubes and not full energy |
| Decoder compute | UNKNOWN | Backend, time/event, memory, peak queues and power not included in the numerical source estimate |
| Classical I/O | UNKNOWN; proxies below | Readout format, physical channel layout, soft records and preprocessing placement not specified |
| Routing/connectivity | 2D NN + planar surgery region — SRC | Need ancillary area algorithm allocation; Total cycle-level geometry/communication trace not checked |
| Magic production/delivery | 4.8 million accepted T resources — CALC | Average demand ≈4.21 million T/s; additional transfer units, synthesis/delivery ancillas and classical Infrastructure not fully integrated |
| Extra spares / runtime remap | UNKNOWN | Not included historical numeric ledger; The original model doesn't ask defect/burst/drift reserve |
| Full machine cost / Energy | UNKNOWN | Quantum allocation, classical processing, wiring and cooling Cannot add without additional models |

So,, ledger preserves published quantum resource snapshot, But not full on the quantum side: additional synthesis/delivery ancillas and transfer costs deleted. Give the only final number for a full real machine would be false accuracy. Modern recalculation and clarification coverage in [modern_ftqc_ledger.md](modern_ftqc_ledger.md).

### Error budget

Use equal parts target ε=0.002: \(\epsilon_{log}=\epsilon_T=\epsilon_{syn}=\epsilon/3\). This is a model budget allocation that is consistent with the source approach rather than measured. contributions.

| Source modeled execution error | Acceptable Contribution | Check — CALC |
|---|---|---|
| Logical operations/storage | ≤6.67×10⁻⁴ | 460×150000×P(d); I need it. P≤9.66×10⁻¹² as at logical step |
| Error accepted T states | ≤6.67×10⁻⁴ | 4.8M×P_T; I need it. P_T≤1.389×10⁻¹⁰ as at accepted output |
| Rotation synthesis | ≤6.67×10⁻⁴ | Agree synthesis bound original circuits; This is approximation contribution, not physically Bernoulli fault |
| Unmodeled drift/bursts/repair | No additional free budget | When added mechanisms Redistribute parts or prove their inclusion in noise model |

Prin d=19 formula ♪ Gives me ♪ P≈3×10⁻¹² and logical contribution ≈2.07×10⁻⁴. It's a stock. **in toy/resource model**, Not proof fidelity Real lattice-surgery execution. Prin d=17, Ibid. C and no improvement decoder, contribution ≈2.07×10⁻³ — above the allocated budget. Can't count d=17 allowed just from a smaller footprint.

### I/O and compute: I'm sure you can at least count

**CALC, uncompressed binary proxies:** if 200 normal data patches Issued d²−1 check bits every 400 ns, the flow is equal to 180 Gbit/s. If all 460 ISA positions It's like that 414 Gbit/s. Ancillary surgery geometry Changed, so the second indicator — proxy, Not accurate trace.

If **conditional** half of total 16.4M-machine measure each of these cycle, envelope is 20.5 Tbit/s. It's a scenario, not a published real one. I/O: factory measurements, Activity, local aggregation and compression may be very different. Gate pulses, metadata and soft readout Doesn't come in here..

For 200 data patches Support required 500 million patch-rounds/s; for 460-position proxy — 1.15 billion patch-rounds/s. It's a flow of work, **not number FLOPS**. To get decoder cost, I need a measured backend profile; Averaging single-patch latency You can't certainly multiply by the number of patches. Classical hardware capacity remains the entrance that source ledger It doesn't, it can't be assumed endlessly.

## 6. What is known after strong decisions and the child's self-esteem. for the future

### Factory and compiler headroom Can not be measured by old weak configuration

Already known distance-tuned factories and cultivation. Therefore, «98% factories» this reference Doesn't mean that any modern FTQC workload There's almost everything footprint for new optimizations. Need replacement historical factory model **better compatible existing** with the same output target, Before the new headroom. [Distance tuning](https://arxiv.org/html/1905.06903), [cultivation](https://arxiv.org/html/2409.17595)

Checking simple transfer cultivation: published example p=10⁻³ reaches output error Near 2×10⁻⁹. Prin 4.8 million of these outputs union-budget contribution I would have been near 0.0096 — above ours T budget. Therefore, this is not an example ready drop-in replacement for reference. The result is in another physical p Can't count in SOFTWARE ONLY. Possible other valid configurations I must evaluate, not consider, impossible. [Cultivation abstract / results](https://arxiv.org/abs/2409.17595)

There's a positive certificate material software headroom: FlowRouter compares modern compilers/schedulers and tells me less complete **Simulated cultivation-aware spacetime volume** In-house benchmarks. It's an existing job, not a free idea for. ORCHESTRA. Her. code distances, circuits and execution-error regime doesn't automatically confirm the resource gain on my long-term 200-working-qubit reference. [FlowRouter](https://arxiv.org/html/2609.23756)

### Decoder and estimator headroom And it demands the right competition

Variance static→adaptive or uncorrelated→correlated matching — already known of the same software benefit. Balance for new method to count from tuned adaptive/correlated competitor, compatible LCD, Strong neural baseline and near-optimal reference, where technically feasible. Do Not Sumble improvements several methods, if they fix one mismatch.

Near-optimal decoding fixed memory model Doesn't guarantee near-optimal operations; I'm gonna need surgery to check information class and correlations. Set first measured reference gap, Then transfer it to the permissible distances and full ledger.

## 7. Contingent numerical estimate headroom

All scenarios in this section — **CALC / WHAT-IF**, not forecasts and not new algorithms. Hardware primitives, physical p and workload fixed. Installations are not decreasing; necessary/occupied resources or time change.

### 7.1. Only algorithm-region decoding accuracy

Let's say, purely-classical improvement Shares P(d) per multiplier g, Not changing factories, noise and information. It is a conditional model; accessibility g unknown and must be measured relative to the decoder. The necessary, not the achievement, is shown below. improvement.

| Distance | Minimum g Under logical budget to C=150000 | Algorithm physical qubits | Reduction total peak allocation with fixed factories | Idealized logical-path runtime |
|---|---|---|---|---|
| 19 | 1 It's already done.. | 332 120 | reference level | 1.14 c |
| 17 | ≥3.11 | 265 880 | Near 0.40% — CALC | 1.02 c |
| 15 | ≥31.1 | 207 000 | Near 0.76% — CALC | 0.90 c |
| 13 | ≥311 | 155 480 | Near 1.08% — CALC | 0.78 c |

Last column — **Not a promise to accelerate the full programme**. With constant factory throughput will need the previous time 4.8M T states. Then extra idle steps Increase exposure: e.g. under d=17 and wall time 1.14 c required g≈3.47, Not 3.11. The table also does not include change geometry for repackaging.

Even mathematically, you can take it all away algorithm-region space, Left factories, would only take away the near **2.03%** complete allocation in this historical Model. Such a defecation is physically impossible; it is the upper assessment of the impact **Only this component**. If representation/decoder improvement Helps factory circuits, The analysis should include them — limiting them 2.03% Then not applicable.

### 7.2. Fixed classical decoder, Quicker implementation on the ground

If real trace has baseline time \(T=T_{essential}+T_{avoidable}\), Total elimination avoidable **critical-path** Waiting gives speedup No more \(T/T_{essential}\). Simultaneous work stages must not be counted twice T_avoidable.

B source numerical runtime decoder overhead None. Therefore, relative **this idealized 1.14-Second model** latency-only optimization Doesn't give another acceleration. The relative gain is not known: the winner is unknown decoder Creates backlog, He can be very important. Required trace, Not a fictional one stall percentage.

### 7.3. Existing factory protocols / utilisation

Use approximate factory portion from ledger And I ask: what would happen if he? footprint has been reduced in s one under **Ibid. accepted output error, throughput and delivery**? This condition is considerably stronger "one factory takes less space». Resource ratio:

\[
G_Q(s)=\frac{Q_{alg}+Q_{fact}}{Q_{alg}+Q_{fact}/s}.
\]

| Conditional s | New peak allocation | Quantum allocation improvement | What does that mean? |
|---|---|---|---|
| 2 | Near 8.37M | Near 1.96×, or 49.0% less than — CALC | Sensitivity test; not an assertion that available SOTA gap equal to 2 |
| 10 | Near 1.94M | Near 8.46×, or 88.2% less than — CALC | The greatest gain is only if all demands are maintained; the source does not confirm it for ours. target |
| Formally.. s→∞ | 0.332M | Near 49.4× — CALC | Non-physical "free of charge", and so forth factories» limit, **not maximum plausible improvement** |

To reduce runtime on a fixed chip, the area released could be used for known valid resources, if paths/controls allowed. But speedup then limit logical dependencies, physical cycles, resource consumption and classical reaction. Redistribution does not automatically produce the same area multiplier for runtime.

### 7.4. Full compiliation / T demand

Reduction T demand, volume routing and idle intervals affects several areas immediately and can be more important accelerations decoder. But ours C and M already relevant to a certain existing compilation. Estimate residual should compare the best existing methods as at **Ibid.** Hamiltonian evolution, synthesis accuracy, hardware and target, including cultivation/distillation costs.

FlowRouter and other compiler results Affirm that program representation/placement can change volume. They don't ask the maximum.. remaining gain After all the best methods. Not appointed here arbitrary 10%, 50% or 10×; available benefits for reference Not yet measured.

## 8. Estimate PTC-The idea of changing the representation to decoder

This section is added to discuss the motivating PTC/Hybrid results 60/60 and native-gate savings — user-driven data; data repository/benchmark I haven't checked here. They illustrate the type of approach, but they don't provide proof. QEC headroom.

**Estimate:** Change of presentation - a mathematically sound direction for analysis a. The general idea of "complexing" hypergraph → preprocessing → Normal fast decoder» already implemented in prior art. It can't be considered new, and it can't be assumed that auxiliary variables automatically eliminate complexity. The important thing is to keep not only acceptable syndromes, But also probability of the same **logical results**.

### 8.1. What is before: of the two decoder

For stabilizer circuit c stochastic Pauli faults It's easy to write:

\[
s=He\pmod2,\qquad \ell=Be\pmod2,\qquad P(e).
\]

- e — hidden fault variables; decoder does not take into account their true meaning.
- H — What are detection events Called by each fault; s — Observed events.
- B — What are logical observable flips Called faults; ℓ — Pursuit logical result.
- P(e) — Probability model, including necessary correlations.

DEM — It's not easy. H: It contains probabilities, detector targets and logical observable targets. Classical binary independent DEM I can imagine Bernoulli variables, but arbitrary leakage/coherent channels Need a richer model. Raw measurements → detectors is already a transformation. It may not include useful soft signal/herald; Retain information on DEM doesn't mean to keep everything physically available. telemetry. [Stim format](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md)

### 8.2. What is allowed mathematically

It's a list **of existing equivalents and conditions**, Not the new draft decoder.

| Change | Condition of preservation of information / inference | Where the price might be hidden |
|---|---|---|
| Reschedule detector/fault indices | H, B, priors and inverse mapping agreed | Almost doesn't change the mathematical problem; it can improve data layout |
| The Reversing Change detector basis | s′=Us, H′=UH, U Reverse GF(2); logical mapping and prior retained | H′ It can get thicker; global/time mixing Creates delay |
| Additional derived parity checks | New bits Computed from old; old bits either retained or restored | Independent evidence is not added:, or less than one-half:; correlated/redundant checks cannot be considered independent observations |
| Removal of Some checks | Retained sufficient statistics for P(ℓ|s), either proven/measured approximation | Normal rank loss may lose useful information; not any full-rank subset noisy physical measurements Enough. |
| The Reversing Change fault variables | e′=Ve, H′=HV⁻¹, B′=BV⁻¹; P′(e′)=P(V⁻¹e′) | Independent faults They can become correlated; Simple view H does not guarantee simple prior |
| Introduction latent / auxiliary variables | Marginal Under auxiliaries Plays the original joint P(s,ℓ); the regulation is taken into account and multiplicity | Needed hard constraints, coupling or marginalization; ordinary independent-edge MWPM Maybe not express them |
| Exact elimination / contraction | Retained joint probabilities/partition sums Under logical classes | Elimination may create large factors; The value has not disappeared |
| Integration fault mechanisms | Saved together detector **and logical** effect and correct probability law | Same syndrome Different logical effect You can't just leak |
| Approximate splitting / dropping correlations | Clearly declared approximation and validation LER | That's a change inference; Can't be called guaranteed information preserving |
| New physical checks / gauge / code | New protocol with proven accuracy and all on the ground costs | Changed circuit and physical actions; it is no longer just classical representation layer |

Prin streaming additional need **causation**: transform should not require future syndrome before current deadline. Replacement detector basis The same information does not increase optimal accuracy: P(ℓ|Us)=P(ℓ|s) For reversible U. She can do a rough one solver A little bit more optimistic or cheaper. It's an important difference between algorithmic headroom and the information ceiling.

**CALC, An example of a known shift binary basis:** instead of four bits A,B,C,D You can store A, A⊕B, A⊕C, A⊕D. Everything is recovering backwards XOR. Fault signature 1111 new basis becomes 1000 — one column is really simplified. But signature 1000 becomes 1111: The other column becomes more complex. It's an illustration of normal linear transformations, not new. QEC algorithm. The improvement must be assessed across the entire H, prior and logical mapping, Not a beautifully transformed one hyperedge.

### 8.3. Why drawing with P1/P2 Not enough

**CALC, minimum example:** one fault f c probability p Turns over A,B,C,D simultaneously. Only possible 0000 and 1111. If you replace it with two independents edge faults A–B and C–D with the same p, will be 1100 and 0011 c probability p(1−p), a 1111 will have probability p² instead p. Prin p=0.01 This is 0.0099 for each new partial pattern and 0.0001 instead 0.01 for all-four pattern.

The equivalent entry will require both parts to be included together, for example, with a stored. equality/correlation constraint. Draw them separate edges And forget the connection - change noise model. If virtual P1/P2 Not measured, not just given decoder their true identity syndrome bits: They need to be removed in a permissible way or sum up hidden values. Where?-then the remaining task is correlated inference.

Stim `decompose_errors` already produces suggested graphlike decomposition. Recording `error(p) D0 D1 ^ D2 D3` Saves information on joint event; Remove the dividers and restore the source event Yes, yes.. But the concept of component as independent in a normal matching — additional approach decoder. [Official description Stim](https://github.com/quantumlib/Stim/blob/main/src/stim/cmd/command_analyze_errors.cc)

### 8.4. The most recent methods available

| Work/tool | Why the Principle Under Discussion | What does not follow from the result of the substance |
|---|---|---|
| [Splitting decoders for correcting hypergraph faults](https://arxiv.org/html/2309.15354) | Preprocessing hyperedges for existing MWPM/UF; Directly declared heuristic splitting methods | Not universal exact transformation and not universal good performance |
| [Stim decomposition](https://github.com/quantumlib/Stim/blob/main/src/stim/cmd/command_analyze_errors.cc) + [correlated PyMatching](https://github.com/oscarhiggott/PyMatching/blob/master/src/pymatching/matching.py) | Degradation correlated events and future use correlation structure | Ordinary MWPM Independent expert edges Not automatically decides the source correlated ML |
| [Chromobius / Möbius decoder](https://github.com/quantumlib/chromobius) | Other graph representation for color-code decoding | Not generic Arbitrary converter DEM; Need supported code/circuit structures |
| [BeliefMatching](https://arxiv.org/abs/2203.04948) | Factor-graph inference Helps matching working with correlated circuit noise | It's already known hybridization; generic «latent variables + matching» Not new |
| [BSV / tensor networks](https://arxiv.org/abs/1405.4883) | Other probability-sum recording logical classes; Special cases happen tractable | Factorization Doesn't make it arbitrary. contraction Cheap |
| [Composable EDEMs](https://research.nvidia.com/publication/2026-09_composing-detector-error-models) | Compilation and agreed boundary representation for logical operations/windows | Composition/precompilation Not a guarantee by itself, cheap inference |

For general stabilizer codes optimal degenerate decoding known computational hardness. Therefore, universal effectiveness and ed exact Transforming all such tasks into easy forms would be a very strong statement. This result of the world **Doesn't rule out** the effective transformation of a particular structured family and is not proven runtime lower bound For my circuits. [Iyer–Poulin](https://arxiv.org/abs/1310.3235)

### 8.5. What would measure headroom, without the invention of a solution

1. Select already published supported transform and its correct information class; not to develop a new mechanism in this task.
2. Small tractable circuit Comparison original and transformed joint probabilities Under syndrome **and logical class**, with full account latent states; one for the first time for the second time feasible-syndrome set Not enough.
3. Compare existing fast decoder before/after transform c splitting, correlated matching, BeliefMatching, neural baseline and near-optimal reference on the same data.
4. Count transform/build/update time, causal waiting, memory, inverse/logical interpretation, p99 and throughput; offline Part separately amortize.
5. Translate measured accuracy/time changes in ledger programme, including factory/operation circuits. If winning is only a small one algorithm region, do not declare large system gain.

**A verdict by analogy of the country:** A useful question for analysing the submission, but not a confirmed new idea and a way to remove general decoding complexity. The outlook depends on structured family and retention prices correlations. Except decoding You should remember: program/operation representation already change compiler workload; It's separate.. software headroom, also with existing prior art.

## 9. Answer to central question

**If hardware fixed, as credible as possible end-to-end improvement Not currently quantified.** Embezzle him 2×, 10× or any percentage of these two review documents would be fictional. Needed strong contemporary baseline and at least measured factory frontier, full operation trace and classical critical path.

What is justified?:

- **For narrow decoder-only improvement** with fixed on fixed-line on fixed-line-side on fixed-line-side-side-side-side-side-side-side-side-side-side-side-side-side-by-side-side-side-side-side-side-side-by-side-side-side-side-side-side-by-side-by-side-by-side-side-by-side-by-side-by-side-by-side-by-side-by-side-by-side-by-side-by-by-side-by-side-by-side-by-side operations/factories effect on quantum allocation limited to the corresponding share of the machine. In ours historical reference She's around. 2.03%; conditional d=19→17 Gives you around 0.40%. It's not the limit decoder all areas of the machine and not the universal limit FTQC.
- **For software on all permissible protocols** More important effect possible through existing compilation, allocation, T-resource configuration/delivery and calibration gap. There are published material volume improvements specific benchmarks; They can't be announced.. residual maximum for another workload.
- **After powerful modern methods** leftover headroom Not yet measured for ours 200-working-qubit batch. Historical factory dominance is a sign of where to look, not a reason to promise almost free. T states.
- **Physical/code/information limits** remaining: primitive time/noise, topology, protection during operations, sufficient information and nonzero cost accepted quantum resources. They can't be deducted from ledger How software inefficiency.

Therefore, **software-first research — A Sound Purpose and the right direction**, If you estimate it by full workload and a strong existing wall. **Software-only fundamental leap is not yet justified.** No resources 200-qubit Cars, no new car found algorithm/representation The mechanism is not stated here of the mechanism.

## 10. What data would convert this estimate into a quantitative result and the data will be used to measure the value of the estimate as

| Missing value | How to Get Without New algorithm design | What you need |
|---|---|---|
| Best existing factory frontier for P_T≤1.389×10⁻¹⁰ as at fixed primitives | Agreed calculation and other measures to ensure that the required level/validation published by the protocols, output/s and full delivery | Replace historical factory region; Identify the largest remaining |
| Contemporary compilation trace reference | Start existing compatible compilers on the original task and accuracy target | Measure residual M, C, routing/ancillary space |
| Decoder/estimator accuracy gap | Strongly compatible baselines and small exact reference Under [benchmark protocol](benchmark_protocol.md) | Identify available g and permissible distances |
| Classical hardware and reaction trace | Profile of existing implementation/selected platform model | Calculate stalls, Releases, compute/I/O and their price |
| Calibration floor / drift / defects | Real traces or expressly designated validated device model | Do not count hardware improvement or absence bursts in software gain |
| Representation equivalence / cost | Verification of existing transforms Full joint problem | Segregate the preservation of information from statistical approximation |

The mission included a background check and arithmetic, a document. None simulation/decoder training, No new QEC architecture, No new transform Not implemented. The next measurement is how to check the available reserve, not the proposals for new solutions..
