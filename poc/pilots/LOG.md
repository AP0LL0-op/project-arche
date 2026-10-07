# Pilot log

Every pilot variant tried, including the ones that lost. Pilots are evidence about the design, not results. They never use governed seeds (governed runs: seeds 0–4 in Pymunk; Pymunk pilots: seeds 100–199). See `PREREG.md`.

Balanced accuracy (BA) throughout, 5 seeds unless noted, mean (min–max).

---

## P1 — agreement label, numpy proxy (`pilot.py`)

**Setup.** Numpy proxy physics (not Pymunk): motor drives ω toward the commanded rate, walls at ±1 rad, random ball kicks. 30,000 ticks. 16-node population, Sanger's rule gated by readout error. Label: "did my own commands over the last K = 30 ticks agree in sign with my motion?" Decoder: logistic regression, second half of the run, 70/30 time split.

**Result.**
- Real agent: 96–99% of windows are "agree." Nothing to decode.
- Yoked agent: a frozen nonlinear population decodes the label at 0.92–0.97, because it's computable from the agent's own inputs.
- The difference-in-differences came out positive anyway (linear: +0.11, 4/5 seeds; relu: +0.08, 3/5), driven by plasticity degrading the yoked agent.

**Verdict.** Label dropped. Also shows the DiD can "pass" on a label that measures nothing.

## P2 — "who moved it," external mover added to the drive (`pilot2.py`)

**Setup.** As P1, plus an external mover with the same babbling profile, added to the drive. Label 1 = motor only, 0 = external only.

**Result.**
| Condition | BA |
|---|---|
| sensations only | 0.42 (0.25–0.63) |
| real, relu, frozen | 0.87 (0.79–0.93) |
| real, relu, plastic | 0.68 (0.39–0.85) |
| real, linear, frozen | 0.45 |
| yoked, relu, frozen | 0.40 |

**Verdict (after P3).** Looked like a pass. It wasn't: see P3.

## P3 — breaking P2 (Claude Code; scripts lost when its scratchpad was reset, results recorded here)

**Finding 1: the P2 label reduces to "am I commanding."** On every labelled tick, label 1 ⇔ command ≠ 0 (fraction of labelled ticks with command ≠ 0 and label 0: 0.000).
| Decoded from | BA |
|---|---|
| \|trace\| alone, linear | 0.903 (0.88–0.92) |
| trace only, frozen relu population | 0.877 |
| full real agent | 0.865 |

The command alone beats the agent. "Nonlinearity required" in P2 = computing |trace|.

**Finding 2: an external mover twice as strong, added to the drive, leaks the label into sensations.** Sensations only (frozen relu population): 0.81. Rejected.

**Finding 3: an overriding external mover works.** When active, the mover replaces the motor drive (same profile). Label 0 = external active, whether or not the agent is commanding.
| Condition | BA |
|---|---|
| sensations only (frozen relu pop) | 0.52 (0.48–0.59) |
| command only (frozen relu pop) | 0.58 (0.47–0.64) |
| **real, frozen** | **0.71 (0.55–0.82)** |
| yoked, frozen | 0.50 (0.44–0.55) |
| real, plastic | 0.60 (0.46–0.72) |

**Verdict.** Adopted as the PREREG design (overriding mover; sensation-only and command-only baselines; validity gate). Plasticity still lowers BA (0.71 → 0.60): the placeholder rule's open problem.

## P4 — diagnosing why plasticity hurts (`diag.py`, `dir.py`)

- Ruled out: dead nodes (15/16 active after learning).
- Ruled out: decoder staleness. Interleaved-block decoder: plastic 0.62 vs frozen 0.75. A random split appeared to close the gap, but that was neighbouring ticks leaking into the test set.
- Partly supported, inconsistent across seeds: learning reshapes weights toward dominant input variance, and the command-vs-motion direction loses weight in some seeds.
- Confirmed: capacity matters (4 nodes worse than 16, frozen and plastic).

**Verdict.** Error-gated Sanger's rule isn't aimed: the gate sets how much it learns, not what. Rule to be chosen by Pymunk pilots (CLAUDE.md step 4g).

## P5 — external mover in Pymunk: override form and on-probability p (`pilots/p5_mover_duty.py`)

First Pymunk pilot. Setup-adequacy only: no population, no decoder, so p is chosen blind to BA.

**Setup.** Step-3 loop (efference model `state + w·command`, blind model `state + w·1`, learning rate 0.01, no input normalisation). Agent babbling per PREREG 3a ({−2, 0, +2}, 30–180 ticks). External mover = second `SimpleMotor` on the arm driven by its own `Babbler`, `p_zero = 1 − p`. 300 s per run. Seeds: agent s, mover s + 50, s = 100–104. Moving = |ω| > 0.1 rad/s; trailing label per PREREG 4 with K_trail = 30.

**Variant A (rejected): mover overpowers the motor.** Mover `max_force` 10× the motor's (1e6 vs 1e5), both engaged. The override works (opposing commands: arm follows mover), but the mover spins the arm up to 2 rad/s in 3 ticks versus the motor's 24. The driver is readable from angular velocity onset alone, the P2 leak in another form.

**Variant B (adopted): mover replaces the motor.** When active, the agent's motor goes to `max_force = 0` and the mover drives at the motor's `max_force`. Spin-up is identical (24 ticks both). Matches P3's overriding mover. PREREG 3a's proposed form ("higher `max_force`") needs updating to this.

**Result (variant B), mean over 5 seeds.**
| p | self drives | mover drives | still | trailing ticks self / ext (min–max) | ext-while-commanding share of label 0 |
|---|---|---|---|---|---|
| 1/3 | 0.41 | 0.36 | 0.20 | 320 (256–431) / 241 (169–301) | 0.61 (0.45–0.76) |
| 1/2 | 0.29 | 0.54 | 0.15 | 222 (133–335) / 335 (221–383) | 0.68 (0.51–0.80) |
| 2/3 | 0.19 | 0.68 | 0.11 | 136 (98–162) / 465 (395–563) | 0.66 (0.56–0.75) |

≥ 25% external-while-commanding holds at every p (independent schedules make it ≈ P(agent commanding) regardless of p).

**Agency gain (last 60 s) is negative on angular velocity (≈ −2e-3) and contact (≈ −100) at every p, and also at p = 0 (no mover).** Not caused by the mover. Causes: the two models are not nested (efference has a command term and no bias; blind has a bias and no command), the model form can't express a velocity-target motor (Δω depends on ω, not just the command), and contact is unnormalised, so the efference model's effective rate (lr·command² = 4·lr) makes it jitter harder on the noisiest channel. Learning tier, placeholder model; superseded by step 4c (normalised inputs, nested readouts on [activity, command] vs [activity]).

**Verdict.** Variant B adopted. **p = 1/3 provisional**: most body control, most trailing data, classes within ~1.3:1; 2/3 rejected (self-trailing ticks as low as 98 per 5 min, ~1:3.5). Re-check once 4c exists, because "does the agent learn its own body" couldn't be assessed with the step-3 model. Note for PREREG: ~560 trailing ticks per 5 min is thin once blocked CV drops 200 ticks per block; revisit window length and K_trail.
