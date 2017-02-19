"""
Integration tests for the solution.py with mode = MODE_NO_DIAGONAL
"""

"""
Tests for the solution.py with mode = MODE_NO_DIAGONAL
"""
import unittest
from sudoku_env import *
import solution
solution.UNITLIST, solution.UNITS, solution.PEERS = get_units_peers(MODE_WITH_DIAGONAL)

class TestDiagonalSolution(unittest.TestCase):


    def test_solve_negative(self):
        # given
        grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

        # when
        values = solution.solve(grid)

        # then
        self.assertFalse(values)

    def test_solve_positive(self):
        # given
        grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

        # when
        values = solution.solve(grid)

        # then
        self.assertTrue(solution.is_solved_correctly(values))

        solution.display(values)

if __name__ == '__main__':
    unittest.main()