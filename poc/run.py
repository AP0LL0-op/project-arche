from world import World
from forward_model import ForwardModel
from forward_model import EfferenceModel
import os
from logger import Logger
os.makedirs("logs", exist_ok=True)

dt = 1/60
run_seconds = 10
reverse_seconds = 4
world = World()
channels = list(world.read_sensors())
persistence = ForwardModel()
efference = EfferenceModel(channels, learning_rate=0.01)
fieldnames = ["sim_time", "command"]
for channel in channels:
    fieldnames.append(f"{channel}_pred")
    fieldnames.append(f"{channel}_obs")
    fieldnames.append(f"{channel}_err")
logger = Logger('logs/run.csv', fieldnames)

# 1. read sensors           → current state     (what I feel now)
# 2. pick a motor command
# 3. predict next state     → prediction        (what I think I'll feel next)
# 4. apply command, step    → physics happens
# 5. read sensors again     → observed state    (what I actually feel)
# 6. error = observed − predicted, per channel
# 7. log it

for tick in range(round(run_seconds/dt)):
    sim_time = tick * dt
    window = int(sim_time//reverse_seconds)
    if window % 2 == 0:
        command = 2
    else:
        command = -2
    state = world.read_sensors()
    blind_pred = persistence.predict(state)
    eff_pred = efference.predict(state, command)
    world.apply_motor(command)
    world.step(dt)
    observed = world.read_sensors()
    blind_error = {}
    eff_error = {}
    row = {"sim_time": sim_time, "command": command}
    for channel in observed:
        blind_error[channel] = observed[channel] - blind_pred[channel]
        eff_error[channel] = observed[channel] - eff_pred[channel]
        row[f"{channel}_pred"] = blind_pred[channel]
        row[f"{channel}_obs"] = observed[channel]
        row[f"{channel}_err"] = blind_error[channel]
    efference.learn(command, eff_error)
    if tick % 60 == 0:
        print(round(sim_time), efference.weights)
    logger.log(row)
logger.close()