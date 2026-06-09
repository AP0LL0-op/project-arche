**PROJECT ARCHE**

*Brain Model Mapping — v3.4*

*Companion document to Architecture Specification v4.6*

# **Changelog — v3.3 to v3.4**

Architecture v4.6 introduced the bipedal humanoid body, completed the sensory channel set (stereo vision and stereo audition), and folded the structural-ceiling / pruning mechanism and the formal node specification into the Local Plasticity Stack. This revision maps that new functional ground to biology, and opens Gap 11.

Changes in this revision:

- Gap 11 opened and specified: synaptic pruning / structural maintenance. Mapped to the decay side of Hebbian plasticity and to astrocyte/microglia maintenance regulators.

- New Section 4A — Structural Maintenance and the Node. Biological grounding for the fixed-node / dynamic-connectivity decision, the node capability set, accumulated-weight pruning, energy-coupled maintenance, and circadian pruning timing.

- Section 3 sensory entries updated: stereo audition added (auditory channel no longer dormant); stereoscopic vision detail expanded; cross-modal binding noted. Cerebellum entry updated for the richer humanoid kinematic chain.

- Section 1A lookup table updated for new and revised component mappings and reference to Architecture v4.6.

- Channel-agnostic node mapping note added: cross-modal plasticity is the biological warrant for one node type whose specialization is emergent, not pre-assigned.

# **Changelog — v3.2 to v3.3**

Architecture v4.3 removed all biological structure names and neurotransmitter analogs from the architecture specification. This document is the single authoritative source for all biological mappings. Section 1A lookup table added; structure tables updated to reference functional components by name and section; gap and cross-reference entries updated to functional component names.

# **Changelog — v3.0 to v3.2**

Gap 4 (Prefrontal Layer Designation) closed when the layer numbering system was retired at v4.0. Brain Stem entry gained the two-component energy recovery grounding (PCr fast component, glycogen/oxidative slow component, asymmetric recovery). Hippocampus entry gained the consolidation gating clarification: consolidation requires arousal below threshold AND energy above threshold simultaneously; biological basis is that slow-wave sleep is low-arousal but high-metabolic.

# **Purpose**

This document is the single authoritative source for all biological mappings in Project Arche. Beginning at Architecture v4.3, the architecture specification is functional-only — it names components by what they do, not by the brain structures whose function they implement. This document carries the biological grounding.

Three disciplines this document enforces:

- Constraint. Biological naming forces fidelity to the actual mechanism and catches architectural drift early. If the biological name does not fit the functional mechanism precisely, either the mapping or the mechanism is wrong.

- Research surface. Every named structure has a literature. Accurate mapping opens that literature as a design resource.

- Neurological simulation precision. The tunable neuromodulatory profiles in the research application become more mechanistically accurate when the underlying structures are correctly identified.

This document is a living companion. When a new architectural mechanism is added to the architecture specification, an entry should be added here before implementation begins. Status fields update as architecture evolves.

**Status Legend**

- PRESENT — Fully implemented in current architecture.

- PARTIAL — Analog exists but mechanism incomplete.

- MISSING — Identified gap, not yet implemented.

- SPECIFIED — Formally specified, pending implementation.

# **Section 1A — Architecture Component → Brain Structure Lookup**

Maps the functional component names used in Architecture v4.6 to their biological analogs. Bidirectional navigation aid.

