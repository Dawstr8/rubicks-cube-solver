def simple_heuristic(s1, s2):
    distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1
    
    return distance / 12.0