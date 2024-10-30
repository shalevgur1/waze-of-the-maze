import numpy as np
from enum import Enum

class Action(Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

class WazeAgent:
    """
    Waze of the Maze: This agent class is designed to discover and learn the most efficient 
    path to the exit within a maze. It employs Reinforcement Learning and the Q-Learning 
    technique to navigate and solve the maze.
    """

    def __init__(self, maze, current_position):
        # Init properties
        self.maze = maze
        self.q_table = np.zeros((maze.shape[0], maze.shape[1], len(Action)))  # Q-table
        self.current_position = current_position  # Current position of the agent
        # Set Q Table with None value for walls and actions that goes into walls
        self._set_q_table_valid()

    def _set_q_table_valid(self):
        # Set the Q Table wall cells or actions leading to walls to None
        for i, j in np.ndindex(self.maze.shape):
            if self.maze[i, j] == 1:
                # Wall tile - all actions should be None
                self.q_table[i, j, :] = None
            else:
                # Trail tile - actions that lead into walls should be None
                _, actions_to_trails = self._get_available_tiles(self.maze, (i,j))
                self.q_table[i, j] = actions_to_trails

    def _get_available_tiles(self, maze, tile):
        """
        Returns:
        - A list of available trail tiles adjacent to the given tile in the maze.
        - A list of available actions (up, down, left, right)
        """
        row, col = tile
        available_tiles = []
        available_actions = [None, None, None, None]

        # Define possible movements (up, down, left, right)
        movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (row_change, col_change)

        for index, move in enumerate(movements):
            new_row, new_col = row + move[0], col + move[1]

            # Check if the new tile is within the maze bounds
            if 0 <= new_row < maze.shape[0] and 0 <= new_col < maze.shape[1]:
                if maze[new_row, new_col] == 0:  # Check if the tile is a trail
                    available_tiles.append((new_row, new_col))
                    available_actions[index] = 0

        return available_tiles, available_actions
