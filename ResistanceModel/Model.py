from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from ResistanceModel.Spy import Spy
from ResistanceModel.Resistance import Resistance
from mlsolver.model import Resistance3Agents
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
            if i in spies_ids:
                a = Spy(i, self)
            else:
                a = Resistance(i, self)
            a.initKB()
            self.schedule.add(a)
            self.grid.place_agent(a, (i+1, 0))
        self.kripke_model = Resistance3Agents()
        self.team_sizes = [2,2,2] # number of agents that go on each mission
        self.mission_leader = None
        self.mission_number = 0

        self.running = True

    def set_mission_leader(self):
        ''' Set the mission leader for the round '''
        if self.mission_leader == None:
            self.mission_leader = random.randint(1, self.num_agents)
        else: 
            self.mission_leader = self.mission_leader + 1 if self.mission_leader < self.num_agents else 1

    def step(self):
        '''Advance the model by one step.'''
        self.mission_number += 1
        self.set_mission_leader()
        print(f"The mission leader of mission {self.mission_number} is agent {self.mission_leader}")
        self.schedule.step()




