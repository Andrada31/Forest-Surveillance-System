from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from model import ForestModel
from agents import DroneAgent, LawAgent, LumberjackAgent, TreeCell

def agent_portrayal(agent):
    if isinstance(agent, TreeCell):
        img = "tree.png"
        if agent.is_cut:
            img = "tree_cut.png"
        return {
            "Shape": f"static/{img}",
            "Layer": 0,
            "scale": 1.0
        }
    elif isinstance(agent, DroneAgent):
        return {
            "Shape": "static/drone.png",
            "Layer": 1,
            "scale": 0.9
        }
    elif isinstance(agent, LawAgent):
        return {
            "Shape": "static/law.png",
            "Layer": 2,
            "scale": 0.8
        }
    elif isinstance(agent, LumberjackAgent):
        if agent.caught:
            return {
                "Shape": "circle",
                "Color": "red",
                "Layer": 3,
                "r": 0.4
            }
        else:
            return {
                "Shape": "static/lumberjack.png",
                "Layer": 3,
                "scale": 0.9
            }
    return {
        "Shape": "static/unknown.png",
        "Layer": 4,
        "scale": 0.5
    }

class LogElement(TextElement):
    def render(self, model):
        return "<div style='font-family: monospace; font-size: 14px; max-height: 500px; overflow-y: scroll; border: 1px solid #ccc; padding: 5px;'>\
                <b>📜 Event Log</b><br>" + "<br>".join(model.logs[-30:]) + "</div>"
    
class PopupElement(TextElement):
    def render(self, model):
        if model.show_popup:
            model.show_popup = False 
            return "<script>alert('🚨 Illegal activity was stopped.');</script>"
        return ""



width = 10
height = 10
log_panel = LogElement()
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

server = ModularServer(
    ForestModel,
    [grid, log_panel, PopupElement()],
    "Illegal Deforestation Simulation",
    {"width": width, "height": height, "num_drones": 1, "num_law": 1, "num_lumberjacks": 1}
)
server.port = 8521