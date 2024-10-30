
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# ***************************************
#          CONFIGURATION AREA
# ***************************************

# Visualization settings
color_path = 'green'
color_wall = 'black'
color_start_end = 'blue'

# ***************************************

def visualize_maze(maze, start_point, end_point, color_wall='black', color_path='green', color_start_end='blue'):
    # Set the starting and ending points in the maze
    maze[start_point] = 3
    maze[end_point] = 4

    # Define a custom color map with specific colors for each value:
    # 0 -> green, 1 -> black, 3 and 4 -> blue
    cmap = ListedColormap([color_path, color_wall, color_start_end])

    # Map the values in the maze to the colors:
    # - 0 maps to 0 (green)
    # - 1 maps to 1 (black)
    # - 3 and 4 both map to 2 (blue)
    display_maze = np.where((maze == 3) | (maze == 4), 2,
                            np.where(maze == 0, 0, 1))

    # Plot the maze
    plt.imshow(display_maze, cmap=cmap, interpolation='nearest')
    plt.axis('off')  # Hide the axis
    plt.show()