| **Arche Component (Architecture v4.6)** | **Biological Analog** | **Reference Section** |
| --- | --- | --- |
| Bipedal Humanoid Body (3.1) | Musculoskeletal system / motor periphery | Section 3 — Cerebellum, Somatosensory |
| Efference Copy Mechanism (3.1) | Cerebellar forward model | Section 3 — Cerebellum |
| Sensory Encoding (3.3) | Thalamus | Section 3 — Thalamus |
| Stereo Audition (3.2) | Cochlea + superior olivary complex (ITD/ILD) | Section 3 — Auditory |
| Internal State: Energy (3.4) | Brain Stem / Reticular Formation | Section 4 — Brain Stem |
| Internal State: Arousal (3.4) | Locus Coeruleus / Norepinephrine | Section 1 — Locus Coeruleus |
| Internal State: Prediction Confidence (3.4) | Dopaminergic System (precision weighting) | Section 4 — Dopaminergic System |
| Internal State: Attention (3.4) | Insular cortex; thalamic relevance signal | Sections 3, 5 |
| Credit Assignment: Neuromodulatory Broadcast (3.5) | Dopamine / Norepinephrine broadcast | Section 4 |
| Node / Structural Plasticity (3.5) | Generic cortical neuron + glial maintenance | Section 4A |
| Structural Maintenance / Pruning (3.5) | Astrocyte / microglia regulation | Section 4A |
| Conflict Detection (3.5) | Anterior Cingulate Cortex | Section 4 — ACC |
| Episodic Memory (3.6) | Hippocampus | Section 1 — Hippocampus |
| Procedural Memory (3.6) | Basal Ganglia | Section 4 — Basal Ganglia |
| Significance Encoder (3.6) | Amygdala | Section 1 — Amygdala |
| Oscillatory Timing Signal (3.5) | Medial Septal Nucleus | Section 2 — Medial Septal Nucleus |
| Goal Maintenance Component (3.8) | Prefrontal Cortex | Section 1 — Prefrontal Cortex |
| Symbol Grounding (3.9) | Broca's / Wernicke's Areas | Section 5 — Broca's / Wernicke's |

# **Section 1 — The Core Circuit**

The hippocampal-prefrontal-amygdala-locus coeruleus circuit is the foundation of executive function and internal arousal generation. Goal maintenance integration is designated post-Substrate; it layers on top of an already-coherent physics world model, consistent with human neurodevelopment.

Full circuit: Hippocampus reconstructs predicted state → Amygdala evaluates significance via Hebbian connection weight → Locus Coeruleus fires → plasticity window opens, attention competition biased → Prefrontal Cortex sustains the loop via return signal to amygdala and top-down relevance bias to sensory encoding.

| **Structure** | **Function** | **Arche Component** | **Status** | **Neuro Sim Relevance** |
| --- | --- | --- | --- | --- |
| Locus Coeruleus | Norepinephrine broadcast. Fires on significant prediction error or amygdala relay. Opens plasticity window. | Arousal (3.4); neuromodulatory broadcast (3.5) | PRESENT | NE arousal threshold. Central to ADHD, depression, PTSD. |
| Hippocampus | Episodic encoding and retrieval. Prospective simulation. Phase-sensitive temporal encoding. | Episodic Memory (3.6) | PRESENT | Consolidation rate. Fragmented in PTSD, disrupted in depression. |
| Amygdala | Significance relay. Reads weight from reactivated traces. Drives LC broadcast. | Significance Encoder (3.6) | SPECIFIED | PTSD: strong threat weights. Depression: weakened. Psychosis: fires on ungrounded matches. |
| Prefrontal Cortex | Goal maintenance. Top-down bias. Inhibition. Temporal bridging. | Goal Maintenance (3.8) | SPECIFIED | ADHD: bias decays without dopamine. PTSD: inhibition overwhelmed. |

*Developmental constraint: the goal maintenance component (PFC analog) operates meaningfully only once Substrate is demonstrated in the registry. Concept formation during Genesis through Substrate proceeds via passive statistical accumulation from undirected exploration.*

# **Section 2 — Temporal Encoding Structures**

These structures handle the when-ness of experience. Salience, emotional weight, and sensory texture encode naturally via Hebbian co-activation. Temporal sequence requires a separate phase scaffold. Oscillator frequencies are runtime values derived from physics timescales: gamma clocks from the Genesis physics timestep; theta and delta seed from biological midpoints (~6Hz, ~1Hz) and are replaced empirically as behavioral acts complete and consolidation cycles run.

