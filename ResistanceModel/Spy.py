from ResistanceModel.AbstractAgent import AbstractAgent
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star

class Spy(AbstractAgent):
	def __init__(self,unique_id, model):
		super().__init__(unique_id, model)

	def initKB(self):
		formula = str(self.unique_id)
		print(formula)
		self.KB.add(formula)
		self.card = None

	def step(self):
		if self.model.state == "choose_team":
			if self.model.mission_leader == self.unique_id:
				self.model.grid.move_agent(self, (self.unique_id, 2))
				#self.chooseTeam()
				self.model.mission_team = [1,2]
				print(f"team is {self.model.mission_team}")

		if self.model.state == "vote":
		   print(f"not sure whether this will be different for resistance and spy")

		if self.model.state == "go_on_mission":
			if self.unique_id in self.model.mission_team:
				self.model.grid.move_agent(self, (self.unique_id, 4))

		if self.model.state == "play":
			if self.unique_id in self.model.mission_team:
				self.card = "Fail"
				print(f"{self.card} card is played by {self.unique_id}")
		   

		if self.model.state == "update_knowledge":
			self.model.grid.move_agent(self, (self.unique_id, 0))
			self.updateKB()
			self.updateMissionPreference()

	def updateKB(self):
		print(f"Still needs to be implemented")

	def updateMissionPreference(self):
		print(f"Still needs to be updated")

