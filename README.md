# Planet Exploration Rover Simulation

This repository contains algorithmic solutions for autonomous rover surface mapping, terrain exploration, and constrained pathfinding across planetary environments.

---

## Overview

The codebase handles surface mapping in two distinct phases:

1. **Unconstrained Surface Mapping (Phase 1):** Utilizes Depth-First Search (DFS) with recursive backtracking to discover and map fully accessible planetary grid layouts.
2. **Battery-Constrained Exploration (Phase 2):** Implements Breadth-First Search (BFS) path tracking to explore space within strict energy constraints (e.g., maximum 10 steps from home origin), guaranteeing safe return/recharge cycles.

---

## Architecture & Algorithm Design

### 1. Spatial Discovery via Recursive DFS
- **`explore_planet_space`**: Traverses unexplored adjacent coordinates (`N`, `E`, `S`, `W`). Upon exploring a node, it recursively visits adjacent spaces and executes an explicit backtracking move (`get_opposite_direction`) to restore the physical rover position to the caller state.
- **`build_grid_from_explored_dict`**: Dynamically determines the bounding box (`min_x`, `max_x`, `min_y`, `max_y`) from the visited walkable locations, normalizes relative coordinates, and converts the mapped spatial dictionary into a compact list-of-strings grid representation.

### 2. Battery & Distance Constrained BFS
- **`map_surface_with_battery_constraint`**: Uses a `collections.deque` queue to store `(x, y, path_from_home)`.
- Recreates or resets rover states from Home base `(0, 0)` following `path_from_home` to explore surrounding nodes safely without exceeding battery capacity or step limits.

---

## Grid Legend

| Symbol | Description |
| :---: | :--- |
| `H` | Home base / Landing origin `(0, 0)` |
| `.` | Walkable terrain |
| `X` | Obstructed space / Barrier |
| `w` | Water / Surface feature |

---

## Key Functions Summary

| Function | Purpose |
| :--- | :--- |
| `map_surface(planet)` | Main entry point for Phase 1 unconstrained mapping (infinite battery). |
| `build_grid_from_explored_dict(explored)` | Normalizes coordinates and builds matrix strings. |
| `get_opposite_direction(direction)` | Utility returning vector reversal (`N` ↔ `S`, `E` ↔ `W`). |
| `map_surface_with_battery_constraint(planet)` | Main entry point for Phase 2 battery-constrained BFS mapping. |
| `submit_planet_1_map()`, `submit_planet_2_map()`, `submit_planet_3_map()` | Hardcoded grid maps discovered from Phase 1 execution for submission. |

---

## Quick Start Example

```python
import math
from planet_intel import PlanetIntel
from rover import Rover

# Load target planet intel
planet = PlanetIntel.get_planet_1()

# Map the surface (Phase 1)
discovered_grid = map_surface(planet)

# Print discovered grid layout
for row in discovered_grid:
    print(row)



Gemini isn’t human. It can make mistakes, so double-check it.

# Planet Exploration Rover Simulation

This repository contains algorithmic solutions for autonomous rover surface mapping, terrain exploration, and constrained pathfinding across planetary environments.

---

## Overview

The codebase handles surface mapping in two distinct phases:

1. **Unconstrained Surface Mapping (Phase 1):** Utilizes Depth-First Search (DFS) with recursive backtracking to discover and map fully accessible planetary grid layouts.
2. **Battery-Constrained Exploration (Phase 2):** Implements Breadth-First Search (BFS) path tracking to explore space within strict energy constraints (e.g., maximum 10 steps from home origin), guaranteeing safe return/recharge cycles.

---

## Architecture & Algorithm Design

### 1. Spatial Discovery via Recursive DFS
- **`explore_planet_space`**: Traverses unexplored adjacent coordinates (`N`, `E`, `S`, `W`). Upon exploring a node, it recursively visits adjacent spaces and executes an explicit backtracking move (`get_opposite_direction`) to restore the physical rover position to the caller state.
- **`build_grid_from_explored_dict`**: Dynamically determines the bounding box (`min_x`, `max_x`, `min_y`, `max_y`) from the visited walkable locations, normalizes relative coordinates, and converts the mapped spatial dictionary into a compact list-of-strings grid representation.

### 2. Battery & Distance Constrained BFS
- **`map_surface_with_battery_constraint`**: Uses a `collections.deque` queue to store `(x, y, path_from_home)`.
- Recreates or resets rover states from Home base `(0, 0)` following `path_from_home` to explore surrounding nodes safely without exceeding battery capacity or step limits.

---

## Grid Legend

| Symbol | Description |
| :---: | :--- |
| `H` | Home base / Landing origin `(0, 0)` |
| `.` | Walkable terrain |
| `X` | Obstructed space / Barrier |
| `w` | Water / Surface feature |

---

## Key Functions Summary

| Function | Purpose |
| :--- | :--- |
| `map_surface(planet)` | Main entry point for Phase 1 unconstrained mapping (infinite battery). |
| `build_grid_from_explored_dict(explored)` | Normalizes coordinates and builds matrix strings. |
| `get_opposite_direction(direction)` | Utility returning vector reversal (`N` ↔ `S`, `E` ↔ `W`). |
| `map_surface_with_battery_constraint(planet)` | Main entry point for Phase 2 battery-constrained BFS mapping. |
| `submit_planet_1_map()`, `submit_planet_2_map()`, `submit_planet_3_map()` | Hardcoded grid maps discovered from Phase 1 execution for submission. |

---

## Quick Start Example

```python
import math
from planet_intel import PlanetIntel
from rover import Rover

# Load target planet intel
planet = PlanetIntel.get_planet_1()

# Map the surface (Phase 1)
discovered_grid = map_surface(planet)

# Print discovered grid layout
for row in discovered_grid:
    print(row)
```