| **Structure** | **Function** | **Arche Component** | **Status** | **Notes** |
| --- | --- | --- | --- | --- |
| Medial Septal Nucleus | Theta pacemaker. Broadcasts endogenous timing signal to hippocampus for phase-sensitive temporal encoding. | Oscillatory phase coupling (3.5) | SPECIFIED | Gamma: physics timestep. Theta ~6Hz, Delta ~1Hz seeds, replaced empirically. Timing disruption relevant to attention and arousal dysregulation profiles. |

# **Section 3 — Sensory and Encoding Structures**

Transduction, encoding, and initial processing of sensory input. Attention bandwidth ceiling = f(arousal, energy, prediction confidence); confidence is the developmental modulator. Minimum 1–2 concurrent streams at Genesis, maximum 3–6 at maturity.

| **Structure** | **Function** | **Arche Component** | **Status** | **Notes** |
| --- | --- | --- | --- | --- |
| Thalamus | Sensory relay and encoding. Biased competition for attentional selection. Receives top-down relevance bias. | Sensory Encoding (3.3) | PRESENT | Bottom-up salience parameter. Disrupted in psychosis, sensory profiles. |
| Occipital Cortex | Primary visual processing. Edge, motion, depth. | Stereoscopic Photoreception (3.2) | PRESENT | Bifocal depth-native ray tracing. Raw RGB+depth+disparity; depth privileged. Features emerge from prediction error. |
| Cochlea + Superior Olivary Complex | Auditory transduction; ITD/ILD computation for sound localization. | Stereo Audition (3.2) | SPECIFIED | Physics-grounded synthesis from contact data. ITD/ILD spatial positioning. HRTF deferred. No longer dormant. |
| Somatosensory Cortex | Tactile, proprioceptive, pressure. Body surface and force mapping. | Mechanoreceptive Channels (3.2) | PRESENT | Three channels. Material discrimination from prediction error on force waveforms. Tactile-overwhelm profiles. |
| Cerebellum | Forward model for motor actions. Efference copy. Balance and fine motor coordination. | Efference Copy Mechanism (3.1) | PARTIAL | Richer signal under the humanoid chain: bipedal balance and independent finger actuation. Self/world boundary is the cerebellar-analog output. |
| Temporal Cortex | Language comprehension, auditory processing, memory integration. | Memory (3.6); Language (3.9) | PARTIAL | Memory integration present. Auditory now active. Language substrate at Logos. |

*Cross-modal binding note: a single contact event produces a contact-force signature, a synthesized stereo sound, and (often) a visual depth candidate at the same moment and consistent spatial location. Binding across these channels via temporal contiguity is the substrate for unified physical concepts — biologically the role of multisensory integration regions (superior colliculus, posterior parietal, superior temporal sulcus), which are expected to emerge rather than be engineered. Candidate for monitoring via the registry.*

# **Section 4 — Neuromodulatory Structures**

Chemical broadcasting systems that modulate learning, attention, and plasticity. Substrate of the neurological profile simulation application.

| **Structure** | **Function** | **Arche Component** | **Status** | **Notes** |
| --- | --- | --- | --- | --- |
| Dopaminergic System (VTA / SN) | Reward prediction error. Plasticity gating. Salience and pattern significance. | Prediction Confidence (3.4); Credit Assignment broadcast (3.5) | PRESENT | Dopamine broadcast strength. Dysregulated across a range of neurological and psychiatric conditions. |
| Basal Ganglia | Action selection. Inhibition of competing motor programs. Habit formation. Procedural gating. | Procedural Memory (3.6) | PARTIAL | Consolidation from episodic is the BG analog. Action selection pending. Habit-formation profiles. |
| Anterior Cingulate Cortex | Error monitoring. Conflict detection. Attention allocation. | Conflict Detection (3.5) | SPECIFIED | Prediction error weighting. Elevated in autism spectrum and PTSD. Active post-Substrate. |
| Brain Stem (Reticular Formation) | Arousal regulation. Homeostatic drives. Sleep/wake. Energy via two-component metabolic recovery (PCr fast + glycogen slow). | Energy (3.4); Arousal threshold (3.4) | PRESENT | Asymmetric recovery: fast-component rate degrades as slow-component depletion deepens. Chronic slow-component deficit maps to burnout, chronic fatigue, depression fatigue. |

