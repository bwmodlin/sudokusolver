import random
from copy import deepcopy as dc
import numpy as np
import time
import math

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

hard = [
    [0, 6, 0, 0, 0, 0, 0, 1, 0],
    [0, 5, 0, 0, 3, 0, 0, 7, 0],
    [0, 2, 0, 5, 6, 0, 4, 0, 0],
    [0, 0, 8, 0, 4, 0, 0, 9, 0],
    [0, 0, 3, 0, 0, 9, 1, 0, 0],
    [0, 0, 0, 1, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 9, 0, 0, 0, 2],
    [0, 0, 7, 0, 5, 0, 0, 4, 0]
]

problem2 = np.zeros((9, 9)).tolist()


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
    side = len(matrix[0])
    sqrt = int(math.sqrt(side))
    def remove_values(i, j):
        possible_values = {}
        for k in range(1, side+1):
            possible_values[k] = True

        for l in range(sqrt):
            for m in range(sqrt):
                val = matrix[sqrt * i + l][sqrt * j + m]
                if val == 0:
                    continue
                elif possible_values[val]:
                    possible_values[val] = False

        return possible_values

    def set_values(i, j, possible_values):
        choice_array = [val for val in possible_values if possible_values[val]]
        for l in range(sqrt):
            for m in range(sqrt):
                val = matrix[sqrt * i + l][sqrt * j + m]
                if val == 0:
                    choice = random.randint(0, len(choice_array) - 1)
                    matrix[sqrt * i + l][sqrt * j + m] = choice_array[choice]
                    choice_array.pop(choice)

    for width in range(sqrt):
        for height in range(sqrt):
            set_values(width, height, remove_values(width, height))


def switch_element(matrix, initial):
    side = len(matrix[0])
    sqrt = int(math.sqrt(side))

    try_matrix = dc(matrix)
    box_x = random.randint(0, sqrt-1)
    box_y = random.randint(0, sqrt-1)
    while (True):
        first_x = sqrt * box_x + random.randint(0, sqrt-1)
        first_y = sqrt * box_y + random.randint(0, sqrt-1)
        second_x = sqrt * box_x + random.randint(0, sqrt-1)
        second_y = sqrt * box_y + random.randint(0, sqrt-1)

        if initial[first_x][first_y] == 0 and initial[second_x][second_y] == 0:
            store_first = try_matrix[first_x][first_y]
            try_matrix[first_x][first_y] = try_matrix[second_x][second_y]
            try_matrix[second_x][second_y] = store_first
            break
        else:
            continue

    return try_matrix


def run_annealing(matrix, tempset = 0.1):
    temperature = get_std(matrix)
    initial = dc(matrix)
    set_initial_values(matrix)
    initial_temp = temperature
    initial_tempset = tempset

    stuck = 0

    while True:
        if stuck > 5000:
            temperature = tempset
            if temperature > initial_temp:
                temperature = initial_temp
                tempset = initial_tempset
            stuck = 0
            if tempset < 2:
                tempset *= 2.0

        try_case = switch_element(matrix, initial)
        try_cost = get_cost(try_case)
        curr_cost = get_cost(matrix)

        delta_cost = try_cost - curr_cost

        if delta_cost <= 0:
            if delta_cost == 0:
                stuck += 1
            else:
                stuck = 0

            matrix = try_case
            if try_cost == 0:
                return matrix
            temperature *= 0.999
        else:
            chance = 1 / (1 + np.exp(delta_cost / temperature))

            if random.random() < chance:
                if delta_cost == 0:
                    stuck += 1
                else:
                    stuck = 0

                matrix = try_case
                if try_cost == 0:
                    return matrix
                temperature *= 0.999
            else:
                stuck += 1


def get_std(matrix):
    cost_list = []
    for i in range(1000):
        matrix_copy = dc(matrix)
        set_initial_values(matrix_copy)
        cost_list.append(get_cost(matrix_copy))

    return np.std(cost_list)


def print_board(matrix):
    rows_list = []
    for i in range(len(matrix)):
        rows_list.append(matrix[i])

    for row in rows_list:
        row.insert(3, '|')
        row.insert(7, '|')
    for i in range(len(rows_list)):
        if i == 3:
            print("-------------------------------------")
        if i == 6:
            print("-------------------------------------")
        print(rows_list[i])


def test(n, matrix):
    times = []
    for i in range(n):
        start_time = time.time()
        run_annealing(dc(matrix), 0.1)
        total_time = time.time() - start_time
        print(f"Trial {i+1}: {total_time}")
        times.append(total_time)

    print(f"Average Time: {sum(times)/len(times)}")

def one_test():
    start_time = time.time()
    print_board(run_annealing(dc(hard), 0.1))
    print(time.time() - start_time)

test(10, PROBLEM)


