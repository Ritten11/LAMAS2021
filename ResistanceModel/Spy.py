from ResistanceModel.AbstractAgent import AbstractAgent
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
import random
import copy


class Spy(AbstractAgent):
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
        update_knowledge: spies do not need to update their knowledge
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
            self.vote = self.decide_on_vote_0th_order()
            if self.model.debugging:
                print(f"Agent {self.unique_id} voted {self.vote}")

        if self.model.state == "go_on_mission":
            if self.unique_id in self.model.mission_team:
                self.model.grid.move_agent(self, (self.unique_id, 4))

        if self.model.state == "play":
            if self.unique_id in self.model.mission_team:
                if self.model.spy_reasons and self.model.mission_number <= 4:
                    self.card = self.play_card_2nd_order()
                else:
                    self.card = self.play_card_0th_order()
                if self.model.debugging:
                    print(f"{self.card} card is played by {self.unique_id}")

        if self.model.state == "update_knowledge":
            self.model.grid.move_agent(self, (self.unique_id, 0))

    def choose_team(self):
        '''
        This function is the spy agent's reasoning for choosing a team.
        We first go through the agents to see whether any of them know the identity of a spy.
        If a spy has been identified, they will not choose that spy for the mission. If both
        spies have been identified they will randomly choose one spy for the mission. The rest
        of the team is filled of resistance agents randomly.
        :return: the chosen mission team
        '''
        mission_team = []
        dont_choose = []
        for agent in range(1, self.model.num_agents+1):
            if agent not in self.model.spies_ids:
                formula1 = And(Box_a(str(agent), Atom(str(self.model.spies_ids[0]))),
                               Atom(str(self.model.spies_ids[0])))  # agent knows that spy1
                nodes1 = self.model.kripke_model.ks.nodes_not_follow_formula(formula1)
                formula2 = And(Box_a(str(agent), Atom(str(self.model.spies_ids[1]))),
                               Atom(str(self.model.spies_ids[1])))  # agent knows that spy2
                nodes2 = self.model.kripke_model.ks.nodes_not_follow_formula(formula2)
                if len(nodes1) < len(self.model.kripke_model.ks.worlds) and self.model.spies_ids[0] not in dont_choose:
                    dont_choose.append(self.model.spies_ids[0])
                if len(nodes2) < len(self.model.kripke_model.ks.worlds) and self.model.spies_ids[1] not in dont_choose:
                    dont_choose.append(self.model.spies_ids[1])

        if dont_choose == len(self.model.spies_ids):
            mission_team.append(random.choice(dont_choose))
        else:
            mission_team.append(self.model.spies_ids[self.model.spies_ids != dont_choose])
        while len(mission_team) != self.model.team_sizes[self.model.mission_number - 1]:
            temp = random.choice(range(1, self.model.num_agents+1))
            if temp not in self.model.spies_ids and temp not in mission_team:
                mission_team.append(temp)
        return mission_team

    def decide_on_vote_0th_order(self):
        '''
        Function defining the decision of the agent on the voting on the team composition
        :return: The actual decision
        '''
        # 0th order knowledge behavior:
        # Vote "Yes" for all missions with at least one spy

        if self.number_of_spies_on_team() > 0:
            return "Yes"
        else:
            return "No"

    def play_card_0th_order(self):
        '''
        Decision of the agent on whether to play the "fail" card. For 0th-order reasoning, this is always fail
        :return: The decision
        '''
        return "Fail"

    def play_card_2nd_order(self):
        '''
        Decision of the agent on whether to play the "fail" card. For 2nd-order reasoning, the agent will not play a
        "fail" card if the agent knows that a member of the resistance would know who both of the spies are. Under all
        other circumstances, it plays a "fail" card
        :return: The decision
        '''
        if self.model.debugging:
            print("The spies are now using higher order knowledge")
        mission_team = self.model.mission_team
        if len(mission_team) == 2:
            formula = Or(Atom(str(mission_team[0])), Atom(str(mission_team[1])))
        elif len(mission_team) == 3:
            formula = Or(Or(Atom(str(mission_team[0])), Atom(str(mission_team[1]))), Atom(str(mission_team[2])))
        elif len(mission_team) == 4:
            formula = Or(Or(Or(Atom(str(mission_team[0])), Atom(str(mission_team[1]))), Atom(str(mission_team[2]))), Atom(str(mission_team[3])))
        else:
            raise IOError("Amount of team members selected for mission not within range [2,4]")
        kripke_model_copy = copy.deepcopy(self.model.kripke_model.ks)
        card = "Fail"
        for agent in self.get_non_spies():
            hypothetical_model = kripke_model_copy.solve(formula)
            new_formula = Box_a(str(self.unique_id),
                                And(
                                    Box_a(str(agent.unique_id), Atom(str(self.model.spies_ids[0]))),
                                    Box_a(str(agent.unique_id), Atom(str(self.model.spies_ids[1])))))
            excluded_nodes = hypothetical_model.nodes_not_follow_formula(new_formula)

            if len(excluded_nodes) == 0:  # Meaning that in all worlds, a resistance members would know both spies
                card = "Pass"
                print(f"Would normally play 'fail' card but now plays a 'Pass' card due to higher order reasoning")
        return card

    def number_of_spies_on_team(self):
        '''
        A helper function used to determine the current number of spies on a team
        :return: The number of spies on the team
        '''
        team = self.model.mission_team
        number_of_spies = 0
        for agent in team:
            if agent in self.model.spies_ids:
                number_of_spies += 1
        return number_of_spies

    def get_non_spies(self):
        '''
        A helper function to retrieve all of the non spies
        :return: A list with all of the non-spies.
        '''
        non_spies = []
        for agent in self.model.schedule.agents:
            if agent.unique_id not in self.model.spies_ids:
                non_spies.append(agent)
        return non_spies
