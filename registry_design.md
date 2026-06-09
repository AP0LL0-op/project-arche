**PROJECT ARCHE**

*Concept Registry — Monitoring Layer Design*

*v0.1 — June 2026*

*Companion to Architecture Specification v4.6*

# **Purpose**

The registry is the only observation window into the developing system. Architecture Specification Section 4 defines it as an architecturally isolated, asynchronous, read-only monitoring layer that observes the network without influencing it. This document specifies how that layer is built: what it reads, when it reads, what it stores, and what it computes from what it stores.

This document is active, not frozen. The schemas below are provisional. The architecture establishes the constraints the registry must honor — isolation, read-only access, no influence on the network — and those constraints are fixed. The specific field sets, thresholds, and data shapes are working drafts that will be revised once the Genesis build produces real activation data. The discipline is to let the data shapes settle before treating any schema as final. It is easier to add a field than to un-collect noise.

The registry is a companion to the Architecture Specification. It does not restate architecture. It specifies the monitoring layer the architecture calls for.

# **Design Constraints**

These constraints are inherited from Architecture Specification Section 4 and are not subject to revision. Every design decision in this document is made within them.

- Isolation. The registry runs in a separate process with separate memory space. It may live in the full-store memory tier alongside the full connection store and episodic traces.

- Read-only. The registry receives snapshots of network activation state. It never writes back. There is no path — direct or indirect — by which the registry can send signals, adjust parameters, modify thresholds, or influence consolidation.

- No new systems. The registry reads from buffers the brain already maintains for its own purposes. It does not require the brain to compute anything it would not otherwise compute, and it does not introduce new data structures into the brain process.

- Invisibility. The network has no representation of the registry's existence. Nothing in the learning path is aware it is being observed. There is no evaluation signal, no test trigger, no awareness of being measured.

- Passive recognition. The registry recognizes when the network has already formed a concept. It does not classify, label, or decide what a concept is. It detects structure that is already present in the activation data.

# **Architectural Position**

The brain maintains a rolling activation buffer as part of its own operation. This buffer exists because credit assignment requires it: temporal contiguity (Architecture Specification Section 3.5) is time-sensitive, and connections active in the moments leading up to a prediction error are the ones that update. The brain therefore already keeps a recent history of activation state. The registry reads from this existing buffer. It does not create it.

The significance trigger is the neuromodulatory broadcast signal. The brain already computes this signal: significant prediction error triggers a system-wide broadcast that opens the plasticity window (Architecture Specification Section 3.5, Credit Assignment). The registry watches this same signal through the shared-memory boundary. When broadcast magnitude crosses a threshold, the registry takes a snapshot of the current buffer state. No new computation is introduced; the registry observes a value the brain produces regardless.

The data flow is one-directional across the process boundary:

Brain process (maintains rolling activation buffer for credit assignment)

        |

        |  shared memory, read-only, no synchronization that can block the brain

        v

Registry process (polls buffer asynchronously at its own rate)

        |

        |  significance trigger: neuromodulatory broadcast crosses threshold

        v

Snapshot store (full-store memory tier)

        |

        v

Concept candidate detector / behavioral sequence detector (analysis layers)

If the brain runs faster than the registry can poll, the registry misses intermediate states. This is acceptable and by design. The brain never waits on the registry. The shared-memory interface uses no locks or synchronization primitives that could stall the brain process; the registry tolerates missed reads rather than imposing back-pressure.

# **Layer 1 — Buffer Interface**

The registry attaches to the brain's rolling activation buffer as a read-only consumer via a memory-mapped region. The brain writes; the registry reads. The registry polls at its own rate and watches the neuromodulatory broadcast value within the same shared region.

**Window size**

The snapshot captures a rolling window of activation state preceding and surrounding the trigger event. The window size is a small multiple of τ_stdp, the spike-timing window constant. Because τ_stdp is derived from the Genesis physics timestep at runtime (Architecture Specification Section 3.5, Quantitative Growth and Pruning Rules), the window size is also a runtime value rather than a hardcoded constant. Physics sets the timescale; the registry inherits it. The exact multiple is a calibration task during the Genesis build.

**Trigger**

The significance trigger is the neuromodulatory broadcast magnitude crossing a threshold. The threshold value is provisional and will be calibrated against real broadcast signal distributions during the Genesis build: set too low it captures noise, set too high it misses genuine concept-formation events. The trigger is the brain's own signal rather than a registry computation.

# **Layer 2 — Snapshot Store**

When the significance trigger fires, the registry writes a snapshot record to the store in the full-store memory tier. The snapshot is the raw record of a significant internal moment. Provisional schema:

snapshot_id:        uuid

sim_time:           float64    # simulation clock, not wall clock

phase_label:        enum       # Genesis | Anima | Substrate | Logos | Telos

trigger_magnitude:  float32    # prediction error that fired the broadcast

trigger_level:      enum       # L1 | L2 | L3 (predictive core level)

internal_state: {

    energy_fast:            float32

    energy_slow:            float32

    arousal:               float32

    attention:             float32

    prediction_confidence: float32

}

