import copy
import time
from multiprocessing import Process, Manager
import heapq

INFINITY = 99999999999999999

class PQ:
    def __init__(self):
        self.queue = []
        self.lookup_set = set()
    
    def push(self, priority, value):
        heapq.heappush(self.queue, (priority, value))
        self.lookup_set.add(str(value))

    def pop(self):
        (priority, value) = heapq.heappop(self.queue)
        self.lookup_set.remove(str(value))
        return value
    
    def empty(self):
        return len(self.queue) == 0
    
    def includes(self, value):
        return str(value) in self.lookup_set

def A_star(start, goal, heuristic, max_g_value=None, result_list=[], closed_set=[], goal_closed_set=[], start_finished=[False, None], end_finished=[False, None]):
    start_time = time.time()
    str_start = str(start)
    str_goal = str(goal)

    # priority queue to visit most promising states first
    pq = PQ()
    pq.push(0, start)

    # tracking found nodes to use by second A*
    closed_set.append(str_start)

    # kept to be able to watch history of nodes
    came_from = {}

    # real distance from the start
    g_score = {}
    g_score[str_start] = 0

    # heuristic distance to the goal
    h_score = {}
    h_score[str_start] = heuristic(start.state, goal.state)

    # sum of real distance from start and heuristic to the goal
    f_score = {}
    f_score[str_start] = h_score[str_start]

    visited_nodes = {}
    visited_nodes[str_start] = start

    while not pq.empty():
        # take most promising state
        current = pq.pop()
        str_current = str(current)

        # finish possibilities
        if end_finished[0]:
            # print('second search found full path')
            return []
        
        if end_finished[1] is not None:
            # print('retrieving path from found node')
            # tutaj nie może być end_finished, bo ten ma inny last move
            end_node = visited_nodes[end_finished[1]]
            result_list.extend(reconstruct_path(came_from, visited_nodes, end_node))
            return result_list
        
        if str_current == str_goal or str_current in goal_closed_set:
            print(time.time() - start_time)
            if str_current == str_goal:
                # print('full path found')
                start_finished[0] = True
            else:
                # print('node already in second A*')
                start_finished[1] = str_current
                
            result_list.extend(reconstruct_path(came_from, visited_nodes, current))
            return result_list
        
        if max_g_value and max_g_value < g_score[str_current]:
            continue
        
        for action in current.possible_actions():
            # create neighbor from possible action
            neighbor = copy.deepcopy(current)
            neighbor.apply(action)
            new_g_score = g_score[str_current] + 1
            str_neighbor = str(neighbor)
            if str_neighbor not in g_score or new_g_score < g_score[str_neighbor]:
                came_from[str_neighbor] = str_current
                visited_nodes[str_neighbor] = neighbor
                g_score[str_neighbor] = new_g_score
                if str_neighbor not in h_score:
                    h_score[str_neighbor] = heuristic(neighbor.state, goal.state)

                f_score[str_neighbor] = new_g_score + h_score[str_neighbor]
                if not pq.includes(neighbor):
                    pq.push(f_score[str_neighbor], neighbor)
                    closed_set.append(str_neighbor)
        
    return []

def reconstruct_path(came_from, visited_nodes, current):
    path = []
    while str(current) in came_from:
        path.append(current.last_action)
        current = visited_nodes[came_from[str(current)]]

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
    # if start_finished[1] is not None:
    #     print('start', start_finished[1])
    # elif end_finished[1] is not None:
    #     print('end', end_finished[1])

    path_from_start = list(result_list_start)
    path_from_end = flip_path(list(result_list_goal))

    return path_from_start + path_from_end