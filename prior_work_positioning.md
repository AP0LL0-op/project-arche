**PROJECT ARCHE**

*Prior Work and Positioning — Research Report*

*Source material for the Positioning section of the Research Hypothesis Document.*

# **Purpose**

This document maps the prior work landscape relevant to Project Arche and identifies how Arche relates to each comparable effort. The intent is to provide source material for a Positioning section in the Research Hypothesis Document. It is descriptive, not advocacy. Where Arche differs from prior work, that difference is stated. Where prior work has already done what Arche proposes, that overlap is stated honestly.

Six comparators are covered: the Thousand Brains Project / Monty, active inference implementations, the iCub developmental robotics platform, NEUCOGAR, ACT-R and SOAR, and the broader developmental robotics field. Each section follows the same structure: what the project is, what it does, where it overlaps with Arche, and what it is missing that Arche has — or what Arche is missing that it has.

# **1. Thousand Brains Project — Monty**

**What it is**

The Thousand Brains Project is an open-source initiative launched by Numenta in November 2024 and now run as an independent non-profit (partly funded by the Gates Foundation). Its first implementation, Monty, is a sensorimotor learning framework based on Jeff Hawkins's Thousand Brains Theory. The theory holds that intelligence arises from the repeated structure of cortical columns, each of which builds a complete model of objects in its own reference frame, voting together to produce unified perception. The reference paper is Clay, Leadholm, and Hawkins (December 2024), 'The Thousand Brains Project: A New Paradigm for Sensorimotor Intelligence' (arXiv:2412.18354). Follow-up quantitative work: Leadholm et al. (2025), 'Thousand-Brains Systems: Sensorimotor Intelligence for Rapid, Robust Learning and Inference' (arXiv:2507.04494). Code at github.com/thousandbrainsproject/tbp.monty.

**What it does**

Monty consists of sensor modules, learning modules (the cortical column analogs), and a motor system. Each learning module builds structured 3D object representations using explicit reference frames. Modules communicate via a Cortical Messaging Protocol (CMP). Learning is associative and Hebbian-adjacent, with explicit spatial structure as an inductive bias. The system uses sensorimotor interaction in both learning and inference. Movement is foundational — even simple sensory inputs enable complex object learning through active sampling.

**Where it overlaps with Arche**

- Both reject deep learning and backpropagation as foundational mechanisms.

- Both treat sensorimotor interaction as central rather than incidental.

- Both use Hebbian-adjacent local learning rules.

- Both are explicitly brain-inspired at the architectural level rather than at the metaphorical level.

- Both treat embodiment and movement as load-bearing for learning.

**Where Arche differs**

- Internal state. Monty has no neuromodulatory dimensions. No energy, arousal, prediction confidence, or attention as dynamic load-bearing parameters. Arche's four-dimensional internal state is a structural absence in Monty.

- Stakes and finite resources. Monty does not model resource depletion, energy recovery, or constraints that produce honest behavior. There are no consequences in the architectural sense.

- Efference copy mechanism. Monty does sensorimotor learning but does not explicitly tag every motor output with a paired predictive signal for self/world boundary resolution. The Anima-phase mechanism is not present as a load-bearing component.

- Three-system memory. Monty uses learning modules with reference frames. It does not separate working, episodic, and procedural memory with explicit consolidation gating.

- Credit assignment mechanism. Monty handles credit assignment through the modular column structure and reference frames. Arche uses neuromodulatory broadcasting, temporal contiguity, and cascading prediction reshaping — explicitly different mechanisms.

- Neurological simulation capability. Monty's parameters are not designed to map onto dysregulated neuromodulatory systems. Arche's parameter space is explicitly tunable to model dysregulated neuromodulatory systems underlying a range of neurological and psychiatric conditions.

- Phase-structured development. Arche has explicit developmental phases (Genesis, Anima, Substrate, Logos, Telos) with dependencies. Monty does not have an equivalent developmental staging.

**Where Monty has things Arche does not**