active_nodes:   [(node_id, weight, activation_level)]   # sparse, above threshold only

window_context: [(sim_time, node_id, activation_level)] # rolling window preceding trigger

**Notes on fields**

- sim_time is the simulation clock, never wall-clock time. All cross-referencing between registry data streams and between the registry and human observation notes is done on sim_time.

- phase_label is assigned by the registry based on its own detection criteria, never declared by the brain. Initially every snapshot is Genesis. The registry upgrades the label when the criteria for a later phase are observed in the data (see Phase Labelling below).

- trigger_level distinguishes raw sensorimotor surprise (L1) from violations of slow environmental regularities (L3). The same trigger magnitude means something different at each level, and the developmental trajectory is not legible without this distinction.

- active_nodes is sparse — only nodes above an activation threshold are recorded, not the full population. This keeps snapshot size bounded as the connection economy grows.

- internal_state records all four neuromodulatory dimensions at the moment of the snapshot, with energy split into its fast and slow components per the two-component model. This is the substrate for correlating concept formation with internal state, and later for the neurological simulation application.

# **Layer 3 — Concept Candidate Detector**

This layer runs asynchronously against the snapshot store, entirely within the registry process. It never touches the brain. It looks across snapshot history for recurring activation signatures — the same node cluster co-activating repeatedly, across different trigger contexts, with stable co-activation geometry. A stable recurring signature is the operational definition of a concept candidate, consistent with the cell-assembly account of concept formation in Architecture Specification Section 3.7.

Provisional candidate schema:

candidate_id:           uuid

first_seen:             sim_time

last_reinforced:        sim_time

stability_score:        float32    # consistency of co-activation geometry across appearances

generalization_breadth: float32    # range of trigger contexts the candidate appears in

node_cluster:           [node_id]  # the stable co-activating set

channel_profile: {                 # which sensory channels contribute

    mechanoreception: float32

    proprioception:   float32

    vision:           float32

    audition:         float32

}

cross_modal:    bool               # does activation require multiple channels

status:         enum               # candidate | stable | degrading

**Derived measures**

- stability_score is computed from the variance in co-activation geometry across the candidate's appearances. Low variance — the same nodes firing together reliably — is the signature of a cell assembly forming. High variance means the pattern is not yet a stable concept.

- generalization_breadth measures how many distinct trigger contexts the candidate activates in. A pattern that only ever appears in one specific situation is not generalizing; one that activates across many contexts is becoming a genuine concept.

- channel_profile records which sensory channels contributed to the candidate's activation. This matters for the neurological simulation application: when neuromodulatory parameters are tuned, the channel composition of concept candidates is one of the observable effects.

- status tracks the candidate's lifecycle. A previously stable candidate moving to degrading is itself meaningful data — it can indicate pruning pressure under chronic energy depletion (the burnout/depression structural signature).

# **Layer 4 — Behavioral Log**

The concept candidate detector observes what is forming inside the network. The behavioral log observes what the system is doing in the world. The two are complementary, and the science lives in their relationship: a concept candidate appearing in the detector at the same sim_time that a behavioral pattern stabilizes in the log is evidence the concept is load-bearing — the system is using it, not merely forming it.

The brain already generates motor output, and Genesis already reports contact events, force magnitudes, and body state each physics step. The behavioral log is a structured read on those existing signals, not a new collection system. It operates on discrete interaction events rather than on every physics timestep: a contact lasting a fraction of a second is one behavioral unit, not hundreds of timestep records.

**Event record (provisional)**

event_id:        uuid

sim_time_start:  float64

sim_time_end:    float64

event_type:      enum       # contact | locomotion | posture | orientation

body_part:       [joint_id] # body segments involved

object_id:       uuid       # object in the Environment; null if self-motion

force_profile: {

    peak:          float32

    duration:      float32

    waveform_hash: bytes    # fingerprint of force waveform, not the full waveform

}

spatial_context: {

    body_position:   vec3

    object_position: vec3

    facing_vector:   vec3

}

internal_state_ref: snapshot_id  # nearest snapshot by sim_time, for cross-reference

The waveform_hash is a deliberate economy. Storing full force waveforms for every contact would be expensive; a hash lets the registry recognize when the same material is being contacted again without storing redundant waveforms. Full waveforms are retained only on first encounter per material signature.

**Sequence detector (provisional)**

Above the raw event log sits a sequence detector, structurally the same idea as the concept candidate detector but operating on event chains rather than activation patterns. It looks for recurring sequences of events — the operational form of the door observable states in the Environment design v0.3, and of any other recurring behavioral pattern such as material exploration loops or locomotion stabilizing as balance prediction improves.

sequence_id:      uuid

first_seen:       sim_time

last_seen:        sim_time

event_chain:      [(event_type, object_id, body_part)]  # the recurring pattern

recurrence_count: int

consistency_score: float32   # stability of the sequence geometry across recurrences

concept_refs:     [candidate_id]  # concept candidates active during this sequence

