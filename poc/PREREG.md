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
| Seed streams | Each governed seed s yields independent named streams from `numpy.random.SeedSequence(s).spawn(5)`, in this fixed order: [0] init (population weights), [1] agent babbler, [2] mover, [3] yoked babbler, [4] null-yoked babbler. A numpy stream is `numpy.random.default_rng(child)`. A Python `random.Random` stream (e.g. `Babbler`) is seeded with `int(child.generate_state(1)[0])`. New streams are appended at the end so existing ones don't change. Pilots used ad hoc offsets instead (W0 s + 7, mover s + 50, proxy body noise s + 100, yoked babble s + 999, P6 mask s + 13); governed runs use this scheme only. Implemented in step 4c. |
| Motor command schedule | Babbling: hold a value from {−2, 0, +2} (equiprobable) for a duration uniform in 0.5–3 s |
| External mover | Independent babbling schedule, same profile: {−2, +2} when on, held 0.5–3 s; drawing 0 means off. **When active it replaces the motor**: the agent's motor goes slack (`max_force` 0) and a second, world-owned `SimpleMotor` on the arm drives at the motor's own `max_force`, so its sensory signature matches the motor's. When inactive the mover's `max_force` is 0 and the motor's is restored. The agent's command is still issued and logged while the mover is active; it has no physical effect. Proxy pilot: an external mover twice as strong *added* to the drive leaked the label into sensations (sensation-only 0.81); the overriding form did not (0.52). Pymunk pilot P5: a mover that overpowers the motor with 10× `max_force` spun the arm up in 3 ticks vs the motor's 24, leaking the driver into angular velocity; the replacing form matches exactly (24 vs 24). |
| External mover on-probability p | ⟨proposed 1/3⟩, the probability a mover segment is on (`p_zero = 1 − p`). Chosen in P5 on setup adequacy only, no decoder: most body control and most trailing data, classes within ~1.3:1; p = 2/3 rejected (self-trailing ticks as low as 98 per 5 min). Provisional until re-checked with the step-4c population. |
| External mover visibility | Its schedule is ground truth: observer-only `World` method → logger. Never in `read_sensors()`. |

## 3b. Agent (DRAFT until Pymunk pilots)

