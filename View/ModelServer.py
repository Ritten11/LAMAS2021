from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from ResistanceModel.Model import ResistanceModel
from ResistanceModel.Spy import Spy
from ResistanceModel.Resistance import Resistance

def resistance_agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": True,
        "Layer": 1,
        "r": 0.5,
        "text": str(agent.KB),
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


grid_width = 5
grid_height = 2

canvas_element = CanvasGrid(resistance_agent_portrayal, grid_width, grid_height, 500, 500)
server = ModularServer(ResistanceModel,
                       [canvas_element],
                       "Resistance Model",
                       {"N":3, "S":1, "width":grid_width, "height":grid_height})
server.port = 8521 # The default
server.launch()