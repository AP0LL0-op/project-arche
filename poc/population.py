import numpy as np
from normalizer import Normalizer

SENSORY = ["angle", "angular_velocity", "contact"]


# PREREG 3b: W ~ Gaussian(0, 0.5), the first draw from the init stream
def initial_weights(init_stream, n_nodes=16, n_inputs=4):
    return np.random.default_rng(init_stream).normal(0, 0.5, (n_nodes, n_inputs))


# builds the population input x(t): the sensors plus (optionally) the command trace,
# every one normalised by its own Normalizer, same rule for all
class Inputs:
    def __init__(self, use_trace=True, trace_decay=0.95):
        self.use_trace = use_trace
        self.trace_decay = trace_decay
        self.trace = 0.0
        names = SENSORY + (["trace"] if use_trace else [])
        self.normalizers = {name: Normalizer() for name in names}

    def assemble(self, sensors, command=None):
        raw = {name: sensors[name] for name in SENSORY}
        if self.use_trace:
            # signed trace, includes this tick's command (PREREG 3b)
            self.trace = self.trace_decay * self.trace + (1 - self.trace_decay) * command
            raw["trace"] = self.trace
        return np.array([self.normalizers[name].normalize(raw[name]) for name in self.normalizers])


# leaky ReLU nodes: a(t) = leak * a(t-1) + (1 - leak) * relu(W x(t) - theta)
# frozen: W never changes until a plasticity rule is added
class Population:
    def __init__(self, W, leak=0.9, theta=0.0):
        self.W = np.array(W, dtype=float)
        self.leak = leak
        self.theta = theta
        self.a = np.zeros(self.W.shape[0])

    def step(self, x):
        drive = np.maximum(self.W @ x - self.theta, 0.0)
        self.a = self.leak * self.a + (1 - self.leak) * drive
        return self.a
