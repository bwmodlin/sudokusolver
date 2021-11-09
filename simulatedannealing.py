import random
from copy import deepcopy as dc
import numpy as np
import time

PROBLEM = [
    [1, 0, 0, 0, 0, 6, 3, 0, 8],
    [0, 0, 2, 3, 0, 0, 0, 9, 0],
    [0, 0, 0, 0, 0, 0, 7, 1, 6],

    [7, 0, 8, 9, 4, 0, 0, 0, 2],
    [0, 0, 4, 0, 0, 0, 9, 0, 0],
    [9, 0, 0, 0, 2, 5, 1, 0, 4],

    [6, 2, 9, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 7, 6, 0, 0],
    [5, 0, 7, 6, 0, 0, 0, 0, 3],
]
#problem = [([0]* 9)*9]


def get_cost(matrix):
    total_cost = 0
    rows_list = []
    column_list = []

    for i in range(len(matrix)):
        rows_list.append(matrix[i])

    for i in range(len(matrix[0])):
        column_list.append([matrix[j][i] for j in range(0, len(matrix))])

    def duplicate_count(array):
        already_used = {}
        array_cost = 0
        for num in array:
            if num == 0:
                continue
            elif num in already_used:
                array_cost += 1
            else:
                already_used[num] = True

        return array_cost

    for row in rows_list:
        total_cost += duplicate_count(row)

    for column in column_list:
        total_cost += duplicate_count(column)

    return total_cost


# only works for 9x9 at the moment
def set_initial_values(matrix):
    def remove_values(i, j):
        possible_values = {}
        for k in range(1, 10):
            possible_values[k] = True

        for l in range(3):
            for m in range(3):
                val = matrix[3 * i + l][3 * j + m]
                if val == 0:
                    continue
                elif possible_values[val]:
                    possible_values[val] = False

        return possible_values

    def set_values(i, j, possible_values):
        choice_array = [val for val in possible_values if possible_values[val]]
        for l in range(3):
            for m in range(3):
                val = matrix[3 * i + l][3 * j + m]
                if val == 0:
                    choice = random.randint(0, len(choice_array) - 1)
                    matrix[3 * i + l][3 * j + m] = choice_array[choice]
                    choice_array.pop(choice)

    for width in range(3):
        for height in range(3):
            set_values(width, height, remove_values(width, height))


def get_new_matrix(matrix, initial):
    try_matrix = dc(matrix)

    box_x = random.randint(0, 2)
    box_y = random.randint(0, 2)
    for i in range(3):
        for j in range(3):
            try_matrix[3 * box_x + i][3 * box_y + j] = initial[3 * box_x + i][3 * box_y + j]

    set_initial_values(try_matrix)
    return try_matrix


def run_annealing(matrix):
    initial = dc(matrix)
    set_initial_values(matrix)
    temperature = 4.2

    while True:
        try_case = get_new_matrix(matrix, initial)
        try_cost = get_cost(try_case)
        curr_cost = get_cost(matrix)

        delta_cost = try_cost - curr_cost
        if delta_cost < 0:
            print(try_cost)
            matrix = try_case
            if try_cost == 0:
                return matrix
            temperature *= 0.99
        else:
            chance = 1 / (1 + np.exp(delta_cost / temperature))
            #print(f"chance: {chance} temperature: {temperature}")
            if random.random() < chance:
                print(try_cost)
                matrix = try_case
                if try_cost == 0:
                    return matrix

                temperature *= 0.99


start_time = time.time()
print(run_annealing(dc(PROBLEM)))
print(time.time()-start_time)

def get_std(matrix):
    cost_list = []
    for i in range(1000):
        matrix_copy = dc(matrix)
        set_initial_values(matrix_copy)
        cost_list.append(get_cost(matrix_copy))

    return np.std(cost_list)

