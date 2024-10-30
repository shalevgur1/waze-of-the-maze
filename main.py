from maze_generator import maze_generator
import visualizer
from waze_agent_lib import WazeAgent


def main():

    # Get a new maze
    (maze, start_point, end_point) = maze_generator(5, 5)

    waze_agent = WazeAgent(maze, start_point)
    print(waze_agent.q_table)

    visualizer.visualize_maze(maze, start_point, end_point)


if __name__ == "__main__":
    main()