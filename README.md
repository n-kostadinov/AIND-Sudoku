# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: To solve the naked twins problem a new constraint is implemented - if a unit contains two boxes with identical two character values, all other boxes in that unit are not allowed to contain either of the characters. This constraint is propagated at every puzzle reduction step to all units - that are all rows, columns, 3x3 squares, and in a diagonal sudoku the two diagonals.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We add a new type of unit, that is the diagonal. In the process of solving the constraints (i.e. elimination, only choice, naked twins, hidden twins) are propagated to all units. By propagating the constraints to the diagonal, the sudoku gets solved as a diagonal sudoku.

# A NOTE to the Reviewer
The sudoku_env.py modul has beed included to enable turning on and off the diagonal sudoku mode. The diagonal sudoku mode is turned on by default. It is intentionally switched off in the solution_unit_test.py as it was easier to test and debug an ordinary sudoku. Hopefully, the additional test modules that have been used do not present any difficulties.
An additional strategy has been implemented and tested - the hidden twins strategy.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.