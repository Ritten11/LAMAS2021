from mesa import Agent


class AbstractAgent(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.KB = set()
        self.model = model
        self.unique_id = unique_id

    def step(self):
        self.updateKB()
        self.updateMissionPreference()

    def initKB(self):
        print(f"initKB not properly implemented in child class of AbstractAgent")
        pass

    def updateKB(self):
        print(f"updateKB not properly implemented in child class of AbstractAgent")
        pass

    def updateMissionPreference(self):
        print(f"updateMissionPreference not properly implemented in child class of AbstractAgent")
        pass
