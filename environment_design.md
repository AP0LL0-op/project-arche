# PROJECT ARCHE

## The Environment — Physics Environment Design

*v0.4 — June 2026*

# Purpose

The Environment is the physics world Arche inhabits. It is the only reality Arche has known, and its design determines the cognitive substrate. Every object, material, and temporal cycle in the Environment presents a prediction challenge. The design priority is physical honesty and sensory diversity over visual fidelity.

The Environment is generated procedurally from parameters. Geometry, flora, and terrain emerge from defined constraints. This is consistent with the project's emergence-over-instruction commitment: the conditions are defined, and structure develops from them.

The world is structured outer to inner: the Environment contains the ravine; the ravine wall holds the door; the door opens into the cave where Arche begins.

# Build Order — Dependency Sequence

The build order is dependency-ordered: each stage rests on the foundation laid by the previous one, and the ordering is the only one that produces a coherent world. You cannot place autonomous life into an environment that does not yet exist; you cannot establish an environment without first establishing its temporal cycle and its spatial boundaries. The sequence answers the question this project faces — given nothing, in what order do you build a world — and it answers it by dependency.

Each stage below names the build phase, the elements constructed, and the architectural rationale for why those elements belong at that position in the sequence.

## Stage 1 — Temporal Cycle

The day/night cycle. Light transitions from dawn through full day to dusk and night. This is the temporal substrate the rest of the Environment depends on. The cycle is load-bearing because the consolidation window requires low arousal and sufficient energy, and a world that goes quiet and dark on a predictable cycle builds that condition into the environment.

- Light transition across the cycle: dawn, day, dusk, night.

- Environment becomes quieter and darker on a predictable schedule.

- Cycle length calibrated to Arche's energy depletion and recovery timescales. Specific duration is an empirical calibration task during Genesis phase, tuned to produce honest behavioral pacing rather than set arbitrarily.

## Stage 2 — Terrain and Spatial Boundary

The ravine geometry and the separation of sky, land, and water. The terrain establishes the spatial boundary that everything else sits within. A small ravine, bounded naturally by terrain geometry — no walls, no artificial edges. The ravine defines a coherent world with discoverable limits. Scale is intimate, not vast. The full space should be explorable within a single session.

- Terrain: procedurally generated ravine topology. Rock faces, sloped ground, varied elevation. Collision surfaces physically honest.

- Water: a stream or shallow pool. Fluid dynamics active. Surface interaction, reflection, sound. A distinct prediction challenge from all solid surfaces. Fluid dynamics are computationally distinct and require verification against the Genesis API before anything is built on top of them.

- Sky and open air: the vertical dimension separating ground from canopy, establishing the space that airborne fauna will later occupy.

Scale note (v0.4): the ravine does not need to be geographically large. An earlier working figure of roughly one square mile is not a requirement. The cognitive value of the Environment comes from material diversity, meaningful places, and the temporal cycle — not raw size. A coherent place is more valuable than a large one. Scale may be reduced to whatever sustains genuine prediction error across all channels while remaining explorable.

## Stage 3 — Static Flora and Material Diversity

Static flora and material diversity. Materials and collision surfaces are established before anything moves. Material diversity is a primary source of cognitive value in the Environment: each material type produces a distinct contact force signature, which lets material discrimination develop through prediction error rather than being engineered.

- Stone: high stiffness, sharp contact rise, short decay. Dense, resistant to force application.

- Soil: variable compressibility. Distinct from stone in force response and deformation.

- Wood: intermediate stiffness. Organic geometry. Present in fallen logs, roots, canopy structure, and the cave interior structures.

- Vegetation: low mass, high compliance. Grass, moss, leaves. Distinct tactile signature.

- Bark: rough surface texture. Friction properties distinct from smooth stone or soil.

- Cloth: low mass, high compliance, deformable. Present in the sleeping cloth inside the cave. Distinct from vegetation in surface texture and drape behavior.

