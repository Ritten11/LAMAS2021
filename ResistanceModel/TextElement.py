
from mesa import Agent


class TextElement(Agent):

    def __init__(self, unique_id, model, description):
        '''
        An agent solely created for the purpose of adding text within the grid of the simulation. It has no other
        purpose than being informational.
        :param unique_id: Id of the agent
        :param model: Model in which the agent resides
        :param description: Text that is to be printed within the grid
        '''
        super().__init__(unique_id, model)
        self.description = description

    def step(self):

        pass

