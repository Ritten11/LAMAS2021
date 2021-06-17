from ResistanceModel.AbstractAgent import AbstractAgent
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
# from ResistanceModel.ResistanceModel import ResistanceModel
import random

class Spy(AbstractAgent):
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)

	def initKB(self):
		formula = str(self.unique_id)
		print(formula)
		self.KB.add(formula)
		self.card = None
		self.vote = None

	def step(self):
		if self.res_model.state == "choose_team":
			if self.res_model.mission_leader == self.unique_id:
				self.res_model.grid.move_agent(self, (self.unique_id, 2))
				self.res_model.mission_team = self.choose_team()
				print(f"team is {self.res_model.mission_team}")

		if self.res_model.state == "vote":
			self.vote = self.decide_on_vote()
			print(f"Agent {self.unique_id} voted {self.vote}")

		if self.res_model.state == "go_on_mission":
			if self.unique_id in self.res_model.mission_team:
				self.res_model.grid.move_agent(self, (self.unique_id, 4))

		if self.res_model.state == "play":
			if self.unique_id in self.res_model.mission_team:
				self.card = "Fail"
				print(f"{self.card} card is played by {self.unique_id}")
		   

		if self.res_model.state == "update_knowledge":
			self.res_model.grid.move_agent(self, (self.unique_id, 0))
			self.updateKB()
			self.updateMissionPreference()


	def choose_team(self):
		mission_team = []
		# in the first mission the spy wants any one spy in the mission so that it fails, but not both
		if self.res_model.mission_number == 1:
			mission_team.append(random.choice(self.res_model.spies_ids))
			while len(mission_team) != self.res_model.team_sizes[self.res_model.mission_number - 1]:
				temp = random.choice(range(1, self.res_model.num_agents + 1))
				if temp not in self.res_model.spies_ids:
					mission_team.append(temp)
		else: 
			mission_team = [1,2]
		print(f"chosen_team: {mission_team}")
		return mission_team

	def decide_on_vote_0th_order(self):
		# 0th order knowledge behavior:
		#	Vote "Yes" for all missions with at least one spy

		if self.number_of_spies_on_team() > 0:
			return "Yes"
		else:
			return "No"

	def decide_on_vote_2nd_order(self):
		# 1st order knowledge behaviour:
		#	Vote "No" if there are no spies on the team
		# 	Vote "No" if this team will result in a resistance member knowing both Spies.

		if self.number_of_spies_on_team() == 0:
			return "No"
		else:
			print(f"To be implemented!!! - decide_on_vote_2nd_order(self)")
			if True:  # Somehow use the mlsolver to see whether an announcement will result in an agent knowing both spies
				return "Yes"

	def number_of_spies_on_team(self):
		team = self.res_model.mission_team
		number_of_spies = 0
		for agent in team:
			if agent in self.model.spies_ids:
				number_of_spies += 1
		return number_of_spies


	def updateKB(self):
		print(f"Still needs to be implemented")

	def updateMissionPreference(self):
		print(f"Still needs to be updated")

