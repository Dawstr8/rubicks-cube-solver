from rubicks_cube import Cube
from bfs import BFS
from a_star import A_star

def heuristic(s1, s2):
    distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1
    
    return distance / 12;

cube = Cube()
cube.shuffle(10)
end_cube = Cube()

# path = BFS(cube, end_cube)
path = A_star(cube, end_cube, heuristic)
print(path)