- Reference frames. Monty's explicit use of reference frames for 3D object representation is a major architectural commitment. Arche does not have an equivalent. Whether Arche needs one is an open question — reference frames may emerge from concept formation, or they may be a missing component.

- Multi-column voting architecture. Monty distributes object representation across many cortical column analogs that vote on perception. Arche has a single predictive hierarchy rather than a distributed voting structure.

- Quantitative benchmark validation. Monty has published quantitative performance on 3D object recognition tasks (Leadholm et al. 2025). Arche has no such validation yet.

- Operating funding and team. Monty is supported by an institutional structure with funding and full-time researchers. Arche is independent development.

**Honest assessment**

Monty is the closest existing analog to Arche by a significant margin. Both share core architectural commitments — biological grounding, sensorimotor learning, rejection of deep learning, embodiment. The combination of mechanisms that distinguishes Arche (efference copy as self/world boundary generator, four-dimensional neuromodulatory internal state, three-system memory with consolidation gating, credit assignment through three specific local mechanisms, neurological profile simulation as an application) does not appear in Monty. Conversely, Monty's reference frame architecture and voting mechanism do not appear in Arche. The two systems are genuinely different instances of brain-inspired AI built from first principles.

# **2. Active Inference and Predictive Processing Implementations**

**What it is**

Active Inference is the formal framework developed by Karl Friston around the Free Energy Principle. It treats the brain as a generative model that minimizes prediction error by acting on the world (active) and updating internal beliefs (inference). Andy Clark's Predictive Processing is the more accessible philosophical framing. Recent implementations include Çatal et al.'s Cortical Column Networks for object recognition (2022), Hamburg et al. 'Active Inference for Learning and Development in Embodied Neuromorphic Agents' (Entropy, 2024), Priorelli et al. 'Learning and embodied decisions in active inference' (bioRxiv, 2024), and a substantial body of work surveyed in Lanillos et al. (2021) 'Active inference in robotics and artificial agents: Survey and challenges'.

**What it does**

Active inference systems build hierarchical generative models that predict sensory input and minimize variational free energy by either updating the model (perception) or acting on the world (action). Implementations typically use variational message passing across hierarchical levels, often with Bayesian inference machinery. Some implementations are pure software agents (decision tasks, perceptual inference), others are embodied robotic systems.

**Where it overlaps with Arche**

- Prediction error as the central learning signal. This is the foundational commitment shared with Arche.

- Hierarchical generative models. Both Arche's three-level predictive core and active inference's hierarchical message passing follow Rao and Ballard (1999).

- Action as inference. The idea that motor output is part of the same predictive system as perception. Arche's efference copy mechanism implements a version of this.

- Embodiment as necessary. Recent active inference work has converged on the same position Arche holds: embodied implementations are necessary, not optional.

**Where Arche differs**

- Mathematical formalism. Active inference uses variational free energy minimization with explicit Bayesian machinery. Arche does not. Learning proceeds via local Hebbian plasticity refined by spike-timing dependence and neuromodulatory gating, without an explicit variational objective.

- Backpropagation status. Many active inference implementations use backpropagation through hierarchical generative models as a practical optimization choice, even when the theory does not require it. Arche rejects backpropagation absolutely.

- Credit assignment. Active inference handles credit assignment through the variational free energy gradient. Arche uses three specific local mechanisms (neuromodulatory broadcasting, temporal contiguity, cascading prediction reshaping).

- Internal state as load-bearing parameter substrate. Active inference has precision weighting as a key concept, but does not typically formalize energy, arousal, and confidence as separate dynamic dimensions that gate bandwidth and consolidation.

- Neurological profile simulation. Active inference has been used to model some psychiatric conditions (especially psychosis and depression) but not as an explicit tunable parameter substrate spanning the range Arche targets.

- Developmental phase structure. Active inference implementations typically do not have an explicit phase-staged developmental trajectory.

**Where active inference has things Arche does not**

- Formal mathematical foundations. The Free Energy Principle is a unified mathematical framework. Arche's combination of mechanisms is principled but not unified under a single mathematical objective.

