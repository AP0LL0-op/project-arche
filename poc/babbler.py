import random

class Babbler:
    def __init__(self, seed, p_zero=1/3):
        self.rng = random.Random(seed)
        self.command = 0 
        self.ticks_left = 0
        self.p_zero = p_zero

    def next_command(self):
        if self.ticks_left == 0:
            self.command = self.rng.choices([-2, 0, 2], weights=[(1 - self.p_zero) / 2, self.p_zero, (1 - self.p_zero) / 2])[0]
            self.ticks_left = self.rng.randint(30, 180)
        self.ticks_left -= 1
        return self.command