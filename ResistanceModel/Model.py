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
    def __init__(self, N, S, width, height, debugging=False):
        random.seed(42)  # I think we want to change the seed
        self.debugging = debugging
        self.num_agents = N
        self.num_spies = S
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # Create agents
        #self.spies_ids = random.sample(range(self.num_agents), self.num_spies)
        self.spies_ids = [1,2]#[s+1 for s in self.spies_ids]
        if debugging:
            print(f"Spies in this model: {self.spies_ids}")
        for i in range(1,self.num_agents+1):
            #print(i)
            if i in self.spies_ids:
                a = Spy(i, self)
                print(f"spy is {i}")
            else:
                a = Resistance(i, self)
            a.initKB()
            self.schedule.add(a)
            self.grid.place_agent(a, (i, 0))
        self.kripke_model = Resistance5Agents()
        self.team_sizes = [2, 3, 2, 3, 3]  # number of agents that go on each mission
        self.mission_leader = None
        self.mission_number = 0
        self.mission_team = []
        self.state = None
        self.announcement = None
        self.running = True

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
            self.mission_number += 1
            self.set_mission_leader()
            print(f"The mission leader of mission {self.mission_number} is agent {self.mission_leader}")
            self.schedule.step()
            
            self.state = "vote"

        elif self.state == "vote":
            self.schedule.step()
            self.state = "go_on_mission" if self.check_vote_passed() else "choose_team"
            for agent in self.schedule.agents:
                agent.card = None

        elif self.state == "go_on_mission":
            self.schedule.step()
            self.state = "play"

        elif self.state == "play":
            self.schedule.step()
            self.announce_mission_result()
            self.state = "update_knowledge"

        elif self.state == "update_knowledge":
            
            self.schedule.step()
            self.state = "choose_team"
        print(f"state is {self.state}")


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
        
        print(f"played: {played}")
        # maybe we want another one where it counts the number of fail cards ? cause with 5 agents 
        # there could be 2 fails and 1 pass
        if "Fail" not in played:
            temp = [Not(Atom(str(a))) for a in self.mission_team]
            self.announcement = And(temp[0], temp[1])
            if self.team_sizes[self.mission_number - 1] == 3:
                self.announcement = And(self.announcement, temp[2])
            print("fail not in")
        elif "Fail" in played and "Pass" in played: 
            temp = [Atom(str(a)) for a in self.mission_team]
            self.announcement = Or(temp[0], temp[1])
            if self.team_sizes[self.mission_number - 1] == 3:
                self.announcement = Or(self.announcement, temp[2])
            print("fail and pass")
        elif "Pass" not in played:
            temp = [Atom(str(a)) for a in self.mission_team]
            self.announcement = And(temp[0], temp[1])
            if self.team_sizes[self.mission_number - 1] == 3:
                self.announcement = And(self.announcement, temp[2])
            print("pass not in")
        print(self.announcement)


        print("before announcement:")
        print(f"worlds: {[world.name for world in self.kripke_model.ks.worlds]}")
        print(self.kripke_model.ks.relations)

        self.kripke_model.ks = self.kripke_model.ks.solve(self.announcement)
        print("After announcement:")
        print(f"worlds: {[world.name for world in self.kripke_model.ks.worlds]}")
        print(self.kripke_model.ks.relations)

