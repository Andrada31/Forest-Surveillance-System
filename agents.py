from mesa import Agent

class Tree(Agent):
    def __init__(self, unique_id, model, is_tree=True):
        super().__init__(unique_id, model)
        self.is_tree = is_tree
        self.is_cut = False

class DroneAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.path_index = 0
        self.direction = 1  
        self.path = self.generate_sweep_path()

    def step(self):
        if 0 <= self.path_index < len(self.path):
            self.move()
            self.detect_illegal_activity()
            self.model.visible_area = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=True
            )
        else:
            self.direction *= -1  
            self.path_index += self.direction  

    def move(self):
        next_pos = self.path[self.path_index]
        self.model.grid.move_agent(self, next_pos)
        self.path_index += self.direction



    def detect_illegal_activity(self):
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell:
            if isinstance(obj, LumberjackAgent) and not obj.caught:
                self.model.report_illegal_activity(self.pos)

    def generate_sweep_path(self):
        width, height = self.model.grid.width, self.model.grid.height
        path = []
        for x in range(width):
            col = [(x, y) for y in range(height)] if x % 2 == 0 else [(x, y) for y in reversed(range(height))]
            path.extend(col)
        return path



class LawAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.target_agent = None

    def step(self):
        if self.target_agent and not self.target_agent.caught:
            self.chase_target()
        elif self.model.alerts:
            self.find_target_from_alert()

    def find_target_from_alert(self):
        alert_pos = self.model.alerts.pop(0)
        cell_contents = self.model.grid.get_cell_list_contents([alert_pos])
        for agent in cell_contents:
            if isinstance(agent, LumberjackAgent) and not agent.caught:
                self.target_agent = agent
                break

    def chase_target(self):
        path = self.model.get_shortest_path(self.pos, self.target_agent.pos)
        if len(path) > 1:
            self.model.grid.move_agent(self, path[1])

        if self.pos == self.target_agent.pos:
            self.target_agent.caught = True
            self.model.log_event(
                f"👮 Law {self.unique_id} caught Lumberjack {self.target_agent.unique_id} at {self.pos}"
            )
            self.model.show_popup = True
            self.target_agent = None



class LumberjackAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.caught = False
        self.cut_delay = 0

    def step(self):
        if self.caught:
            return
        if self.cut_delay > 0:
            self.cut_delay -= 1
            return
        self.cut_tree()  
        self.move()     


    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def cut_tree(self):
        if self.cut_delay > 0:
            self.cut_delay -= 1
            return
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell:
            if isinstance(obj, Tree) and obj.is_tree and not obj.is_cut:
                self.cut_delay = 4  
                obj.is_cut = True
                obj.is_tree = False
                self.model.log_event(f"🪓 Lumberjack {self.unique_id} cut a tree at {self.pos}")