- Decades of theoretical development. Active inference has been refined since the early 2000s with substantial neuroscience literature behind it. Arche is new.

- Demonstrated implementations across many domains. Working active inference systems exist for visual object recognition, decision making, motor control, robotics.

**Honest assessment**

Arche is best described as predictive-processing-compatible without being an active inference implementation. The foundational commitments overlap substantially. The mathematical machinery and credit assignment mechanisms differ substantially. Active inference and Arche could be viewed as two different bets on how to implement the same underlying neuroscience theory.

# **3. iCub Developmental Robotics Platform**

**What it is**

iCub is a humanoid robot platform developed since the mid-2000s at IIT (Istituto Italiano di Tecnologia) and used by a global research community. It was designed from scratch as a research platform for developmental robotics — the study of how cognition can emerge from autonomous sensorimotor interaction in a humanoid body. The cognitive architecture has been described across many papers including Metta et al. (2010) 'The iCub humanoid robot: An open-systems platform for research in cognitive development' (Neural Networks) and Vernon et al.'s work on the iCub cognitive architecture. The DAC-h3 architecture (Moulin-Frier et al., 2017) is one recent integrated cognitive architecture running on iCub.

**What it does**

iCub provides a physical humanoid body with dense sensory and motor capability: vision (binocular cameras), audition, vestibular sense, distributed force-torque sensors, whole-body tactile sensors, 53 joint encoders. Cognitive architectures running on iCub typically model hippocampus, basal ganglia, amygdala analogs and use sensorimotor prediction as a developmental driver. The platform supports research on language acquisition, object affordances, imitation, joint attention, and developmental learning.

**Where it overlaps with Arche**

- Developmental approach. iCub research is explicitly developmental — cognition emerges through autonomous interaction over time, not from pretrained representations.

- Embodiment as foundational. iCub is designed around the premise that a physical body is necessary for grounded cognition.

- Biologically grounded architectures. iCub architectures typically include hippocampus, basal ganglia, amygdala, cerebellum analogs.

- Predictive sensorimotor control. The iCub roadmap (von Hofsten, Fadiga, Vernon) treats prediction as central to development.

- Symbol grounding and language acquisition. iCub research explicitly addresses how symbols can attach to physical concepts.

**Where Arche differs**

- Physical vs simulated embodiment. iCub is a physical robot. Arche is embodied in a Genesis physics simulation. This is a real difference — physical robots face genuine wear, noise, calibration drift, and unstaged environmental variation that simulation does not produce. Arche's commitment to physics-honest geometry is partial compensation, not full equivalence.

- Single-developer scale. iCub is a multi-institution research platform with hundreds of contributors over two decades. Arche is one person.

- Neuromodulatory parameter substrate. iCub cognitive architectures include some neuromodulatory analogs (especially basal ganglia / dopamine in DAC-h3) but do not typically expose them as tunable parameters spanning neurological profile simulation.

- Phase-structured development with explicit dependencies. Arche's Genesis-Anima-Substrate-Logos-Telos structure with explicit input dependencies between components is more rigid than the typical iCub architectural framing.

- Three-system memory with consolidation gating. Not typically present as a unified architectural commitment in iCub work.

**Where iCub has things Arche does not**

- Physical embodiment. Genuine sensorimotor noise, calibration drift, mechanical failures, real-world unpredictability.

- Decades of empirical results. Published findings on language acquisition, object affordances, joint attention, imitation, all in a real body.

- Multi-institutional validation. The iCub platform has been used by many independent groups, producing convergent findings about what works and what does not.

- Social and linguistic interaction research. iCub work has substantially developed human-robot interaction research that Arche has not addressed.

**Honest assessment**

iCub is the most established developmental robotics platform and represents the largest accumulated body of work on developmental cognition in embodied AI. Arche shares core developmental commitments with iCub research. The major architectural differences — Arche's neuromodulatory parameter substrate, three-system memory with consolidation gating, efference copy as explicit load-bearing component, neurological simulation application — are real differentiation. The major non-architectural difference is that iCub is a physical robot with decades of empirical results and Arche is a simulation with no results yet. This is a serious gap that empirical work alone can close.

