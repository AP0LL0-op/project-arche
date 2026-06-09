**PROJECT ARCHE**

*Architecture Specification — v4.6*

# **1. Design Principles**

Project Arche is a developmental cognitive architecture built from first principles. The system is composed of functional components with explicit dependency relationships. Each component becomes active when its required inputs exist.

This document specifies the architecture in functional terms only. Biological analogs for each component — the brain structures whose function each component implements — are documented in the companion Brain Model Mapping document. The architecture specification does not depend on those mappings being correct; if a mapping turns out to be wrong, the functional specification stands unchanged.

Core architectural commitments:

- Grounded cognition. The system operates without symbolic scaffolding and without pretrained representations. All concepts emerge from physical interaction with a consistent environment.

- Prediction error as the only learning signal. The system operates without a reward function, without batch training, and without backpropagation.

- Local plasticity only. Hebbian co-activation is the foundational mechanism. Spike-timing dependence, neuromodulatory gating, and oscillatory phase windows constrain when and how much Hebbian updating occurs. No backpropagation, no global error signals, no batch training.

- Finite resources. Bandwidth, working memory, energy, and structural capacity are capped. These constraints affect system behavior directly.

- Dependency-driven activation. Components activate when their inputs exist.

- Passive observation. The registry observes the system without influencing it.

# **2. Physics Engine Substrate**

