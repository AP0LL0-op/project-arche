import random

class Babbler:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.command = 0 
        self.ticks_left = 0

    def next_command(self):
        if self.ticks_left == 0:
            self.command = self.rng.choice([-2, 0, 2])
            self.ticks_left = self.rng.randint(30, 180)
        self.ticks_left -= 1
        return self.command