"""Pilot P5: external mover on-probability p (setup adequacy only, no decoder).

For each p and pilot seed, runs the step-3 loop (efference + blind models,
babbler, mover) and reports setup-level quantities only:
  - fraction of ticks where self / mover drives the arm, and where it is still
  - trailing-label counts per class (PREREG section 4)
  - "external while commanding" share of label-0 trailing ticks (must be >= 25%)
  - mean per-channel agency gain over the last minute
Decoder BA is deliberately not computed: p is chosen on setup adequacy,
blind to the result.

Seeds: agent babbler s, mover s + 50, for s in 100..104 (pilot range 100-199).
Run from the repo root: python3 pilots/p5_mover_duty.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from babbler import Babbler
from forward_model import BlindModel, EfferenceModel
from world import World

DT = 1 / 60
RUN_SECONDS = 300
LEARNING_RATE = 0.01
DEADBAND = 0.1   # rad/s, PREREG proposed
K_TRAIL = 30     # ticks, PREREG proposed
SEEDS = range(100, 105)
PS = [1 / 3, 1 / 2, 2 / 3]


def run(seed, p):
    world = World(mover_seed=seed + 50, mover_on_prob=p)
    babbler = Babbler(seed=seed)
    channels = list(world.read_sensors())
    efference = EfferenceModel(channels, learning_rate=LEARNING_RATE)
    blind = BlindModel(channels, learning_rate=LEARNING_RATE)

    n_ticks = round(RUN_SECONDS / DT)
    last_minute = n_ticks - round(60 / DT)
    gain_sum = {c: 0.0 for c in channels}
    counts = {"self": 0, "external": 0, "undefined": 0, "still": 0}
    trailing = {1: 0, 0: 0}
    ext_while_cmd = 0
    last_driver = None      # (driver, agent_was_commanding) of last moving tick
    ticks_since_moving = None

    for tick in range(n_ticks):
        command = babbler.next_command()
        state = world.read_sensors()
        blind_pred = blind.predict(state)
        eff_pred = efference.predict(state, command)
        world.apply_motor(command)
        world.step(DT)
        truth = world.ground_truth()
        observed = world.read_sensors()

        blind_err = {c: observed[c] - blind_pred[c] for c in channels}
        eff_err = {c: observed[c] - eff_pred[c] for c in channels}
        efference.learn(command, eff_err)
        blind.learn(blind_err)
        if tick >= last_minute:
            for c in channels:
                gain_sum[c] += blind_err[c] ** 2 - eff_err[c] ** 2

        moving = abs(observed["angular_velocity"]) > DEADBAND
        if moving:
            if truth["mover_active"]:
                driver = "external"
            elif command != 0:
                driver = "self"
            else:
                driver = "undefined"
            counts[driver] += 1
            last_driver = (driver, command != 0)
            ticks_since_moving = 0
        else:
            counts["still"] += 1
            if ticks_since_moving is not None:
                ticks_since_moving += 1
                if ticks_since_moving <= K_TRAIL and last_driver[0] != "undefined":
                    label = 1 if last_driver[0] == "self" else 0
                    trailing[label] += 1
                    if label == 0 and last_driver[1]:
                        ext_while_cmd += 1

    n_last = n_ticks - last_minute
    return {
        "frac": {k: v / n_ticks for k, v in counts.items()},
        "trailing": trailing,
        "ext_while_cmd": ext_while_cmd / trailing[0] if trailing[0] else float("nan"),
        "gain": {c: gain_sum[c] / n_last for c in channels},
    }


def main():
    print(f"P5: {RUN_SECONDS}s per run, seeds {SEEDS.start}-{SEEDS.stop - 1}, "
          f"deadband {DEADBAND}, K_trail {K_TRAIL}\n")
    for p in PS:
        print(f"=== p = {p:.2f} ===")
        print("seed | self  ext   undef still | trail self  trail ext | ext&cmd | "
              "gain angle   gain angvel  gain contact")
        for seed in SEEDS:
            r = run(seed, p)
            f, t, g = r["frac"], r["trailing"], r["gain"]
            print(f"{seed} | {f['self']:.2f}  {f['external']:.2f}  {f['undefined']:.2f}  "
                  f"{f['still']:.2f} | {t[1]:10d} {t[0]:10d} | {r['ext_while_cmd']:7.2f} | "
                  f"{g['angle']:+.2e}   {g['angular_velocity']:+.2e}   {g['contact']:+.2e}")
        print()


if __name__ == "__main__":
    main()
