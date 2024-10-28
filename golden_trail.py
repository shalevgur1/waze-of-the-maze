
import numpy as np
import random
from enum import Enum
import matplotlib.pyplot as plt


class GoldenTiles(Enum):
    UNDEFINED = 0
    NOPASS = 1
    GOLDEN = 2

def get_possible_next_golden(maze, row, col, end_point):
    # Retrun a list with all the adjusted tiles
    # that can be the next golden tile

    (rows_len, cols_len) = maze.shape

    # Define the relative positions of the neighbors (including diagonals)
    neighbors = [
        (row-1, col),   # Above
        (row, col-1), (row, col+1),     # Sides
        (row+1, col),   # Below
    ]

    # Collect indeces of valid neighbors
    possible_neighbors = []

    # Disable close to maze frame neighbors
    if (col == cols_len - 2 or col == 1) and row == 1:
        neighbors = neighbors[1:]
    if row == rows_len - 2:
        if end_point[1] < col:
            del neighbors[2]
        elif end_point[1] > col:
            del neighbors[1]

    # Check for undefiend tiles
    for r, c in neighbors:
        if 0 <= r < rows_len and 0 <= c < cols_len:  # Check if within bounds
            if (r, c) == end_point: # one tile next to end point
                return [(r,c)]
            if maze[r, c] == GoldenTiles.UNDEFINED:
                possible_neighbors.append((r, c))

    return possible_neighbors



def generate_golden_trail(maze, start_point, end_point):
    # Generate a golden trail in empty maze
    (rows_len, cols_len) = maze.shape

    # Loop to generate golden path
    current_tile = start_point
    while current_tile != end_point:
        # Get possible options for next tile    
        next_tiles = get_possible_next_golden(maze, current_tile[0], current_tile[1], end_point)
        # Set the next tile
        if not next_tiles:
            return
        next_tile = next_tiles.pop(random.randrange(0, len(next_tiles)))
        maze[next_tile] = GoldenTiles.GOLDEN
        # Eliminate the other tiles from being chosen again
        for tile in next_tiles:
            maze[tile] = GoldenTiles.NOPASS
        current_tile = next_tile

def visualize_maze(maze):
    # Create a color map: 0 -> black, 1 -> black, 2 -> white
    color_map = np.zeros(maze.shape, dtype=int)  # Initialize with black (0)
    color_map[maze == 2] = 1  # Set white (1) where the value is 2
    
    # Plot the maze
    plt.imshow(color_map, cmap='gray', interpolation='nearest')
    plt.axis('off')  # Hide the axis
    plt.show()

def main():
    # Set empty maze matrix
    maze_size = (20, 20)
    maze = np.full(maze_size, GoldenTiles.UNDEFINED, dtype=object)

    (rows_len, cols_len) = maze.shape
    
    # Set start and end points
    start_point = (0, random.randrange(0, cols_len))
    end_point = (rows_len - 1, random.randrange(0, cols_len))
    maze[start_point] = GoldenTiles.GOLDEN
    maze[end_point] = GoldenTiles.GOLDEN

    print(start_point, end_point)
    
    generate_golden_trail(maze, start_point, end_point)

    int_maze = np.vectorize(lambda x: x.value)(maze)

    visualize_maze(int_maze)

if __name__ == "__main__":
    main()



# # Example matrix (0 = path, 1 = wall)
# maze_matrix = np.array([
#     [1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 1, 0, 1],
#     [1, 1, 0, 1, 0, 1],
#     [1, 0, 0, 0, 0, 1],
#     [1, 1, 1, 1, 1, 1]
# ])

# # Function to visualize the matrix as a graph
# def visualize_maze(matrix):
#     plt.figure(figsize=(6, 6))  # Set the figure size
#     plt.imshow(matrix, cmap='binary', interpolation='nearest')  # Display the matrix
#     plt.xticks([])  # Hide x ticks
#     plt.yticks([])  # Hide y ticks
#     plt.title("Maze Visualization")
#     plt.show()