# Backtracking Algorithm

# Works by going cell by cell and checking which number can go in
# Once number is placed, call that same function again recursively, if it turns out that there are no options
# for the next cell, it means that the previous cell was wrong, so we revert back and start over on the next iteration

# size of board
# how many clues we have in a 9x9 grid
import random
from utilities import is_possible
import sys
import pygame as pg


# Solves a sudoku board of size n x n, NOTE: n should be a perfect square
def backtracking_solve(board, display=False, game=None):
    row = None
    col = None

    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                row = r
                col = c

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
        game.board = board
        game.new_board(row=row, col=col)

    # If no empty spots were found, we are done and return True:
    if row is None and col is None:
        return True

    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(choices)

    for x in range(1, len(board) + 1):

        num = choices.pop()

        if is_possible(board, row, col, num):
            board[row][col] = num

            # Recursively call the solve function again
            if backtracking_solve(board, display=display, game=game):
                return True

            # If returned false, then the choice was wrong, reset
            board[row][col] = 0

    # Backtrack
    return False