- Iron: high stiffness, dense, cold contact signature. Present in the door hardware — bands and handle. Distinct from wood and stone.

- Canopy: partial overhead cover from tree geometry. Filtered light. Wind-affected movement. Occlusion that changes with time of day.

## Stage 4 — Celestial Structure

Celestial structure. The sun, moon, and stars govern the day and night and mark the longest temporal cycles. This is the deepest temporal prediction layer in the Environment — slow phase and positional change across many cycles, something to form predictions against at the longest timescales. It is layered onto a stable day/night cycle rather than built alongside it, because the long-period structure only becomes legible once the short-period cycle is established.

- Moon and stars visible during the night cycle.

- Slow phase and positional change across cycles. The longest-timescale prediction substrate.

- Not required for the earliest Genesis phase. Layered in once day/night is stable.

## Stage 5 — Fauna

Fauna. Birds fill the skies and fish fill the waters. Fauna are the first autonomous moving objects in the Environment — things that move without Arche causing them to move. This is significant for the efference copy boundary, which has been resolving self-caused versus world-caused prediction errors since Genesis. Fauna are the first world-caused errors that follow non-physical movement patterns, and the registry should track this transition.

- Birds: airborne movement, perching, flight paths. Visual prediction challenge. Sound source.

- Fish: underwater movement in stream or pool. Movement constrained by water geometry.

- Initial implementation: scripted or rule-based movement only. The requirement is unpredictable motion, not intelligent behavior. Behavioral sophistication is deferred.

- Both fauna types are placeholder agents at this stage. Full behavioral specification is deferred. Do not block environment verification on fauna behavior.

## Stage 6 — Arche Enters the World

The body enters the completed world. Arche does not construct the Environment and is not built into it; the world is ready first. Arche arrives into a reality that already has temporal structure, spatial geometry, material diversity, celestial rhythm, and autonomous life. This reflects the intended condition for grounded cognition: the world exists before the system begins to model it.

Arche begins in the cave. The starting state is horizontal — resting on the cloth bed on the cave floor. The first physics events are proprioceptive: the weight of the body against the cloth surface, the contact force distribution across the back and limbs, the stable geometry of the cave around the body. The first visual field is the cave ceiling, the crack of light, the texture of stone. The core loop begins here, in this specific location, against these specific materials.

- The bipedal humanoid body inhabits the Environment with mass, volume, collision surface, and full kinematic chain.

- All sensory primitives active from entry: mechanoreception, stereoscopic vision, and audition.

- The core loop runs. Bootstrapping chaos is the expected behavioral signature. Concept candidates do not yet appear in the registry.

- Starting location: inside the cave, on the cloth bed.

