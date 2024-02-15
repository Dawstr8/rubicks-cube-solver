import copy
import numpy as np

# 0 - white, 1 - red, 2 - blue, 3 - orange, 4 - green, 5 - yellow
#     000
#     000
#     000
# 444 111 222 333
# 444 111 222 333
# 444 111 222 333
#     555
#     555
#     555

# 0000(0)0000 1111(1)1111 2222(2)2222 3333(3)3333 4444(4)4444 5555(5)5555

N = 8 * 6

permutations = [
    'T', 'T2', 'Tp',
    'F', 'F2', 'Fp',
    'R', 'R2', 'Rp',
    'B', 'B2', 'Bp',
    'L', 'L2', 'Lp',
    'D', 'D2', 'Dp',
]

cycles = {
    'T': [
        [0, 2, 5, 0],
        [1, 4, 6, 3],
        [8, 32, 24, 16],
        [9, 33, 25, 17],
        [10, 34, 26, 18]
    ],
    'F': [
        [8, 10, 15, 13],
        [9, 12, 14, 11],
        [5, 16, 45, 39],
        [6, 19, 46, 36],
        [7, 21, 47, 34]
    ],
    'R': [
        [16, 18, 23, 21],
        [17, 20, 22, 19],
        [7, 24, 40, 15],
        [4, 27, 43, 12],
        [2, 29, 45, 10]
    ],
    'B': [
        [24, 26, 31, 29],
        [25, 28, 30, 27],
        [2, 32, 42, 23],
        [1, 35, 41, 20],
        [0, 37, 40, 18]
    ],
    'L': [
        [32, 34, 39, 27],
        [33, 36, 38, 35],
        [0, 8, 47, 31],
        [3, 11, 44, 28],
        [5, 13, 42, 26]
    ],
    'D': [
        [40, 42, 47, 45],
        [41, 44, 46, 43],
        [13, 21, 29, 37],
        [14, 22, 30, 38],
        [15, 23, 31, 39]
    ],
}

def cycles_to_matrix(cycles):
    identity = np.identity(N, dtype=np.int8)
    permutation = copy.deepcopy(identity)
    for cycle in cycles:
        for i in range(len(cycle)):
            permutation[:, cycle[i]] = identity[:, cycle[(i+1) % len(cycle)]]
        
    return permutation

permutations = {k: cycles_to_matrix(v) for k, v in cycles.items()}
solved_cube = [i for i in range(6) for j in range(8)]

# test purposes
new_cube = np.matmul(permutations['D'], solved_cube)
print(new_cube)