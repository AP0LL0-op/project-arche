**PROJECT ARCHE**

*Research Hypothesis Document — v1.2*

*Research hypothesis and evaluation framework for Project Arche.*

# **Purpose**

This document states the foundational claims, primary hypotheses, secondary hypotheses, neurological simulation hypotheses, open questions, and explicit out-of-scope boundaries for Project Arche. It functions as an evaluation framework, with the registry as the primary instrument for testing the predictions stated here.

This document is a companion to Architecture Specification v4.6 and Brain Model Mapping v3.4. Architectural mechanisms referenced here are fully specified in those documents. This document does not restate architecture — it states what the architecture predicts.

# **Foundational Claims**

These are the premises the entire project rests on. If any of these are false, the project design is wrong at the root. They are stated here, not tested. Testing begins with the primary hypotheses.

### **Claim 1**

Physical reality and internal state are both necessary conditions for grounded intelligence, and neither is sufficient without the other.

### **Claim 2**

Finite resources and genuine consequences are necessary conditions for grounded behavior. Constraints are the mechanism by which a world model becomes honest.

### **Claim 3**

Prediction error against physical reality is the sole trigger for learning. The local plasticity stack determines how learning proceeds, but prediction error is the only signal that initiates it.

# **Primary Hypotheses**

These are direct predictions about what Arche will do. Each hypothesis includes a mechanism, an observable, a falsification condition, and a phase reference. The registry is the primary instrument of evaluation.

## **Primary Hypothesis 1 — Unsupervised Concept Formation**

**Statement**

Stable physical concepts — mass, friction, causality, object permanence — form without instruction, through prediction error alone, given Arche’s architectural conditions.

**Mechanism**

The efference copy mechanism establishes the self/world boundary by tagging prediction errors as self-generated or externally-driven. This boundary is the prerequisite for coherent world model construction. Without it the predictive hierarchy cannot distinguish signal from noise and concept formation cannot proceed.

**Observable**

The registry contains stable concept clusters — mass, friction, causality, object permanence — that were not seeded by external instruction.

**Falsification Condition**

The registry contains no stable concept clusters after sufficient runtime, or concept candidates appear but never stabilize.

**Phase Relevance**

Substrate.

## **Primary Hypothesis 2 — Exponential Developmental Trajectory**

**Statement**

Concept formation follows a slow exponential trajectory. Early development is characterized by high chaos and minimal concept candidacy, accelerating as prediction confidence compounds and the bandwidth ceiling rises.

**Mechanism**

Prediction confidence gates the bandwidth ceiling. Stable predictions raise confidence, which raises bandwidth, which enables richer predictive processing, which produces more stable predictions. The compounding loop drives acceleration.

**Observable**

Registry concept candidate density starts near zero, remains low through early Genesis phase, then rises at an accelerating rate as the system approaches Substrate.

**Falsification Condition**

Concept candidate density rises linearly or randomly rather than accelerating, suggesting the confidence-bandwidth compounding loop is not functioning as specified.

**Phase Relevance**

Genesis through Substrate.

## **Primary Hypothesis 3 — Efference Copy as Prerequisite**

**Statement**

Stable concept candidacy does not emerge prior to self/world boundary resolution. The efference copy consistency patterns that define Anima are a prerequisite for concept formation rather than a parallel process.

**Mechanism**

Without a resolved self/world boundary, prediction errors carry no reliable attribution. The predictive hierarchy cannot build stable representations from ambiguous error signals. Concept candidacy requires the boundary to be sufficiently resolved first.

**Observable**

Registry shows zero stable concept candidates prior to Anima. First concept candidates appear only after efference copy consistency patterns are demonstrable.

**Falsification Condition**

Stable concept candidates appear in the registry before efference copy consistency patterns are observable, suggesting concept formation does not depend on self/world boundary resolution.

**Phase Relevance**

Genesis through Anima.

# **Secondary Hypotheses**

These are downstream predictions that depend on the primary hypotheses holding. They address what Arche predicts beyond Substrate — toward Logos, Telos, and emergent behavior.

## **Secondary Hypothesis 1 — Emergent Criticality**

**Statement**

Arche’s architecture contains mechanisms that together produce a functional analog of self-organized criticality without requiring stochastic noise, through the dynamic interaction of competing drives toward order and chaos.

**Mechanism**

Criticality in biology is maintained at the boundary between ordered and chaotic dynamics. In biological neural systems, this balance is partly sustained by stochastic noise in synaptic transmission. In Arche, four explicit mechanisms create an equivalent tension without noise:

The bandwidth ceiling caps concurrent processing, preventing runaway cascade while preserving sensitivity to novel input.

The energy model with depletion asymmetry creates natural oscillation between high-engagement and recovery states, preventing the system from locking into either pure exploitation or pure exploration.

Arousal modulation of Hebbian update magnitude means high-arousal events drive strong plastic change while low-arousal periods allow consolidation — the same order/chaos tension criticality requires, implemented explicitly rather than stochastically.

The pruning economy continuously removes over-consolidated structure, preventing the network from drifting into rigid order — which is the failure mode criticality theory predicts for subcritical systems.

Together these four mechanisms do not add noise to maintain criticality. They create competing deterministic pressures — toward order through consolidation and pruning, toward sensitivity through arousal and bandwidth — that should dynamically balance at a functional analog of the critical point.

**The Key Difference from Biological Criticality**