# **Section 4A — Structural Maintenance and the Node**

New in v3.4. Grounds the structural-ceiling mechanism (Architecture 3.5: Node Specification, Fixed Node Population, Structural Plasticity and the Structural Ceiling). Where the rest of the document maps named structures, this section maps a general principle of neural tissue: a brain is a finite physical organ, and connections are physical commitments that cost energy to maintain.

**The node**

The node maps to a generic neuron defined functionally rather than anatomically. The architecture deliberately omits dendrites, axons, and membrane simulation: the biological warrant is that the computationally relevant role of a neuron, for this architecture, is to hold a prediction, compute error, integrate over a time window, fire on threshold, associate via Hebbian co-activation, and cost energy to persist. The node is channel-agnostic. The warrant for one node type whose sensory specialization is emergent rather than pre-assigned is cross-modal plasticity: congenitally blind individuals recruit visual cortex for tactile and auditory processing, and sensory-substitution devices route one modality's signal through another's cortical machinery. Cortex computes whatever signal arrives; specialization is developmental, not intrinsic.

**Fixed node population, dynamic connectivity**

Maps to human neurodevelopment: the infant brain has essentially its full neuron complement, and intelligence emerges through synaptogenesis, reinforcement, and pruning rather than neurogenesis. Arche inherits a complete body and a fixed node population; what develops is connectivity. Concept formation is connection patterns stabilizing into cell assemblies (Hebb).

**Structural maintenance / pruning**

Maps to the decay side of Hebbian plasticity and to glial maintenance regulators — astrocytes and microglia, which in biology physically prune synapses, with activity and complement signaling influencing which connections are removed. Architectural correspondences:

- Survival by accumulated weight, not recent activation — corresponds to long-term potentiation persistence and the protection of consolidated synapses, avoiding loss of important-but-currently-quiet connections.

- Energy-coupled maintenance — corresponds to the metabolic cost of maintaining synapses; chronic metabolic deficit degrades existing structure. This is the structural (not merely functional) basis for the chronic-fatigue / depression / burnout signatures in the neurological research application.

- Circadian pruning timing — corresponds to sleep-dependent synaptic homeostasis (downscaling during sleep), sequenced after consolidation within the same window, aligned to the Environment's day/night cycle.

- Emergent connections-per-node ratio — corresponds to region-specific synaptic density reflecting the prediction problem a region solves; not a set parameter. Prior-art model for balanced pruning/regeneration: SD-SNN (Han et al., 2022).

# **Section 5 — Emergent and Higher-Order Structures**

Either expected to emerge during operation, planned for later phases, or requiring monitoring via the registry. Observed rather than engineered.

| **Structure** | **Function** | **Arche Component** | **Status** | **Notes** |
| --- | --- | --- | --- | --- |
| Default Mode Network | Internal mentation at rest. Prospective memory. Self-referential processing. | Not yet placed | MISSING | May emerge during low-arousal consolidation. Monitor via registry. Hyperactive in depression/rumination. |
| Insular Cortex | Interoception. Internal body-state awareness. Homeostatic integration. | Internal State as a whole (3.4) | PARTIAL | Internal state dimensions approximate insular function. Explicit body-state signal pending. More grounded now given an energy-costly body. |
| Multisensory Integration (SC, PPC, STS) | Binding of signals from multiple modalities into unified percepts. | Cross-modal cell assemblies (3.7) | MISSING | Expected to emerge from temporal-contiguity binding of force/sound/vision. Observe via registry, do not engineer. |
| Broca's / Wernicke's Areas | Language production and comprehension. Symbol-concept binding. | Symbol Grounding (3.9) | MISSING | Planned for Logos. Language emerges rather than being added. |

# **Section 6 — Identified Gaps Summary**

