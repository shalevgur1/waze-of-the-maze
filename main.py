import numpy as np
import matplotlib.pyplot as plt
import random
from enum import Enum

class MazeTile(Enum):
    UNDEFINED = 0
    WALL = 1
    TRAIL = 2
    GOLDEN = 3

def get_all_neighbors(array, row, col):
    # Get the number of rows and columns
    num_rows, num_cols = array.shape
    
    # Define the relative positions of the neighbors (including diagonals)
    neighbors = [
        (row-1, col-1), (row-1, col), (row-1, col+1),  # Above
        (row, col-1),               (row, col+1),      # Sides
        (row+1, col-1), (row+1, col), (row+1, col+1)   # Below
    ]
    
    # Collect values of valid neighbors
    neighbor_values = []
    for r, c in neighbors:
        if 0 <= r < num_rows and 0 <= c < num_cols:  # Check if within bounds
            neighbor_values.append(array[r, c])
    
    return neighbor_values

def trail_squre(maze, i, j):
    # Check for 3 tiles of trails around the given tile.
    # To make sure there is no 4 tiles next to each other.
    trail_tiles = {MazeTile.TRAIL, MazeTile.GOLDEN}

    if i > 0:
        if j > 0:
            if (maze[i][j-1] in trail_tiles 
                and maze[i-1][j] in trail_tiles 
                and maze[i-1][j-1] in trail_tiles):
                return True
        # if j < maze.shape[1] - 1:
        #     if (maze[i][j+1] in trail_tiles 
        #         and maze[i-1][j] in trail_tiles 
        #         and maze[i-1][j+1] in trail_tiles):
        #         return True

    return False

def next_to_golden(maze, i, j):
    # Check if given tile is next to a golden tile
    neighbors = get_all_neighbors(maze, i, j)
    if MazeTile.GOLDEN in neighbors:
        return True
    return False

def generate_maze(size):

    # Set empty maze matrix
    maze = np.zeros((5, 5), dtype=int)
    (rows_len, cols_len) = maze.shape

    # Set start and end points
    start_point = (0, random.randint(0, cols_len))
    end_point = (rows_len, random.randint(0, cols_len))
    maze[start_point] = MazeTile.GOLDEN
    maze[end_point] = MazeTile.GOLDEN

    # Iterating over maze matrix
    # for i in range(len(maze)):
    #     for j in range(len(matrix[i])):
    #         if maze[i][j] == 0:
    #             if trail_squre(maze, i, j):
    #                 # Set a wall next to 3 trails
    #                 maze[i][j] = MazeTile.WALL
    #             elif next_to_golden(maze, i, j) and not next_to_golden(maze, )








    



def main():
    # visualize_maze(maze_matrix)
    generate_golden_trail(5)

if __name__ == "__main__":
    main()