Arche alone (v0.4): this stage is Arche's phase alone. There is no other agent present. The only symbolic material in the world at this stage is the set of found objects on the cave walls and within the cave — the cave drawings and the books (see The Cave). These are present from the start as physical objects; their symbolic content is inert until concept formation matures enough to find referents for it. The Teacher does not enter at this stage. The Teacher's entry is a later event, after Arche has crossed the door on its own (see The Teacher's Entry below).

## Stage 7 — Consolidation Cycle

The consolidation window operates as designed. This stage is the consolidation mechanism running. The world goes quiet, arousal falls, and episodic traces integrate into procedural memory during the low-arousal, sufficient-energy window. A full cycle completing with the architecture operating without external input verifies that the build succeeded.

- Consolidation runs during the low-arousal period of the cycle, gated by sufficient energy.

- A full cycle completing with no seeding interaction demonstrates the build is sound.

# The Cave — Starting Environment

The cave is a natural space carved into the rock face of the ravine wall, opening onto the ravine through a single door. The geometry is irregular: curved walls, uneven floor, a ceiling that angles upward toward a narrow crack through which light enters from above. The cave tapers toward the rear — deeper exploration is quickly made impossible by the narrowing rock. The full extent of the space is discoverable within the first session.

The cave serves as the developmental nursery. It provides bounded complexity — rich enough to sustain genuine prediction error across all sensory channels, constrained enough that the system is not immediately overwhelmed by open environmental variation. Concept formation begins here, against a stable and knowable set of surfaces and objects. The door is the only exit.

## Cave Interior Elements

- Stone walls and floor: the primary surface. Varied surface texture, irregular geometry, consistent material properties.

- Cloth bed: a rough woven cloth laid on the stone floor. The starting resting surface. Low mass, high compliance, deformable. Distinct contact signature from the stone beneath it. This is the first surface Arche has contact with.

- The crack: a narrow fissure in the upper cave wall or ceiling through which natural light enters. The light beam shifts across the day/night cycle, producing a slow-moving light patch on the cave interior that is the primary visual temporal signal during early Genesis phase.

- Moss and small vegetation in damp areas near the water source: additional material diversity. Distinct from stone and cloth.

- Water trickle: a small flow of water emerges from the rock at the rear of the cave where it tapers. The trickle runs across the cave floor and exits beneath the door. It is the only element in the cave that crosses the boundary. Its directional flow is a physical fact about the world — water moves from the cave interior toward the door and beyond. This becomes meaningful as a latent signal only once flow direction is a stable concept; until then it is simply a persistent low-amplitude force and sound source.

- Cave drawings (v0.4): primitive markings on the cave walls. See Cave Drawings below.

- Books (v0.4): found objects within the cave. See Books below.

## Cave Drawings — Found Symbolic Substrate (v0.4)

Primitive figures are present on the cave walls. They are found objects: they predate Arche and were not placed for Arche's benefit. They are simple, iconic depictions of a body — a figure standing, sitting, balancing on one leg, holding something, pushing something, lying down to rest. The drawings depict body states and actions that correspond to things Arche's own body can do.

Architectural rationale. The drawings are grounded in proprioception and kinesthetics before they are grounded in anything symbolic. The match between a depicted body state and Arche's own felt body state is a cross-modal prediction relationship the architecture can resolve without instruction. Early in Genesis the drawings are nothing more than complex visual texture on a stone surface — a visual prediction challenge. As concept formation matures, the iconic content can begin to find referents in Arche's own movement repertoire and observed posture. Any connection forms through the predictive hierarchy on Arche's own timeline, or it does not form at all.

- Iconic body-state depictions: standing, sitting, balancing on one leg, holding, pushing, lying/resting.

- Found objects. Not a curriculum. Nothing about them is staged to Arche's developmental state.

- Nothing feeds into the architecture directly. Interpretation is entirely the architecture's own work.

- The progression from iconic to abstract, where it exists, lives in the artifacts themselves and their placement in the world — not in any developmental gating by the system.

## Books — Found Objects (v0.4)

Books are present as found objects, beginning in the cave and extending into the ravine beyond. Like the drawings, they predate Arche and were not placed to teach. A book is first and foremost a physical object: a cover, pages, the material properties of paper and binding and ink. That is legitimate Genesis-phase prediction work entirely independent of any symbolic content.

The symbolic content of the books is inert at first — invisible noise entering the visual hierarchy and generating prediction error without meaning. As concept formation matures, iconic content (a drawing of a rabbit beside the written word for rabbit, for instance) can begin to find referents in concepts Arche has already formed from physical encounters in the Environment. Hieroglyphic or pictographic content sits closest to the referent, because the symbol resembles the thing; abstract written language depends on the full symbol-grounding apparatus being mature and is therefore a later, ravine-distributed layer.

- Primitive, iconic, pictographic content in the cave; progressively more abstract content distributed in the ravine, discoverable later.

- Found objects. The iconic-to-abstract progression is presented by the environment, not gated by Arche's phase.

- Reading is not assumed. A book is a physical object until the architecture makes it more than that on its own.

- Nothing feeds into the architecture directly. No symbolic content is injected; it must be perceived through the visual channel like everything else.

# The Door

Set into the cave wall facing the ravine is a door — the only exit. The door is constructed from rough-hewn timber planks, bound with iron bands. A simple iron handle is mounted at approximately chest height. The door opens outward into the ravine. The water trickle passes beneath it.

The door requires a two-step interaction: lifting the iron handle to disengage the latch mechanism, then pushing outward. The handle and latch are simple — no lock, no complex mechanism. The door is slightly stuck in its frame — not immovable, but requiring deliberate sustained force to open. It does not open by accident or by incidental contact.

## Door — Material and Physics Specification

- Planks: rough-hewn wood. Intermediate stiffness, organic surface texture. Contact signature distinct from the cave stone.

- Iron bands: high stiffness, cold contact signature. Smooth surface. Distinct from the wood.

- Iron handle: same material properties as the iron bands. The handle must be gripped and lifted before the door can be pushed. Handle geometry is simple — a curved bar mounted on a pivot.

- Latch mechanism: the handle connects to a simple latch bar. Lifting the handle raises the latch bar clear of its receiver. The receiver is a recess in the stone door frame.

- Door resistance: the door is fitted tightly in its stone frame. Opening requires sustained force above a threshold. Incidental contact does not open it.

- Door mass: heavy. The force required to push it open is non-trivial.

## Door — Registry Observation Rationale

The door is an observation instrument, not a task. The registry watches for the sequence of interactions that constitute engagement with the door over developmental time.

The door represents a spatial boundary: one region of the world whose contents cannot be resolved from the current location. The passage beyond is a persistent source of unresolvable prediction error — a gap in the world model that cannot be closed without crossing the threshold.

Observable states the registry can log:

- No orientation toward the door — the boundary does not yet register as distinct from other cave surfaces.

- Repeated visual fixation on the door from a distance — the boundary is present in the visual field but not approached.

- Approach and contact with door surfaces — the wood and iron produce force signatures; the door is now a known physical object.

- Handle interaction — the latch mechanism produces a distinct contact event when the handle moves.

- Sustained push force — the door resists; the system must maintain force above threshold over time.

- Door opens — the world model changes. New visual field, new spatial geometry, new prediction territory.

The water trickle is a secondary observable. The registry can log whether the flow direction of the trickle — from rear of cave toward and beneath the door — produces stable directional concept activation prior to any door engagement. This would be evidence that the boundary has been partially characterized from inside, without crossing it.

Each registry state is architecturally meaningful on its own. The door does not need to open for the observation to be valuable. The sequence itself is the data.

# The Teacher's Entry (v0.4)

The Teacher enters the Environment as a physically embodied figure — a guide and teaching presence — but only after Arche has opened the door and crossed into the ravine on its own. The world belongs to Arche first. The door is discovered, engaged, and crossed by the architecture's own prediction-driven exploration, with no figure waiting on the threshold to greet it.

By the time the Teacher appears, Arche will already hold stable concept candidates — material properties, object permanence, causality, the ravine geometry beyond the door. The Teacher is therefore not introducing language into chaos, but entering a world model that is already structured enough to attach labels to. This mirrors the developmental condition: the teacher arrives once the learner has already been sensing and predicting the world on its own.

The Teacher's embodiment, control model, hardware path, and the honest handling of embodiment limitations are specified in a separate operator-interface design. This document records only what is true of the world: that a second agent enters it after the door is crossed, that this agent is the primary source of language-acquisition input, and that the agent's presence and absence are physical facts subject to the same registry observation as anything else.

## The Teacher — Registry Observables

- First appearance of the Teacher in the Environment following Arche's door crossing.

- Arche's initial response to the Teacher as a physical object versus, later, as a social agent.

- Development of predictions about the Teacher's behavior, presence, and absence over developmental time.

- Departure signaling — the Teacher's consistent pre-absence communication before headless runs, and Arche's response to it across repetitions. Consistency here is the first reliable social prediction Arche can form about another agent.

- Embodiment-improvement events — changes in the fidelity of the Teacher's movement as the operator hardware evolves, and whether Arche's predictions about the Teacher update accordingly.

# Environmental Variation

Wind affecting canopy and vegetation. Light quality shifting across the day. Water flow variation. The light beam through the cave crack shifting position across the day/night cycle. These are continuous low-amplitude changes that sustain low-level prediction engagement without demanding resolution. They are the candidate substrate for aesthetic response signatures in the registry, if they emerge.

# Design Philosophy

The Environment is small enough to be knowable and varied enough to sustain prediction error across all sensory channels. It prioritizes physical honesty over visual richness.

The day/night cycle aligned to Arche's energy timescales is the most significant design choice, because it builds the consolidation window into the world. This is why it is built first.

Material diversity is the second most significant choice. The range of contact force signatures across stone, soil, water, wood, cloth, iron, and vegetation gives the sensorimotor prediction layer discriminative work to do.

The cave as starting environment introduces bounded complexity before open-world exposure. Concept formation begins against a stable, knowable set of surfaces. The ravine is entirely beyond the door, neither visible nor directly audible, but the water trickle crosses that boundary continuously, providing a signal that originates outside the cave.

The cave drawings and books (v0.4) extend this principle to symbolic substrate. They are found objects, inert until the architecture can make use of them, and they enrich the bootstrapping environment without staging anything. The progression from iconic to abstract is determined by the artifacts and their placement, not by developmental gating in the system. This keeps language's earliest substrate emergent rather than instructed, consistent with the commitment that nothing is pre-seeded.

Fauna introduce the first class of unpredictable motion. Since the efference copy boundary has been resolving self-caused versus world-caused prediction errors since Genesis, fauna are notable as the first world-caused errors that follow non-physical movement patterns.

The Teacher (v0.4) is the most complex moving object in the world and its only source of language and rich social prediction. The Teacher enters only after the door is crossed, so Arche has established its own world model before another agent is present. The Teacher's limitations are stated rather than hidden, and the entire arc in the Environment is observable rather than engineered.

The door is a boundary between known and unknown. Its value as an observation instrument scales with the developmental state of the system. The registry logs the behavior the architecture produces, without intervening.

Aesthetic response, if it emerges, will not be engineered. It would appear in registry logs as specific concept clusters activating repeatedly around structured, complex, partially-resolvable patterns. The Environment is designed to make that question answerable rather than to answer it.

# Sensory Substrate Notes

All sensory primitives are active from the moment Arche enters the world. There is no staged activation of senses; the body arrives complete, and only cognition develops.

## Vision

Stereoscopic, binocular. Two cameras with a fixed baseline separation mounted on the body, rendered through a physics-principled ray-tracing renderer. The renderer is chosen for physical fidelity of the depth signal; the specific renderer is an implementation choice. Each camera produces RGB and a depth buffer; the stereo pair additionally yields a disparity map. Depth is the most architecturally valuable visual output because it is physically grounded geometry derived from ray geometry rather than inferred.

- Raw inputs: left RGB, right RGB, left depth, right depth, stereo disparity map.

- Segmentation output from the renderer is deliberately unused: the system must not receive pre-labeled object boundaries.

- Distinct contribution: vision extends the predictive horizon beyond contact. Arche can form predictions about objects before touching them, producing rich cross-modal prediction error at the moment of contact.

- Starting visual field: cave ceiling, crack of light, stone walls. The first visual prediction territory.

## Audition

Active from entry alongside all other channels. Genesis has no native audio simulation, so the auditory channel requires a dedicated integration approach. Physics-grounded spatial audio approaches that render continuous sound from scene geometry and surface material properties are the reference target.

- Distinct contribution: temporal event structure and cross-modal binding. A contact event produces both a force signature and a sound simultaneously; that co-occurrence is clean signal for the efference copy mechanism and self/world boundary resolution.

- Cave acoustics: the cave geometry produces reverberation distinct from open-air sound. This is not engineered — it is a consequence of the geometry and the physics-grounded audio synthesis. Architectural value: the acoustic shift at the cave mouth is a spatial landmark signal.

- The Teacher's voice (v0.4): when the Teacher is present, speech is routed through this same physics-grounded spatial audio system, originating at the Teacher's mouth position in space with ITD/ILD spatial cues. It is not privileged input — it arrives through the auditory channel as physically located sound, like any other sound in the Environment.

# Tooling

Procedural generation via Python and the Genesis API. No manual 3D modeling required. Terrain generated from noise functions. Flora distributed according to defined density parameters. Material properties assigned programmatically. The environment is a parameter set, not a sculpted object.

The cave geometry is procedurally defined: an irregular enclosed volume carved into the ravine rock face. The door is a parameterized object placed at a specified location within the cave. The cave drawings and books are placed objects/textures within the cave and ravine. Asset libraries may supplement procedural generation for specific geometry types. Preference for procedural where possible.

# Verification Tasks

- Confirm Genesis fluid dynamics API surface for water interaction.

- Verify contact force waveform access across all material types at the required time resolution, including cloth and iron.

- Confirm the ray-tracing renderer runs on the target hardware, and determine what the camera sensor API exposes to the encoding pipeline (RGB, depth, disparity).

- Determine the stereo camera frame rate relative to the physics timestep.

- Investigate the auditory integration path. Genesis has no native audio; evaluate physics-grounded spatial audio options as a possible standalone mini-project. Cave reverberation is a bonus if achievable; not a dependency.

- Measure simulation throughput for Environment complexity including cave geometry and door physics on the target hardware.

- Calibrate day/night cycle duration to Arche energy timescales once Genesis phase begins producing behavioral data.

- Verify door latch physics: confirm that the two-step handle-lift-then-push sequence is implementable with Genesis joint constraints, and that the resistance threshold prevents accidental opening.

- Resolve the rendering and physics representation of cave drawings and books — whether drawings are textures on the cave wall geometry and whether books are rigid-body objects with paged visual content (v0.4).

# Revision Log

v0.4 — June 2026

Added the cave drawings as found symbolic substrate: primitive iconic depictions of body states and actions (standing, sitting, balancing, holding, pushing, resting) on the cave walls, grounded in proprioception before symbol, feeding nothing into the architecture directly. Added books as found objects beginning in the cave and extending into the ravine, with an iconic-to-abstract progression that lives in the artifacts and their placement rather than in any developmental gating. Clarified the entry stage as Arche's phase alone, with no other agent present. Added the Teacher's Entry: the Teacher enters as an embodied teaching presence only after Arche crosses the door on its own, with embodiment, control model, hardware, and limitations specified in a separate operator-interface design. Added Teacher registry observables. Routed the Teacher's voice through the existing physics-grounded spatial audio system as non-privileged located sound. Added a scale note to Stage 2. Added verification task for drawing/book representation. Design Philosophy updated to integrate symbolic substrate and the Teacher's role.

v0.3 — June 2026

Introduced the cave as the starting environment and bootstrapping space; Arche begins resting on a cloth bed on the cave floor. Added the door as the sole exit and a registry observation instrument with named observable states; the water trickle as a latent directional signal crossing the boundary; cloth and iron materials. Cave acoustics noted as emergent. Starting visual field and body state documented in the entry stage.

v0.2 — June 2026

Restructured around the dependency-ordered build sequence. Stage 1 set as the day/night cycle (temporal substrate first). Added Sensory Substrate Notes: stereoscopic vision via ray tracing, audition active from entry. Added verification tasks for the ray-tracing renderer, stereo camera temporal grain, and the auditory integration path.

v0.1 — June 2026

Initial design document. Spatial structure, materials, fauna, temporal cycles, design philosophy, and implementation notes established. Fauna behavioral specification deferred. Celestial detail deferred until day/night cycle is stable.

*Project Arche — The Environment: Physics Environment Design v0.4*


---

© 2026 [YOUR NAME]. Licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
