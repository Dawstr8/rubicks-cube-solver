import copy
import time
from multiprocessing import Process, Manager
import heapq

INFINITY = 99999999999999999

class PQ:
    def __init__(self):
        self.queue = []
        self.lookup_set = set()
    
    def push(self, priority, item):
        heapq.heappush(self.queue, (priority, item))
        self.lookup_set.add(item)

    def pop(self):
        (priority, item) = heapq.heappop(self.queue)
        self.lookup_set.remove(item)
        return item
    
    def empty(self):
        return len(self.queue) == 0
    
    def includes(self, item):
        return item in self.lookup_set

class Node:
    def __init__(self, cube, parent_key=None, g=0, h=INFINITY):
        self.cube = cube
        self.parent_key = parent_key
        self.g = g
        self.h = h

    def __str__(self):
        return str(self.cube)

    def f(self):
        return self.g + self.h
    
    def neighbors(self, heuristic, goal):
        neighbors = []
        for action in self.cube.possible_actions():
            neighbor_cube = copy.deepcopy(self.cube)
            neighbor_cube.apply(action)
            neighbors.append(Node(neighbor_cube, str(self), self.g + 1, heuristic(neighbor_cube.state, goal.state)))
        
        return neighbors

def A_star(start, goal, heuristic, max_g_value=None, result_list=[], closed_set=[], goal_closed_set=[], start_finished=[False, None], end_finished=[False, None]):
    start_time = time.time()
    visited = { str(start): Node(copy.deepcopy(start), None, 0, heuristic(start.state, goal.state)) }

    pq = PQ()
    pq.push(0, str(start))
    while not pq.empty():
        # take most promising state
        current_key = pq.pop()
        current = visited[current_key]

        # finish possibilities
        if end_finished[0]:
            return []
        
        if end_finished[1] is not None:
            result_list.extend(reconstruct_path(visited, end_finished[1]))
            return result_list
        
        if current == goal or current_key in goal_closed_set:
            print(time.time() - start_time)
            if current == goal:
                start_finished[0] = True
            else:
                start_finished[1] = current_key
                
            result_list.extend(reconstruct_path(visited, current_key))
            return result_list
        
        if max_g_value and max_g_value < current.g:
            continue
        
        for neighbor in current.neighbors(heuristic, goal):
            neighbor_key = str(neighbor)
            if neighbor_key not in visited or neighbor.g < visited[neighbor_key].g:
                visited[neighbor_key] = neighbor
                if not pq.includes(neighbor_key):
                    pq.push(neighbor.f(), neighbor_key)
                    closed_set.append(neighbor_key)
        
    return []

def reconstruct_path(visited, current_key):
    path = []
    current = visited[current_key]
    while current.parent_key in visited:
        path.append(current.cube.last_action)
        current = visited[current.parent_key]

    return path[::-1]

def flip_path(path):
    new_path = []
    for step in path:
        if len(step) == 0:
            continue 
        elif len(step) == 1:
            new_path.append(step + 'p')
        elif step[1] == '2':
            new_path.append(step)
        else:
            new_path.append(step[0])

    return new_path[::-1]

def A_star_both_sides(start, goal, heuristic, max_g_value=None):
    manager = Manager()
    start_shared_set = manager.list()
    goal_shared_set = manager.list()
    result_list_start = manager.list()
    result_list_goal = manager.list()
    start_finished = manager.list([False, None])
    end_finished = manager.list([False, None])

    p1 = Process(target=A_star, args=(start, goal, heuristic, max_g_value, result_list_start, start_shared_set, goal_shared_set, start_finished, end_finished))
    p2 = Process(target=A_star, args=(goal, start, heuristic, max_g_value, result_list_goal, goal_shared_set, start_shared_set, end_finished, start_finished))

    # Start the processes
    p1.start()
    p2.start()

    # Wait for the processes to finish
    p1.join()
    p2.join()

    print(list(result_list_start), list(result_list_goal))
    path_from_start = list(result_list_start)
    path_from_end = flip_path(list(result_list_goal))

    return path_from_start + path_from_end