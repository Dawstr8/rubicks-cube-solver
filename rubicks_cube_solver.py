from rubicks_cube import Cube
from bfs import BFS

import time

cube = Cube()
cube.shuffle(4)
end_cube = Cube()

start = time.time()
moves_sequence = BFS(cube, end_cube)
print(time.time() - start)
print(moves_sequence)