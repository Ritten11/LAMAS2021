from ResistanceModel.AbstractAgent import AbstractAgent
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
import random
import copy

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
		if self.model.state == "choose_team":
			if self.model.mission_leader == self.unique_id:
				self.model.grid.move_agent(self, (self.unique_id, 2))
				self.model.mission_team = self.choose_team()
				print(f"team is {self.model.mission_team}")
			else:
				self.model.grid.move_agent(self, (self.unique_id, 0))

		if self.model.state == "vote":
			self.vote = self.decide_on_vote_0th_order()
			print(f"Agent {self.unique_id} voted {self.vote}")

		if self.model.state == "go_on_mission":
			if self.unique_id in self.model.mission_team:
				self.model.grid.move_agent(self, (self.unique_id, 4))

		if self.model.state == "play":
			if self.unique_id in self.model.mission_team:
				self.card = self.play_card_2nd_order()
				print(f"{self.card} card is played by {self.unique_id}")
		   

		if self.model.state == "update_knowledge":
			self.model.grid.move_agent(self, (self.unique_id, 0))
			self.updateKB()


	# TODO: Make sure mission team is unique members
	def choose_team(self):
		mission_team = []
		# in the first mission the spy wants any one spy in the mission so that it fails, but not both
		'''if self.model.mission_number == 1:
									mission_team.append(random.choice(self.model.spies_ids))
									while len(mission_team) != self.model.team_sizes[self.model.mission_number - 1]:
										temp = random.choice(range(1, self.model.num_agents+1))
										if temp not in self.model.spies_ids:
											mission_team.append(temp)
								else: 
									'''
		dont_choose = []
		#knows = []
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
					#knows.append(agent)
				if len(nodes2) < len(self.model.kripke_model.ks.worlds):
					dont_choose.append(self.model.spies_ids[1])
					#knows.append(agent)

		if dont_choose == len(self.model.spies_ids):
			mission_team.append(random.choice(dont_choose))
		else: 
			mission_team.append(self.model.spies_ids[self.model.spies_ids != dont_choose])
		while len(mission_team) != self.model.team_sizes[self.model.mission_number - 1]:
			temp = random.choice(range(1, self.model.num_agents+1))
			if temp not in dont_choose and temp not in mission_team:
				mission_team.append(temp)
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
			formula = Or(Atom(str(self.model.mission_team[0])), Atom(str(self.model.mission_team[1])))
			kripke_model_copy = copy.deepcopy(self.model.kripke_model.ks)
			vote = "Yes"
			for agent in self.get_non_spies():
				hypothetical_model = kripke_model_copy.solve(formula)
				new_formula = Box_a(str(self.unique_id),
									And(
										Box_a(str(agent.unique_id), Atom(str(self.model.spies_ids[0]))),
										Box_a(str(agent.unique_id), Atom(str(self.model.spies_ids[1])))))
				excluded_nodes = hypothetical_model.nodes_not_follow_formula(new_formula)

				if len(excluded_nodes) == 0:  # Meaning that in all worlds, a resistance members knows both spies
					vote = "no"
				print(f"Results for agent {agent.unique_id} and spy {self.model.spies_ids[1]}:")
				print(f"Original							: {self.model.kripke_model.ks.get_power_set_of_worlds()}")
				print(f"Hypothetical						: {hypothetical_model.get_power_set_of_worlds()}")
				print(f"Worlds in which spies are not known	: {str(excluded_nodes)}")
			return vote

	def play_card_2nd_order(self):
		mission_team = self.model.mission_team
		if len(mission_team) == 2:
			formula = Or(Atom(str(mission_team[0])), Atom(str(mission_team[1])))
		else:
			formula = Or(Atom(str(mission_team[0])), Atom(str(mission_team[1])), Atom(str(mission_team[2])))
		kripke_model_copy = copy.deepcopy(self.model.kripke_model.ks)
		vote = "Yes"
		for agent in self.get_non_spies():
			hypothetical_model = kripke_model_copy.solve(formula)
			new_formula = Box_a(str(self.unique_id),
								And(
									Box_a(str(agent.unique_id), Atom(str(self.model.spies_ids[0]))),
									Box_a(str(agent.unique_id), Atom(str(self.model.spies_ids[1])))))
			excluded_nodes = hypothetical_model.nodes_not_follow_formula(new_formula)

			if len(excluded_nodes) == 0:  # Meaning that in all worlds, a resistance members knows both spies
				vote = "no"
			print(f"Results for agent {agent.unique_id} and spy {self.model.spies_ids[1]}:")
			print(f"Original							: {self.model.kripke_model.ks.get_power_set_of_worlds()}")
			print(f"Hypothetical						: {hypothetical_model.get_power_set_of_worlds()}")
			print(f"Worlds in which spies are not known	: {str(excluded_nodes)}")
		return "Fail"

	def number_of_spies_on_team(self):
		team = self.model.mission_team
		number_of_spies = 0
		for agent in team:
			if agent in self.model.spies_ids:
				number_of_spies += 1
		return number_of_spies

	def get_non_spies(self):
		non_spies = []
		for agent in self.model.schedule.agents:
			if agent.unique_id not in self.model.spies_ids:
				non_spies.append(agent)
		return non_spies


	def updateKB(self):
		print(f"Still needs to be implemented")