# **4. NEUCOGAR — Neuromodulating Cognitive Architecture**

**What it is**

NEUCOGAR (Neuromodulating Cognitive Architecture) is a cognitive architecture developed by Vallverdú, Talanov, Distefano, Mazzara and colleagues starting around 2015. It explicitly maps monoamine neurotransmitters — dopamine, serotonin, noradrenaline — onto computational parameters in a Von Neumann architecture. Validation work has simulated specific affective states (fear, disgust) using the NEST Neural Simulation Tool with rat brain as the biological model. Reference papers include Vallverdú et al. (2016) 'A Cognitive Architecture for the Implementation of Emotions in Computing Systems' (arXiv:1606.02899).

**What it does**

NEUCOGAR uses Lövheim's three-dimensional cube of emotions, with axes corresponding to the three monoamine neurotransmitters. The architecture maps these to computational parameters — dopamine controls attention, serotonin controls inhibition, noradrenaline affects arousal — and simulates how varying these parameters produces different affective and cognitive behaviors. Validation has focused on demonstrating that emotion-modulated computation reproduces expected patterns of computing resource allocation.

**Where it overlaps with Arche**

- Neuromodulatory parameters as load-bearing architectural elements. Both NEUCOGAR and Arche treat dopamine, norepinephrine and related systems as explicit tunable dimensions rather than implicit details.

- Biological grounding for parameter choices. NEUCOGAR maps to mammalian neurotransmitter systems. Arche maps to the same systems.

- Architectural separation of neuromodulatory dynamics from core computation. Both systems treat neuromodulation as orthogonal to the substrate.

**Where Arche differs**

- Embodiment. NEUCOGAR is not embodied. It runs as a simulation of neurotransmitter effects on computational performance, not as an agent in a physical environment.

- Learning mechanism. NEUCOGAR does not implement Hebbian local plasticity or predictive processing. It models how neuromodulators affect existing computation, not how learning itself proceeds.

- Concept formation. NEUCOGAR has no concept formation mechanism. It does not learn world models.

- Developmental trajectory. NEUCOGAR does not have a developmental phase structure.

- Self/world boundary. No efference copy or comparable mechanism.

- Memory architecture. NEUCOGAR does not implement three-system memory or consolidation gating.

- Scope. NEUCOGAR targets affective states (fear, disgust). Arche targets full developmental cognition with neurological profile simulation as a research application.

**Where NEUCOGAR has things Arche does not**

- Validated mapping of three monoamines simultaneously. NEUCOGAR has demonstrated dopamine, serotonin, and noradrenaline mappings together. Arche currently treats dopamine and norepinephrine; serotonin is not yet explicit.

- Published simulation results. NEUCOGAR has published validation work showing that neurotransmitter modulation produces expected effects on computation.

- Connection to NEST. NEUCOGAR uses the NEST Neural Simulation Tool, an established computational neuroscience platform with substantial community.

**Honest assessment**

NEUCOGAR is the closest existing analog to Arche's neurological profile simulation application — and only to that application. It does not attempt the developmental cognition that is Arche's primary commitment. NEUCOGAR is a useful reference for how to formalize neuromodulatory mappings rigorously, and the question of whether serotonin should be added to Arche's internal state dimensions is worth carrying forward as an open question. NEUCOGAR's existence demonstrates that the neurological simulation domain is being actively worked, but with a fundamentally different architectural target.

# **5. ACT-R and SOAR — Symbolic Cognitive Architectures**

**What they are**

ACT-R (Adaptive Control of Thought — Rational) was developed by John Anderson at Carnegie Mellon starting in the 1980s. SOAR was developed by Allen Newell, John Laird, and Paul Rosenbloom in the same era. Both are foundational cognitive architectures in the field. ACT-R is widely used in academic research; SOAR has been used in AI and modeling applications. Both have been continuously refined for decades and remain active research platforms. Recent work includes Laird, Lebiere, Rosenbloom, Stocco (2025) 'A Proposal to Extend the Common Model of Cognition with Metacognition' (arXiv:2506.07807).

