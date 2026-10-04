**PROJECT ARCHE**

*Architecture Specification — v4.8*

# **1. Design Principles**

Project Arche is a developmental cognitive architecture built from first principles. The system is composed of functional components with explicit dependency relationships. Each component becomes active when its required inputs exist.

This document specifies the architecture in functional terms only. Biological analogs for each component — the brain structures whose function each component implements — are documented in the companion Brain Model Mapping document. The architecture specification does not depend on those mappings being correct; if a mapping turns out to be wrong, the functional specification stands unchanged.

Core architectural commitments:

- Grounded cognition. The system operates without symbolic scaffolding and without pretrained representations. All concepts emerge from physical interaction with a consistent environment.

- Prediction error as the only learning signal. The system operates without a reward function, without batch training, and without backpropagation.

- Local plasticity only. Hebbian co-activation is the foundational mechanism. Spike-timing dependence, neuromodulatory gating, and oscillatory phase windows make Hebbian updating precise, selective, and temporally coherent. No backpropagation, no global error signals, no batch training.

- Finite resources. Bandwidth, working memory, energy, and structural capacity are capped. These constraints are load-bearing.

- Dependency-driven activation. Components activate when their inputs exist.

- Passive observation. The registry observes the system without influencing it.

- Machinery, not content. The architecture supplies mechanisms — plasticity rules, oscillators, the efference comparator, bandwidth limits. These are designed priors and are named as such. What the mechanisms produce — features, categories, concepts, and the self/world distinction itself — is never designed, labeled, or seeded. No component outputs a category the system is meant to discover.

# **2. Physics Engine Substrate**

