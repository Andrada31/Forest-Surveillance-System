# Forest Surveillance Simulation

This project is a multi-agent simulation built with the [Mesa](https://mesa.readthedocs.io/en/stable/) framework, designed to model and visualize illegal deforestation detection using autonomous agents such as drones, law enforcement, lumberjacks, and trees.

## Agents

- **Drone Agent**: Patrols the forest using a sweeping automated path. Detects illegal activities (tree cutting).
- **Law Agent**: Responds to alerts from drones. Uses BFS shortest-path logic to reach and catch lumberjacks.
- **Lumberjack Agent**: Randomly moves around the grid, cuts down trees unless caught.
- **Tree Agent**: Passive agents that can be cut. Represent forest density and deforestation status.

## Features
- **Real-Time Visualization**: Interactive grid-based visualization using Mesa's modular server.
- **Event Logging**: Live updates of important actions, such as tree cutting and arrests.
- **FPS Slider**: Adjust the simulation speed dynamically via a frames-per-second slider in the UI.

  ## Customization

- **Grid size and number of agents**  
  Can be modified in `server.py` under the `ModularServer` initialization:
  ```python
  server = ModularServer(
      ForestModel,
      [grid, log_panel, PopupElement()],
      "Illegal Deforestation Simulation",
      {
          "width": 10,
          "height": 10,
          "num_drones": 1, 
          "num_law": 1,
          "num_lumberjacks": 1 
      }
  )


## Requirements

- Python 3.8+
- Mesa
- NetworkX
- Tornado (used by Mesa for visualization)

Install all dependencies using:

```bash
pip install -r requirements.txt
