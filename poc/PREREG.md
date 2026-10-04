# PREREG — Efference PoC, steps 4–6

Pre-registered pass/fail criteria for the Efference PoC. Committed before any run it governs; the commit hash is the timestamp. Any change after a governed run starts goes in **Amendments** with the reason, and the original criterion is kept.

Spec reference: Architecture Specification v4.8 (Sections 3.1, 3.3, 3.5, 6). Prior work: Ye (2026), arXiv:2606.05605.

**Status: DRAFT.** Values marked ⟨proposed⟩ need a decision. **Section 3b (population) stays draft until Pymunk pilots pick the rule** (CLAUDE.md steps 4g–5). Pilots use seeds 100–199; governed runs use seeds 0–4. No governed seed is run before this file is final and committed. Every pilot variant tried is logged in `pilots/LOG.md`.

---

## 1. Question

When something moves the arm, does a small, locally-plastic agent whose own commands cause its motion carry, in its internal state, which source moved it (its motor or an external mover), beyond what its sensations alone carry, beyond what its command alone carries, and beyond an identical agent whose commands are not causal?

## 2. Conditions

| Condition | Body driven by | Agent's own commands | Population plasticity |
|---|---|---|---|
| **Real, plastic** | own motor + external mover | causal | on |
| **Real, frozen** | own motor + external mover | causal | input weights frozen at initial values; readout still learns |
| **Yoked, plastic** | Real agent's replayed commands + same external mover | independent babbling seed, not applied | on |
| **Yoked, frozen** | as Yoked | as Yoked | as Real, frozen |
| **Null yoked** (plastic + frozen) | as Yoked | a second independent seed | as above; used only for the noise floor |
| **Ablation** (each of the above, re-run) | as above | as above | as above, command-trace input removed |

All conditions share the same random initial weights per seed. Yoked agents receive exactly the Real agent's observation sequence for that seed.

## 3a. World and schedule

| Parameter | Value |
|---|---|
| Physics tick `dt` | 1/60 s |
| Run length | 30 min sim time (108,000 ticks) |
| Seeds | N = 5 (seeds 0–4) |
| Motor command schedule | Babbling: hold a value from {−2, 0, +2} (equiprobable) for a duration uniform in 0.5–3 s |
| External mover | Independent babbling schedule, same profile. **When active it sets the arm's rate and overpowers the motor**, so its sensory signature matches the motor's ⟨proposed Pymunk form: a second, world-owned `SimpleMotor` on the arm with higher `max_force`, max_force 0 when inactive⟩. Proxy pilot: an external mover twice as strong *added* to the drive leaked the label into sensations (sensation-only 0.81); the overriding form did not (0.52). |
| External mover visibility | Its schedule is ground truth: observer-only `World` method → logger. Never in `read_sensors()`. |

## 3b. Agent (DRAFT until Pymunk pilots)

