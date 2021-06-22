from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from ResistanceModel.Spy import Spy
from ResistanceModel.Resistance import Resistance
from ResistanceModel.mlsolver.model import Resistance3Agents, Resistance5Agents
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
import random


class ResistanceModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, S, width, height, hok, ps, debugging=False):
        random.seed(21)  # I think we want to change the seed
        self.debugging = debugging
        self.num_agents = N
        self.num_spies = S
        self.spy_reasons = hok  # Higher Order Knowledge use of the spies
        self.ps = ps            # party size
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # Create agents
        #self.spies_ids = random.sample(range(self.num_agents), self.num_spies)
        self.spies_ids = [1,2]#[s+1 for s in self.spies_ids]
        self.true_world = ""
        if debugging:
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
        # Create Kripke model
        self.kripke_model = Resistance5Agents(N=self.num_agents)
        
        self.team_sizes = self.init_team_size()
        
        self.mission_leader = None
        self.try_leader = 0
        self.mission_number = 1
        self.mission_team = []
        self.spy_points = 0
        self.resisitance_points = 0
        self.identity_revealed = 0
        self.state = None
        self.announcement = None
        self.running = True

    def init_team_size(self): # I can also include the number of agents in here if we want to include that?
        # number of agents that go on each mission
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
            self.mission_leader = 4

        else: 
            self.mission_leader = self.mission_leader + 1 if self.mission_leader < (self.num_agents) else 1

    def step(self):
        '''Advance the model by one step.'''
        if self.state == None:
            self.state = "choose_team"
        
        if self.state == "choose_team":    
            self.set_mission_leader() # mission leader is set
            self.try_leader += 1
            print(f"The mission leader of mission {self.mission_number} is agent {self.mission_leader}: try {self.try_leader}")
            self.mission_team = self.schedule.agents[self.mission_leader - 1].choose_team()
            self.schedule.step()
            self.state = "vote"

        elif self.state == "vote":
            self.schedule.step()
            if self.check_vote_passed():
                self.state = "go_on_mission"
            else:
                self.state = "choose_team"
                if self.try_leader == 5:
                    self.mission_number += 1
                    self.spy_points += 1
                    self.try_leader = 0
                
                if self.mission_number > 5:
                    self.state = "Game_over"

        elif self.state == "go_on_mission":
            self.schedule.step()
            self.state = "play"

        elif self.state == "play":
            self.schedule.step()
            self.state = "update_knowledge"

        elif self.state == "update_knowledge":
            self.announce_mission_result()
            self.schedule.step()
            self.mission_number += 1
            self.try_leader = 0
            self.state = "choose_team"
        
        elif self.state == "Game_over":
            self.running = False
            print(f"Game over: spies got {self.spy_points}, resistance got {self.resisitance_points}")

        print(f"state is {self.state}")

    def game_end(self):
        result = ""
        if self.spy_points > self.resisitance_points:
            result = "Spies won"
        else:
            result = "Resistance won: " + str(self.identity_revealed)
        return result

    def check_vote_passed(self):
        votes = []
        for agent in self.schedule.agents:
            votes.append(agent.vote)
        return True if votes.count("Yes") >= votes.count("No") else False
    

    def announce_mission_result(self):
        played = []
        print(f"played: {played}")
        for agent in self.schedule.agents:
            if agent.card != None:
                played.append(agent.card)
                agent.card = None
        print(f"played: {played}")

        if "Pass" not in played: # there are only "fail" cards played
            self.spy_points += 1
            temp = [Atom(str(a)) for a in self.mission_team]
            self.announcement = And(temp[0], temp[1])
            if self.team_sizes[self.mission_number - 1] == 3:
                self.announcement = And(self.announcement, temp[2])
            print("pass not in")

        elif "Fail" in played and "Pass" in played: # both "pass" and "fail" cards were played
            self.spy_points += 1
            if played.count("Fail") == 1:
                temp = [Atom(str(a)) for a in self.mission_team]
                self.announcement = Or(temp[0], temp[1])
                if self.team_sizes[self.mission_number - 1] == 3:
                    self.announcement = Or(self.announcement, temp[2])
            else: # case "fail", "fail", "pass"
                temp = [Atom(str(a)) for a in self.mission_team]
                self.announcement = Or(Or(And(temp[0], temp[1]), And(temp[0], temp[2])), And(temp[1], temp[2]))
            print("fail and pass")
        # comment in if spies only play a fail card
        elif "Fail" not in played:
            self.resisitance_points += 1
            if self.spy_reasons == False:
                temp = [Not(Atom(str(a))) for a in self.mission_team]
                self.announcement = And(temp[0], temp[1])
                if self.team_sizes[self.mission_number - 1] == 3:
                    self.announcement = And(self.announcement, temp[2])
                print("fail not in")
            else: # I hate this but it should work <- is
                temp = [Atom(str(a)) for a in range(1, self.num_agents+1)]
                self.announcement = Or(Or(Or(Or(temp[0], temp[1]), temp[2]), temp[3]), temp[4])
                if self.num_agents == 6:
                    self.announcement = Or(self.announcement, temp[5])
        print(f"announcement is: {self.announcement}")

        
        print("before announcement:")
        print(f"worlds: {[world.name for world in self.kripke_model.ks.worlds]}")
        print(self.kripke_model.ks.relations)

        self.kripke_model.ks = self.kripke_model.ks.solve(self.announcement)
        print("After announcement:")
        print(f"worlds: {[world.name for world in self.kripke_model.ks.worlds]}")
        print(self.kripke_model.ks.relations)

        if len(self.kripke_model.ks.worlds) == 1 and self.kripke_model.ks.worlds[0].name == self.true_world and self.identity_revealed == 0:
            self.identity_revealed = self.mission_number
            print(f"reavealed at {self.identity_revealed}")


