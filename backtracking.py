# Backtracking Algorithm

# Works by going cell by cell and checking which number can go in
# Once number is placed, call that same function again recursively, if it turns out that there are no options
# for the next cell, it means that the previous cell was wrong, so we revert back and start over on the next iteration

# size of board
# how many clues we have in a 9x9 grid

import math
import copy
import random
import time
import matplotlib.pyplot as plt
import statistics

# Helper function to check if a number can be placed at board[row][col]
def is_possible(board, row, col, num):
    # If possible vertically
    for i in range(len(board)):
        if board[row][i] == num:
            return False
    # If possible horizontally
    for i in range(len(board)):
        if board[i][col] == num:
            return False
    # If possible in the square
    for i in range(0, int(math.sqrt(len(board)))):
        for j in range(0, int(math.sqrt(len(board)))):
            if board[((row // int(math.sqrt(len(board)))) * int(math.sqrt(len(board)))) + i][
                ((col // int(math.sqrt(len(board)))) * int(math.sqrt(len(board)))) + j] == num:
                return False
    return True


# Solves a sudoku board of size n x n, NOTE: n should be a perfect square
def backtracking_solve(board):
    row = None
    col = None

    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                row = r
                col = c

    # If no empty spots were found, we are done and return True:
    if row is None and col is None:
        return True

    for num in range(1, len(board) + 1):

        if is_possible(board, row, col, num):
            board[row][col] = num

            # Recursively call the solve function again
            if backtracking_solve(board):
                return True

            # If returned false, then the choice was wrong, reset
            board[row][col] = 0

    # Backtrack
    return False


# prints a matrix of size n x n where n is a perfect square
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
        print(rows_list[i])

# Generates a sudoku board of size n x n,
# p is the percentage of cells that we want to set to 0
# Example: If p = 50, a 9x9 grid with 81 cells would have ~41 random cells (50%) set to 0
# NOTE: n should be a perfect square
def generate_sudoku_board(n, p):
    # Recursive solver
    def _generate(board):
        row = None
        col = None

        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == 0:
                    row = r
                    col = c

        # If no empty spots were found, we are done and return True:
        if row is None and col is None:
            return True

        buffer = {}

        for x in range(1, len(board) + 1):

            num = None
            while True:
                num = random.randint(1, len(board))
                if num not in buffer:
                    buffer[num] = "used"
                    break

            if is_possible(board, row, col, num):
                board[row][col] = num

                # Recursively call the solve function again
                if _generate(board):
                    return True

                # If returned false, then the choice was wrong, reset
                board[row][col] = 0

        # Backtrack
        return False

    matrix = []

    for i in range(0, n):
        matrix.append([])
        for j in range(0, n):
            matrix[i].append(0)

    if _generate(matrix):

        # Making a percentage of the board to be 0
        cells_buffer = {}
        number_of_cells = math.ceil((n * n) * (p / 100))

        for i in range(0, number_of_cells):

            rand_row = None
            rand_col = None

            while True:
                rand_row = random.randint(0, n - 1)
                rand_col = random.randint(0, n - 1)
                if (rand_row, rand_col) not in cells_buffer:
                    cells_buffer[(rand_row, rand_col)] = "used"
                    matrix[rand_row][rand_col] = 0
                    break

        return matrix


# Test 1: Constant board size but changing the number of clues
# We will generate a 9x9 board and incrementing the percentage of blank cells on the board
def percentage_test():
    backtracking_runtime = []
    percentage_of_empty = []

    # 1% to 99%
    for percentage in range(1, 100, 2):

        percentage_of_empty.append(percentage)
        y = []

        # 10 trials at each percent
        for i in range(10):
            print(percentage)
            PROBLEM = generate_sudoku_board(9, percentage)

            start = time.time()
            backtracking_solve(PROBLEM)
            end = time.time()

            y.append(end - start)

        # Taking the average of the ten trials
        backtracking_runtime.append(statistics.median(y))

    plt.plot(percentage_of_empty, backtracking_runtime)
    plt.xlabel("Percentage Of Board That Are Empty Cells")
    plt.ylabel("Solve Time (seconds)")
    plt.title("Backtracking Runtime vs. Percentage Of Board That Are Empty Cells")
    plt.show()

# Test 2: Constant percentage of blanks on the board but changing the board size
# We will generate 4x4, 9x9, and 16x16 boards with a constant 40% being empty
def board_size_test():
    # 4x4
    four_trials = []
    for i in range(10):
        PROBLEM = generate_sudoku_board(4, 30)
        start = time.time()
        backtracking_solve(PROBLEM)
        end = time.time()
        four_trials.append(end - start)
        print(i, "four")

    four_by_four = statistics.median(four_trials)

    # 9x9
    nine_trials = []
    for i in range(10):
        PROBLEM = generate_sudoku_board(9, 30)
        start = time.time()
        backtracking_solve(PROBLEM)
        end = time.time()
        nine_trials.append(end - start)
        print(i, "nine")

    nine_by_nine = statistics.median(nine_trials)

    # 16x16
    sixteen_trials = []
    for i in range(10):
        PROBLEM = generate_sudoku_board(16, 30)
        start = time.time()
        backtracking_solve(PROBLEM)
        end = time.time()
        sixteen_trials.append(end - start)
        print(i, "sixteen")

    sixteen_by_sixteen = statistics.median(sixteen_trials)

    labels = ["4x4", "9x9", "16x16"]
    values = [four_by_four, nine_by_nine, sixteen_by_sixteen]

    plt.bar(labels, values)
    plt.ylabel("Time (s)")
    plt.title("Backtracking Performance for Different Board Sizes at 30 Percent Unfilled")
    plt.show()

# Test 3, tests the best, average, and worst cases using 9x9 boards
def runTime():
    times = []
    for i in range(1, 99):

        PROBLEM = generate_sudoku_board(9, 30)
        start_time = time.time()
        backtracking_solve(PROBLEM)
        times.append(time.time() - start_time)

        print(i)

    plt.ylabel("Time (s)")
    plt.title("Cases for Backtracking Solving 9x9 Boards 30 Percent Unfilled")
    plt.bar(["Best Case", "Average Case", "Worst Case"], [min(times), sum(times)/len(times), max(times)])
    plt.show()

board_size_test()




