from rubicks_cube import Cube, get_shuffled_cube
from bfs import BFS
from a_star import A_star, A_star_both_sides
from heuristics import simple_heuristic

if __name__ == "__main__":
    start_cube = get_shuffled_cube(10)
    goal_cube = Cube()
    path = A_star_both_sides(start_cube, goal_cube, simple_heuristic, 10)
    print('finished', path)