class ForwardModel:

    # persistence baseline: predict next tick = this tick
    def predict(self, state):
        return state.copy()