| Parameter | Value |
|---|---|
| Population size | 16 ⟨proposed⟩ |
| Activity | a(t) = 0.9·a(t−1) + 0.1·relu(W·x(t) − θ), θ = 0 ⟨proposed⟩ |
| Inputs x | angle, angular velocity, contact, command trace; each normalised by running mean and variance (EMA, time constant 1,000 ticks), identical rule for all |
| Command trace | τ(t) = 0.95·τ(t−1) + 0.05·command(t), signed (deviation from Ye's \|a\|, documented) |
| Population rule | ⟨locked after pilots⟩. Starting point: Sanger's rule × m(t). Candidates to pilot: lateral inhibition; eligibility traces (temporal contiguity); node perturbation (aimed, scalar broadcast) |
| Modulator m(t) | mean over channels of (e_c / σ_c)², e_c = efference readout error on channel c, σ_c its running SD; clipped at 3 ⟨proposed⟩ |
| Population learning rate | ⟨set from Pymunk pilots⟩ |
| Readout | Delta rule on [activity, command], learning rate ⟨proposed 1e-3⟩ |

## 4. Ground truth and label (observer only)

- **Event truth per tick:** motor active / external mover active / contact (wall, ball).
- **Primary label "who moved it":** **self = 1** when the motor command is non-zero, the external mover is inactive, and the arm is moving (|angular velocity| > 0.1 rad/s ⟨proposed deadband⟩); **external = 0** when the external mover is active and the arm is moving, *whether or not the agent is commanding*. Ticks matching neither are excluded.
- The "external while commanding" ticks are what stop the label collapsing to "am I commanding." Report their fraction; it must be ≥ 25% of label-0 ticks.

## 5. Decoding protocol

- **Decoder:** linear logistic regression, class-balanced; observer side, trained offline.
- **Inputs:** population activity only. Never errors, raw inputs, or the trace.
- **Split:** within each evaluation window, train on the first 70%, test on the last 30% (held-out *time*, no shuffling).
- **Evaluation windows:** consecutive 5-minute blocks, so decodability is tracked across the run.
- **Metric:** balanced accuracy.

## 6. Primary criterion (pass/fail)

In the final evaluation window, per seed, on the **plastic** population (Arche's claim: the distinction emerges through local learning):

> **G = BA(Real, plastic) − max(BA(Yoked, plastic), BA(sensation-only), BA(command-only))**

The same statistic on the frozen population, G_frozen, is reported as a reference line ("the design can carry it"), not as the claim.

- **Sensation-only baseline:** the same frozen population fed sensations with the trace zeroed.
- **Command-only baseline:** the same frozen population fed the trace with sensations zeroed.
- **Noise floor σ₀:** SD across seeds of BA(Yoked) − BA(Null yoked).
- **PASS** if all hold: mean G ≥ 3·σ₀; G > 0 in ≥ 4 of 5 seeds; 95% CI of mean G excludes 0.
- **Validity gate (must hold or the run doesn't count):** sensation-only BA ≤ 0.60 and command-only BA ≤ 0.68. (0.68 set before any governed run, after a proxy pilot seed reached 0.64.) If a baseline passes, the ambiguity isn't real; that's a physics/channel-tier setup fix, not a result.

## 7. Secondary criteria

1. **Plasticity vs reference:** D = BA(Real, plastic) − BA(Real, frozen), and the difference-in-differences (plastic − frozen)Real − (plastic − frozen)Yoked. Reported with CIs. **Pre-registered prediction: D ≥ 0** (the locked rule preserves or sharpens self-information). Proxy pilots found D ≈ −0.1 to −0.19 with the placeholder rule.
2. **Agency gain:** mean per-channel agency gain on angle and angular velocity > 0 in the final window, all seeds. Reported separately.
3. **Spike test:** zeroing the command input to the Real readout raises its angle and velocity error; ratio > 1 with CI excluding 1.
4. **Wall stays world:** in the Real agent, wall-contact ticks remain separable from free-motion ticks late in the run: final-window separation ≥ 0.8 × first-window separation.

## 8. Exploratory (not pass/fail)

- Command-trace ablation: change in G and D without the trace (spec v4.8 open question).
- Ball vs wall separation in population activity.
- Decodability trajectory across windows (does it rise, hold, or decay).

## 9. Failure-tier mapping

- **Physics / channel tier:** validity gate fails, or a sanity check fails. Fix, re-run, not counted.
- **Learning tier:** Real efference error on angle/velocity doesn't fall from first to final window; the population blows up, goes silent, or collapses (median pairwise weight cosine ≥ 0.9 after the first 5 min); or **the primary fails on the plastic population while G_frozen would pass**. The boundary claim is untested, not failed.
- **Boundary tier:** validity gate holds, the population is healthy, and the primary fails on the plastic population **and** G_frozen fails too; or Secondary 4 fails.

## 10. Sanity checks before any governed run

- Yoked agents receive the identical observation sequence to the Real agent (assert every tick).
- Frozen conditions' population weights don't change (assert).
- Decoder inputs contain no error, raw-input, or trace columns (assert on column names).
- No cognitive module imports `pymunk` (grep).
- External-mover schedule never appears in `read_sensors()` output (assert on keys).

## Amendments

(none)