**What they do**

Both are symbolic cognitive architectures organized around production systems. ACT-R has declarative memory (chunks), procedural memory (production rules), and modules including visual, manual, goal, and imaginal. SOAR organizes processing around problem-space search with production rules and chunking as the learning mechanism. Both have rational analysis foundations — cognition modeled as adaptive solutions to environmental challenges. Both have been mapped onto fMRI data and used to model human cognitive performance quantitatively.

**Where it overlaps with Arche**

- Cognitive architecture as a systematic theory of mind. Both ACT-R and SOAR treat their architecture as a hypothesis about how cognition is organized.

- Modular structure with explicit components. Both have explicit specifications of what components exist and how they communicate.

- Declarative/procedural memory distinction. Arche's episodic/procedural memory distinction is structurally similar to ACT-R's declarative/procedural distinction.

- Multi-decade refinement and revision. Both ACT-R and SOAR have version histories with substantial documentation of architectural changes — the same discipline Arche is applying through its versioned specifications.

**Where Arche differs**

- Symbolic versus subsymbolic foundation. ACT-R and SOAR operate on symbolic chunks and production rules. Arche has no symbolic substrate — concepts emerge from physical interaction and only later attach to symbols via Hebbian pairing.

- Pretrained knowledge versus developmental emergence. ACT-R and SOAR are typically populated with chunks and production rules by the modeler before a simulation runs. Arche starts from zero — no chunks, no rules, no symbols.

- Embodiment. ACT-R and SOAR are not embodied in a physical or simulated environment as a foundational commitment. They can interface with environments but the core architecture is environment-agnostic.

- Prediction error as sole learning trigger. ACT-R uses utility learning and base-level learning; SOAR uses chunking. Neither treats prediction error against physical reality as the foundational learning signal.

- Neuromodulatory parameter substrate. Neither ACT-R nor SOAR has tunable dopamine/norepinephrine analogs as explicit dimensions.

- Phase-structured development. ACT-R and SOAR do not have developmental phase trajectories.

**Where ACT-R and SOAR have things Arche does not**

- Decades of empirical validation. Hundreds of published models predicting human cognitive performance on specific tasks.

- Quantitative fit to neural data. ACT-R modules have been mapped to specific brain regions with fMRI correlations.

- Production system formalism. The rigorous specification language ACT-R and SOAR use for cognitive models.

- Established research communities. Active conferences, training programs, software ecosystems.

**Honest assessment**

ACT-R and SOAR are the foundational symbolic cognitive architectures and represent a fundamentally different bet about how cognition works. They are not direct competitors to Arche — they operate on a different substrate (symbolic) and start from a different assumption (knowledge can be pre-populated and reasoned over). Arche is in the opposing tradition: subsymbolic, developmental, grounded, with symbols emerging from concept formation rather than being foundational. The honest framing is that Arche assumes ACT-R and SOAR are working at the wrong level of abstraction for explaining how grounded intelligence develops, while ACT-R and SOAR can still produce useful models of expert-level cognition that has already developed.

# **6. The Broader Developmental Robotics Field**

**What it is**

Developmental robotics is an established subfield dating to the early 2000s, organized around the principle that cognition should emerge from sensorimotor interaction over time rather than being programmed in. Key references include Asada, Cangelosi, and others editing 'Cognitive Robotics' (MIT Press, 2022) and the IEEE Transactions on Autonomous Mental Development / Cognitive and Developmental Systems. A recent overview is Vernon (2025) 'The Future of Research in Cognitive Robotics: Foundation Models or Developmental Cognitive Models?' (Advanced Robotics Research).

**What it does**

The field studies how cognitive capabilities can emerge through autonomous, self-organized interaction between embodied agents and their environments. It targets task-independent learning, open-ended development, lifelong learning, and the emergence of language and social skills. Vernon's 2025 paper explicitly argues that developmental cognitive models — not foundation models — are the path to autonomous robots that can perceive, understand, and act with genuine flexibility.

