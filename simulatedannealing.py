import random
from copy import deepcopy as dc
import numpy as np
import math
import pygame as pg
import sys


# gets the cost of a specific matrix. Counts the duplicates in the columns and rows (the boxes by definition have no duplicates)
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


# sets all the zeros to random values (that are not duplicates inside each box)
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


# switches two random elements in the same box
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

        if initial[first_x][first_y] == 0 and initial[second_x][second_y] == 0 and (first_x, first_y) != (
                second_x, second_y):
            store_first = try_matrix[first_x][first_y]
            try_matrix[first_x][first_y] = try_matrix[second_x][second_y]
            try_matrix[second_x][second_y] = store_first

            if display:
                return try_matrix, first_x, first_y, second_x, second_y
            break
        else:
            continue

    return try_matrix


# determines if any zeros exist in a matrix
def no_zeros(matrix):
    nozeros = True
    for i in range(len(matrix)):
        if 0 in matrix[i]:
            nozeros = False

    return nozeros


# runs the annealing experiment
def run_annealing(matrix, tempset=0.1, display=False, game=None):
    temperature = get_std(matrix)  # sets the initial temperature to the standard deviation of the cost
    initial = dc(matrix)  # remembers the initial state so we don't switch the initial clues
    set_initial_values(matrix)  # sets the zeros to random values
    initial_temp = temperature
    initial_tempset = tempset

    first_x, first_y, second_x, second_y = None, None, None, None

    # Keeps track of how long algorithm is stuck so we can increase the temperature if needed
    stuck = 0

    if get_cost(matrix) == 0 and no_zeros(matrix):
        return matrix

    while True:
        # a bunch of event handlers for the GUI. Ignore if grading the algorithm
        if display:
            for event in pg.event.get():
                if event.type == pg.QUIT: sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    start = False
                    while not start:
                        for e in pg.event.get():
                            if e.type == pg.QUIT: sys.exit()
                            if e.type == pg.MOUSEBUTTONDOWN:
                                start = True
                            if e.type == pg.KEYDOWN:
                                if e.key == pg.K_ESCAPE or e.key == pg.K_q:
                                    sys.exit(0)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                        sys.exit(0)

            game.board = matrix
            game.new_board(row=(first_x, second_x), col=(first_y, second_y), annealing=True)
            try_case, first_x, first_y, second_x, second_y = switch_element(matrix, initial, display=True)
        else:
            # None gui part
            try_case = switch_element(matrix, initial)

        if stuck > (10000 / 9) * len(matrix[0]):
            temperature = tempset
            if temperature > initial_temp:
                temperature = initial_temp
                tempset = initial_tempset
            stuck = 0
            if tempset < 2:  # we don't want the temperature getting to high or it will never think long enough
                tempset *= 2.0
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
            # equation to get the chance based on the delta cost
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


# gets the standard deviation of the cost of the matrix to set the temperature
def get_std(matrix):
    cost_list = []
    for i in range(1000):
        matrix_copy = dc(matrix)
        set_initial_values(matrix_copy)
        cost_list.append(get_cost(matrix_copy))

    return np.std(cost_list)
