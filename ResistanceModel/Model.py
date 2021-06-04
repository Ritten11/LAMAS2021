from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from ResistanceModel.Spy import Spy
from ResistanceModel.Resistance import Resistance
import random


class ResistanceModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, S, width, height, debugging=False):
        random.seed(42)
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


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()




