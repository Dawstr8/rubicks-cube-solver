from collections import deque
import copy

def dijkstra(start, max_depth=10):
    visited = set()
    actions = {}
    distance = {}
    queue = deque([start])
    visited.add(start.to_string())
    distance[start.to_string()] = 0

    while queue:
        state = queue.popleft()
        print(distance[state.to_string()])
        if distance[state.to_string()] == max_depth:
            break

        for action in state.possible_actions():
            new_state = copy.deepcopy(state)
            new_state.apply(action)
            print(new_state.to_string() not in visited)
            if new_state.to_string() not in visited:
                queue.append(new_state)
                visited.add(new_state.to_string())
                actions[new_state.to_string()] = action
                distance[new_state.to_string()] = distance[state.to_string()] + 1
    
    return distance
        