Genesis (Genesis-Embodied-AI/Genesis). The Genesis project technical report is dated December 2024 (Genesis Authors, Genesis: A Generative and Universal Physics Engine for Robotics and Beyond, https://github.com/Genesis-Embodied-AI/Genesis). Capabilities relevant to Arche per official sources: Python-native API; unified rigid body, MPM, SPH, FEM, PBD, and stable fluid solvers; explicit material parameters including stiffness, elasticity, damping, friction; reported simulation speed 10 to 80 times faster than Isaac Gym/Sim/Lab and MuJoCo MJX. GPU-accelerated backend confirmed working on the development hardware. Detailed capability sourcing and verification status documented in the Brain Model Mapping.

The physics engine is integrated with the cognitive architecture. Oscillator frequencies, behavioral timescales, and encoding grain are derived from physics environment parameters at runtime. The Genesis environment design — specified in the Environment design document — is the other half of the cognitive substrate.

# **3. Functional Architecture**

The system is specified as a set of functional components with explicit input dependencies. All components are present from system start. Each becomes operationally meaningful when its dependencies are satisfied.

## **3.1 Embodiment**

### **Bipedal Humanoid Body**

A physical body inhabiting the Genesis environment. Bipedal humanoid morphology with a full human kinematic chain. The body is inherited complete at system start; only cognition develops. The richer kinematic chain (relative to a simple effector) is an architectural choice: it produces a richer efference copy signal, a more complex self/world boundary resolution problem, and a denser cross-modal prediction surface.

- Mass, volume, and collision surface across all body segments.

- Full human degrees of freedom as the kinematic ceiling: spine (cervical, thoracic, lumbar), shoulders (ball joints), elbows, wrists, fingers (three joints per finger, two per thumb, independent actuation), hips (ball joints), knees, ankles, neck.

- Joint limits, damping, and torque specified per joint via an inherited or adapted human URDF. Genesis accepts URDF natively and handles the physics of the articulated chain.

- Bipedal balance is a continuous prediction problem that keeps the sensorimotor system engaged and produces ongoing low-level prediction error.

- Independent finger articulation provides a dense cross-modal surface: manipulation produces simultaneous proprioceptive, visual, and contact predictions, with the hands visible in the visual field.

- The body surface is a visual prediction substrate. Skin appearance varies with illumination, and hair provides continuous low-amplitude visual motion tied to both self-movement and environmental wind; both serve as efference copy test cases. Appearance is non-overtly human. Aesthetic detail is an implementation concern and does not affect the functional specification.

Motor output at start is uncalibrated. Force and motor calibration develop through interaction with the environment.

*Depends on: Genesis physics engine.*

### **Efference Copy Mechanism**

Self/world boundary generator. Every motor action produces a paired predictive signal simultaneously.

- Consistent match between predicted and observed outcome produces self attribution.

- Mismatch produces world attribution.

- Self/world distinction emerges as a consistency pattern from this mechanism. The richer the kinematic chain, the richer this signal.

*Depends on: Humanoid body. Motor output across the kinematic chain.*

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

### **Static and Dynamic Contact Force**

Surface boundary, contact intensity, distribution, directionality.

- Encodes location, magnitude, duration, gradient.

*Depends on: Body collision surface. Genesis contact reporting.*

### **Stereoscopic Photoreception**

Bifocal depth-native vision. Two cameras with fixed baseline separation mounted on the body, rendered through a physics-principled ray-tracing renderer producing RGB and depth.

- Raw outputs: left RGB, right RGB, left depth, right depth, stereo disparity map.

- Raw signal enters the predictive hierarchy. Features are not engineered; they emerge from prediction error (Rao & Ballard). Renderer segmentation output is deliberately unused — the system must not receive pre-labeled object boundaries.

- Depth is privileged as the most physically grounded visual channel — it is geometry derived from ray geometry rather than statistically inferred.

- Vision extends the predictive horizon beyond contact: predictions form about objects before contact, producing cross-modal prediction error at the moment of contact.

*Depends on: Genesis rendering pipeline. Two-camera body configuration.*

### **Stereo Audition**

Vibration-based audition, active from entry. Genesis has no native audio; the auditory signal is generated by physics-grounded synthesis from Genesis contact data, so sound shares the same physical substrate as mechanoreception.

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

### **Self/World Tagging**

Efference copy signal tags incoming sensory data as self-generated or externally-driven. Applies across all channels, including self-caused visual change (e.g., a limb or hair moving in the visual field).

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

E_slow(t) = E_slow_max × (1 − e^(−t/τ_slow))   where τ_fast << τ_slow

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

Three hierarchical levels operating at different timescales. Top-down predictions cascade downward. Bottom-up error signals propagate upward, filtered at each level. Learning proceeds via local plasticity: Hebbian co-activation as the foundational rule, modulated by spike-timing dependence, neuromodulatory broadcasting, and oscillatory phase windows. A GPU tensor compute layer (e.g., PyTorch) provides the underlying array operations.

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

- Slow regularities consolidate here: the day/night lighting cycle, stable ravine geometry, fauna movement patterns, and the body's own appearance across lighting conditions.

*Depends on: Stable Level 2 predictions. Long-term memory consolidation.*

### **Local Plasticity Stack**

Three distinct mechanisms operate together to produce the learning behavior of the predictive core. They are not interchangeable.

- Learning rule. How weights change locally. Hebbian co-activation is foundational. Spike-timing dependence and homeostatic normalization refine when and how much co-activation produces a weight change. Structural plasticity allows topology itself to reshape with experience — both growth and decay (see Structural Plasticity and Structural Ceiling below).

- Credit assignment. How useful updates become localized. Neuromodulatory broadcasting, temporal contiguity, and cascading prediction reshaping.

- Systems coordination. How distributed components synchronize. Oscillatory phase coupling, bandwidth gating, attentional competition, and biased competition at the sensory encoder.

Hebbian updating is the foundational rule. The remainder of the stack constrains when and how much it occurs. The architecture rejects backpropagation, global error signals, and batch training; it draws on the broader local plasticity literature.

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

Connections compete for a fixed resource budget. The architecture specifies both growth and decay:

- Growth. Connections form and strengthen via Hebbian co-activation, with update magnitude modulated by arousal.

- Decay and pruning. A connection occupies storage and draws maintenance energy to persist. Pruning removes connections the system cannot afford to maintain, retaining those with sufficient accumulated weight.

- Survival rule. Survival is a function of accumulated weight (lifetime reinforcement), not recent activation alone — avoiding the failure mode where a critical but recently-inactive connection is pruned. This is consistent with significance treated as connection-weight geometry.

- Energy coupling. Maintenance has metabolic cost, so chronic energy depletion raises pruning pressure and degrades existing structure over time, not just new learning. This is the architectural basis for the chronic-fatigue / depression / burnout signatures in the neurological research application.

- Circadian timing. Pruning runs on the sleep window aligned to the Environment's day/night cycle, sequenced after consolidation, never before — reversing the order would prune connections consolidation was about to reinforce.

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

w < w_min

is pruned. w_min is not hardcoded — it is a function of current total connection count relative to the hardware budget ceiling:

w_min = f(current_connections / hardware_ceiling)

When the network is sparse, w_min is low — connections are cheap to maintain. As the network approaches the ceiling, w_min rises — only the strongest connections survive. The system self-regulates toward the ceiling without being told what the ratio should be.

**Equilibrium and emergent ratio**

At steady state, growth rate equals decay rate for the surviving connection population. That equilibrium point is the emergent conn/node ratio for that region. Different regions settle at different ratios because different prediction problems demand different connection densities. The ratio is a measurement of what the region computes, not a design parameter.

Structural ceiling as physical budget. The brain is the running process, not a data structure operated on from outside. The structural ceiling is the physical compute budget of the hardware the system runs on, rather than a configuration value. The implementation budget and the two-tier memory model (a fast working-set tier and a larger full-store tier, with cold connections paged into the working set on demand) are tracked operationally pending empirical measurement.

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

Minutes to days. Physical event traces with sensory features, efference copy tags, prediction errors, and arousal at encoding. Arousal at encoding determines trace strength. Prospective simulation output wired to the significance encoder.

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

- Asynchronous: runs in a separate process with separate memory space (may live in the full-store memory tier).

- Read-only: receives snapshots of network activation states; never writes back.

- Operates outside any learning component path: cannot send signals, adjust parameters, modify thresholds, or influence consolidation.

- Logs: concept candidates, formation time, stability score, generalization breadth.

- The network has no representation of the registry's existence.

The registry recognizes when the network has already formed a concept. Passive recognition, not active classification. Specialization — node populations consistently activating on particular channels or cross-modal patterns — should become visible here as emergent topographic structure, not as anything engineered.

### **Observation Views (Planned)**

Beyond the concept log, two observation views are planned, both pure read-only and non-influencing: a first-person view (the raw stereo visual feed from Arche's own cameras) and a third-person view (an external Genesis camera observing the body in the Environment). A live map of emerging specialization is a planned visualization goal alongside the static log.

# **5. The Core Loop**

The core loop runs continuously. Prediction error is the only learning signal.

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

Registry observes systematic differences between self-generated and externally-driven prediction errors. Efference copy consistency patterns demonstrate that the self/world boundary has begun resolving. Concept candidates may begin appearing in unstable form.

**Substrate**

Registry observes stable physical property concept clusters: mass, friction, causality, object permanence. Concept formation has produced sufficient stable representations to serve as substrate for goal-directed processing. Goal maintenance dependencies are met from this point onward.

**Logos**

Registry observes stable causal relational concepts. Language pairing is introduced. Symbols attach to existing concept clusters via Hebbian pairing. Reasoning signatures are identifiable.

**Telos**

Registry logs behavior with no seeding interaction. Self-directed exploration and concept formation continue without external input. The system operates on its own across the environment, reflecting the structure it developed over the preceding phases rather than any externally imposed objective.

# **7. Implementation Stack**

- Python 3.12 — orchestration, environment layer, memory systems, registry, rapid iteration.

- C++ / Cython / Numba — hot paths in core learning loop.

- A GPU tensor compute layer (e.g., PyTorch) — array operations on the accelerator. Autograd optional.

- Genesis — physics engine. Python-native API. GPU-accelerated backend. Headless operation supported.

- A physics-principled ray-tracing renderer for stereo vision (RGB + depth).


- A Python environment manager.

- A Linux operating system.

# **8. Changelog**

**v4.6 — Embodiment, sensory completion, structural plasticity, node spec, quantitative pruning rules**

- Section 3.1 Embodiment: polygonal body placeholder replaced with a fully specified bipedal humanoid body (human DOF ceiling, URDF-sourced joint limits, balance and finger articulation as load-bearing prediction surfaces, body surface as visual prediction substrate). Efference copy updated to reference the full kinematic chain.

- Section 3.2 Sensory Primitives: all channels confirmed active from entry. Stereoscopic photoreception specified (ray-traced RGB+depth+disparity, depth privileged, no engineered features). Stereo audition added (physics-grounded synthesis from Genesis contact data, ITD/ILD spatial positioning, HRTF deferred).

- Section 3.3: added Sampling Rate Asymmetry (vision at render rate, mechanoreception at physics rate, audition at its own rate). Self/world tagging extended to self-caused visual change.

- Section 3.5 Predictive Core: Level 1 updated to receive all raw channels and perform self-visual prediction; Levels 2 and 3 updated for cross-modal binding and slow environmental regularities. Added Node Specification, Fixed Node Population, Structural Plasticity and the Structural Ceiling (growth + decay/pruning, survival by accumulated weight, energy coupling, circadian timing, emergent conn/node ratio), and Quantitative Growth and Pruning Rules (Δw_growth, Δw_decay, w_min, equilibrium condition). τ_stdp derived from Genesis physics timestep at runtime. Closes the structural-ceiling gap (Findings 1–5) and the quantitative rules gap.

- Section 3.4 Energy: noted that the bipedal body makes the energy model more physically honest. Structural maintenance added to the list of processes internal state modulates.

- Section 4 Registry: added planned first-person and third-person observation views and the emergent-specialization visualization goal.


**v4.5 — Final phase renamed**

- Section 6: Prometheus renamed to Telos. The phase describes self-directed behavior that develops given sufficient time and undirected operation.

**v4.4 — Implementation stack verification and environment update**

- Section 2 and Section 7 updated to reflect the verified development environment. Development Log introduced as authoritative record for operational progress.

**v4.3 — Architecture/biology decoupling**

- All biological structure names and neurotransmitter analogs removed from the architecture specification; biological mappings live exclusively in the Brain Model Mapping document. Section headings renamed to functional terms.

**v4.2 — Learning stack clarification and Gap 4 closure**

- Three-layer local plasticity stack description added. Gap 4 (Prefrontal Layer Designation) closed.

**v4.1 — Energy specification expansion and source-grounded corrections**

- Two-component energy recovery model specified. Consolidation gating added. Section 2 corrected to remove unsupported capability confirmations.

**v4.0 — Function-based restructuring**

- Document restructured around functional components and dependency relationships. Phases relocated to Section 6 as registry observation baseline.

*Project Arche — Architecture Specification v4.6*

---

© 2026 [YOUR NAME]. Licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
