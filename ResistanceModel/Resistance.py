from ResistanceModel.AbstractAgent import AbstractAgent
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
import random


class Resistance(AbstractAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def initKB(self):  # I dont think we need this right? we can just initialize this in __int__?
        self.card = None
        self.vote = None

    def step(self):
        '''
        Advances the model by one step using flags.
        choose_team: if the agent is the mission leader they get to choose the team
        vote: the agent gets to vote on the chosen team
        go_on_mission: if the agent is on the mission they choose a card to play
        update_knowledge: the agent deliberates on the voting results of the mission
            based on the result of the mission
        '''
        if self.model.state == "choose_team":
            if self.model.mission_leader == self.unique_id:
                self.model.grid.move_agent(self, (self.unique_id, 2))
                self.model.mission_team = self.choose_team()
                if self.model.debugging:
                    print(f"team is {self.model.mission_team}")
            else:
                self.model.grid.move_agent(self, (self.unique_id, 0))

        if self.model.state == "vote":
            if self.decide_on_vote():
                self.vote = "Yes"
            else:
                self.vote = "No"
            if self.model.debugging:
                print(f"Agent {self.unique_id} voted {self.vote}")

        if self.model.state == "go_on_mission":
            if self.unique_id in self.model.mission_team:
                self.model.grid.move_agent(self, (self.unique_id, 4))

        if self.model.state == "play":
            if self.unique_id in self.model.mission_team:
                self.card = "Pass"  # resistance agents always play a "pass" card
                if self.model.debugging:
                    print(f"{self.card} card is played by {self.unique_id}")

        if self.model.state == "update_knowledge":
            self.model.grid.move_agent(self, (self.unique_id, 0))

    def choose_team(self):
        '''
        This function is the resistance agent's reasoning for choosing a team.
        We first go through the agents to see whether the agent knows the spies. If the agent
        knows the identity of a spy, they will decide not to choose them for the mission. The
        agent will always trust themselves and will fill the rest of the mission team randomly.
        :return: the chosen mission team
        '''
        mission_team = []
        dont_choose = []

        for agent in range(1, self.model.num_agents+1):
            formula = And(Box_a(str(self.unique_id), Atom(str(agent))), Not(Atom(str(self.unique_id))))
            nodes = self.model.kripke_model.ks.nodes_not_follow_formula(formula)
            if len(nodes) < len(self.model.kripke_model.ks.worlds):
                dont_choose.append(agent)

        mission_team.append(self.unique_id)  # agent always trusts themselves
        while len(mission_team) != self.model.team_sizes[self.model.mission_number - 1]:
            temp = random.choice(range(1, self.model.num_agents+1))
            if temp not in mission_team and temp not in dont_choose:
                mission_team.append(temp)
        return mission_team

    def decide_on_vote(self):
        '''
        TODO: Missing a description
        :return:
        '''
        # Checks whether the agent accepts the mission team or not
        relations = self.model.kripke_model.ks.relations[str(self.unique_id)]
        worlds = [rel[1] for rel in relations if rel[0] == self.model.true_world]
        suspicions = [0] * len(self.model.mission_team)
        for i, agent in enumerate(self.model.mission_team):
            if agent == self.unique_id:
                continue
            else:
                for world in worlds:
                    if str(agent) in world:
                        suspicions[i] += 1
        for s in suspicions:
            if s == len(worlds):
                return False

        return True
