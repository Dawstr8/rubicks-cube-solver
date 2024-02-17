from rubicks_cube import Cube
from dijkstra import dijkstra

import time

cube = Cube()
cube.shuffle(100)
cube.draw()

start = time.time()
print(len(dijkstra(cube, 3)))
print(time.time() - start)