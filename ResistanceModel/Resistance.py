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
		if self.model.state == "choose_team":
			if self.model.mission_leader == self.unique_id:
				self.model.grid.move_agent(self, (self.unique_id, 2))
				self.model.mission_team = self.choose_team()
				print(f"team is {self.model.mission_team}")

		if self.model.state == "vote":
			# Checks whether the agent accepts the mission team or not
			suspicions = [0] * self.model.num_agents
			relations = self.model.kripke_model.relations[str(self.unique_id)]
			worlds = [rel[1] for rel in relations if rel[0] == self.model.true_world]
			print(worlds)
			for agent in self.model.schedule.agents:
				ids = str(agent.unique_id)
				idx = agent.unique_id-1
				if agent.unique_id == self.unique_id:
					continue
				else:
					for world in worlds:
						if ids in world:
							suspicions[idx] += 1

			s = 0
			for a in self.model.mission_team:
				s += suspicions[a - 1]

			# TODO: Find good condition for this
			if s < len(worlds):
				self.vote = "Yes"
			else:
				self.vote = "No"
			print(f"Agent {self.unique_id} voted {self.vote}")

		if self.model.state == "go_on_mission":
			if self.unique_id in self.model.mission_team:
				self.model.grid.move_agent(self, (self.unique_id, 4))

		if self.model.state == "play":
			if self.unique_id in self.model.mission_team:
				self.card = "Pass"
				print(f"{self.card} card is played by {self.unique_id}")
		   

		if self.model.state == "update_knowledge":
			self.model.grid.move_agent(self, (self.unique_id, 0))
			self.updateKB()
			self.updateMissionPreference()

	# TODO: Make sure that mission_team is unique members
	def choose_team(self):
		mission_team = []
		# in the first mission the resistance agent trusts themselves but knows nothing about other agents
		if self.model.mission_number == 1:
			mission_team.append(self.unique_id)
			while len(mission_team) != self.model.team_sizes[self.model.mission_number - 1]:
				temp = random.choice(range(1, self.model.num_agents+1))
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
				if temp not in mission_team and temp not in dont_choose:
					mission_team.append(temp)
		return mission_team


	def updateKB(self):
		print(f"Still needs to be implemented")

	def updateMissionPreference(self):
		print(f"Still needs to be updated")

