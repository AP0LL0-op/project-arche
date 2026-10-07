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

class BlindModel:

    #similar to efference model, but blind to commands and 1 constant
    def __init__(self, channels, learning_rate):
        self.learning_rate = learning_rate
        self.weights = {}
        for channel in channels:
            self.weights[channel] = 0.0

    def predict(self, state):
        prediction = {}
        for channel in state:
            prediction[channel] = state[channel] + self.weights[channel] * 1
        return prediction

    def learn(self, error):
        for channel in self.weights:
            self.weights[channel] += self.learning_rate * error[channel] * 1