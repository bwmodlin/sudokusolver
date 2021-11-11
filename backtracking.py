# Backtracking Algorithm

# Works by going cell by cell and checking which number can go in
# Once number is placed, call that same function again recursively, if it turns out that there are no options
# for the next cell, it means that the previous cell was wrong, so we revert back and start over on the next iteration

# size of board
# how many clues we have in a 9x9 grid

import math
import copy
import random




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
def solve_the_game(board):
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
            if solve_the_game(board):
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


PROBLEM = generate_sudoku_board(9, 1)
print("UNSOLVED:")
print_board(copy.deepcopy(PROBLEM))

if solve_the_game(PROBLEM):
    print("")
    print("SOLVED:")
    print_board(PROBLEM)
else:
    print("No Solution")