concept_refs is the analytical bridge between the behavioral log and the concept store. When a behavioral sequence recurs and a particular concept candidate is consistently active during it, that co-occurrence is the signal that the concept is functionally load-bearing. The registry can then state a developmental timeline with mechanistic grounding: this concept formed at sim_time X, this behavioral sequence first appeared at sim_time Y, the two began co-occurring at sim_time Z.

# **Phase Labelling**

Phases are labels the registry applies to what it observes; they do not exist in the operational architecture (Architecture Specification Section 6). The registry assigns the phase label by its own criteria, reading the data — the brain never declares a phase. The provisional criteria below follow the emergence baseline in the Architecture Specification and will be refined as real trajectories appear.

- Genesis — default. Core loop active, bandwidth ceiling near minimum, no stable concept candidates in the store.

- Anima — the snapshot store shows systematic, separable differences between self-generated and externally-driven prediction errors (efference copy consistency). Concept candidates may appear in unstable form.

- Substrate — the concept store contains stable physical-property clusters (mass, friction, causality, object permanence). This is the point from which goal-maintenance dependencies are met.

- Logos — stable causal relational concepts present; symbol pairing becomes observable as label-concept co-activation.

- Telos — the behavioral log shows self-directed exploration and continued concept formation with no seeding interaction.

These criteria are detection heuristics, not gates. Nothing in the architecture changes when a label changes. The label is a description the registry produces for the human observer.

# **Alerting**

The registry runs during headless operation, when no human is watching the visual feeds. It therefore needs an alert layer: threshold-based notifications that produce a human-readable record of registry-worthy events during unattended runs. Alerts are write-out only — to a file or notification endpoint per the operator's workflow — and have no path back into the brain. Provisional alert conditions:

- First concept candidate reaching stable status.

- Phase-transition criteria met.

- Behavioral sequence recurrence crossing threshold.

- A previously stable concept candidate beginning to degrade.

- Chronic internal-state depletion pattern detected (slow-component energy deficit persisting across cycles).

- First behavioral sequence involving the door.

The alert layer exists so that an unattended run produces a summary of what happened rather than a raw log to be excavated afterward.

# **Visualization and Observation Views**

Architecture Specification Section 4 names three observation views beyond the concept log: a first-person view (the raw stereo visual feed from Arche's own cameras), a third-person view (an external Genesis camera observing the body in the Environment), and a live map of emerging specialization. All are pure read-only and non-influencing.

**Tooling decision**

No off-the-shelf tool fits the registry data cleanly. The conventional neural-network visualization packages (TorchLens, comgra, and similar) assume layered architectures, gradients, and classification outputs, none of which match a sparse Hebbian node population with significance-triggered snapshots. Fighting those assumptions costs more than it saves.

- Third-person physics feed — use the native Genesis viewer. It renders the simulation frame directly and requires no custom work. This covers the third-person view at no cost.

- First-person feed — the raw stereo camera output already produced by the vision pipeline, surfaced read-only. No new rendering.

- Registry dashboards — a lightweight Streamlit (or equivalent) dashboard reading directly from the registry store. The specialization map is a scatter plot of node populations by channel profile; concept-candidate emergence is a timeline; internal-state trajectories are line charts over sim_time; behavioral sequences are a timeline. All standard plotting, no custom tooling.

A custom tool is justified only if the standard dashboard proves insufficient, which is unlikely for the views described. The visualization layer reads the same store the detectors write; it never reads the brain directly and never writes anything.

# **Open Questions**

- Snapshot window multiple of τ_stdp — the exact multiple is a calibration task once physics-timestep-derived τ_stdp is known and real broadcast events can be inspected.

- Significance threshold — must be calibrated against the real distribution of broadcast magnitudes; provisional until Genesis data exists.

- Concept candidate stability and generalization thresholds — the variance cutoff for stable status and the breadth cutoff for generalization are placeholders pending real co-activation data.

- Waveform hash scheme — the fingerprinting method for force waveforms (what counts as the same material signature) needs definition during the sensory-encoding build.

- Snapshot store growth — retention policy and whether older snapshots are downsampled once their concepts have stabilized is an open storage-management question.

- Behavioral event segmentation — the thresholds that define the start and end of a contact, locomotion, posture, or orientation event need calibration against real body-state data.

# **Revision Log**

**v0.1 — June 2026**

Initial registry design. Established the four-layer structure (buffer interface, snapshot store, concept candidate detector, behavioral log) plus phase labelling, alerting, and the visualization/tooling decision. All schemas marked provisional pending real data shapes from the Genesis build. Buffer interface reads the brain's existing rolling activation buffer; significance trigger is the existing neuromodulatory broadcast signal; window size inherits τ_stdp from the physics timestep at runtime. Tooling decision: native Genesis viewer for the third-person feed, lightweight dashboard (Streamlit or equivalent) for registry data, custom tooling only if proven necessary.

*Project Arche — Concept Registry Monitoring Layer Design v0.1*

---

© 2026 [YOUR NAME]. Licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