**Where it overlaps with Arche**

- Task-independent emergence. The field shares Arche's commitment that cognition should be task-independent and develop from interaction rather than instruction.

- Lifelong learning. Continuous learning from experience rather than discrete training phases.

- Embodied and situated cognition. Body and environment as foundational, not optional.

- Anti-foundation-model position. Vernon's 2025 paper is explicit that foundation models are not the answer and developmental cognitive models are. Arche is in this tradition.

**Where Arche differs**

- Specific architectural commitments. Arche has explicit specifications (predictive core levels, neuromodulatory dimensions, three-system memory, efference copy, consolidation gating) that the broader field does not commit to as a unified package.

- Physics simulation as substrate. Most developmental robotics work uses physical robots (iCub, Pepper, etc.) or simpler simulations. Arche uses Genesis, a recent high-fidelity physics engine with continuous contact forces and material parameters.

- Phase-structured developmental staging. Arche's Genesis-Anima-Substrate-Logos-Telos structure with explicit input dependencies is more rigid than typical developmental robotics framing.

- Neurological profile simulation as application. Not present in the broader developmental robotics field.

**Where the field has things Arche does not**

- Empirical results across many platforms. Decades of accumulated findings on what works for developmental learning.

- Theoretical foundations. Asada and Cangelosi's edited works, the enactive cognition tradition, sensorimotor contingency theory.

- Diverse approaches to the same problem. Multiple incompatible architectures all attempting developmental cognition, which is valuable as a research surface.

**Honest assessment**

Arche fits within the developmental robotics tradition. The shared commitments are substantial. What distinguishes Arche from typical developmental robotics work is the specific combination of architectural mechanisms and the neurological simulation application. The field offers extensive theoretical foundation that Arche can draw on, especially Vernon's 2025 paper, which explicitly defends the developmental cognitive model approach against the foundation-model alternative.

# **Synthesis — What Distinguishes Arche**

Across the six comparators, the following combination of architectural commitments appears in Arche but not in any single prior work:

- Efference copy mechanism as explicit, load-bearing self/world boundary generator at the system architecture level (not just sensorimotor control).

- Four-dimensional neuromodulatory internal state (energy with two-component recovery, attention, prediction confidence, arousal) as architecturally load-bearing parameters that gate bandwidth, consolidation, and learning.

- Three-system memory (working, episodic, procedural) with consolidation gating requiring both low arousal AND sufficient energy.

- Credit assignment through three specific local mechanisms (neuromodulatory broadcasting, temporal contiguity, cascading prediction reshaping) without backpropagation.

- Phase-structured developmental trajectory (Genesis, Anima, Substrate, Logos, Telos) observed via a passive read-only registry, with explicit input dependencies determining when each component becomes operationally meaningful.

- Neurological profile simulation as a dormant research application made possible by the same parameter substrate that implements credit assignment.

- Genesis as physics substrate, with oscillator frequencies and behavioral timescales derived from physics environment parameters at runtime.

Individual elements appear elsewhere. Active inference uses prediction error. Monty uses sensorimotor learning. NEUCOGAR uses neuromodulators. iCub uses embodiment. The specific combination — and especially the load-bearing role of efference copy, the two-component energy model, the consolidation gating conditions, and the neurological simulation as an emergent application — is the architectural bet that Arche is making.

This synthesis does not claim that Arche will succeed where others have not. It claims that Arche is testing a combination of commitments that has not been tested before. Whether the combination produces the predicted outcomes is the work of the project.

# **Results-Based Predictions**

Comparable systems have produced empirical results and identified limitations that map onto specific Arche mechanisms. Where Arche has a mechanism that directly addresses a known limitation in prior work, the prediction is stated. These are not claims that Arche will succeed where others failed — they are claims about what should be observable if the relevant Arche mechanism functions as specified.

## **From Monty (Thousand Brains Project)**

