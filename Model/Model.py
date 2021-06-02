from mesa import Model
from mesa.time import RandomActivation
from Spy import Spy
from Resistance import Resistance
import random


class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, S, debugging = False):
        random.seed(42)
        self.debugging = debugging
        self.num_agents = N
        self.num_spies = S
        self.schedule = RandomActivation(self)
        # Create agents
        spies_ids = random.sample(range(self.num_agents), 2)
        if debugging:
            print(f"Spies in this model: {spies_ids}")
        for i in range(self.num_agents):
            if i in spies_ids:
                a = Spy(i, self)
            else:
                a = Resistance(i, self)
            self.schedule.add(a)


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()




