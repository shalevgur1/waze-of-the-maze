
import numpy as np
import random
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

"""
Maze Generator Script

This script generates a customizable maze layout using a grid-based approach.
The maze is initialized with a starting and ending point, which are marked
distinctly, and then a random path is created to connect them. Walls and paths
are defined using a combination of integers and enums to distinguish different
tile types.

Key Features:
- Randomized Path Creation: A trail from the starting point to the ending
  point is created by selecting adjacent tiles, ensuring there is at least one
  valid path.
- Tile Types: The maze includes several tile types:
  - Wall tiles: Represent impassable areas.
  - Path tiles: Represent walkable areas.
- Visualization: The maze is visualized using matplotlib, with each tile type
  represented by a specific color (e.g., green for paths, black for walls,
  and blue for start/end points).

Usage:
1. Run this script to generate a maze with a single solution.
2. Adjust parameters within the script for different maze sizes and layouts.
3. Use the visualization function to render the maze in a readable format,
   with each tile color-coded for easy understanding.

Dependencies:
- numpy: For matrix operations and grid representation.
- matplotlib: For visualizing the generated maze layout.
"""

# ***************************************
#          CONFIGURATION AREA
# ***************************************

# Maze dimensions
maze_width = 30
maze_height = 30

# Visualization settings
color_path = 'green'
color_wall = 'black'
color_start_end = 'blue'

# ***************************************


# Enum to represent the maze tiles
class MazeTiles(Enum):
    UNDEFINED = 0
    WALL = 1
    TRAIL = 2

def set_nopass_around_endpoint(maze, end_point, path):
    # Set nopass around endpoint
    (row, col) = end_point
    (rows_len, cols_len) = maze.shape

    neighbors = [
        (row-1, col),   # Above
        (row, col-1), (row, col+1),     # Sides
    ]

    # Check for undefiend tiles
    for r, c in neighbors:
        if 0 <= r < rows_len and 0 <= c < cols_len:  # Check if within bounds
            if (r,c) != path:
                maze[r,c]  = MazeTiles.WALL

def get_possible_next_tile(maze, row, col, end_point):
    # Retrun a list with all the adjusted tiles
    # that can be the next path tile

    (rows_len, cols_len) = maze.shape

    # Define the relative positions of the neighbors (including diagonals)
    neighbors = [
        (row-1, col),   # Above
        (row, col-1), (row, col+1),     # Sides
        (row+1, col),   # Below
    ]

    # Collect indeces of valid neighbors
    possible_neighbors = []

    # Check for undefiend tiles
    for r, c in neighbors:
        if 0 <= r < rows_len and 0 <= c < cols_len:  # Check if within bounds
            if (r, c) == end_point: # one tile next to end point
                set_nopass_around_endpoint(maze, (r,c), (row,col))
            if maze[r, c] == MazeTiles.UNDEFINED:
                possible_neighbors.append((r, c))

    return possible_neighbors

def check_near_trails(maze, row, col):
    # Check if given tile is next to a trail already
    (rows_len, cols_len) = maze.shape

    # Define the relative positions of the neighbors (including diagonals)
    neighbors = [
        (row-1, col),   # Above
        (row, col-1), (row, col+1),     # Sides
        (row+1, col),   # Below
    ]

    proximate_trail_tiles = []

    # Check for trail tiles
    for r, c in neighbors:
        if 0 <= r < rows_len and 0 <= c < cols_len:  # Check if within bounds
            if maze[r,c] == MazeTiles.TRAIL:
                proximate_trail_tiles.append((r,c))
    
    # No proximate trail tiles
    return proximate_trail_tiles
    

def possible_break_wall(maze, row, col):
    # Retrun a list with all the adjusted tiles
    # that are WALL and can be "breaked" for strating a new path

    (rows_len, cols_len) = maze.shape

    # Define the relative positions of the neighbors (including diagonals)
    neighbors = [
        (row-1, col),   # Above
        (row, col-1), (row, col+1),     # Sides
        (row+1, col),   # Below
    ]

    # Check for WALL tiles
    for r, c in neighbors:
        if 0 <= r < rows_len and 0 <= c < cols_len:  # Check if within bounds
            if maze[r, c] == MazeTiles.WALL:
                if len(check_near_trails(maze, r, c)) == 1:
                    # WALL tile has only one proximate trail tile
                    return (r, c)

def generate_maze_trails(maze, start_point, end_point):
    # Generate all trails in empty maze
    (rows_len, cols_len) = maze.shape
    
    mined_tiles = []

    # Loop to generate TRAIL path
    current_tile = start_point
    # Get possible options for next tile   
    next_tiles = get_possible_next_tile(maze, current_tile[0], current_tile[1], end_point)
    mined_tiles.append(current_tile)
    while not (current_tile == start_point and not next_tiles):
        
        # Advance to chosen tile
        if not next_tiles:
            # Dead end - look for different path
            if len(mined_tiles) == 1:
                current_tile = mined_tiles[0]
            else:
                current_tile = mined_tiles.pop()
            next_tile = possible_break_wall(maze, current_tile[0], current_tile[1])
        else:
            # Choose random tile to advance
            next_tile = next_tiles.pop(random.randrange(0, len(next_tiles)))
        
        if next_tile:
            # Set tile as part of path
            maze[next_tile] = MazeTiles.TRAIL
            current_tile = next_tile
            mined_tiles.append(current_tile)

            # Eliminate the other tiles from being chosen again
            for tile in next_tiles:
                maze[tile] = MazeTiles.WALL
        
        # Get possible options for next tile    
        next_tiles = get_possible_next_tile(maze, current_tile[0], current_tile[1], end_point)

def maze_generator(width=maze_width, height=maze_height):
    # Set empty maze matrix
    maze_size = (width, height)
    maze = np.full(maze_size, MazeTiles.UNDEFINED, dtype=object)

    (rows_len, cols_len) = maze.shape
    
    # Set start and end points
    start_point = (0, random.randrange(0, cols_len))
    end_point = (rows_len - 1, random.randrange(0, cols_len))
    maze[start_point] = MazeTiles.TRAIL
    maze[end_point] = MazeTiles.TRAIL

    print(start_point, end_point)

    # Mine maze paths
    generate_maze_trails(maze, start_point, end_point)

    # Transfering to int from Enum objects
    int_maze = np.vectorize(lambda x: x.value)(maze)
    int_maze[int_maze == 0] = 1
    int_maze[int_maze == 2] = 0
    print(int_maze)

    # Return maze and start and end points
    return(int_maze, start_point, end_point)