from rubicks_cube import Cube, get_shuffled_cube
from bfs import BFS
from a_star import A_star, A_star_both_sides

def heuristic(s1, s2):
    distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1
    
    return distance / 12.0

if __name__ == "__main__":
    start_cube = get_shuffled_cube(10)
    goal_cube = Cube()
    path = A_star_both_sides(start_cube, goal_cube, heuristic, 10)
    print('finished', path)