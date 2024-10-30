from maze_generator import maze_generator
import visualizer


def main():

    # Get a new maze
    (maze, start_point, end_point) = maze_generator()
    visualizer.visualize_maze(maze, start_point, end_point)


if __name__ == "__main__":
    main()