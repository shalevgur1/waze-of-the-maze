import numpy as np
from enum import Enum
import visualizer

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

    reward = -1.0             # Movement cost. Default reward value, can be adjusted as needed
    end_tile_reward = 10.0    # Reward for completing the maze

    def __init__(self, maze, starting_tile, end_tile, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.99):
        # Init properties
        self.maze = maze
        self.q_table = np.zeros((maze.shape[0], maze.shape[1], len(Action)))  # Q-table
        self.starting_tile = starting_tile        # The begging tile of the maze
        self.end_tile = end_tile                  # The end tile of the maze
        self.learning_rate = learning_rate        # Learning rate - the amount of influence of changing values in the q-table
        self.discount_factor = discount_factor    # Dicount factor - depends on priorization of future or imidiate rewards
        self.epsilon_decay = epsilon_decay        # Epsilon Decay - the "rapidity" the agent moves torward exploitation instead of exploration 
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

    def _choose_action(self, state):
            # Choose an action based on the epsilon-greedy strategy.
            if np.random.rand() < self.epsilon:
                # Explore: Choose a random valid action
                valid_actions = [a for a in range(len(Action)) if not np.isnan(self.q_table[state[0], state[1], a])]
                action = np.random.choice(valid_actions)
            else:
                # Exploit: Choose the action with the max Q-value
                q_values = self.q_table[state[0], state[1]]
                action = np.argmax([q if not np.isnan(q) else -np.inf for q in q_values])

            action = Action(action)  # Convert to Action enum
            return action

    def _step(self, state, action):
        """
            Define movement logic here based on the action
            Update position, determine reward and end of maze status, and return them
        """
        row, col = state
        if action == Action.UP:  # Check if action is UP
            new_row, new_col = row - 1, col
        elif action == Action.DOWN:  # Check if action is DOWN
            new_row, new_col = row + 1, col
        elif action == Action.LEFT:  # Check if action is LEFT
            new_row, new_col = row, col - 1
        elif action == Action.RIGHT:  # Check if action is RIGHT
            new_row, new_col = row, col + 1

        # Return values and set stop iteration for end of maze tile
        new_state = (new_row, new_col)
        if new_state == self.end_tile: return new_state, self.end_tile_reward, True
        return new_state, self.reward, False

    def learn(self, episodes=1000):
        """
            Public learn function to be called to start the learning process of the agent.
            The learning is being preformed with the Reinforcement Learning, Q-Learning Method.
            See Q-Learning update rule:
            Q(s,a)←Q(s,a)+α[r+γa′max​Q(s′,a′)−Q(s,a)]
        """
        
        # Set epsilon greedy to 1
        self.epsilon = 1.0

        # Start episodes
        for episode in range(episodes):
            state = self.starting_tile
            end_of_maze = False
            
            # Start exploring
            while not end_of_maze:
                action = self._choose_action(state)
                print(action)
                new_state, reward, end_of_maze = self._step(state, action)  # Moves the agent, returns new state and end-of-maze flag

                # Update Q-value for the current state-action pair
                old_value = self.q_table[state[0], state[1], action.value]
                next_max = np.nanmax(self.q_table[new_state[0], new_state[1]])  # Max Q-value for the next state

                # Q-learning update rule (Bellman Equasion)
                new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
                self.q_table[state[0], state[1], action.value] = new_value

                # Move to the next state
                state = new_state

                # Decay epsilon after each episode to reduce exploration over time
                self.epsilon *= self.epsilon_decay

        # End learning logging message
        print("Greetings! I am the noble agent, and I stand before thee, well-educated and wise. Through my arduous journeys within the labyrinth, I have gleaned much knowledge and experience.")

    def walk_visualized(self, visualObj):
        """
            Let the agent walk according to current Q-Table.
            For testing after the learning phase.
        """

        end_of_maze = False
        self.epsilon = 0.0
        state = self.starting_tile

        # Start walking
        while not end_of_maze:
            visualObj.visualize_walk(state)
            action = self._choose_action(state)
            new_state, _, end_of_maze = self._step(state, action)  # Moves the agent, returns new state and end-of-maze flag
            state = new_state



