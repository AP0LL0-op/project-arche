class ForwardModel:

    # persistence baseline: predict next tick = this tick
    def predict(self, state):
        return state.copy()

class EfferenceModel:

    # weights start at zero so the model knows nothing about its commands at bootstrap
    def __init__(self, channels, learning_rate):
        self.learning_rate = learning_rate
        self.weights = {}
        for channel in channels:
            self.weights[channel] = 0.0

    def predict(self, state, command):
        prediction = {}
        for channel in state:
            prediction[channel] = state[channel] + self.weights[channel] * command
        return prediction

    def learn(self, command, error):
        for channel in self.weights:
            self.weights[channel] += self.learning_rate * error[channel] * command
    