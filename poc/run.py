from world import World
from forward_model import BlindModel, EfferenceModel
from babbler import Babbler
import os
from logger import Logger
os.makedirs("logs", exist_ok=True)

dt = 1/60
run_seconds = 10
world = World()
channels = list(world.read_sensors())
truth_names = list(world.ground_truth())
efference = EfferenceModel(channels, learning_rate=0.01)
blind = BlindModel(channels, learning_rate=0.01)
babbler = Babbler(seed=100)
fieldnames = ["sim_time", "command"]
for channel in channels:
    fieldnames.append(f"{channel}_obs")
    fieldnames.append(f"{channel}_blind_pred")
    fieldnames.append(f"{channel}_blind_err")
    fieldnames.append(f"{channel}_eff_pred")
    fieldnames.append(f"{channel}_eff_err")
    fieldnames.append(f"{channel}_gain")
for name in truth_names:
    fieldnames.append(f"truth_{name}")
logger = Logger('logs/run.csv', fieldnames)

# core loop
for tick in range(round(run_seconds/dt)):
    sim_time = tick * dt
    command = babbler.next_command()
    state = world.read_sensors()
    blind_pred = blind.predict(state)
    eff_pred = efference.predict(state, command)
    world.apply_motor(command)
    world.step(dt)
    truth = world.ground_truth()
    observed = world.read_sensors()
    blind_error = {}
    eff_error = {}
    row = {"sim_time": sim_time, "command": command}
    for channel in observed:
        blind_error[channel] = observed[channel] - blind_pred[channel]
        eff_error[channel] = observed[channel] - eff_pred[channel]
        row[f"{channel}_obs"] = observed[channel]
        row[f"{channel}_blind_pred"] = blind_pred[channel]
        row[f"{channel}_blind_err"] = blind_error[channel]
        row[f"{channel}_eff_pred"] = eff_pred[channel]
        row[f"{channel}_eff_err"] = eff_error[channel]
        row[f"{channel}_gain"] = blind_error[channel]**2 - eff_error[channel]**2
    for name in truth:
        row[f"truth_{name}"] = truth[name]
    efference.learn(command, eff_error)
    blind.learn(blind_error)
    if tick % 60 == 0:
        print(round(sim_time))
    logger.log(row)
logger.close()