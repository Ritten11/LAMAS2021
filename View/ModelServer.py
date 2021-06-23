from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from ResistanceModel.ResistanceModel import ResistanceModel
from ResistanceModel.Spy import Spy
from ResistanceModel.Resistance import Resistance


class ModelServer:
    def __init__(self, N, ps, sphok, rhok, debug, S=2):
        if N == 5:
            self.grid_width = 7
        elif N == 6:
            self.grid_width = 8
        else:
            raise IOError("Incorrect number of agents.")
        self.grid_height = 5
        canvas_element = CanvasGrid(self.resistance_agent_portrayal, self.grid_width, self.grid_height, 500, 500)
        self.server = ModularServer(ResistanceModel,
                                    [canvas_element],
                                    "Resistance Model",
                                    {"N": N, "S": S, "width": self.grid_width, "height": self.grid_height,
                                     "ps": ps, "sphok": sphok, "rhok": rhok, "debug": debug})

        self.server.port = 8521  # The default

    def run_server(self):
        self.server.launch()

    def resistance_agent_portrayal(self, agent):
        portrayal = {
            "Shape": "circle",
            "Filled": True,
            "Layer": 1,
            "r": 0.5,
            "text": str(agent.unique_id),
            "text_color": "white",
            "scale": 0.8,
        }
        if type(agent) is Spy:
            portrayal["Color"] = "red"
        elif type(agent) is Resistance:
            portrayal["Color"] = "blue"
        else:
            print("Class of current agent is not defined....")
            raise TypeError
        #
        # portrayal["Shape"] = "circle"
        # portrayal["Filled"] = True
        # portrayal["Layer"] = 1
        # portrayal["r"] = 0.5
        # portrayal["text"] = str(agent.KB)

        return portrayal