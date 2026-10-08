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
        old_mean = self.mean
        self.mean = self.mean + alpha * (x - old_mean)
        # Welford: deviation from the old mean times deviation from the new one,
        # exact running variance during warm-up (squaring the new-mean deviation undercounts)
        self.var = self.var + alpha * ((x - old_mean) * (x - self.mean) - self.var)
        sd = math.sqrt(self.var + self.epsilon)
        return (x - self.mean) / sd