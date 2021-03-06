from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from ResistanceModel.ResistanceModel import ResistanceModel
from ResistanceModel.Spy import Spy
from ResistanceModel.Resistance import Resistance
from ResistanceModel.TextElement import TextElement
from View.LegendElement import LegendElement
from View.SimulationInfoElement import SimulationInfoElement


def resistance_agent_portrayal(agent):
    '''
    Function used to define the appearances of the agents
    :param agent: The to be drawn agent
    :return: A dict with the portrayal of the agent
    '''
    if type(agent) is TextElement:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "w": 1.0,
            "h": 1.0,
            "Layer": 1,
            "Color": "white",
            "text": agent.description,
            "text_color": 'black'
        }
    else:
        portrayal = {
            "Shape": "circle",
            "Filled": True,
            "Layer": 1,
            "r": 0.5,
            "text": str(agent.unique_id),
            "text_color": "white"
        }
        if type(agent) is Spy:
            portrayal["Color"] = "red"
        elif type(agent) is Resistance:
            portrayal["Color"] = "blue"
        else:
            print("Class of current agent is not defined....")
            raise TypeError

    return portrayal


class ModelServer:
    def __init__(self, N, ps, sphok, rhok, debug, S=2):
        '''
        Create a local mesa server with an interactive GUI.
        :param N: Initial value for the number of agents within the simulation
        :param ps: Initial value for the party size
        :param sphok: Initial value on whether the spies use higher order knowledge
        :param rhok: Initial value on whether the resistance uses higher order knowledge
        :param debug: Flag which will activate useful print statements within the simulation. Use only
        for debugging purposes
        :param S: Number of spies within the model.
        '''
        model_params = {
            "N": UserSettableParameter(
                param_type="choice",
                name="Number of agents",
                value=N,
                choices=[5, 6],
                description="Choose how many agents to include in the model",
            ),
            "ps": UserSettableParameter(
                param_type="choice",
                name="Party size",
                value=ps,
                choices=['2', 'default', '3'],
                description="Choose the size of the mission parties. The default party size will use the party"
                            "sizes of the original game",
            ),
            "sphok": UserSettableParameter(
                param_type="checkbox",
                name="Higher order reasoning spies",
                value=sphok,
                description="Turn higher order reasoning for the spies on or off",
            ),
            "rhok": UserSettableParameter(
                param_type="checkbox",
                name="Higher order reasoning resistance",
                value=rhok,
                description="Turn higher order reasoning for the resistance on or off",
            ),
            "S": S, "debug": debug
        }
        if N == 5:
            self.grid_width = 7
        elif N == 6:
            self.grid_width = 7
        else:
            raise IOError("Incorrect number of agents.")

        self.grid_height = 5
        model_params['width'] = self.grid_width
        model_params['height'] = self.grid_height
        canvas_element = CanvasGrid(resistance_agent_portrayal, self.grid_width, self.grid_height, 500, 500)
        self.server = ModularServer(ResistanceModel,
                                    [canvas_element, LegendElement(), SimulationInfoElement()],
                                    "Resistance Model",
                                    model_params)

        self.server.port = 8521  # The default

    def run_server(self):
        self.server.launch()