Monty does sensorimotor learning but has no mechanism that explicitly tags every motor output with a paired predictive signal. The system cannot architecturally distinguish between prediction errors it caused and prediction errors the world caused. It learns from both without attribution.

*Arche mechanism:* Efference copy mechanism generating a paired predictive signal for every motor action. Self/world attribution emerges from consistency patterns, never hardcoded. This mechanism was arrived at from first principles during Arche's design — before the Monty gap was identified — because self/world boundary resolution is a prerequisite for coherent world model construction.

*Prediction:* Arche should demonstrate reliable self/world boundary resolution at the Anima phase, observable in registry logs as systematic differences between self-generated and externally-driven prediction errors. If the efference copy mechanism functions as specified, concept formation should proceed with less noise than systems that do not resolve the boundary, because the predictive hierarchy is not attempting to model self-generated error as world signal.

Monty additionally operates without internal state dynamics. Object recognition performance is consistent across runs because there is no energy depletion, no arousal modulation, no consolidation gating. Behavior does not vary with the system's internal condition.

*Arche mechanism:* Four-dimensional internal state (Energy, Attention, Prediction Confidence, Arousal) with bandwidth ceiling = f(arousal, energy, prediction confidence).

*Prediction:* Arche should exhibit performance variance correlated with internal state. The same object encountered at high energy and low arousal should produce a different learning signature than the same object encountered at depleted energy or elevated arousal. Registry logs should show concept formation rates that track internal state trajectories, not just exposure counts.

Monty also uses reference frames as an explicit architectural commitment for 3D object representation. Arche does not implement reference frames.

*Arche mechanism:* Concept formation via cell assemblies — stable activation patterns forming when episodic traces share consistent signatures across repetitions.

*Prediction:* Spatial structure should emerge in concept clusters without explicit reference frame machinery. If concept formation produces stable representations that support object permanence and spatial reasoning, the prediction holds. If it does not, this is a falsification of the claim that reference frames are unnecessary, and Monty's commitment is vindicated.

## **From Active Inference Implementations**

Active inference has demonstrated working hierarchical generative models but most implementations rely on backpropagation or variational machinery that requires global error signals. The credit assignment problem is handled mathematically rather than mechanistically.

*Arche mechanism:* Credit assignment through three local mechanisms — neuromodulatory broadcasting, temporal contiguity, and cascading prediction reshaping.

*Prediction:* Useful learning should occur without backpropagation or a variational objective. Prediction errors at higher levels of the predictive core should reshape lower-level predictions through cascading reshaping alone, and the registry should show concept formation tracking this cascade. If the three mechanisms are sufficient, Arche should reach Substrate without requiring a global gradient signal. If they are not, learning will stall at the Sensorimotor level and never produce stable higher-level abstractions.

Active inference work has also shown that precision weighting modulates how strongly prediction errors drive updates, with implications for psychiatric modeling, especially psychosis.

*Arche mechanism:* Prediction Confidence as an explicit internal state dimension with precision weighting role, plus the full neurological profile parameter substrate.

*Prediction:* Arche should be able to reproduce the precision-weighting findings from active inference psychiatric modeling using its own parameter space, without requiring the active inference mathematical framework. The neurological research application should show the same behavioral signatures active inference produces for psychosis profiles when Pattern Significance Broadcast is set hyperactive and Top-Down Filter is destabilized.

## **From iCub Developmental Robotics**

iCub has decades of empirical results on developmental learning in a physical body, but the platform does not expose neuromodulatory parameters as tunable dimensions. Developmental trajectories vary by experimental setup but are not driven by an explicit internal state substrate.

*Arche mechanism:* Two-component energy recovery model with depletion asymmetry, plus consolidation gating requiring both low arousal and sufficient energy.

*Prediction:* Arche should exhibit fatigue signatures and consolidation patterns that iCub work has observed behaviorally but not modeled architecturally. Sustained high-effort periods should produce slow-component deficit, which should compound when rest periods are too brief. The registry should log accumulated unconsolidated traces under chronic depletion — a signature analogous to what iCub work has reported as performance degradation under sustained operation, but here with an explicit mechanistic explanation.

