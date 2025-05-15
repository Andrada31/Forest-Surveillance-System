from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import DroneAgent, LawAgent, LumberjackAgent, TreeCell
import random
import networkx as nx

class ForestModel(Model):
    def __init__(self, width, height, num_drones, num_law, num_lumberjacks):
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.alerts = []
        self.logs = []
        self.show_popup = False
        self.next_uid = 0

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                tree = TreeCell(self.next_uid, self)
                self.next_uid += 1
                self.grid.place_agent(tree, (x, y))

        for _ in range(10):
            x, y = random.randrange(width), random.randrange(height)
            cell_contents = self.grid.get_cell_list_contents((x, y))
            for obj in cell_contents:
                if isinstance(obj, TreeCell) and not obj.is_cut:
                    obj.is_cut = True
                    obj.is_tree = False

        for _ in range(num_drones):
            drone = DroneAgent(self.next_uid, self)
            self.schedule.add(drone)
            self.grid.place_agent(drone, (random.randrange(width), random.randrange(height)))
            self.next_uid += 1

        for _ in range(num_law):
            law = LawAgent(self.next_uid, self)
            self.schedule.add(law)
            self.grid.place_agent(law, (width - 1, height - 1))  
            self.next_uid += 1


        for _ in range(num_lumberjacks):
            lumberjack = LumberjackAgent(self.next_uid, self)
            self.schedule.add(lumberjack)
            self.grid.place_agent(lumberjack, (random.randrange(width), random.randrange(height)))
            self.next_uid += 1

    def step(self):
        self.schedule.step()

    def report_illegal_activity(self, pos):
        if pos not in self.alerts:
            self.log_event(f"🚨 ALERT: Illegal deforestation detected at {pos}")
            self.alerts.append(pos)



    def log_event(self, message):
        print(message)
        self.logs.append(message)
        if len(self.logs) > 100:
            self.logs.pop(0)

    
    def get_shortest_path(self, start, goal):
        graph = nx.grid_2d_graph(self.grid.width, self.grid.height)
        try:
            path = nx.shortest_path(graph, source=start, target=goal)
            return path
        except nx.NetworkXNoPath:
            return []