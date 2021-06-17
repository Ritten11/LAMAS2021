from ResistanceModel.AbstractAgent import AbstractAgent
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
import random

class Resistance(AbstractAgent):
	def __init__(self,unique_id, model):
		super().__init__(unique_id, model)

	def initKB(self):
		formula = str(self.unique_id)
		print(formula)
		self.KB.add("p")
		self.card = None
		self.vote = None

	def step(self):
		if self.res_model.state == "choose_team":
			if self.res_model.mission_leader == self.unique_id:
				self.res_model.grid.move_agent(self, (self.unique_id, 2))
				self.res_model.mission_team = self.choose_team()
				print(f"team is {self.res_model.mission_team}")

		if self.res_model.state == "vote":
			self.vote = "Yes" # for testing
			print(f"Agent {self.unique_id} voted {self.vote}")

		if self.res_model.state == "go_on_mission":
			if self.unique_id in self.res_model.mission_team:
				self.res_model.grid.move_agent(self, (self.unique_id, 4))

		if self.res_model.state == "play":
			if self.unique_id in self.res_model.mission_team:
				self.card = "Pass"
				print(f"{self.card} card is played by {self.unique_id}")
		   

		if self.res_model.state == "update_knowledge":
			self.res_model.grid.move_agent(self, (self.unique_id, 0))
			self.updateKB()
			self.updateMissionPreference()

	def choose_team(self):
		mission_team = []
		# in the first mission the resistance agent trusts themselves but knows nothing about other agents
		if self.res_model.mission_number == 1:
			mission_team.append(self.unique_id)
			while len(mission_team) != self.res_model.team_sizes[self.res_model.mission_number - 1]:
				temp = random.choice(range(1, self.res_model.num_agents + 1))
				if temp != self.unique_id:
					mission_team.append(temp)
			mission_team = [1,5]
		else:
			dont_choose = []

			for agent in range(1, self.model.num_agents+1):
				print(f"agent: {agent}")
				formula = And(Box_a(str(self.unique_id), Atom(str(agent))), Not(Atom(str(self.unique_id))))
				nodes = self.model.kripke_model.ks.nodes_not_follow_formula(formula)
				if len(nodes) < len(self.model.kripke_model.ks.worlds):
					dont_choose.append(agent)
				print(nodes)


			mission_team.append(self.unique_id) # agent still trusts themselves
			while len(mission_team) != self.model.team_sizes[self.model.mission_number - 1]:
				temp = random.choice(range(1, self.model.num_agents+1))
				if temp != self.unique_id and temp not in dont_choose:
					mission_team.append(temp)
		return mission_team

	def updateKB(self):
		print(f"Still needs to be implemented")

	def updateMissionPreference(self):
		print(f"Still needs to be updated")