iCub research has also demonstrated that physical embodiment produces calibration drift, sensorimotor noise, and unstaged variability that simulation does not.

*Arche mechanism:* None directly. This is an honest limitation.

*Prediction:* Arche will not reproduce the noise-driven robustness findings from iCub work. If Arche's learning is brittle in ways that physical embodiment would have prevented, this is a known limitation and not a failure of architecture — it is a consequence of the simulation choice.

## **From NEUCOGAR**

NEUCOGAR has validated that mapping monoamine neurotransmitters (dopamine, serotonin, norepinephrine) onto computational parameters reproduces expected patterns of resource allocation under different affective states. The validation is at the level of computational performance under emotion modulation, not at the level of developmental learning.

*Arche mechanism:* Internal state dimensions implementing the functional roles of monoamine systems through orthogonal decomposition rather than one-to-one neurotransmitter mapping.

*Prediction:* Arche should reproduce NEUCOGAR's affective state findings through its four-dimensional state space without requiring an explicit serotonin dimension. If the decomposition captures the functional roles correctly, fear and disgust analogs should emerge from specific combinations of Arousal and Prediction Confidence settings interacting with consolidation gating. If they do not, this is evidence that serotonin needs to be added as a fifth dimension and the decomposition is incomplete.

## **From ACT-R and SOAR**

ACT-R and SOAR have produced hundreds of validated cognitive models, but all rely on pre-populated symbolic chunks and production rules. They do not address how the symbols themselves are grounded in physical experience.

*Arche mechanism:* Symbol grounding through Hebbian pairing of labels to already-formed physical concepts.

*Prediction:* Arche should produce symbol-concept bindings at the Logos phase that are grounded in concept clusters formed during Substrate. The same physical concept (e.g., mass) should be retrievable through either physical interaction or symbolic activation. Registry logs should show symbol activation reliably co-activating the underlying concept assembly. If they do not, the symbol grounding problem remains unsolved for Arche and the architecture has not actually addressed what ACT-R and SOAR sidestep.

## **From the Broader Developmental Robotics Field**

The field has converged on the position that cognition must emerge from sensorimotor interaction over time, but specific architectural commitments vary widely and many implementations lack a unified internal state substrate. Vernon's 2025 paper explicitly argues that developmental cognitive models are the path forward, against the foundation-model alternative.

*Arche mechanism:* Phase-structured developmental trajectory with explicit dependencies, observed via passive registry.

*Prediction:* The Genesis-Anima-Substrate-Logos-Telos phase structure should be observable in registry logs without being declared. Concept formation should accelerate as prediction confidence rises and bandwidth ceiling opens, producing the exponential developmental trajectory specified in Primary Hypothesis 2. If the phase structure does not emerge from registry observation, the architecture has imposed a developmental ordering that the underlying mechanisms do not support, and the phase labels are scaffolding rather than discovery.

# **Notes for the Positioning Section**

If a Positioning section is added to the Research Hypothesis Document, it does not need to recapitulate this entire research report. A short version (roughly half a page) might cover:

- One sentence on the broader tradition Arche fits within (developmental cognitive robotics, predictive processing, brain-inspired AI).

- One paragraph naming the closest analogs (Monty, active inference implementations, iCub) and the substantial overlap.

- One paragraph on what specifically distinguishes Arche (the combination listed in the Synthesis section above).

- One sentence stating the honest limitation: Arche has no empirical results yet, while comparators have decades.

This research report is source material. The Positioning section in the hypothesis document should be written in the author's own voice and at the length judged appropriate.

# **Revision Log**

**v2.1 — May 2026**

Phase references updated throughout: Prometheus renamed to Telos. Four enumerated phase lists and one Results-Based Predictions paragraph updated accordingly.

**v2.0 — May 2026**

Initial research report.

*Project Arche — Prior Work and Positioning Research Report v2.1*

---

© 2026 [YOUR NAME]. Licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
