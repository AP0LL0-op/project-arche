import numpy as np

# PREREG 3a: fixed order; new streams go on the end so existing ones don't change
STREAMS = ["init", "agent", "mover", "yoked", "null_yoked"]


# one run seed -> independent named streams
def seed_streams(seed):
    children = np.random.SeedSequence(seed).spawn(len(STREAMS))
    return dict(zip(STREAMS, children))


# a random.Random seed (e.g. for Babbler) from a stream
def python_seed(child):
    return int(child.generate_state(1)[0])
