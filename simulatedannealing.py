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


# deprecated. Worse way to do case generation
def get_new_matrix(matrix, initial):
    try_matrix = dc(matrix)

    box_x = random.randint(0, 2)
    box_y = random.randint(0, 2)
    for i in range(3):
        for j in range(3):
            try_matrix[3 * box_x + i][3 * box_y + j] = initial[3 * box_x + i][3 * box_y + j]

    set_initial_values(try_matrix)
    return try_matrix


def switch_element(matrix, initial):
    try_matrix = dc(matrix)
    box_x = random.randint(0, 2)
    box_y = random.randint(0, 2)
    while (True):
        first_x = 3 * box_x + random.randint(0, 2)
        first_y = 3 * box_y + random.randint(0, 2)
        second_x = 3 * box_x + random.randint(0, 2)
        second_y = 3 * box_y + random.randint(0, 2)

        if initial[first_x][first_y] == 0 and initial[second_x][second_y] == 0:
            store_first = try_matrix[first_x][first_y]
            try_matrix[first_x][first_y] = try_matrix[second_x][second_y]
            try_matrix[second_x][second_y] = store_first
            break
        else:
            continue

    return try_matrix


def run_annealing(matrix, tempset):
    initial = dc(matrix)
    set_initial_values(matrix)
    temperature = 4.2
    stuck = 0

    while True:
        if stuck > 5000:
            temperature = tempset

        try_case = switch_element(matrix, initial)
        try_cost = get_cost(try_case)
        curr_cost = get_cost(matrix)

        delta_cost = try_cost - curr_cost

        if delta_cost <= 0:
            if delta_cost == 0:
                stuck += 1
            else:
                stuck = 0
            print(try_cost)
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

                print(try_cost)
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


def run_test(n):
    times5 = []
    for i in range(n):
        start_time = time.time()
        run_annealing(dc(PROBLEM), 0.5)
        times5.append(time.time() - start_time)

    times10 = []
    for i in range(n):
        start_time = time.time()
        run_annealing(dc(PROBLEM), 1.0)
        times10.append(time.time() - start_time)

    times20 = []
    for i in range(n):
        start_time = time.time()
        run_annealing(dc(PROBLEM), 2.0)
        times20.append(time.time() - start_time)

    print(f"0.5 Average: {sum(times5) / len(times5)}")
    print(f"1.0 Average: {sum(times10) / len(times10)}")
    print(f"2.0 Average: {sum(times20) / len(times20)}")


start_time = time.time()
print_board(run_annealing(PROBLEM, 1.0))
print(time.time() - start_time)
