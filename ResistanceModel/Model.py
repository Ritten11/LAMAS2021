from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from ResistanceModel.Spy import Spy
from ResistanceModel.Resistance import Resistance
from ResistanceModel.mlsolver.model import Resistance3Agents
import random


class ResistanceModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, S, width, height, debugging=False):
        random.seed(42) # I think we want to change the seed 
        self.debugging = debugging
        self.num_agents = N
        self.num_spies = S
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # Create agents
        spies_ids = random.sample(range(self.num_agents), self.num_spies)
        if debugging:
            print(f"Spies in this model: {spies_ids}")
        for i in range(self.num_agents):
            print(i)
            if i in spies_ids:
                a = Spy(i, self)
                print(f"spy is {i}")
            else:
                a = Resistance(i, self)
            a.initKB()
            self.schedule.add(a)
            self.grid.place_agent(a, (i+1, 0))
        self.kripke_model = Resistance3Agents()
        self.team_sizes = [2,2,2] # number of agents that go on each mission
        self.mission_leader = None
        self.mission_number = 0
        self.mission_team = []
        self.state = None
        self.running = True

    def set_mission_leader(self):
        ''' Set the mission leader for the round '''
        if self.mission_leader == None:
            self.mission_leader = random.randint(1, self.num_agents)
        else: 
            self.mission_leader = self.mission_leader + 1 if self.mission_leader < (self.num_agents-1) else 0

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
            self.state = "go_on_mission"

        elif self.state == "go_on_mission":
            self.schedule.step()
            self.state = "play"

        elif self.state == "play":
            self.schedule.step()
            self.state = "update_knowledge"

        elif self.state == "update_knowledge":
            self.schedule.step()
            self.state = "choose_team"
        print(f"state is {self.state}")

        
        




