import math
from planet_intel import PlanetIntel
from rover import Rover
from collections import deque

### Scaffold LAST UPDATED April 2. V: 1.1

planet_1 = PlanetIntel.get_planet_1()
planet_2 = PlanetIntel.get_planet_2()
planet_3 = PlanetIntel.get_planet_3()

def get_opposite_direction(direction):
    """
    Returns the reverse of a given direction for backtracking.
    """
    opposite = {"N": "S", "E": "W", "S": "N", "W": "E"}
    return opposite.get(direction)

def build_grid_from_explored_dict(explored):
    if not explored:
        return []

    # 1. Filter coordinates to find the "True" boundaries
    # We only look at where the rover actually stood (not the 'X's it saw from afar)
    walkable_coords = [pos for pos, char in explored.items() if char != 'X']
    
    if not walkable_coords:
        return []

    min_x = min(c[0] for c in walkable_coords)
    max_x = max(c[0] for c in walkable_coords)
    min_y = min(c[1] for c in walkable_coords)
    max_y = max(c[1] for c in walkable_coords)

    # 2. Calculate dimensions based on walkable range
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # 3. Initialize grid with 'X'
    # Any coordinate within these bounds that wasn't visited is assumed to be 'X'
    grid_matrix = [['X' for _ in range(width)] for _ in range(height)]

    # 4. Fill the grid using only coordinates that fall within our new bounds
    for (x, y), char in explored.items():
        # Check if this coordinate is within our "walkable" bounding box
        if min_x <= x <= max_x and min_y <= y <= max_y:
            row_idx = max_y - y
            col_idx = x - min_x
            grid_matrix[row_idx][col_idx] = char

    return ["".join(row) for row in grid_matrix]

def explore_planet_space(planet, rover, explored, x, y):
    """
    A recursive DFS that moves the rover, records terrain, 
    and backtracks to maintain positional integrity.
    """
    # 1. Record current location terrain if not already visited
    # We use get_current_location() to see what's under us
    current_terrain = rover.get_current_location()
    explored[(x, y)] = current_terrain

    # 2. Define our movement vectors
    # North: +y, South: -y, East: +x, West: -x
    directions = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0)
    }

    for d_name, (dx, dy) in directions.items():
        next_coords = (x + dx, y + dy)
        
        # Only try moving if we haven't mapped that coordinate yet
        if next_coords not in explored:
            success, message = rover.move(d_name)
            
            if success:
                # Recursive call to explore the new tile
                explore_planet_space(planet, rover, explored, next_coords[0], next_coords[1])
                
                # BACKTRACK: We must move back to our original 'x, y' 
                # so the next iteration of the loop starts from the right place.
                opp = get_opposite_direction(d_name)
                rover.move(opp)
            else:
                # If we hit an "Obstructed Space", record it in our map 
                # so we don't try to walk through it later.
                if message == "Obstructed Space":
                    explored[next_coords] = 'X'

def get_planet_grid(planet, rover):
    """
    Orchestrates the exploration and then formats the gathered data into the required list of strings.
    """
    # Key: (x, y) tuple, Value: character ('.', 'X', 'w', 'H')
    explored = {} 
    
    # Start DFS from home base at (0, 0)
    # We pass the rover's initial terrain type to initialize the home position
    explore_planet_space(planet, rover, explored, 0, 0)
    
    # Once exploration is done, convert the coordinate dictionary into the grid format
    grid = build_grid_from_explored_dict(explored)    
    return grid

def map_surface(planet):
    """
    Main entry point for Phase 1. 
    Initializes a rover with infinite battery and returns the discovered grid.
    """
    rover = Rover(planet, math.inf)
    grid = get_planet_grid(planet, rover)
    return grid


# --- Phase 1 Submissions ---
# After using your map_surface function to discover the layouts locally, 
# hardcode the resulting lists of strings into the functions below. 
# These will be run against the automated tests.

def submit_planet_1_map():
    # Example format: return ['..X..', 'X....', 'ww.H.', 'w...X']
    return ['..X..', 
            'X....', 
            'ww.H.', 
            'w...X']

def submit_planet_2_map():
    return ["w.......",
            "......Xw",
            ".....XXX",
            "..X.H...",
            "XXXX.X..",
            "w..XXX..",
            "........",
            "wX.X...w",
            ]



