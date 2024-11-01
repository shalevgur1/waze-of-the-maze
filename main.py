from maze_generator import maze_generator
from visualizer import Visualizer
from waze_agent_lib import WazeAgent


def main():
    maze_size = 10
    # Get a new maze and show it
    (maze, start_point, end_point) = maze_generator(maze_size, maze_size)
    visual = Visualizer(maze, start_point, end_point)

    waze_agent = WazeAgent(maze, start_point, end_point)
    waze_agent.learn()



if __name__ == "__main__":
    main()