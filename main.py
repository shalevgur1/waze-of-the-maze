from maze_generator import maze_generator
from visualizer import Visualizer
from waze_agent_lib import WazeAgent


def main():
    maze_size = 15
    # Get a new maze and show it
    (maze, start_point, end_point) = maze_generator(maze_size, maze_size)
    visual = Visualizer(maze, start_point, end_point)

    # Iinitalize the agent and preforming learning of the maze
    waze_agent = WazeAgent(maze, start_point, end_point)
    waze_agent.learn()

    # Display agent walk in the maze after learning process
    waze_agent.walk_visualized(visual)



if __name__ == "__main__":
    main()