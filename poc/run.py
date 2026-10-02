from world import World
from forward_model import ForwardModel

dt = 1/60
run_seconds = 10
reverse_seconds = 4
world = World()
model = ForwardModel()

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
    prediction = model.predict(state)
    world.apply_motor(command)
    world.step(dt)
    observed = world.read_sensors()
    error = {}
    for channel in observed:
        error[channel] = observed[channel] - prediction[channel]
    print(error, sim_time, window)