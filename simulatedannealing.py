import random
from copy import deepcopy as dc
import numpy as np
import time
import math
import matplotlib.pyplot as plt
from backtracking import generate_sudoku_board
import statistics

PROBLEM = [[3, 5, 8, 4, 9, 0, 1, 7, 6], [2, 1, 7, 0, 0, 8, 4, 9, 3], [4, 9, 6, 0, 7, 1, 8, 5, 2],
           [0, 7, 0, 8, 2, 5, 0, 0, 4], [0, 3, 2, 0, 4, 0, 9, 8, 0], [8, 6, 0, 7, 3, 9, 0, 0, 5],
           [0, 8, 0, 5, 6, 4, 7, 2, 9], [7, 4, 9, 2, 8, 3, 5, 6, 1], [6, 2, 5, 9, 1, 7, 3, 4, 8]]

allzeros = np.zeros((25, 25)).tolist()

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


def switch_element(matrix, initial):
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


def run_annealing(matrix, tempset=0.1):
    temperature = get_std(matrix)
    initial = dc(matrix)
    set_initial_values(matrix)
    initial_temp = temperature
    initial_tempset = tempset

    stuck = 0

    if get_cost(matrix) == 0 and no_zeros(matrix):
        return matrix

    while True:
        if stuck > (10000 / 9) * len(matrix[0]):
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


def print_board(matrix):
    rows_list = []
    for i in range(len(matrix)):
        rows_list.append(matrix[i])

    for row in range(0, len(rows_list)):

        for column in range(0, len(rows_list[row])):
            if column % (int(math.sqrt(len(matrix))) + 1) == 0:
                rows_list[row].insert(column, '|')

    for i in range(len(rows_list)):
        if i % int(math.sqrt(len(matrix))) == 0:
            print("-------------------------------------")
        # if i == int(math.sqrt(len(matrix))) * 2:
        #     print("-------------------------------------")
        print(rows_list[i])


def percent_test():
    percent = []
    times = []
    for i in range(1, 99, 2):

        current_times = []
        for j in range(10):
            board = generate_sudoku_board(9, i)
            start_time = time.time()
            run_annealing(board, 0.1)
            current_times.append(time.time() - start_time)

        times.append(statistics.median(current_times))
        percent.append(i)
        print(i)

    plt.xlabel("Percent Starting as Zero")
    plt.ylabel("Median Time to Solve (s)")
    plt.title("Simulated Annealing 9x9 Board Solve Times by Filled Percent")
    plt.plot(percent, times)
    plt.show()


def size_test():
    # 4x4
    four_trials = []
    for i in range(10):
        PROBLEM = generate_sudoku_board(4, 30)
        start = time.time()
        run_annealing(PROBLEM)
        end = time.time()
        four_trials.append(end - start)
        print(i, "four")

    four_by_four = statistics.median(four_trials)

    # 9x9
    nine_trials = []
    for i in range(10):
        PROBLEM = generate_sudoku_board(9, 30)
        start = time.time()
        run_annealing(PROBLEM)
        end = time.time()
        nine_trials.append(end - start)
        print(i, "nine")

    nine_by_nine = statistics.median(nine_trials)

    # 16x16
    sixteen_trials = []
    for i in range(10):
        PROBLEM = generate_sudoku_board(16, 30)
        start = time.time()
        run_annealing(PROBLEM)
        end = time.time()
        sixteen_trials.append(end - start)
        print(i, "sixteen")

    sixteen_by_sixteen = statistics.median(sixteen_trials)

    labels = ["4x4", "9x9", "16x16"]
    values = [four_by_four, nine_by_nine, sixteen_by_sixteen]

    plt.bar(labels, values)
    plt.ylabel("Time (s)")
    plt.title("Simulated Annealing Performance for Different Board Sizes at 30 Percent Unfilled")
    plt.show()

def runTime():
    times = []
    for i in range(1, 99):

        board = generate_sudoku_board(9, 30)
        start_time = time.time()
        run_annealing(board, 0.1)
        times.append(time.time() - start_time)

        print(i)

    plt.ylabel("Time (s)")
    plt.title("Cases for Simulated Annealing Solving 9x9 Boards 30 Percent Unfilled")
    plt.bar(["Best Case", "Average Case", "Worst Case"], [min(times), sum(times)/len(times), max(times)])
    plt.show()

size_test()