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
