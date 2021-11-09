# Backtracking Algorithm

# Works by going cell by cell and checking which number can go in
# Once number is placed, call that same function again recursively, if it turns out that there are no options
# for the next cell, it means that the previous cell was wrong, so we revert back and start over on the next iteration

# Functions to impelement

# Our main function
# def solve():
    # find the first blank spot by looping through the grid
    # once blank spot is found, start an iteration through the 9 possible number choices
    # call isPossible on the choice of of number, if True, put the number there
    # recursively call solve() again
    # after, set grid[x][y] = blank
    # After the number iteration loop, return nothing / stop the function

# Helper function that takes in a cell position and a potential input number
# def isPossible(x,y,n):
    # Checks to see if a number can be placed in the current position in the grid

    # 3 Checks:
    # If able vertically
    # If able horizontally
    # If able in square