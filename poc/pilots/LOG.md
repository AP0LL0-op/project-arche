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

## P6 — fixed random sparse input mask, numpy proxy (`pilots/p6_sparse_mask.py`)

Hypothesis: P4 found the plastic rule drags nodes toward dominant input variance and loses the command-vs-motion direction. A fixed random sparse input mask (each node wired to exactly k of the 4 inputs) might constrain that drift and reduce collapse.

**Setup.** Numpy proxy (not Pymunk), P4 setup held fixed: proxy body with overriding external mover, 16 nodes, W0 ~ N(0, 0.5), θ = 0, leak 0.9, error-gated Sanger at η = 2e-3, modulator |e| / running SD on ω (proxy form, not PREREG 3b), delta-rule readout, blocked interleaved CV decoder on the second half of 30,000 ticks. One variable: mask. Each node gets exactly k distinct inputs drawn without replacement from its own RNG (seed + 13). W = W0 × mask; plastic updates × mask; masked weights asserted zero every tick (held). Dense path verified identical to `diag.py` `run()`. Label: trailing "who moved it" per PREREG 4 (P3/P4 used the during-motion label, so dense numbers here are not comparable to P4's). Seeds 100–104. Collapse: median pairwise signed cosine of weight rows at 5 min. Dead: node never active (relu > 0) in the decoder half. Raw output: `pilots/p6_results.txt`.

Validity: external-while-commanding share of label 0 = 0.62 (0.60–0.65), ≥ 25%. The proxy mover is on ~2/3 of the time (P5 rejected p = 2/3 in Pymunk as too thin on self-trailing ticks); held fixed here, so self examples are few and BA is noisy.

**Result.**
| Condition | BA plastic | BA frozen | plastic − frozen | cos plastic | cos frozen | dead (p / f) |
|---|---|---|---|---|---|---|
| dense | 0.66 (0.49–0.81) | 0.67 (0.59–0.75) | −0.01 (−0.10–+0.20), > 0 in 1/5 | −0.01 (−0.09–0.05) | −0.01 (−0.06–0.06) | 0 / 0 |
| sparse k=2 | 0.71 (0.65–0.80) | 0.69 (0.60–0.79) | +0.03 (−0.05–+0.16), > 0 in 2/5 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0 / 0 |
| sparse k=3 | 0.63 (0.50–0.73) | 0.68 (0.60–0.76) | −0.06 (−0.21–+0.06), > 0 in 1/5 | −0.02 (−0.08–0.12) | 0.00 (−0.04–0.05) | 0 / 0 |

- Per-seed gap spread (~±0.15) is larger than any between-condition difference. k=2's +0.03 is not distinguishable from dense with 5 seeds, and k=3 goes the other way.
- No collapse to reduce: dense plastic median cosine ≈ 0, same as frozen. The premise of the hypothesis doesn't show up on this metric.
- The k=2 cosine is exactly 0 in every seed, plastic and frozen: an artifact (pairs with disjoint wiring score 0, which fixes the median). The metric can't speak to k=2.
- Signed cosine also can't see nodes collapsing onto ± the same feature; an |cos| median or `dir.py`'s command-vs-motion projection would measure P4's actual finding (direction loss, not collapse) more directly.
- Masking also halves (k=2) or cuts by a quarter (k=3) each node's expected input drive, a second change that comes with "dense × mask".

**Verdict.** No effect detectable. Sparse masking does not earn a Pymunk pilot on this evidence. Side finding: under the trailing label the dense proxy's plasticity penalty is ≈ 0 (−0.01), versus −0.13 under the during-motion label in P4; whether that holds is for the Pymunk pilots, not this proxy.
