import copy
import numpy as np
from numpy.linalg import matrix_power
import random

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

possible_actions = [
    'T', 'T2', 'Tp',
    'F', 'F2', 'Fp',
    'R', 'R2', 'Rp',
    'B', 'B2', 'Bp',
    'L', 'L2', 'Lp',
    'D', 'D2', 'Dp',
]

cycles = {
    'T': [
        [0, 2, 7, 5],
        [1, 4, 6, 3],
        [8, 32, 24, 16],
        [9, 33, 25, 17],
        [10, 34, 26, 18]
    ],
    'F': [
        [8, 10, 15, 13],
        [9, 12, 14, 11],
        [5, 16, 42, 39],
        [6, 19, 41, 36],
        [7, 21, 40, 34]
    ],
    'R': [
        [16, 18, 23, 21],
        [17, 20, 22, 19],
        [7, 24, 47, 15],
        [4, 27, 44, 12],
        [2, 29, 42, 10]
    ],
    'B': [
        [24, 26, 31, 29],
        [25, 28, 30, 27],
        [2, 32, 45, 23],
        [1, 35, 46, 20],
        [0, 37, 47, 18]
    ],
    'L': [
        [32, 34, 39, 37],
        [33, 36, 38, 35],
        [0, 8, 40, 31],
        [3, 11, 43, 28],
        [5, 13, 45, 26]
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

permutations = {}
for action in possible_actions:
    permutation = cycles_to_matrix(cycles[action[0]])
    times = 0
    if len(action) == 1:
        times = 1
    elif action[1] == '2':
        times = 2
    else:
        times = 3

    permutations[action] = matrix_power(permutation, times)

class Cube:
    def __init__(self):
        self.state = np.array([i for i in range(6) for j in range(8)])
        self.last_action = None
        self.path_len = 0

    def __str__(self):
        to_string = ''
        for elem in self.state:
            to_string += str(elem)
        return to_string

    def __lt__(self, other):
        return self.path_len < other.path_len
    
    def __eq__(self, other):
        return str(self) == str(other)

    def draw(self):
        cube = self.state
        face_center_id = 4
        # first face
        for i in range(9):
            after_center = -1 if i > face_center_id else 0
            if i == face_center_id:
                print(0, end="")
            else:
                print(cube[i + after_center], end="")

            # new line after 3, 6, 9 iterations
            if (i + 1) % 3 == 0:
                print('')

        second_face_id = 1

        # print first row
        for i in range(4):
            current_face_id = second_face_id + i
            for j in range(3):
                print(cube[current_face_id * 8 + j], end="")
            print(' ', end="")

        print('')

        # print second row
        for i in range(4):
            current_face_id = second_face_id + i
            # second row consists of 3rd block of face, center and 4th block
            print(cube[current_face_id * 8 + 3], end="")
            print(current_face_id, end="")
            print(cube[current_face_id * 8 + 4], end="")
            print(' ', end="")

        print('')

        # print third row
        for i in range(4):
            current_face_id = second_face_id + i
            # third row starts at 5th block of face
            for j in range(3):
                print(cube[current_face_id * 8 + j + 5], end="")
            print(' ', end="")

        print('')

        # last face
        last_face_id = 5
        for i in range(9):
            after_center = -1 if i > face_center_id else 0
            if i == face_center_id:
                print(last_face_id, end="")
            else:
                print(cube[last_face_id * 8 + i + after_center], end="")

            # new line after 3, 6, 9 iterations
            if (i + 1) % 3 == 0:
                print('')

        print('')

    def apply(self, action):
        permutation = permutations[action]
        self.state = np.matmul(permutation, self.state)
        self.last_action = action
        self.path_len += 1

    def shuffle(self, n=100):
        random_actions_seq = np.random.choice(self.possible_actions(), size=n, replace=True)
        print('shuffle', random_actions_seq)
        for random_action in random_actions_seq:
            self.apply(random_action)
        self.path_len = 0

    def possible_actions(self):
        if self.last_action is None:
            return possible_actions
        
        return [x for x in possible_actions if x[0] != self.last_action[0]]