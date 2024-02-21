from rubicks_cube import Cube
from bfs import BFS
from a_star import A_star, A_star_both_sides

def heuristic(s1, s2):
    distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1
    
    return distance / 12.0

# path = BFS(cube, end_cube)
# path = A_star(cube, end_cube, heuristic)
# print(path)

if __name__ == "__main__":
    cube = Cube()
    cube.shuffle(6)
    end_cube = Cube()
    path = A_star_both_sides(cube, end_cube, heuristic, 10)
    print('finished', path)