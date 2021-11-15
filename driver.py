from utilities import generate_sudoku_board, print_board
from simulatedannealing import run_annealing
from backtracking import backtracking_solve
from game import game

# This is the driver script. The main purpose of it is to run the GUI, but it can be used to run any of our codebase.
# (This is the file you should run)
if __name__ == "__main__":
    # creates a random 9x9 board with 40 zeros
    board = generate_sudoku_board(9, 40)

    # Uncomment next line to run an annealing GUI game
    game(type="backtracking", board=board)

    # Uncomment next line to solve the board (with annealing) and print out the results to the terminal
    #print_board(run_annealing(board))



