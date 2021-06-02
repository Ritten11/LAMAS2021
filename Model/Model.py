from mesa import Model
from mesa.time import RandomActivation
from State import EpistemicState


class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = EpistemicState(i, self, False)
            self.schedule.add(a)

    def pickSpy(self):
        agents = self.schedule.agent_buffer(shuffled=True)


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()