| **Gap** | **Status** | **Notes** |
| --- | --- | --- |
| Gap 1 — Amygdala | CLOSED | Significance as Hebbian connection-weight geometry set at encoding. |
| Gap 2 — Prefrontal Cortex | CLOSED | Goal maintenance, inhibition, temporal bridging. Meaningful once Substrate stability shown. |
| Gap 3 — Default Mode Network | OPEN | May emerge during low-arousal consolidation. Observe, do not engineer. |
| Gap 4 — Prefrontal Layer Designation | CLOSED | Dissolved when layer numbering retired at v4.0. |
| Gap 5 — ACC Upgrade | CLOSED | Conflict detection between competing goal representations defined. Active post-Substrate. |
| Gap 6 — Attention Bandwidth Ceiling | CLOSED | Ceiling = f(arousal, energy, prediction confidence). |
| Gap 7 — Oscillatory Mechanoreception Synthesis | CLOSED | Dissolved by Genesis continuous contact force data. |
| Gap 8 — Substrate/Goal-Maintenance Timing | CLOSED | Substrate is a pre-goal-maintenance milestone, per neurodevelopment. |
| Gap 9 — Energy Recovery Model | CLOSED | Two-component exponential model specified, grounded in Brain Stem entry. |
| Gap 10 — Consolidation Gating Conditions | CLOSED | Requires arousal below threshold AND energy above threshold. |
| Gap 11 — Synaptic Pruning / Structural Maintenance | OPEN (specified) | Opened v3.4. Mapped in Section 4A to decay-side Hebbian plasticity and astrocyte/microglia regulation. Survival by accumulated weight, energy-coupled maintenance, circadian timing, emergent ratio. Implementation pending; SD-SNN (Han et al., 2022) is the reference model. |

# **Section 7 — Naming Conventions**

**In the architecture specification:**

Components are named by what they do. No brain structure names, no neurotransmitter names. The architecture must read coherently as a functional specification without any biological context.

**In this document:**

Biological structures are primary. Each entry maps a brain structure to the functional Arche component(s) that implement its function.

**When a new architectural mechanism is identified, answer before implementation:**

- What is the biological structure that performs this function?

- What is its precise mechanistic role — the computational operation, not the behavioral output?

- What functional component in the architecture corresponds to this structure?

- What structures does it depend on, and what structures depend on it?

- What neurological simulation parameters does it touch, and how?

Biological naming functions as constraint. If the name does not fit the mechanism precisely, the mechanism is wrong. But the name lives here, not in the architecture.

# **Section 8 — Physics Engine Substrate**

Physics engine: Genesis (changed from PyBullet at v3.0). GPU-accelerated backend confirmed working on the development hardware. Capabilities per official sources: Python-native API; unified rigid body, MPM, SPH, FEM, PBD, stable fluid solvers; explicit material parameters (stiffness, elasticity, damping, friction); continuous contact force data; reported 10–80x speed over Isaac Gym/Sim/Lab and MuJoCo MJX. Current release at time of writing post v0.4.7.

**Architectural implications for Arche**

- Oscillatory synthesis layer removed: material discrimination via prediction error on continuous force waveforms.

- Theta bootstrap: gamma anchor derives from the physics timestep; theta and delta seed from biological midpoints and are replaced empirically.

- Vision: stereoscopic via a physics-principled ray-tracing renderer.

- Audition: no native Genesis audio; physics-grounded synthesis from contact data, stereo via ITD/ILD.

- Parallel seed comparison architecturally viable per Genesis capability claims; throughput on target hardware to be measured.

**Open verification tasks**

- Confirm continuous force waveform access at the time resolution required for oscillatory mechanoreception and audio synthesis.

- Confirm the ray-tracing renderer runs on the target hardware; determine camera sensor API surface (RGB, depth, disparity).

- Measure stereo camera frame rate relative to physics timestep; calibrate visual encoding rate.

- Measure simulation throughput for Environment complexity; validate parallel environment scaling.

*Project Arche — Brain Model Mapping v3.4 — Companion to Architecture Specification v4.6*

---

© 2026 [YOUR NAME]. Licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
