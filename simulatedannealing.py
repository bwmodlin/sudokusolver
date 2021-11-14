import random
from copy import deepcopy as dc
import numpy as np
import math

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
        for k in range(1, side + 1):
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


def switch_element(matrix, initial, display=False):
    side = len(matrix[0])
    sqrt = int(math.sqrt(side))

    try_matrix = dc(matrix)
    box_x = 0
    box_y = 0
    while (True):
        box_x = random.randint(0, sqrt - 1)
        box_y = random.randint(0, sqrt - 1)

        possible_switch = 0
        for i in range(sqrt):
            for j in range(sqrt):
                if initial[sqrt * box_x + i][sqrt * box_y + j] == 0:
                    possible_switch += 1
        if possible_switch >= 2:
            break

    while (True):
        first_x = sqrt * box_x + random.randint(0, sqrt - 1)
        first_y = sqrt * box_y + random.randint(0, sqrt - 1)
        second_x = sqrt * box_x + random.randint(0, sqrt - 1)
        second_y = sqrt * box_y + random.randint(0, sqrt - 1)

        if initial[first_x][first_y] == 0 and initial[second_x][second_y] == 0:
            store_first = try_matrix[first_x][first_y]
            try_matrix[first_x][first_y] = try_matrix[second_x][second_y]
            try_matrix[second_x][second_y] = store_first

            if display:
                return (try_matrix, first_x, first_y, second_x, second_y)
            break
        else:
            continue

    return try_matrix


def no_zeros(matrix):
    nozeros = True
    for i in range(len(matrix)):
        if 0 in matrix[i]:
            nozeros = False

    return nozeros


def run_annealing(matrix, tempset=0.1, display=False, game = None):
    temperature = get_std(matrix)
    initial = dc(matrix)
    set_initial_values(matrix)
    initial_temp = temperature
    initial_tempset = tempset

    first_x = 0
    first_y = 0
    second_x = 0
    second_y = 0

    stuck = 0

    if get_cost(matrix) == 0 and no_zeros(matrix):
        return matrix

    while True:
        if display:
            game.board = matrix
            game.new_board(row=(first_x, first_y), col=(second_x, second_y), annealing=True)

        if stuck > (10000 / 9) * len(matrix[0]):
            temperature = tempset
            if temperature > initial_temp:
                temperature = initial_temp
                tempset = initial_tempset
            stuck = 0
            if tempset < 2:
                tempset *= 2.0
        if display:
            try_case, first_x, first_y, second_x, second_y = switch_element(matrix, initial, display=True)
        else:
            try_case = switch_element(matrix, initial)
        try_cost = get_cost(try_case)
        curr_cost = get_cost(matrix)

        delta_cost = try_cost - curr_cost

        if delta_cost <= 0:
            if delta_cost == 0:
                stuck += 1
            else:
                stuck = 0
            # print(try_cost)
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
                # print(try_cost)
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

