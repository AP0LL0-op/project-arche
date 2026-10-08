import numpy as np


# linear readout: predicts the next sensory state as current state + R z,
# where z = the features with a constant 1 appended (bias)
# learns by the delta rule: each weight moves by learning_rate * its channel's error * its input
class Readout:
    def __init__(self, channels, n_features, learning_rate=1e-3):
        self.channels = list(channels)
        self.learning_rate = learning_rate
        self.R = np.zeros((len(self.channels), n_features + 1))

    def _z(self, features):
        return np.append(features, 1.0)

    def predict(self, state, features):
        change = self.R @ self._z(features)
        return {c: state[c] + change[i] for i, c in enumerate(self.channels)}

    def learn(self, features, error):
        e = np.array([error[c] for c in self.channels])
        self.R += self.learning_rate * np.outer(e, self._z(features))
