from mesa import Agent


class AbstractAgent(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.KB = set()
        self.model = model
        self.unique_id = unique_id

    def step(self):
        if self.model.state == "choose_team":
            if self.model.mission_leader == self.unique_id:
                self.model.grid.move_agent(self, (self.unique_id, 2))
                #self.chooseTeam()
                self.model.mission_team = [1,2]
                print(f"not sure whether this will be different for resistance and spy")

        if self.model.state == "vote":
           print(f"not sure whether this will be different for resistance and spy")

        if self.model.state == "go_on_mission":
            if self.unique_id in self.model.mission_team:
                self.model.grid.move_agent(self, (self.unique_id, 4))

        if self.model.state == "play":
            if self.unique_id in self.model.mission_team:
                print(f"Pass or Fail card is played")
           

        if self.model.state == "update_knowledge":
            self.model.grid.move_agent(self, (self.unique_id, 0))
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
