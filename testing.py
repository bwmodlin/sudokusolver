from backtracking import backtracking_solve
from simulatedannealing import run_annealing
from utilities import generate_sudoku_board, get_possibilities
from copy import deepcopy as dc
import statistics
import time
import matplotlib.pyplot as plt

# runs a test on different sizes of matrices
def size_test():
    # 4x4
    four_trials = []
    four_trials2 = []
    for i in range(30):
        board = generate_sudoku_board(4, 30)
        start = time.time()
        run_annealing(dc(board))
        end = time.time()
        four_trials.append(end - start)

        start = time.time()
        backtracking_solve(dc(board))
        end = time.time()
        four_trials2.append(end - start)
        print(i, "four")

    four_by_four = statistics.mean(four_trials)
    four_by_four2 = statistics.mean(four_trials2)

    # 9x9
    nine_trials = []
    nine_trials2 = []
    for i in range(30):
        board = generate_sudoku_board(9, 30)
        start = time.time()
        run_annealing(dc(board))
        end = time.time()
        nine_trials.append(end - start)

        start = time.time()
        backtracking_solve(dc(board))
        end = time.time()
        nine_trials2.append(end - start)

        print(i, "nine")

    nine_by_nine = statistics.mean(nine_trials)
    nine_by_nine2 = statistics.mean(nine_trials2)

    # 16x16
    sixteen_trials = []
    sixteen_trials2 = []
    for i in range(10):
        board = generate_sudoku_board(16, 30)
        start = time.time()
        run_annealing(dc(board))
        end = time.time()
        sixteen_trials.append(end - start)

        start = time.time()
        backtracking_solve(dc(board))
        end = time.time()
        sixteen_trials2.append(end - start)
        print(i, "sixteen")

    sixteen_by_sixteen = statistics.mean(sixteen_trials)
    sixteen_by_sixteen2 = statistics.mean(sixteen_trials2)

    labels = ["4x4 Annealing", "9x9 Annealing", "16x16 Annealing"]
    values = [four_by_four, nine_by_nine, sixteen_by_sixteen]

    labels2 = ["4x4 Backtracking", "9x9 Backtracking", "16x16 Backtracking"]
    values2 = [four_by_four2, nine_by_nine2, sixteen_by_sixteen2]

    plt.bar(labels, values)
    plt.bar(labels2, values2)
    plt.ylabel("Time (s)")
    plt.yscale('log')
    plt.title("Performance for Different Board Sizes at 30 Percent Unfilled")
    plt.show()


# finds the best, average,and case for each algorithm on 9x9 30 percent filled boards
def runTime():
    times = []
    times2 = []
    for i in range(1, 100):

        board = generate_sudoku_board(9, 30)
        start_time = time.time()
        run_annealing(dc(board), 0.1)
        times.append(time.time() - start_time)

        start_time = time.time()
        backtracking_solve(dc(board))
        times2.append(time.time() - start_time)

        print(i)

    plt.ylabel("Time (s)")
    plt.title("Cases for Solving 9x9 Boards 30 Percent Unfilled")
    plt.bar(["Annealing Best", "Annealing Average", "Annealing Worst"], [min(times), sum(times)/len(times), max(times)])
    plt.bar(["Backtracking Best", "Backtracking Average", "Backtracking Worst"], [min(times2), sum(times2) / len(times2), max(times2)])
    plt.yscale('log')
    plt.show()


# tracks the performance of an algorithm based on the possibilities to fill in the board (increments by percent filled)
def percent_test(type):
    percent = []
    times = []
    for i in range(1, 100, 2):
        time_list = []
        board = generate_sudoku_board(9, i)
        percent.append(get_possibilities(board))
        for j in range(50):
            print("j", j)
            myboard = dc(board)
            if type == "annealing":
                start_time = time.time()
                run_annealing(dc(myboard), 0.1)
                time_list.append(time.time() - start_time)
            elif type == "backtracking":
                start_time = time.time()
                backtracking_solve(dc(myboard))
                time_list.append(time.time() - start_time)
        times.append(statistics.mean(time_list))
        print(i)

    plt.xlabel("Number of Board Possibilities")
    plt.ylabel("Mean Time to Solve (s)")
    plt.title(f"{type.title()} 9x9 Board Solve Times by Board Possibilities")
    plt.semilogx(percent, times, ".")
    plt.show()