def submit_planet_3_map():
    return ["....w.X.....",
            "...XXXX..w..",
            ".........X..",
            "...H.....X..",
            ".........w..",
            "XXX...X.....",
            ".w.......X..",
            "...X........",
            "..X.....w...",
            "w.X..XX.XX.."]

# --- Phase 2 ---

def get_valid_unexplored_neigbhor_node(planet, curr_node, explored):
    print(curr_node)
    curr_rover = curr_node[2]
    
    if curr_rover.get_battery_life() < 1:
        return []

    possible_move_with_neigbhor = [(0, 1, "N"), (0, -1, "S"), (1, 0, "E"), (-1, 0, "W")]

    path = curr_node[3] # A list of moves to get to that node e.g ["N", "E"]

    neigbhor_node_to_explore = []
    for dx, dy, next_move in possible_move_with_neigbhor:
        pos_neigbhor_coords = (curr_node[0] + dx, curr_node[1] + dy)

        if pos_neigbhor_coords in explored:
            continue
        new_rover = Rover(planet, 20)
        
        for move_dir in path:
            new_rover.move(move_dir)

        success, response = new_rover.move(next_move)
        
        if success:
            new_path = path.copy()
            new_path.append(next_move)
            neigbhor_node_to_explore.append((pos_neigbhor_coords[0], pos_neigbhor_coords[1], new_rover, new_path))
            explored[pos_neigbhor_coords] = new_rover.get_current_location()
        else:
            if response == "Obstructed Space":
                explored[pos_neigbhor_coords] = "X"

    return neigbhor_node_to_explore  



def explore_planet_space_with_constraints(planet, rover, explored):
    queue = deque([(0, 0, rover, [])])
    
    while queue:
        curr_node = queue.popleft()
        print(curr_node)

        for valid_unexplored_neigbhor_node in get_valid_unexplored_neigbhor_node(planet, curr_node, explored):
            queue.append(valid_unexplored_neigbhor_node)

    return explored



def can_return_home(current_pos, steps_to_home):
    # If it took us 10 steps to get here, we MUST go back now.
    return steps_to_home < 10

def map_surface_with_battery_constraint(planet):
    # Initialize the single rover
    rover = Rover(planet, 20)
    explored = {(0, 0): "H"}
    
    # Queue stores: (x, y, path_from_home)
    # The 'path_from_home' tells us exactly how to get back or move to a neighbor
    queue = deque([(0, 0, [])])

    while queue:
        curr_x, curr_y, current_path = queue.popleft()
        
        # Check all 4 directions
        directions = [(0, 1, "N"), (0, -1, "S"), (1, 0, "E"), (-1, 0, "W")]
        
        for dx, dy, move_dir in directions:
            next_coords = (curr_x + dx, curr_y + dy)
            
            # 1. Skip if already explored
            if next_coords in explored:
                continue
            
            # 2. Check battery constraint (Distance limit)
            # current_path length is how many steps away we are.
            if len(current_path) >= 10:
                continue

            # 3. Physical Movement Logic
            # To use ONE rover, we must move it from (0,0) to the current node, 
            # then attempt the next move.
            
            # Reset rover to Home (simulating the return trip/recharge)
            rover = Rover(planet, 20) 

            
            for step in current_path:
                rover.move(step)
            
            # Attempt the new move
            success, response = rover.move(move_dir)
            
            if success:
                # Mark as explored and add to queue
                explored[next_coords] = rover.get_current_location()
                new_path = current_path + [move_dir]
                queue.append((next_coords[0], next_coords[1], new_path))
            else:
                if response == "Obstructed Space":
                    explored[next_coords] = "X"
    grid = build_grid_from_explored_dict(explored)
    return grid

rows = [
            "........",
            ".....Xw.",
            ".....XXX",
            "...X.H...",
            "XXXX.X..",
            "w..XXX..",
            "........",
            "wX.X...w"
        ]

# test_planet = PlanetIntel.create_test_planet(rows)
# grid = (map_surface_with_battery_constraint(planet_3))
# for row in grid:
#     print(row)
# print()
# print("Planet2")
# grid = (map_surface(planet_2))
# for row in grid:
#     print(row)

# print(planet_2)