Biology maintains criticality partly through stochastic noise preventing lock-in to pure order. Arche replaces stochastic noise with explicit competing deterministic drives. The functional outcome — a system poised between rigid order and chaotic sensitivity — should be equivalent. Whether it actually is equivalent is what the experiment tests.

**Observable**

The registry should show concept candidates that stabilize without becoming rigid. Generalization breadth — the candidate schema field already specified in Registry Design v0.1 — should remain nonzero after stabilization. A system that has drifted subcritical shows candidates with high stability score but collapsing generalization breadth. A system that has drifted supercritical shows candidates that never stabilize at all.

Both failure modes are observable in the registry without adding any new instrumentation.

**Falsification Condition**

Concept candidates consistently show one of two signatures: high stability with collapsing generalization breadth (subcritical drift — system locked into rigid order), or permanent instability with no candidates reaching stable status (supercritical drift — system too sensitive to consolidate). Either signature falsifies the hypothesis that Arche’s deterministic mechanisms maintain functional criticality.

**If the Hypothesis Holds**

Arche demonstrates that explicit competing deterministic drives can replace stochastic noise as the mechanism for maintaining criticality. This has implications beyond this project for how artificial cognitive systems are designed.

**If the Hypothesis Fails**

A noise injection mechanism needs to be added to the architecture. The specific form — whether synaptic noise, threshold jitter, or another mechanism — would be informed by which failure mode the registry reveals. Subcritical failure points toward insufficient arousal range. Supercritical failure points toward insufficient consolidation gating.

**Phase Relevance**

Substrate through Telos. Observable from first stable concept candidates onward.

**Grounding**

Empirical literature on brain criticality establishes that healthy human cortex operates near the edge of chaos during conscious states, that distance to criticality correlates with fluid intelligence, and that departures from criticality accompany loss of consciousness and disrupted information processing. The hypothesis that Arche’s deterministic architecture achieves this regime through explicit mechanism rather than stochastic noise is an original claim specific to this project.

*Remaining secondary hypotheses to be completed. Continue section by section.*

# **Neurological Simulation Hypotheses**

These are claims about specific neuromodulatory parameter configurations producing specific behavioral signatures in the Genesis environment. The evidentiary standard is different from primary and secondary hypotheses — these require a functional Arche before testing can begin.

*Dormant. To be written after a functional Arche exists, once neuromodulatory parameter configurations can be tested directly.*

# **Open Questions**

These are things the project genuinely does not know the answer to. Not hypotheses — no outcome is predicted. These are honest uncertainties the project may resolve during development.

### **Open Question 1 — Minimum Viable Node Count for Stable Concept Formation**

What is the minimum node population at which Arche’s Hebbian cell assembly mechanism produces stable concept candidates? The biological reference provides a rough bound, but Arche’s deterministic float32 substrate may require substantially fewer nodes than biological analogs for equivalent functional outcomes. This question is not answerable from first principles. Genesis runs at progressively scaled node populations will begin to answer it empirically.

### **Open Question 2 — Efficiency Multiplier of Deterministic vs Biological Substrate**

How many Arche nodes are functionally equivalent to one healthy adult human cortical neuron? The biological efficiency analysis conducted during pre-implementation reasoning identified four sources of biological inefficiency: signal reliability redundancy (largely negligible in healthy adult cortex), representational precision, metabolic overhead, and wiring cost. The honest range is approximately 10-200x, with 100x as a defensible central estimate. Whether the real multiplier is sufficient for Telos on current hardware is an open empirical question.

### **Open Question 3 — Noise as Functional Requirement**

Does deterministic float32 computation produce functionally equivalent emergent properties to noisy biological computation, or does the noise floor itself contribute to outcomes the architecture predicts? The criticality hypothesis addresses one dimension of this question. Stochastic resonance — the enhancement of subthreshold signal detection by optimal noise levels — represents a capability biology has that Arche’s clean substrate does not directly implement. Whether Genesis physics produces prediction errors in the subthreshold regime where stochastic resonance would matter is unknown before runs begin.

### **Open Question 4 — Default Mode Network Emergence**

Will a Default Mode Network analog emerge during low-arousal consolidation periods? This is explicitly not engineered. The registry is positioned to observe it if it appears. Its emergence would constitute evidence that the architecture’s consolidation gating produces internal mentation as a byproduct, consistent with the biological DMN’s role in prospective simulation and self-referential processing.

# **Out of Scope**

Project Arche explicitly does not claim the following. These boundaries exist to keep the project honest and to prevent scope drift.

*To be completed.*

# **Revision Log**

**v1.2 — June 2026**

Secondary Hypothesis 1 (Emergent Criticality) added. Open Questions section populated with four entries: minimum viable node count, efficiency multiplier, noise as functional requirement, and Default Mode Network emergence. Companion document version references updated to Architecture v4.6. Hypothesis document version reference corrected from v4.5 to v4.6.

**v1.1 — May 2026**

Final phase reference updated from Prometheus to Telos in Secondary Hypotheses section. Companion document version references updated to Architecture v4.5.

**v1.0 — May 2026**

Initial document. Foundational claims and primary hypotheses established. Secondary hypotheses, neurological simulation hypotheses, open questions, and out-of-scope sections stubbed for continuation.

*Project Arche — Research Hypothesis Document v1.2*

---

© 2026 [YOUR NAME]. Licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
