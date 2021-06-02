from mesa import Agent


class EpistemicState(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, is_spy):
        super().__init__(unique_id, model)
        self.KB = []
        self.R = []

    def step(self):
        # Update
        print (f"Hi, this state contains the KB {str(self.KB)}.")