| Parameter | Value |
|---|---|
| Population size | 16 |
| Initial weights | W ~ Gaussian(0, 0.5), dense 16×4: `numpy.random.default_rng(init).normal(0, 0.5, (16, 4))`, the first draw from the init stream (3a). Effective rank of the governed inits (Section 9), computed before any run: seeds 0–4 → 3.21, 3.09, 3.58, 3.18, 3.02; none below 2.5. Dense deviates from spec v4.8 "sparsely connected". Sparsity belongs to the connection economy (out of POC scope). P6 (proxy): a sparse mask, k=2 and k=3, made no detectable difference. |
| Activity | a(t) = 0.9·a(t−1) + 0.1·relu(W·x(t) − θ), θ = 0 for every node, no jitter. Random W breaks symmetry; θ is not needed for it. |
| Inputs x | angle, angular velocity, contact, command trace; each normalised by running mean and variance (EMA, time constant 1,000 ticks), identical rule for all, one normaliser per input. Step size max(1/t, 1/1000): an exact cumulative average during warm-up, then the EMA, so starting values can't produce spurious early z. |
| Command trace | τ(t) = 0.95·τ(t−1) + 0.05·command(t), signed (deviation from Ye's \|a\|, documented) |
| Population rule | ⟨locked after pilots⟩. Pilot order: **(d) first**, then (a)–(c). (d) first: (a)'s modulator scales how much it learns, not what (P4; cf. Han 2026, arXiv:2606.30191, selection vs actuation). (d) is a selection rule. (a) error-gated Sanger's rule (baseline); (b) (a) + eligibility trace (temporal contiguity; Gerstner et al. 2018); (c) (a) + LPL-style predictive term (Halvagal & Zenke 2023); (d) sign-flipping inhibitory cancellation from command onto sensory nodes, Meng & Wang 2026–style: Hebbian on match, anti-Hebbian on mismatch. (d)'s match/mismatch threshold is a free parameter and must be fixed here before governed runs. Node perturbation remains a fallback candidate. Parked: (e) agency-gated plasticity: not piloted. Gating plasticity on a self/world signal risks making decodability true by construction. |
| Modulator m(t) | mean over channels of (e_c / σ_c)², e_c = efference readout error on channel c, σ_c its running SD; clipped at 3 ⟨proposed⟩ |
| Population learning rate | ⟨set from Pymunk pilots⟩ |
| Readout | Delta rule on [activity, command], learning rate ⟨proposed 1e-3⟩ |
| Blind model (observer) | Its own population, same initial weights with the trace column removed (W[:, :3]), same activity rule and (when plastic) same rule, fed the three normalised sensory inputs only; its readout is the efference readout minus the command input. Real and blind differ in exactly one thing, command information, so agency gain isolates it. A blind readout on the real population would not be blind: the trace reaches it through the activity. |

## 4. Ground truth and label (observer only)

- **Event truth per tick:** motor active / external mover active / contact (wall, ball).
- **Driver per moving tick:** a tick is *moving* when |angular velocity| > 0.1 rad/s ⟨proposed deadband⟩. On a moving tick the driver is **self** if the motor command is non-zero and the external mover is inactive, **external** if the external mover is active (*whether or not the agent is commanding*), and undefined otherwise.
- **Primary label, "who moved it" (trailing):** on each *non-moving* tick within K_trail = 30 ticks ⟨proposed⟩ after the last moving tick, the label is that last moving tick's driver (self = 1, external = 0). Excluded if the driver is undefined. Nothing is moving, so cancelling self-motion (implicit compensation) can't carry this label; only state that persists can.
- **Secondary label, "who moved it" (during motion):** on each moving tick, the label is its driver.
- The "external while commanding" ticks are what stop either label collapsing to "am I commanding." Report their fraction for each label; it must be ≥ 25% of label-0 ticks for each.

## 5. Decoding protocol

- **Decoder:** linear logistic regression, class-balanced; observer side, trained offline.
- **Inputs:** population activity only. Never errors, raw inputs, or the trace.
- **Split:** blocked, interleaved cross-validation within each evaluation window: split the window into 10 contiguous blocks, train on even blocks and test on odd blocks, and drop the first 200 ticks of every block after the first so neighbouring ticks can't leak across the train/test boundary. **Never a random split.** (Pilot P4: a random split falsely closed the plastic-vs-frozen gap through neighbour leakage.)
- **Evaluation windows:** consecutive 5-minute blocks, so decodability is tracked across the run.
- **Metric:** balanced accuracy.

## 6. Primary criterion (pass/fail)

In the final evaluation window, per seed, on the **plastic** population (Arche's claim: the distinction emerges through local learning), using the **trailing** label:

> **G = BA(Real, plastic) − max(BA(Yoked, plastic), BA(Yoked, frozen), BA(sensation-only), BA(command-only))**

BA(Yoked, frozen) is in the max because its weights never change, so it can't collapse: a yoked-plastic population that collapses under non-causal commands can't lower the bar. Yoked collapse flags (Section 9) are still reported as diagnostics.

The frozen statistic, **G_frozen = BA(Real, frozen) − max(BA(Yoked, frozen), BA(sensation-only), BA(command-only))**, is reported as a reference line ("the design can carry it"), not as the claim.

- **Sensation-only baseline:** the same frozen population fed sensations with the trace zeroed.
- **Command-only baseline:** the same frozen population fed the trace with sensations zeroed.
- **Noise floor σ₀:** SD across seeds of BA(Yoked) − BA(Null yoked).
- **PASS** if all hold: mean G ≥ 3·σ₀; G > 0 in ≥ 4 of 5 seeds; 95% CI of mean G excludes 0.
- **Baselines and gate use the same label as the statistic** (trailing here, during-motion for Secondary 5).
- **Validity gate (must hold or the run doesn't count):** sensation-only BA ≤ 0.60 and command-only BA ≤ 0.68. (0.68 set before any governed run, after a proxy pilot seed reached 0.64.) If a baseline passes, the ambiguity isn't real; that's a physics/channel-tier setup fix, not a result.

## 7. Secondary criteria

1. **Plasticity vs reference:** D = BA(Real, plastic) − BA(Real, frozen), and the difference-in-differences (plastic − frozen)Real − (plastic − frozen)Yoked. Reported with CIs. **Pre-registered prediction: D ≥ 0** (the locked rule preserves or sharpens self-information). Proxy pilots found D ≈ −0.1 to −0.19 with the placeholder rule.
2. **Agency gain:** mean per-channel agency gain on angle and angular velocity > 0 in the final window, all seeds, **computed on self-driven, no-contact ticks** (driver = self per Section 4; ground truth shows no contact). Observer-side conditioning on ground truth; the agent never sees it. Reported separately. Descriptives, not pass/fail: the all-ticks mean and the mean on external-driven ticks. Why conditioned: the efference readout bets on the command, so on external-driven ticks its error is larger than blind's and gain is negative by design (that difference is the self/world signal), and rare impacts dominate the all-ticks mean. Frozen-population pilot (P7): angvel gain on self-driven no-contact ticks +1.7e-3 to +3.0e-3 in all 5 seeds, negative on the rest, top 1% of ticks = 92–96% of error²; the unconditioned mean was ≈ 0 with mixed sign.
3. **Spike test:** zeroing the command input to the Real readout raises its angle and velocity error; ratio > 1 with CI excluding 1.
4. **Wall stays world:** in the Real agent, wall-contact ticks remain separable from free-motion ticks late in the run: final-window separation ≥ 0.8 × first-window separation.
5. **During-motion decoding:** G computed exactly as in Section 6 but on the during-motion label (G_during). Same pass rule. A pass here alone may reflect implicit compensation (cancelled self-motion), so it is reported as secondary evidence, never as the claim.

## 8. Exploratory (not pass/fail)

- Command-trace ablation: change in G and D without the trace (spec v4.8 open question).
- Ball vs wall separation in population activity.
- Decodability trajectory across windows (does it rise, hold, or decay).

## 9. Failure-tier mapping

- **Physics / channel tier:** validity gate fails, or a sanity check fails. Fix, re-run, not counted.
- **Learning tier:** Real efference error on angle/velocity doesn't fall from first to final window; the population blows up, goes silent, or collapses (effective-rank flag below); or **the primary fails on the plastic population while G_frozen would pass**. The boundary claim is untested, not failed.
  - **Direction-loss diagnostic** (from `pilots/dir.py`): f(W, d) = ‖W·d‖ / ‖W‖, with d = (trace − angular velocity)/√2 in the input order [angle, ang_vel, contact, trace], i.e. d = (0, −1, 0, 1)/√2. Report f(W_final, d) / f(W_0, d) per seed for every plastic condition (not the ablation, which has no trace input). Flag a seed if the ratio falls below 0.5. Why: P4 found the command-vs-motion direction losing weight under plasticity with no dead nodes, and P6 found the median pairwise cosine ≈ 0 in the plastic population, so a cosine check can't catch this failure.
  - **Collapse diagnostic (effective rank):** r(W) = (Σσᵢ²)² / Σσᵢ⁴ over W's singular values σᵢ (participation ratio; 1 ≤ r ≤ 4 for 16×4 W). Report r(W_final) / r(W_0) per seed for every plastic condition. Flag a seed if r(W_final) / r(W_0) < 0.65, **or** r(W_final) < 2.5 **and** r(W_final) < r(W_0). The ratio catches large relative drops (a 2D collapse from a typical init is ≈ 1.9 / 3.2 ≈ 0.6). The floor catches a 2D collapse from a low-starting init, which the ratio alone misses in ~36% of random inits; the "and below initial" guard stops a seed being flagged just for starting low (~1.6% of random inits start below 2.5). Catches both ± collapse (nodes on +v and −v, r = 1) and subspace collapse (all nodes in a 2D plane, r ≈ 2), which a pairwise cosine check misses (signed cosine is blind to ±; no pairwise check sees a shared subspace). Reference: a random dense 16×4 N(0, 0.5) init has r ≈ 3.2 (≈ 4 / (1 + 4/16); 1st percentile 2.4, 10,000 draws); a healthy run may exceed ratio 1, since Sanger's rule orthogonalises.
  - **Per-seed rule (both diagnostics):** a seed is flagged if either diagnostic flags it in the Real plastic condition (Yoked plastic flags are reported as diagnostics only; Section 6 keeps them from affecting G); seeds are judged individually, never on the mean across seeds. If 2 or more seeds are flagged, the run is learning tier (boundary claim untested), since 4 healthy seeds are no longer possible for the primary rule (G > 0 in ≥ 4 of 5). A single flagged seed is reported but doesn't reclassify the run.
- **Boundary tier:** validity gate holds, the population is healthy, and the primary fails on the plastic population **and** G_frozen fails too; or Secondary 4 fails.
- **Named outcome, "encoding gap reproduced":** Secondary 5 (during motion) passes and the primary (trailing) fails. The agent compensates for its own motion but doesn't carry readable self-state once motion stops: Ye's encoding gap in this system. Boundary-tier result about spec v4.8's claim that the command trace makes the boundary legible; read it alongside the trace ablation.

## 10. Sanity checks before any governed run

- Yoked agents receive the identical observation sequence to the Real agent (assert every tick).
- Frozen conditions' population weights don't change (assert).
- Decoder inputs contain no error, raw-input, or trace columns (assert on column names).
- No cognitive module imports `pymunk` (grep).
- External-mover schedule never appears in `read_sensors()` output (assert on keys).

## Amendments

(none)
