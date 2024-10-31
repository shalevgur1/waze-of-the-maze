
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

def visualize_maze(maze, start_point, end_point):
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

def set_player(maze, position):
    pass

def visualize_walk(maze, old_position, new_position):
    pass

def delete_player(maze, position):
    pass


class Visualizer:
    """
        Class for visualize the maze and the player walking in the maze.
        Simple - using a simple graphing module.
    """

    def __init__(self, maze, start_point, end_point):
        self.maze = maze                # Store the original maze
        self.color_path = 'green'       # Color for the path (0)
        self.color_wall = 'black'       # Color for the wall (1)
        self.player_color = 'yellow'    # Color for the agent (2)
        self.color_start_end = 'blue'   # Color for start and end points (3 and 4)
        self.start_point = start_point  # Starting tile of the maze
        self.end_point = end_point      # Ending tile of the maze
        self.player_position = start_point # Set player position to starting point

    def visualize_maze(self):
        """Visualize the maze with the start and end points."""
        # Create a display maze based on the original maze
        display_maze = np.where((self.maze == 0), 0,  # Green path
                                np.where((self.maze == 1), 1,  # Black wall
                                         np.where((self.maze == 2), 2,  # Yellow Agent
                                                  np.where((self.maze == 3), 3,  # Blue start
                                                           np.where((self.maze == 4), 4, 1)))))

        # Set the starting and ending points in the display maze
        display_maze[self.start_point] = 3  # Represent start point with 3
        display_maze[self.end_point] = 4  # Represent end point with 4

        # Define a custom color map
        cmap = ListedColormap([self.color_path, self.color_wall, self.player_color, self.color_start_end])

        # Plot the maze
        plt.imshow(display_maze, cmap=cmap, interpolation='nearest')
        plt.axis('off')  # Hide the axis
        plt.show()

    def visualize_walk(self, new_position):
        """Visualize the player walking from one position to another."""
        # Change player position
        self.maze[self.player_position] = 0
        self.maze[new_position] = 2 

        self.visualize_maze()

    def reset(self):
        """Remove the player from the maze."""
        self.maze[self.player_position] = 0         # Reset player position to 0 (green)
        self.player_position = self.start_point     # Reset player to starting position
