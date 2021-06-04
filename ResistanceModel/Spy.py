from ResistanceModel.AbstractAgent import AbstractAgent

class Spy(AbstractAgent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

    def initKB(self):
        self.KB.add("q")

    def updateKB(self):
        print(f"Still needs to be implemented")

    def updateMissionPreference(self):
        print(f"Still needs to be updated")

