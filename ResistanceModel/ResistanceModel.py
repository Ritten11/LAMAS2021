from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from ResistanceModel.Spy import Spy
from ResistanceModel.Resistance import Resistance
from ResistanceModel.mlsolver.model import Resistance3Agents, Resistance5Agents
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
import random


def get_identity_revealed(model):
    return model.identity_revealed


class ResistanceModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, S, width, height, sphok, rhok, ps, debug):
        self.debugging = debug
        if debug:
            random.seed(21)
        self.num_agents = N
        self.num_spies = S
        self.spy_reasons = sphok  # Higher Order Knowledge use of the Spies
        self.resistance_reasons = rhok  # Higher Order Knowledge use of the Resistance
        
        self.ps = ps            # party size
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # Create agents
        self.spies_ids = random.sample(range(self.num_agents), self.num_spies)
        self.spies_ids = [s+1 for s in self.spies_ids]
        self.true_world = ""
        if debug:
            print(f"Spies in this model: {self.spies_ids}")
        for i in range(1,self.num_agents+1):
            if i in self.spies_ids:
                a = Spy(i, self)
                self.true_world += str(i)
            else:
                a = Resistance(i, self)
            a.initKB()
            self.schedule.add(a)
            self.grid.place_agent(a, (i, 0))
        if debug:
            print(f"true world: {self.true_world}")
        
        self.kripke_model = Resistance5Agents(N=self.num_agents) # Create Kripke model
        
        self.team_sizes = self.init_team_size()
        
        # mission initializations
        self.mission_leader = None
        self.try_leader = 0
        self.mission_number = 1
        self.mission_team = []
        self.rounds_won_spies = [0, 0, 0, 0, 0]
        self.identity_revealed = 0
        self.state = None
        self.announcement = None
        self.running = True
        self.ui_message = "New model is initialized"

    def init_team_size(self):
        ''' 
        Initialise the array for the number of agents on the team per mission 
        :return: the team sizes based on the provided flag
        '''
        team_sizes = []
        if self.ps == "2":
            team_sizes = [2] * 5
        elif self.ps == "3":
            team_sizes = [3] * 5
        elif self.num_agents == 6:
            team_sizes = [2, 3, 4, 3, 4]
        else:
            team_sizes = [2, 3, 2, 3, 3] # basecase
        return team_sizes

    def set_mission_leader(self):
        ''' Set the mission leader for the round '''
        if self.mission_leader == None:
            self.mission_leader = random.randint(1, self.num_agents)
        else: 
            self.mission_leader = self.mission_leader + 1 if self.mission_leader < (self.num_agents) else 1

    def step(self):
        '''Advance the model by one step.'''
        if self.state == None:
            self.state = "choose_team"
        
        if self.state == "choose_team":    
            self.set_mission_leader()  # mission leader is set
            self.try_leader += 1
            self.ui_message = f"The mission leader of mission {self.mission_number} is agent {self.mission_leader}. Current amount of tries: {self.try_leader}"
            if self.debugging:
                print(f"The mission leader of mission {self.mission_number} is agent {self.mission_leader}: try {self.try_leader}")
            self.schedule.step()
            self.ui_message = f"The mission leader of mission {self.mission_number} is agent {self.mission_leader}. " \
                              f"The proposed team is {self.mission_team}. Current amount of tries: {self.try_leader}"
            self.state = "vote"

        elif self.state == "vote":
            self.schedule.step()
            self.ui_message = f"The mission leader proposed the team: {str(self.mission_team)}"
            if self.check_vote_passed():
                self.ui_message = f"The team was accepted. The agents voted:"
                for agent in self.schedule.agents:
                    self.ui_message += f"<br>{(agent.unique_id, agent.vote)}"
                self.state = "go_on_mission"
            else:
                self.state = "choose_team"
                self.ui_message = f"The team was rejected. The agents voted:"
                for agent in self.schedule.agents:
                    self.ui_message += f"<br>{(agent.unique_id, agent.vote)}"
                self.ui_message += f"<br> A new team leader needs to be selected."
                if self.try_leader == 5:
                    self.ui_message = f"Team selection failed too often. The spies automatically win this round."
                    self.rounds_won_spies[self.mission_number - 1] = 1
                    self.mission_number += 1
                    self.try_leader = 0

        elif self.state == "go_on_mission":
            self.schedule.step()
            self.ui_message = "The team is currently on the mission."
            self.state = "play"

        elif self.state == "play":
            self.schedule.step()
            played = [agent.card for agent in self.schedule.agents if agent.card != None]
            self.ui_message = f"The mission is completed. Cards played during this mission: {played}"
            self.state = "update_knowledge"

        elif self.state == "update_knowledge":
            self.announce_mission_result()
            self.ui_message = f"The following announcement has been made to the model: {self.announcement}"
            if self.resistance_reasons:
                formula = self.announce_voting_reasoning()
                if formula:
                    self.ui_message += f"<br>Additionally, the resistance agents have learned the following from the voting round: {formula}"

            self.schedule.step()

            self.mission_number += 1
            self.try_leader = 0
            self.state = "choose_team"

        elif self.state == "Game_over":
            self.running = False

            self.ui_message = f"Game over: spies got {sum(self.rounds_won_spies)}, resistance got {(self.mission_number-1)-sum(self.rounds_won_spies)}"
            print(self.ui_message)
            print(self.game_end())
        
        if self.mission_number > len(self.team_sizes):
            self.state = "Game_over"

        if self.debugging:
            print(f"state is {self.state}")

    def game_end(self):
        ''' 
        Return the result of the game 
        :return: a string with the result
        '''
        result = ""
        if sum(self.rounds_won_spies) >= 3:
            result = "Spies won"
        else:
            result = "Resistance won: " + str(self.identity_revealed)
        return result

    def check_vote_passed(self):
        ''' 
        Checks whether the agents voted for the mission or againt it.
        If at least 3 agents vote "Yes", the vote has passed
        :return: a boolean
        '''
        votes = []
        for agent in self.schedule.agents:
            votes.append(agent.vote)
        return True if votes.count("Yes") >= votes.count("No") else False

    def announce_voting_reasoning(self):
        '''
        This function helps the agent learn from the votes of agents for the mission.
        If an agent voted for a mission that failed, then that agent may be a spy.
        '''
        formula = None
        if self.debugging:
            print("The resistance is now using higher order knowledge")
        if self.failed: 
            yes_votes = []
            no_votes = []
            for agent in self.schedule.agents:
                if agent.vote == "Yes":
                    yes_votes.append(agent.unique_id)
                if agent.vote == "No":
                    no_votes.append(agent.unique_id)
            print(f"yes: {yes_votes}")
            print(f"no: {no_votes}")

            if len(no_votes) > 0:
                temp = [Not(Atom(str(a))) for a in no_votes]
                formula = temp[0]
                if len(no_votes) > 1:
                    for i in range(1,len(temp)+1):
                        formula = And(formula, temp[i])
                print(formula)
                self.kripke_model.ks = self.kripke_model.ks.solve(formula)
        return formula

    def announce_mission_result(self):
        '''
        This function announces the result of the mission. 
        The annoucement is created based on the cards played by the agents and then applied
        to the current kripke model. 
        '''
        self.failed = True
        played = []
        for agent in self.schedule.agents:
            if agent.card != None:
                played.append(agent.card)
                agent.card = None
        if self.debugging:
            print(f"played: {played}")

        if "Pass" not in played: # there are only "fail" cards played
            self.rounds_won_spies[self.mission_number-1] = 1
            temp = [Atom(str(a)) for a in self.mission_team]
            self.announcement = And(temp[0], temp[1])
            if self.team_sizes[self.mission_number - 1] == 3: # I dont think we need this if statement cause there can never be a case where all cards are fail and 3 agents were on the mission
                self.announcement = And(self.announcement, temp[2])

        elif "Fail" in played and "Pass" in played: # both "pass" and "fail" cards were played
            self.rounds_won_spies[self.mission_number-1] = 1
            if played.count("Fail") == 1:
                temp = [Atom(str(a)) for a in self.mission_team]
                self.announcement = Or(temp[0], temp[1])
                if self.team_sizes[self.mission_number - 1] == 3:
                    self.announcement = Or(self.announcement, temp[2])
                if self.team_sizes[self.mission_number - 1] == 4:
                    self.announcement = Or(Or(self.announcement, temp[2]), temp[3])
            else: # case "fail", "fail", "pass" OR "fail", "fail", "pass", "pass"
                temp = [Atom(str(a)) for a in self.mission_team]
                self.announcement = Or(Or(And(temp[0], temp[1]), And(temp[0], temp[2])), And(temp[1], temp[2]))
                if self.team_sizes[self.mission_number - 1] == 4:
                    self.announcement = Or(Or(Or(self.announcement, And(temp[0], temp[3])), And(temp[1], temp[3])), And(temp[2], temp[3]))

        elif "Fail" not in played:
            self.failed = False
            self.rounds_won_spies[self.mission_number-1] = 0
            if self.spy_reasons == False: # if spies dont reason then no one in the mission is a spy
                temp = [Not(Atom(str(a))) for a in self.mission_team]
                self.announcement = And(temp[0], temp[1])
                if self.team_sizes[self.mission_number - 1] == 3:
                    self.announcement = And(self.announcement, temp[2])
                if self.team_sizes[self.mission_number - 1] == 4:
                    self.announcement = And(And(self.announcement, temp[2]), temp[3])
            else: # if spies reason then anyone can be a spy
                temp = [Atom(str(a)) for a in range(1, self.num_agents+1)]
                self.announcement = Or(Or(Or(Or(temp[0], temp[1]), temp[2]), temp[3]), temp[4])
                if self.num_agents == 6:
                    self.announcement = Or(self.announcement, temp[5])
        if self.debugging:
            print(f"announcement is: {self.announcement}")
            print("before announcement:")
            print(f"worlds: {[world.name for world in self.kripke_model.ks.worlds]}")
            print(self.kripke_model.ks.relations)

        self.kripke_model.ks = self.kripke_model.ks.solve(self.announcement)
        
        if self.debugging:
            print("After announcement:")
            print(f"worlds: {[world.name for world in self.kripke_model.ks.worlds]}")
            print(self.kripke_model.ks.relations)

        if len(self.kripke_model.ks.worlds) == 1 and self.kripke_model.ks.worlds[0].name == self.true_world and self.identity_revealed == 0:
            self.identity_revealed = self.mission_number
            print(f"reavealed at {self.identity_revealed}")

