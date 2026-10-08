import math

class Normalizer:
    def __init__(self, time_constant=1000):
        self.alpha = 1 / time_constant
        self.mean = 0
        self.var = 1
        self.epsilon = 1e-8
        self.count = 0

    def normalize(self, x):
        self.count = self.count + 1
        alpha = max(1/self.count, self.alpha)
        self.mean = self.mean + alpha * (x - self.mean)
        self.var = self.var + alpha * ((x - self.mean)**2 - self.var)
        sd = math.sqrt(self.var + self.epsilon)
        return (x - self.mean) / sd