from world import World
from babbler import Babbler
from population import Inputs, Population, initial_weights
from readout import Readout
from seeds import python_seed, seed_streams
import numpy as np
import os
from logger import Logger
os.makedirs("logs", exist_ok=True)

dt = 1/60
run_seconds = 10
run_seed = 100  # pilot range 100-199; governed runs use 0-4
streams = seed_streams(run_seed)
world = World(mover_seed=python_seed(streams["mover"]), mover_on_prob=1/3)
channels = list(world.read_sensors())
truth_names = list(world.ground_truth())
babbler = Babbler(seed=python_seed(streams["agent"]))

# agent: population on sensors + command trace; efference readout on [activity, command]
W = initial_weights(streams["init"])
real_inputs = Inputs(use_trace=True)
real_population = Population(W)
efference = Readout(channels, n_features=W.shape[0] + 1)

# observer: blind population (same weights minus the trace column, sensors only); readout on [activity]
blind_inputs = Inputs(use_trace=False)
blind_population = Population(W[:, :3])
blind = Readout(channels, n_features=W.shape[0])
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
    eff_features = np.append(real_population.step(real_inputs.assemble(state, command)), command)
    blind_features = blind_population.step(blind_inputs.assemble(state))
    eff_pred = efference.predict(state, eff_features)
    blind_pred = blind.predict(state, blind_features)
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
    efference.learn(eff_features, eff_error)
    blind.learn(blind_features, blind_error)
    if tick % 60 == 0:
        print(round(sim_time))
    logger.log(row)
logger.close()