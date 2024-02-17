from collections import deque
import copy
import time

def BFS(start, end, max_depth=10):
    start_time = time.time()
    queue = deque([start])
    actions_sequence = {}
    actions_sequence[start.to_string()] = []

    current_distance = 0
    while queue:
        state = queue.popleft()

        state_actions_sequence = len(actions_sequence[state.to_string()])
        if state_actions_sequence > current_distance:
            current_distance += 1
            print(time.time() - start_time, current_distance)

        if state_actions_sequence > max_depth or state.to_string() == end.to_string():
            print(time.time() - start_time)
            return actions_sequence[end.to_string()]

        for action in state.possible_actions():
            new_state = copy.deepcopy(state)
            new_state.apply(action)
            if new_state.to_string() not in actions_sequence:
                previous_state_actions_sequence = copy.deepcopy(actions_sequence[state.to_string()])
                previous_state_actions_sequence.append(action)
                actions_sequence[new_state.to_string()] = previous_state_actions_sequence
                queue.append(new_state)
    
    return []