Genesis (Genesis-Embodied-AI/Genesis). The Genesis project technical report is dated December 2024 (Genesis Authors, Genesis: A Generative and Universal Physics Engine for Robotics and Beyond, https://github.com/Genesis-Embodied-AI/Genesis). Capabilities relevant to Arche per official sources: Python-native API; unified rigid body, MPM, SPH, FEM, PBD, and stable fluid solvers; explicit material parameters including stiffness, elasticity, damping, friction; reported simulation speed 10 to 80 times faster than Isaac Gym/Sim/Lab and MuJoCo MJX. AMD ROCm backend confirmed working on target hardware (AMD Radeon RX 6800XT, RDNA 2) as of May 2026. Detailed capability sourcing and verification status documented in Brain Model Mapping Section 8.

The physics engine is integrated with the cognitive architecture. Oscillator frequencies, behavioral timescales, and encoding grain are derived from physics environment parameters at runtime. The Genesis environment design — specified in the Eden Physics Environment Design document — is the other half of the cognitive substrate.

# **3. Functional Architecture**

The system is specified as a set of functional components with explicit input dependencies. All components are present from system start. Each becomes operationally meaningful when its dependencies are satisfied.

## **3.1 Embodiment**

### **Bipedal Humanoid Body**

A physical body inhabiting the Genesis environment. Bipedal humanoid morphology with a full human kinematic chain. The body is inherited complete at system start; only cognition develops. The richer kinematic chain (relative to a simple effector) is an architectural choice: it produces a richer efference copy signal, a more complex self/world boundary resolution problem, and a denser cross-modal prediction surface. Complexity here is load-bearing, not decorative.

- Mass, volume, and collision surface across all body segments.

- Full human degrees of freedom as the kinematic ceiling: spine (cervical, thoracic, lumbar), shoulders (ball joints), elbows, wrists, fingers (three joints per finger, two per thumb, independent actuation), hips (ball joints), knees, ankles, neck.

- Joint limits, damping, and torque specified per joint via an inherited or adapted human URDF. Genesis accepts URDF natively and handles the physics of the articulated chain.

- Bipedal balance is a continuous, never-trivially-solved prediction problem — permanent sensorimotor engagement and permanent low-level prediction error. The body is always slightly falling and catching itself.

- Independent finger articulation is the richest cross-modal surface: manipulation produces simultaneous proprioceptive, visual, and contact predictions, with the hands visible in the visual field.

- Body surface is a visual prediction substrate. Opalescent skin produces complex, illumination-dependent appearance; long hair provides continuous low-amplitude visual motion tied to both self-movement and environmental wind. Both are clean efference copy test cases. Appearance is non-overtly human; aesthetic detail is an implementation concern and does not affect the functional specification.

Motor output at start is uncalibrated. Force and motor calibration emerge from consequence.

*Depends on: Genesis physics engine.*

### **Efference Copy Mechanism**

Self/world boundary generator. Every motor action produces a paired copy of the command simultaneously (corollary discharge). The copy goes to two places.

- To the forward model, which uses it to predict the sensory consequences of the action.

- Into the sensory input stream, as a trace of recent motor commands — an explicit signal of what the system has been doing (see encoding gap note below).

Sensation predicted from the command is attenuated in proportion to how well the command predicted it (Section 3.3, Reafference Attenuation). Attenuation is continuous. No component labels any signal as self or world.

Only the command-driven component of prediction is attenuated. Sensory change that is predictable from body state or from regularities of the world — contact with a fixed obstacle at a familiar joint angle, for example — is not attenuated. Being predictable is not the same as being self-caused.

The self/world distinction emerges as a consistency pattern: the portion of sensory change that the system’s own commands reliably predict. It is not computed by any component. It is observed by the registry (Section 6, Anima). The richer the kinematic chain, the richer this signal.

*Depends on: Humanoid body. Motor output across the kinematic chain.*

**Encoding gap and the command trace.** The forward model generates implicit causal knowledge: it compensates for self-caused prediction error through distributed weight dynamics. This compensation alone does not produce readable self-representation — a system can perfectly predict its own effects without encoding “I am acting” as a distinguishable internal state (Ye 2026, arXiv:2606.05605). In Ye’s system the gap was crossed by feeding a trace of the system’s own action back in as input. A channel carrying the action’s consequences was already present and did not cross it. Arche therefore routes a trace of recent motor commands into the sensory input stream, so the system’s own causal activity is available as explicit signal rather than only as implicit compensation. Biologically this is corollary discharge reaching sensory areas.

Joint state and force feedback (Section 3.2) remain essential: they report the consequences against which the command’s predictions are checked. Whether joint-state proprioception alone would also cross the encoding gap in a rich body is untested. It is an open question, examined by ablation in the efference proof of concept.

*Depends on: Kinesthetic / Proprioceptive Force (Section 3.2). The efference copy generates the boundary; the command trace makes it legible; proprioception supplies the consequences it is checked against.*

## **3.2 Sensory Primitives**

All sensory primitives are active from the moment the body enters the world. There is no staged activation of senses; the body arrives complete, and only cognition develops. Three channels of mechanoreception (subcategories of mechanical force detection), stereoscopic photoreception, and stereo audition.

### **Oscillatory Mechanoreception**

Vibration propagation. Encodes frequency signature, amplitude, duration, decay rate.

- Material discrimination via prediction error on continuous force waveforms.

- Stiff materials produce sharp rise, short decay; damped materials produce slow rise, long tail.

- Genesis provides continuous contact force data natively.

*Depends on: Genesis contact force output. Material damping parameters.*

### **Kinesthetic / Proprioceptive Force**

Resistance to applied force and joint state across the kinematic chain. Inertial mass perception and limb position sense.

- Encodes magnitude, rate of change, consistency, and joint configuration.

*Depends on: Articulated body. Genesis rigid body dynamics.*

**Architectural role.** This channel serves a dual function. As a sensory primitive, it provides limb position and force data for motor calibration and physical interaction. As the companion to the efference copy mechanism (Section 3.1), it is the consequence side of the self/world comparison: the command predicts, proprioception reports. Without it there is nothing reliable to check self-caused predictions against. Whether joint state also carries enough action history to make the boundary readable on its own, without the command trace, is an open question. See Section 3.1, encoding gap note.

### **Static and Dynamic Contact Force**

Surface boundary, contact intensity, distribution, directionality.

- Encodes location, magnitude, duration, gradient.

*Depends on: Body collision surface. Genesis contact reporting.*

### **Stereoscopic Photoreception**

Bifocal depth-native vision. Two cameras with fixed baseline separation mounted on the body, rendered through the Luisa ray tracer (Vulkan backend; the CUDA-only Nyx renderer is unavailable on AMD hardware).

- Raw outputs: left RGB, right RGB, left depth, right depth, stereo disparity map.

- Raw signal enters the predictive hierarchy. Features are not engineered; they emerge from prediction error (Rao & Ballard). Renderer segmentation output is deliberately unused — the system must not receive pre-labeled object boundaries.

- Depth is privileged as the most physically grounded visual channel — it is geometry derived from ray geometry rather than statistically inferred.

- Vision extends the predictive horizon beyond contact: predictions form about objects before contact, producing cross-modal prediction error at the moment of contact.

*Depends on: Genesis/Luisa rendering pipeline. Two-camera body configuration.*

### **Stereo Audition**

Vibration-based audition, active from entry. Genesis has no native audio; the auditory signal is generated by physics-grounded synthesis from Genesis contact data, keeping sound rooted in the same physical substrate as mechanoreception.

- Synthesis mapping: material stiffness → frequency content; impact force magnitude → amplitude; damping → decay rate and resonance tail; contact surface → spectral shape. A contact event produces a force signature and a sound from the same physical parameters.

- Stereo: two microphones at ear-position on the body with human-scale baseline separation. Spatial position of each sound is encoded via interaural time difference (ITD, azimuth) and interaural level difference (ILD, azimuth and distance).

- Cross-modal binding: a contact event produces force, sound, and (often) a visual depth candidate at the same moment and consistent spatial location. Temporal contiguity binds these into unified physical concepts.

- Head-related transfer function (HRTF) is deferred — ITD/ILD alone provide meaningful spatial prediction. HRTF is reserved for specialized experiments or physical embodiment.

*Depends on: Genesis contact events and material parameters. Two-microphone body configuration. Implementation may proceed as a standalone synthesis mini-project.*

## **3.3 Sensory Encoding and Attention**

### **Feature Vector Extraction**

Raw sensory signals encode into feature vectors before reaching the predictive core. Temporal, magnitude, and spatial features. No engineered semantic features.

*Depends on: All sensory primitive channels.*

### **Sampling Rate Asymmetry**

Sensory channels feed the predictive core at different rates, and this asymmetry is intentional. Mechanoreception and proprioception feed at the physics timestep. Vision feeds at the render rate, which is lower than the physics rate — two ray-traced stereo cameras per physics step is likely prohibitive, so there are physics steps with no visual update. Audition feeds at its own computationally honest sample rate. This mirrors biology, where sensory modalities do not share a sampling clock, and is a design constraint the predictive core must accommodate rather than a defect.

*Depends on: Render throughput measured on target hardware.*

### **Reafference Attenuation**

Sensory data predicted from the efference copy is attenuated before it enters the competition for bandwidth, in proportion to the command-driven prediction. Self-caused sensation therefore tends to be less salient than equivalent world-caused sensation, as in biology. Applies across all channels, including self-caused visual change (e.g., a limb or hair moving in the visual field). Attenuation is continuous and carries no self/world label. The distinction is left to emerge (Section 3.1) and to be observed by the registry (Section 6).

*Depends on: Efference copy mechanism.*

### **Biased Competition Attention**

Finite-bandwidth attention with a hard throughput ceiling. Signals compete for processing; low-priority signals are excluded entirely when bandwidth saturates.

- Salience score: magnitude, novelty, rate of change vs baseline expectation.

- Relevance score: predictive core pull for this signal.

- Priority = (salience weight × novelty delta) + (relevance weight × predictive core pull).

*Depends on: Internal state dimensions (Section 3.4). Predictive core for relevance signal.*

### **Bandwidth Ceiling Function**

Total processing bandwidth = f(arousal, energy, prediction confidence).

- Arousal raises ceiling temporarily.

- Energy depletion lowers ceiling.

- Prediction confidence modulates relevance signal strength and gates ceiling growth.

- Operating range: 1 to 2 concurrent streams when relevance signal is weak; 3 to 6 when predictive core is well-structured.

- Bandwidth scales with what the relevance signal can usefully direct.

*Depends on: Internal state. Predictive core (for relevance signal). This is the developmental gate.*

## **3.4 Internal State**

Four dimensions modulate encoding bandwidth, Hebbian update magnitude, precision weighting, memory consolidation, structural maintenance, and attention competition. Tunable. Architecturally load-bearing. The functional roles correspond to neuromodulatory systems in biology (see Brain Model Mapping) and are the tunable substrate for the neurological profile simulation research application.

### **Energy**

Energy follows a two-component recovery model. Total available energy is the sum of a fast component and a slow component, each with its own recovery time constant.

Total energy: E_total(t) = E_fast(t) + E_slow(t)

Passive recovery (no action):

E_fast(t) = E_fast_max × (1 − e^(−t/τ_fast))

E_slow(t) = E_slow_max × (1 − e^(−t/τ_slow)) where τ_fast \<\< τ_slow

Depletion (during action): action draws from E_fast first; once E_fast reaches floor, action draws from E_slow; draw rate scales with action intensity; recovery floor is non-zero (minimal action remains available at depletion).

Depletion asymmetry: recovery rate of the fast component degrades as depletion of the slow component deepens.

τ_fast_effective = τ_fast × (1 + k × depletion_depth)

depletion_depth = (E_slow_max − E_slow) / E_slow_max

Bandwidth ceiling input: energy_factor = E_total / E_total_max.

Empirical calibration: constants τ_fast, τ_slow, k, E_fast_max, E_slow_max are placeholder-seeded and replaced empirically during Genesis runs. The form of the equations is fixed; the values are tuned to produce honest behavioral pacing. The bipedal body makes this model more physically honest — balance, locomotion, and posture all draw from the energy budget continuously.

*Depends on: Action output. Internal state arousal level.*

### **Attention**

- Finite focus vector.

- Relevance signal strength to sensory encoding.

### **Prediction Confidence**

- Precision weighting modulator.

- Developmental bandwidth gate.

- Modulates learning rate.

### **Arousal**

- Novelty-driven.

- Modulates Hebbian update magnitude.

- Modulates bandwidth ceiling.

## **3.5 Predictive Core**

Three hierarchical levels operating at different timescales. Top-down predictions cascade downward. Bottom-up error signals propagate upward, filtered at each level. Learning proceeds via local plasticity: Hebbian co-activation as the foundational rule, modulated by spike-timing dependence, neuromodulatory broadcasting, and oscillatory phase windows. PyTorch operates as a GPU tensor compute layer.

### **Level 1 — Sensorimotor Prediction**

Millisecond timescale. Predicts immediate next sensory state across all channels.

- Raw physical surprise. Heaviest Hebbian updating. Directly coupled to sensory encoding output.

- All raw sensory channels feed here: mechanoreception and proprioception at physics rate; raw RGB, depth, and disparity from stereo vision at render rate (depth privileged); stereo auditory waveform with ITD/ILD. Features emerge from prediction error rather than being engineered.

- Self-visual prediction occurs here: the body surface (opalescent skin, hair) is in the visual field, and the core must predict its own appearance under changing illumination and pose.

*Depends on: Sensory encoding output. Internal state for update magnitude.*

### **Level 2 — Situational Prediction**

Seconds-to-minutes timescale. Predicts sequences and patterns.

- Object identity and physical property clustering. Cross-modal binding of force, sound, and visual signatures from the same event.

- Receives filtered errors from Level 1 only — structured prediction error, not raw pixels or waveforms.

*Depends on: Stable Level 1 predictions. Episodic memory traces.*

### **Level 3 — Contextual Prediction**

Minutes-to-hours timescale. Predicts environmental regularities.

- Rare significant errors only. Stable concept consolidation territory.

- Slow regularities consolidate here: the day/night lighting cycle, stable ravine geometry, fauna movement patterns, and the body’s own appearance across lighting conditions.

*Depends on: Stable Level 2 predictions. Long-term memory consolidation.*

### **Local Plasticity Stack**

Three distinct mechanisms operate together to produce the learning behavior of the predictive core. They are not interchangeable.

- Learning rule. How weights change locally. Hebbian co-activation is foundational. Spike-timing dependence and homeostatic normalization refine when and how much co-activation produces a weight change. Structural plasticity allows topology itself to reshape with experience — both growth and decay (see Structural Plasticity and Structural Ceiling below).

- Credit assignment. How useful updates become localized. Neuromodulatory broadcasting, temporal contiguity, and cascading prediction reshaping.

- Systems coordination. How distributed components synchronize. Oscillatory phase coupling, bandwidth gating, attentional competition, and biased competition at the sensory encoder.

Hebbian updating is the foundational principle. The remainder of the stack makes it precise, selective, and temporally coherent. The architecture rejects backpropagation, global error signals, and batch training. It does not reject the broader local plasticity literature.

### **Credit Assignment — Three Mechanisms**

- Neuromodulatory broadcasting. Significant prediction error triggers a system-wide broadcast signal; the plasticity window opens temporarily, increasing readiness for change across the system.

- Temporal contiguity. Hebbian learning is time-sensitive. Connections active in the moments leading up to an error update. Recency serves as the credit assignment mechanism.

- Cascading prediction reshaping. Unresolved errors at higher levels propagate back down as modified predictions. Level 3 error reshapes Level 2 predictions; Level 2 adjustment reshapes Level 1. Hebbian updating handles the rest locally at each level.

### **Node Specification**

A node is defined functionally by what it must do, not by biological analogy. There is one kind of node. It is channel-agnostic: a node does not know whether it is processing visual, auditory, or mechanoreceptive signal. Sensory specialization emerges from experience (consistent with cross-modal plasticity in biology — e.g., cortex reassigned by developmental input), it is not pre-specified.

Minimum capability set. A node must:

- Hold a prediction — a stored expected value for its input at the next timestep.

- Receive incoming signal — from connected nodes or sensory encoding.

- Compute prediction error — predicted minus actual, signed.

- Integrate over a time window — accumulate signal across a defined temporal window; required for temporal contiguity and oscillatory phase coupling.

- Fire when a threshold is crossed — emit output when activation crosses the firing threshold.

- Participate in Hebbian association — connection weights update on co-activation with connected nodes.

- Cost maintenance energy to exist — a metabolic commitment regardless of activation state, even while silent.

A node explicitly is not: channel-specific (specialization is emergent); spatially located (addressable but not positioned — topology is connectivity, not geometry); biologically literal (no dendrites, axons, or membrane simulation).

### **Fixed Node Population, Dynamic Connectivity**

The body is inherited complete; the node population is likewise fixed from system start — all nodes present, initially silent and sparsely connected. What develops is connectivity, not node count. This mirrors human neurodevelopment: the infant brain has its full neuron complement, and intelligence emerges through connection formation, reinforcement, and pruning, not neurogenesis. Concept formation is connection patterns stabilizing into cell assemblies across the fixed node population. Node maintenance cost is fixed and known at start; connections are the variable resource and the locus of the developmental economy.

### **Structural Plasticity and the Structural Ceiling**

The network is a finite economy of predictions competing for a fixed resource budget. The architecture specifies both halves of structural plasticity:

- Growth. Connections form and strengthen via Hebbian co-activation, with update magnitude modulated by arousal.

- Decay and pruning. A connection is a physical commitment of finite substrate — it occupies storage and draws maintenance energy to persist. Pruning is not cleanup; it is the system being unable to afford every prediction it could make and keeping the ones that pay.

- Survival rule. Survival is a function of accumulated weight (lifetime reinforcement), not recent activation alone — avoiding the failure mode where a critical but recently-inactive connection is pruned. This is consistent with significance treated as connection-weight geometry.

- Energy coupling. Maintenance has metabolic cost, so chronic energy depletion raises pruning pressure and degrades existing structure over time, not just new learning. This is the architectural basis for the chronic-fatigue / depression / burnout signatures in the neurological research application.

- Circadian timing. Pruning runs on the sleep window aligned to Eden’s day/night cycle, sequenced after consolidation, never before — reversing the order would prune connections consolidation was about to reinforce.

- Emergent ratio. The connections-per-node ratio is not a design parameter; it emerges from the growth and pruning economy, and different regions settle at different ratios depending on what they compute. The design task is specifying growth and pruning rules that let the right ratio emerge, not picking a number. Prior-art reference for balanced pruning/regeneration: SD-SNN (Han et al., 2022).

### **Quantitative Growth and Pruning Rules**

These rules govern how the connection economy reaches structural equilibrium. Constants are placeholder-seeded and replaced empirically during Genesis runs. The form of the equations is fixed; the values are tuned to produce honest structural pacing.

**Growth rule**

When two nodes co-activate within the temporal contiguity window, connection weight increases by:

Δw_growth = η × A × e^(-Δt/τ_stdp)

Where:

- η = base learning rate (small, empirically calibrated)

- A = arousal at time of co-activation (from internal state)

- Δt = time between the two activations

- τ_stdp = spike-timing window constant, derived from the Genesis physics timestep at runtime — not hardcoded. Physics sets the timescale.

**Passive decay rule**

Every timestep, every connection loses:

Δw_decay = -δ × w × (1 + α × depletion_depth)

Where:

- δ = baseline decay rate

- w = current connection weight

- α = energy coupling coefficient

- depletion_depth = (E_slow_max − E_slow) / E_slow_max (same term from the energy model)

Passive forgetting runs at baseline. Chronic energy depletion accelerates structural degradation. The burnout/depression/chronic-fatigue signatures in the neurological research application emerge from this equation, not from special-cased logic.

**Survival threshold**

During the circadian pruning window, any connection where:

w \< w_min

is pruned. w_min is not hardcoded — it is a function of current total connection count relative to the hardware budget ceiling:

w_min = f(current_connections / hardware_ceiling)

When the network is sparse, w_min is low — connections are cheap to maintain. As the network approaches the ceiling, w_min rises — only the strongest connections survive. The system self-regulates toward the ceiling without being told what the ratio should be.

**Equilibrium and emergent ratio**

At steady state, growth rate equals decay rate for the surviving connection population. That equilibrium point is the emergent conn/node ratio for that region. Different regions settle at different ratios because different prediction problems demand different connection densities. The ratio is a measurement of what the region computes, not a design parameter.

Structural ceiling as physical budget. The brain is the running process itself, not a data structure operated on from outside; the structural ceiling is literally the physical compute budget of the target hardware, not an arbitrary configuration value. Implementation budget and the two-tier (VRAM working set / DRAM full store) memory model are tracked in the Development Log pending empirical measurement.

*Depends on: All predictive core levels. Internal state (arousal for growth magnitude; energy for maintenance and pruning pressure). Circadian cycle for pruning window.*

### **Conflict Detection**

Conflict detection between competing signals. Error monitoring. Attention reallocation.

- Detects conflict between competing goal representations.

- Output: conflict magnitude signal to the goal maintenance component and attention reallocation.

*Depends on: Predictive core. Goal maintenance signal (when active).*

## **3.6 Memory Architecture**

Three distinct systems with explicit interfaces. Episodic-to-procedural consolidation runs during low-arousal periods. Episodic retrieval feeds back into working memory as prior context.

### **Working Memory**

Seconds timescale. Active contents of current predictive processing. Limited capacity forces prioritization. Contents = current attention window.

*Depends on: Sensory encoding output. Episodic retrieval. Internal state for capacity modulation.*

### **Episodic Memory**

Minutes to days. Physical event traces with sensory features, efference copy context (command trace and attenuation level), prediction errors, and arousal at encoding. Arousal at encoding determines trace strength. Prospective simulation output wired to the significance encoder.

*Depends on: Working memory contents. Internal state (arousal level).*

### **Procedural Memory**

Persistent. Accumulated Hebbian structural changes consolidated into network topology. Knowledge embodied in architecture. Consolidation from episodic during low-arousal periods.

*Depends on: Episodic memory. Consolidation gating window.*

### **Consolidation Gating**

Episodic-to-procedural consolidation requires two conditions to hold simultaneously: arousal below threshold AND energy above threshold. High arousal during encoding produces strong trace formation; consolidation operates separately and requires low arousal to run, since the system cannot simultaneously write new traces and integrate accumulated traces into topology. Energy must remain above a minimum threshold, since topology reshaping requires sustained processing capacity. Chronic failure to enter the consolidation window produces accumulated unconsolidated traces. Pruning is sequenced after consolidation within the same circadian window.

*Depends on: Internal state arousal and energy levels. Circadian cycle.*

### **Significance Encoder**

Reads significance weight from reactivated episodic traces. Drives the neuromodulatory arousal broadcast. Significance is geometry — a Hebbian connection weight set at encoding time, rather than a stored field. Input: episodic reactivation and prospective simulation output. Output: arousal broadcast proportional to connection weight.

*Depends on: Episodic memory. Episodic reactivation.*

## **3.7 Concept Formation**

### **Cell Assemblies**

Stable activation patterns form when episodic traces share consistent core signatures across sufficient repetitions. Concept formation is observed, not programmed.

- Pattern accumulation: recurring activation signatures.

- Stability threshold: repetition required before candidacy.

- Generalization: observed during normal operation when a candidate pattern activates on novel input. Never triggered as a test. The network operates without awareness of evaluation.

- Concept interaction: higher-order emergence from intersecting assemblies, including cross-modal assemblies binding force, sound, and visual signatures of the same physical event.

- Vector embeddings: serialized activation signatures available to the registry.

*Depends on: Episodic and procedural memory. Predictive core stability.*

## **3.8 Goal Maintenance and Inhibition**

### **Goal Maintenance Component**

Goal maintenance via sustained top-down relevance bias. Inhibition of competing motor programs. Temporal bridging across delays.

- Goal maintenance: sustained top-down relevance bias against bottom-up salience, delivered to sensory encoding.

- Inhibition: counter-signal to predictive core suppressing competing responses.

- Temporal bridging: sustained significance-encoder return loop across delays.

*Depends on: Stable concept clusters in procedural memory. The component is present from start; its outputs become meaningful when concept formation produces stable physical property representations.*

### **Goal-Directed Concept Formation**

Once goal maintenance is operational, concept formation gains a second driver alongside passive statistical accumulation.

- Passive driver: statistical accumulation from undirected exploration.

- Active driver: goal-directed repetition shapes concept stability. Goal-relevant patterns stabilize faster than incidentally-observed patterns.

*Depends on: Goal maintenance operational. Concept formation operational.*

## **3.9 Language Acquisition**

### **Symbol Grounding**

Language attaches to already-formed physical concepts via Hebbian pairing. The system operates without a pretrained language model. The symbol grounding problem resolves by construction.

- Pre-verbal concept storage: vector embeddings representing physical understanding before words exist.

- Internal tagging: proto-symbolic compression emerging from repeated concept activation.

- Pairing mechanism: label correlated with concept activation repeatedly produces Hebbian connection strengthening.

- Grounded symbol: word activates concept, concept connects to physical traces.

*Depends on: Stable, well-formed concept clusters from procedural memory.*

# **4. Concept Registry — Monitoring Layer**

The registry is the only observation window into the developing system. It is architecturally isolated.

- Asynchronous: runs in a separate process with separate memory space (may live in the DRAM tier).

- Read-only: receives snapshots of network activation states; never writes back.

- Operates outside any learning component path: cannot send signals, adjust parameters, modify thresholds, or influence consolidation.

- Logs: concept candidates, formation time, stability score, generalization breadth.

- The network has no representation of the registry’s existence.

The registry recognizes when the network has already formed a concept. Passive recognition, not active classification. Specialization — node populations consistently activating on particular channels or cross-modal patterns — should become visible here as emergent topographic structure, not as anything engineered.

### **Observation Views (Planned)**

Beyond the concept log, two observation views are planned, both pure read-only and non-influencing: a first-person view (the raw stereo visual feed from Arche’s own cameras) and a third-person view (an external Genesis camera observing the body in Eden). A live map of emerging specialization is a planned visualization goal alongside the static log.

# **5. The Core Loop**

The core loop runs continuously. Prediction error is the only learning signal. Physics is the judge.

World State (Genesis)

→ Sensory Encoding (biased competition, finite bandwidth, multi-rate)

→ Predictive Core (3 levels, Hebbian + cascading)

→ Prediction Error (neuromodulatory broadcast)

→ Memory Write (episodic trace, arousal weighted)

→ Registry Snapshot (read only, silent observer)

# **6. Emergence Phases — Registry Observation Baseline**

The architecture runs the core loop continuously from start. Phases are labels the registry uses to describe what it observes. They do not appear in the operational architecture.

**Genesis**

Environment exists. Body exists. Physics runs. Core loop active. Bandwidth ceiling sits near minimum because the relevance signal is unstructured. Bootstrapping chaos is the expected behavioral signature — amplified by the richer humanoid body. Concept candidates do not yet appear in the registry.

**Anima**

Registry observes systematic differences between self-generated and externally-driven prediction errors, and the self/world distinction becomes decodable from the predictive core’s internal state — scored by the registry against ground truth the system never sees, and above a yoked control whose actions are not causal. Efference copy consistency patterns demonstrate that the self/world boundary has begun resolving. Concept candidates may begin appearing in unstable form.

**Substrate**

Registry observes stable physical property concept clusters: mass, friction, causality, object permanence. Concept formation has produced sufficient stable representations to serve as substrate for goal-directed processing. Goal maintenance dependencies are met from this point onward.

**Logos**

Registry observes stable causal relational concepts. Language pairing is introduced. Symbols attach to existing concept clusters via Hebbian pairing. Reasoning signatures are identifiable.

**Telos**

Registry logs behavior with no seeding interaction. Self-directed exploration and concept formation continue without external input. The system moves through its environment as the expression of what it has become — fulfillment of the architecture’s nature given honest conditions and sufficient time. The destination was not imposed; it was latent in the design from Genesis.

# **7. Implementation Stack**

- Python 3.12 — orchestration, environment layer, memory systems, registry, rapid iteration.

- C++ / Cython / Numba — hot paths in core learning loop.

- PyTorch 2.9.1 — GPU tensor compute via ROCm. Installed from AMD official wheels (repo.radeon.com). Autograd optional.

- Genesis — physics engine. Installed from source (post v0.4.7). Python-native API. AMD ROCm backend confirmed working via gs.init(backend=gs.amdgpu). Headless operation confirmed via show_viewer=False.

- Luisa — ray-tracing renderer via Vulkan for stereo vision (Nyx is CUDA-only and unavailable on AMD hardware).

- ROCm 7.2.2 — GPU acceleration on AMD Radeon RX 6800XT (RDNA 2). Installed via AMD official package repository.

- Mamba / Miniforge — Python environment management. Project environment: arche.

- Ubuntu 26.04 LTS — operating system. Requires a libxml2 symlink for Genesis AMD-backend JIT compilation (see Development Log).

# **8. Changelog**

**v4.8 — Self/world boundary as emergent, not labeled**

- Section 1: added the commitment “Machinery, not content.” Mechanisms are designed priors and are named as such; categories, including self/world, are never designed or labeled.

- Section 3.1 Efference Copy Mechanism: rewritten. The efference copy goes to the forward model and, as a command trace, into the sensory stream. Self/world attribution is no longer produced by a component; the distinction emerges as a consistency pattern and is observed by the registry. Only command-driven prediction is attenuated: predictable is not the same as self-caused.

- Section 3.1 encoding gap note: corrected. Ye (2026) crossed the encoding gap with an action trace fed back as input, not with consequence sensing, which was already present. v4.7 attributed the crossing to joint-state proprioception, which Ye did not test. Arche now routes a command trace into the sensory stream; whether joint state alone suffices is recorded as an open question.

- Section 3.2 Kinesthetic / Proprioceptive Force: architectural role revised. Proprioception is the consequence side of the self/world comparison, not the mechanism that crosses the encoding gap.

- Section 3.3: Self/World Tagging replaced by Reafference Attenuation. Continuous attenuation of command-predicted sensation; no labels. Resolves a contradiction between v4.7’s Section 3.1 (distinction emerges) and Section 3.3 (efference copy tags).

- Section 3.6: episodic traces store efference copy context instead of tags.

- Section 6 Anima: the boundary is evidenced by decodability from internal state, scored against ground truth and above a yoked control.


**v4.7 — Proprioception as load-bearing mechanism for self/world boundary legibility**

- Section 3.1 Efference Copy Mechanism: added encoding gap note. Documents that efference copy generates implicit causal knowledge (predictive compensation for self-caused error) but does not by itself produce readable self-representation. Proprioception (Section 3.2) is explicitly designated as the mechanism that crosses this gap — writing action history into the sensory input stream so the self/world boundary becomes a representable feature, not just a predictive accuracy difference. Motivated by Ye 2026 (arXiv:2606.05605), which empirically demonstrated this dissociation in a minimal predictive system.

- Section 3.2 Kinesthetic / Proprioceptive Force: added architectural role note. Elevates proprioception from sensory channel to dual-function component — sensory input for motor calibration AND the architectural pathway through which implicit causal knowledge becomes explicit self-representation. Cross-referenced to the encoding gap note in Section 3.1.

**v4.6 — Embodiment, sensory completion, structural plasticity, node spec, quantitative pruning rules**

- Section 3.1 Embodiment: polygonal body placeholder replaced with a fully specified bipedal humanoid body (human DOF ceiling, URDF-sourced joint limits, balance and finger articulation as load-bearing prediction surfaces, body surface as visual prediction substrate). Efference copy updated to reference the full kinematic chain.

- Section 3.2 Sensory Primitives: all channels confirmed active from entry. Stereoscopic photoreception specified (Luisa/Vulkan, raw RGB+depth+disparity, depth privileged, no engineered features). Stereo audition added (physics-grounded synthesis from Genesis contact data, ITD/ILD spatial positioning, HRTF deferred).

- Section 3.3: added Sampling Rate Asymmetry (vision at render rate, mechanoreception at physics rate, audition at its own rate). Self/world tagging extended to self-caused visual change.

- Section 3.5 Predictive Core: Level 1 updated to receive all raw channels and perform self-visual prediction; Levels 2 and 3 updated for cross-modal binding and slow environmental regularities. Added Node Specification, Fixed Node Population, Structural Plasticity and the Structural Ceiling (growth + decay/pruning, survival by accumulated weight, energy coupling, circadian timing, emergent conn/node ratio), and Quantitative Growth and Pruning Rules (Δw_growth, Δw_decay, w_min, equilibrium condition). τ_stdp derived from Genesis physics timestep at runtime. Closes the structural-ceiling gap (Findings 1–5) and the quantitative rules gap.

- Section 3.4 Energy: noted that the bipedal body makes the energy model more physically honest. Structural maintenance added to the list of processes internal state modulates.

- Section 4 Registry: added planned first-person and third-person observation views and the emergent-specialization visualization goal.

- Section 7: Luisa renderer and libxml2 note added.

**v4.5 — Final phase renamed**

- Section 6: Prometheus renamed to Telos. The phase describes self-directed behavior as the fulfillment of the architecture’s nature given honest conditions and sufficient time, not capability seized through transgression.

**v4.4 — Implementation stack verification and environment update**

- Section 2 and Section 7 updated to reflect the verified environment (ROCm 7.2.2, PyTorch 2.9.1 AMD wheels, Genesis amdgpu backend, Python 3.12, Mamba/Miniforge, Ubuntu 26.04). Development Log introduced as authoritative record for operational progress.

**v4.3 — Architecture/biology decoupling**

- All biological structure names and neurotransmitter analogs removed from the architecture specification; biological mappings live exclusively in the Brain Model Mapping document. Section headings renamed to functional terms.

**v4.2 — Learning stack clarification and Gap 4 closure**

- Three-layer local plasticity stack description added. Gap 4 (Prefrontal Layer Designation) closed.

**v4.1 — Energy specification expansion and source-grounded corrections**

- Two-component energy recovery model specified. Consolidation gating added. Section 2 corrected to remove unsupported capability confirmations.

**v4.0 — Function-based restructuring**

- Document restructured around functional components and dependency relationships. Phases relocated to Section 6 as registry observation baseline.

*Project Arche — Architecture Specification v4.8*
