# Sudoku Solver


# Intentions: 

Sudoku is a popular logic-based number puzzle game. Given a 9x9 grid, the objective is to fill the grid with digits so that each row, each column, and each of the nine 3×3 subgrids or "squares" contain all of the digits from 1 to 9. For our project, we were particularly interested in the idea of how a computer would solve this game.  

Using the two most common algorithms for solving Sudoku, backtracking and simulated annealing, we implemented both and ran a number of experiments to test performance, efficiency, and how they would scale with board sizes other than 9x9.  

Additionally, we also developed a simiple visualizer GUI to simulate the solving process of each algorithm.

# Overview

Our project can be split up into two components, the testing experiments and the GUI. ```backtracking.py``` and ```simulatedannealing.py``` contain the implementation of the corresponding algorithm. ```utilities.py``` contains helper functions used throughout other files such as generating random Sudoku boards or printing matrices in the terminal. ```testing.py``` is where all the experiments and data collections were performed. ```game.py``` contains the GUI implementation and ```driver.py``` starts the game.  

A ```requirements.txt``` is provided for required import installations. You can also manually install the libraries yourself since there are only three: matplotlib, numpy, and pygame.


# Our Tests

Describe each of the tests that we performed and what kind of results we were expecting  
Also describe what the generator does

# How to Run the Testing Experiments

Step by step process on how to run experiments  
Explain more in-depth about testing.py

# Experiment Results

Pictures of our graphs  
Short sentence about what each graph shows and what we learned and if it was what we were predicting  

# How to Run GUI Simulation

To run the GUI, it is best to use the ```driver.py``` script. Creating a game object will create a window. The type parameter and the optional board and stop parameters can be passed ot the constructor for the game class. The type can either be "backtracking" or "annealing" corresponding to which algorithm you want to visualize. If no board parameter is provided, a random board will be generated to solve, but a 2d 9x9 array can be passed to solve a specific board. The stop parameter can be used to change the delay between each step to manipulate the speed of the visualization.

When the visualizztion first starts, the initial unsolved board will be displayed. To start the visualization, simple left click. You can left click once again to pause/start the visuzliation at any time before the board is solved. Besides the exit button in the top left of the window, the esc and q keys can be used to close the window. 

