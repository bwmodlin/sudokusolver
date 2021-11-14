from utilities import generate_sudoku_board
from game import game

if __name__ == "__main__":
    board = generate_sudoku_board(9, 100)
    game(type="annealing", board=board)
