from queue import PriorityQueue
import copy
import time
import numpy as np

INFINITY = 99999999999999999

def A_star(start, goal, heuristic):
    start_time = time.time()
    str_start = start.to_string()
    str_goal = goal.to_string()
    
    # priority queue to visit most promising states first
    pq = PriorityQueue()
    pq.put((0, start))

    # tracking state of the prioriy queue
    open_set = set()
    open_set.add(str_start)

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

    while not pq.empty():
        # take most promising state
        priority, current = pq.get()
        str_current = current.to_string()
        open_set.remove(str_current)

        if str_current == str_goal:
            print(time.time() - start_time)
            return reconstruct_path(came_from, current)
        
        for action in current.possible_actions():
            # create neighbor from possible action
            neighbor = copy.deepcopy(current)
            neighbor.apply(action)
            new_g_score = g_score[str_current] + 1
            str_neighbor = neighbor.to_string()
            if str_neighbor not in g_score or new_g_score < g_score[str_neighbor]:
                came_from[str_neighbor] = current
                g_score[str_neighbor] = new_g_score
                if str_neighbor not in h_score:
                    h_score[str_neighbor] = heuristic(neighbor.state, goal.state)

                f_score[str_neighbor] = new_g_score + h_score[str_neighbor]
                if str_neighbor not in open_set:
                    pq.put((f_score[str_neighbor], neighbor))
                    open_set.add(str_neighbor)

    return []

def reconstruct_path(came_from, current):
    path = []
    while current.to_string() in came_from:
        path.append(current.last_action)
        current = came_from[current.to_string()]

    return path[::-1]