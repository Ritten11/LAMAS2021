from ResistanceModel.AbstractAgent import AbstractAgent
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
import random

class Spy(AbstractAgent):
	def __init__(self,unique_id, model):
		super().__init__(unique_id, model)

	def initKB(self):
		formula = str(self.unique_id)
		print(formula)
		self.KB.add(formula)
		self.card = None
		self.vote = None

	def step(self):
		if self.model.state == "choose_team":
			if self.model.mission_leader == self.unique_id:
				self.model.grid.move_agent(self, (self.unique_id, 2))
				self.model.mission_team = self.choose_team()
				print(f"team is {self.model.mission_team}")
			else: 
				self.model.grid.move_agent(self, (self.unique_id, 0))

		if self.model.state == "vote":
			self.vote = "No" # for testing
			print(f"Agent {self.unique_id} voted {self.vote}")

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


	# TODO: Make sure mission team is unique members
	def choose_team(self):
		mission_team = []
		# in the first mission the spy wants any one spy in the mission so that it fails, but not both
		if self.model.mission_number == 1:
			mission_team.append(random.choice(self.model.spies_ids))
			while len(mission_team) != self.model.team_sizes[self.model.mission_number - 1]:
				temp = random.choice(range(1, self.model.num_agents+1))
				if temp not in self.model.spies_ids:
					mission_team.append(temp)
		else: 
			
			dont_choose = []
			knows = []
			for agent in range(1, self.model.num_agents+1):
				if agent not in self.model.spies_ids:
					print(f"agent: {agent}")
					formula1 = And(Box_a(str(agent), Atom(str(self.model.spies_ids[0]))),Atom(str(self.model.spies_ids[0]))) # agent knows that spy1
					nodes1 = self.model.kripke_model.ks.nodes_not_follow_formula(formula1)
					formula2 = And(Box_a(str(agent), Atom(str(self.model.spies_ids[1]))),Atom(str(self.model.spies_ids[1]))) # agent knows that spy2
					nodes2 = self.model.kripke_model.ks.nodes_not_follow_formula(formula2)
					print(f"nodes for form1: {nodes1}")
					print(f"nodes for form2: {nodes2}")

					if len(nodes1) < len(self.model.kripke_model.ks.worlds):
						dont_choose.append(self.model.spies_ids[0])
						knows.append(agent)
					if len(nodes2) < len(self.model.kripke_model.ks.worlds):
						dont_choose.append(self.model.spies_ids[1])
						knows.append(agent)

			if dont_choose == len(self.model.spies_ids):
				mission_team.append(random.choice(dont_choose))
			else: 
				mission_team.append(self.model.spies_ids[self.model.spies_ids != dont_choose])

			while len(mission_team) != self.model.team_sizes[self.model.mission_number - 1]:
				temp = random.choice(range(1, self.model.num_agents+1))
				if temp not in dont_choose and temp not in mission_team: 
					mission_team.append(temp)
		return mission_team

		print(f"chosen_team: {mission_team}")

	def updateKB(self):
		print(f"Still needs to be implemented")

	def updateMissionPreference(self):
		print(f"Still needs to be updated")

