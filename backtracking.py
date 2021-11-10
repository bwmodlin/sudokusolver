# Backtracking Algorithm

# Works by going cell by cell and checking which number can go in
# Once number is placed, call that same function again recursively, if it turns out that there are no options
# for the next cell, it means that the previous cell was wrong, so we revert back and start over on the next iteration

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


def is_possible(board, row, col, num):
    # If possible vertically
    for i in range(9):
        if (board[row][i] == num):
            return False
    # If possible horizontally
    for i in range(9):
        if board[i][col] == num:
            return False
    # If possible in the square
    for i in range(0, 3):
        for j in range(0, 3):
            if board[((row // 3) * 3) + i][((col // 3) * 3) + j] == num:
                return False
    return True


def solve_the_game(board):
    row = None
    col = None

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                row = r
                col = c

    # If no empty spots were found, we are done and return True:
    if row is None and col is None:
        return True

    for num in range(1, 10):

        if is_possible(board, row, col, num):
            board[row][col] = num

            # Recursively call the solve function again
            if solve_the_game(board):
                return True

            # If returned false, then the choice was wrong, reset
            board[row][col] = 0

    # Backtrack
    return False


if solve_the_game(PROBLEM):
    print_board(PROBLEM)
else:
    print("No Solution")
