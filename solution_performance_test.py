"""
Tests for the solution.py with mode = MODE_NO_DIAGONAL
"""
import unittest
from sudoku_env import *
import solution
solution.UNITLIST, solution.UNITS, solution.PEERS = get_units_peers(MODE_NO_DIAGONAL)

class TestSolution(unittest.TestCase):

    def test_performance(self):

        with open('hard_sudoku.txt') as sudoku_file:
            sudoku_puzzles = sudoku_file.readlines()
            for grid in sudoku_puzzles:
                solution.is_solved_correctly(solution.solve(grid.strip()))

if __name__ == '__main__':
    unittest.main()
