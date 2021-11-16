# Sudoku Solver


## Intentions: 

Sudoku is a popular logic-based number puzzle game. Given a 9x9 grid, the objective is to fill the grid with digits so that each row, each column, and each of the nine 3×3 subgrids or "squares" contain all of the digits from 1 to 9. For our project, we were particularly interested in the idea of how a computer would solve this game.  

Using the two most common algorithms for solving Sudoku, backtracking and simulated annealing, we implemented both and ran a number of experiments to test performance, efficiency, and how they would scale with board sizes other than 9x9.  

Additionally, we also developed a simiple visualizer GUI to simulate the solving process of each algorithm.

## Overview

Our project can be split up into two components, the testing experiments and the GUI. ```backtracking.py``` and ```simulatedannealing.py``` contain the implementation of the corresponding algorithm. ```utilities.py``` contains helper functions used throughout other files such as generating random Sudoku boards or printing matrices in the terminal. ```testing.py``` is where all the experiments and data collections were performed. ```game.py``` contains the GUI implementation and ```driver.py``` starts the visualization.  

A ```requirements.txt``` is provided for required import installations. You can also manually install the libraries yourself since there are only three: matplotlib, numpy, and pygame.

## Our Algorithms

### Backtracking

Backtracking is considered a brute force method and utilizes depth-first search. In other words, it completely explores one branch to a possible solution first before moving on to another branch. Here are the basic steps taken for backtracking:  
1. Find an empty cell. In the case of our implementation, we chose to start from the bottom of the board and work our way up
2. Check to see if it is possible for a number from 1-9 to be placed in that cell according to Sudoku rules
3. If so, the number is placed in the cell and the algorithm proceeds to the next empty cell with the same process
4. If none of the 9 numbers are valid to be placed in a cell during the execution, the cell is left blank and the “backtracking” step occurs and reverts back to the previous cell and chooses a different number from 1-9  

Essentially, backtracking tests out every potentially possible solution.


### Simulated Annealing

Simulated Annealing is a form of stochastic searching algorithm. It attempts to find the minima based on predefined 'cost' function. In the case of Sudoku, we can define cost as the number of duplicates in the rows, columns, and boxes. In our implementation of simulated annealing, we replaced the initially empty cells with numbers that could not be duplicates in any of the boxes. Therefore, we only needed to check for duplicates in the rows and columns.

To find a new candidate 'state' at a different spot in the cost function, we switched two random cells in a random box. We then calculated the cost of the new state. The probability to accept the new state was given by (1 / 1 + e<sup>delta cost - T</sup>). The T in this equation is the 'temperature' the annealing is at. The temperature determines how likely the algorithm is to accept a new cost that is higher than the old one. If the delta cost is negative (meaning there is less duplicates in the new solution), it was always accept the new state. 

100 new states are produced at each temperature, with the temperature being multiplied by 0.999 at each step in the while loop. If the while loop gets stuck at a local minima, the algorithm artificially increases the temperature higher and higher until it gets unstuck.

## Our Tests

Besides testing our algorithms to verify their accuracy, we ran three tests to compare the algorithms based on different benchmarks. 

The first test we ran was comparing the best, average, and worst case scenarios for both algorithms at a constant (30%) unfilled percent. 

Next, we compared the average runtimes of each algorithm with different board sizes again at a constant unfilled percentage (30%). To do this test in a reasonable amount of time, owing to the fact that Sudoku rules are limited to boards of perfect square sizes, we only tested the runtimes for 4x4, 9x9, and 16x16 boards. 

The last and most interesting test we ran was varying the percentage of the board that started filled, and measuring the average runtime of each algorithm. We started from 1% of the board being filled with blanks / 0's and incremented by 2% until we got to 100%, while running 50 trials per percentage level. We graphed the average runtime of each algorithm versus the number of possible ways to fill the board at the start. 

For all the tests, we used a random board generator that solved a completely unfilled board via backtracking. Then we removed random numbers until we got to the percentage of unfilled spots that we wanted. We understand that this generator potentially skews the results towards faster backtracking times, but using random boards from online can run into the same problems depending on how their boards were generated. Additionally, it was clear before the generator was created (and expected before we wrote the algorithms) that the backtracking algorithm would perform significantly better. 

## Experimental Results

_Board Sizes Results_
![Sizes Graph](https://github.com/bwmodlin/sudokusolver/blob/master/results/boardsize.png)

Both algorithms obviously performed exponentially worse as the board size exponentially increased. The main takeaway from this test was that backtracking's 9x9 results were much closer to its 4x4 results as compared to the simulated annealing performance. An interesting test to pursue in the future would be to run the algorithms with larger boards, but with our current algorithms that would take a long time if not forever. 

_Best, Average, and Worst Case Results_
![Cases Graph](https://github.com/bwmodlin/sudokusolver/blob/master/results/cases.png)

Similar to our board size test, the average case for the backtracking algorithm was closer to its best case while the average case for simulated annealing was pretty much in the middle. 

_Runtime versus Initial Possibilities Results_
![Annealing Possibilities Graph](https://github.com/bwmodlin/sudokusolver/blob/master/results/annealingpossibilities.png)

![Backtracking Possibilities Graph](https://github.com/bwmodlin/sudokusolver/blob/master/results/backtrackingpossibilities.png)

Something very interesting we saw here is that both algorithms peaked somewhere in the middle between the least and most possible permutations at the initial unsolved board state. We suspect this has something to do with the combination of the runtime-decreasing effects of having many unfilled spaces to play with and having many spaces already solved. Another interesting trend we saw was that the backtracking algorithm almost always had a much thinner peak runtime than the simulated annealing algorithm. 

To conclude, the backtracking algorithm performed multiple orders of magnitude better in every test. Clearly, backtracking is the better choice between the two algorithms. However, it is interesting to see how simulated annealing does in a problem like Sudoku, and the simulated annealing algorithm could definitely be optimized better in the future. Additionally, in some cases, like at some percentages unfilled, the simulated annealing was more reliable (though still slower on average) at some percentages of the board unfilled, as it had built in measures to make it unstuck. 

## How to Run the Testing Experiments

We ran all of experiments through the ```testing.py``` script. Some of them take a quite a lot of time to run, but we provided the script to see the code that generated the graphs. Each method in the file corresponds to one of the graphs we produced. 

## How to Run GUI Simulation

To run the GUI, it is best to use the ```driver.py``` script. Creating a game object will create a window. The type parameter and the optional board and stop parameters can be passed to the constructor for the game class. The type can either be "backtracking" or "annealing" corresponding to which algorithm you want to visualize. If no board parameter is provided, a random board will be generated to solve, but a 2d 9x9 array can be passed to solve a specific board. The stop parameter can be used to change the delay between each step to manipulate the speed of the visualization.

When the visualization first starts, the initial unsolved board will be displayed. To start the visualization, simply left click. You can left click once again to pause/start the visualization at any time before the board is solved. Besides the exit button in the top left of the window, the esc and q keys can be used to close the window. 

