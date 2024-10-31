from maze_generator import maze_generator
from visualizer import Visualizer
from waze_agent_lib import WazeAgent


def main():
    maze_size = 10
    # Get a new maze
    (maze, start_point, end_point) = maze_generator(maze_size, maze_size)

    #waze_agent = WazeAgent(maze, start_point)
    #print(waze_agent.q_table)

    visual = Visualizer(maze, start_point, end_point)
    visual.visualize_maze()


if __name__ == "__main__":
    main()