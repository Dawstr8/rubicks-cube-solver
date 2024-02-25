import copy
import time
import random
from multiprocessing import Process, Manager
import heapq

INFINITY = 99999999999999999

class PQ:
    def __init__(self):
        self.queue = []
        self.lookup_set = {}
    
    def push(self, priority, item):
        heapq.heappush(self.queue, (priority, item))
        if not item in self.lookup_set:
            self.lookup_set[item] = 0 
        self.lookup_set[item] += 1

    def pop(self):
        (priority, item) = heapq.heappop(self.queue)
        self.lookup_set[item] -= 1
        return item
    
    def empty(self):
        return len(self.queue) == 0
    
    def includes(self, item):
        return item in self.lookup_set and self.lookup_set[item] > 0

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
        
        random.shuffle(neighbors)
        return neighbors

def A_star(start, goal, heuristic, max_g_value=None, path=[], visited_set=[], other_visited_set=[], start_search_params=[False, None], goal_search_params=[False, None], search_name=None):
    start_time = time.time()
    visited = { str(start): Node(copy.deepcopy(start), None, 0, heuristic(start.state, goal.state)) }
    visited_set.append(str(start))

    pq = PQ()
    pq.push(0, str(start))
    while not pq.empty():
        # take most promising state
        current_key = pq.pop()
        current = visited[current_key]

        # finish possibilities
        [is_finished, final_key] = is_search_finished(current, goal, start_search_params, goal_search_params, other_visited_set)
        if is_finished:
            print(search_name, time.time() - start_time)
            if final_key is not None:
                path.extend(reconstruct_path(visited, final_key))
            return
        
        if max_g_value and max_g_value < current.g:
            continue
        
        for neighbor in current.neighbors(heuristic, goal):
            neighbor_key = str(neighbor)
            if neighbor_key not in visited or neighbor.g < visited[neighbor_key].g:
                visited[neighbor_key] = neighbor
                pq.push(neighbor.f(), neighbor_key)
                visited_set.append(neighbor_key)
        
    return []

def is_search_finished(current, goal, start_search_params, goal_search_params, other_visited_set):
    current_key = str(current)
    [other_found_full_path, shared_from_other_set] = goal_search_params

    if other_found_full_path:
        return [True, None]
        
    if shared_from_other_set is not None:
        return [True, shared_from_other_set]
    
    if current == goal or current_key in other_visited_set:
        if current == goal:
            start_search_params[0] = True
        else:
            start_search_params[1] = current_key
        return [True, current_key]
    
    return [False, None]

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
    start_visited_set = manager.list()
    goal_visited_set = manager.list()
    path_from_start = manager.list()
    path_from_goal = manager.list()

    # found full path? first found from other set
    start_search_params = manager.list([False, None])
    end_search_params = manager.list([False, None])

    p1 = Process(target=A_star, args=(start, goal, heuristic, max_g_value, path_from_start, start_visited_set, goal_visited_set, start_search_params, end_search_params, 'start'))
    p2 = Process(target=A_star, args=(goal, start, heuristic, max_g_value, path_from_goal, goal_visited_set, start_visited_set, end_search_params, start_search_params, 'goal'))

    # Start the processes
    p1.start()
    p2.start()

    # Wait for the processes to finish
    p1.join()
    p2.join()

    path_from_start = list(path_from_start)
    path_from_goal = flip_path(list(path_from_goal))
    print(path_from_start, path_from_goal)
    return path_from_start + path_from_goal