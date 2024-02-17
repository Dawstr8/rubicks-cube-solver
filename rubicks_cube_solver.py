from rubicks_cube import Cube
from bfs import BFS

cube = Cube()
cube.shuffle(15)
end_cube = Cube()

moves_sequence = BFS(cube, end_cube)
print(moves_sequence)