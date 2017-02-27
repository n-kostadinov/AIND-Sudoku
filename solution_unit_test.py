"""
Tests for the solution.py with mode = MODE_NO_DIAGONAL
"""
import unittest
from sudoku_env import *
import solution
solution.UNITLIST, solution.UNITS, solution.PEERS = get_units_peers(MODE_NO_DIAGONAL)

class TestSolution(unittest.TestCase):


    def test_cross(self):
        # given
        rows = 'ABC'
        cols = '123'
        crossed = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

        # when
        result = cross(rows, cols)

        # then
        self.assertEquals(crossed, result, msg='Crossed should match.')


    def test_grid_values(self):
        # given
        t_grid_values = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

        # when
        result = solution.grid_values(t_grid_values)

        # then
        self.assertEquals('123456789', result['A1'])
        self.assertEquals('9', result['B1'])
        self.assertEquals('9',result['G6'])
        self.assertEquals('1', result['I5'])

    def test_is_solved_correctly(self):
        # given
        t_values = solution.grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')

        # then
        self.assertFalse(solution.is_solved_correctly(t_values))

    def test_is_solved_correctly_False(self):
        # given
        t_values = solution.grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')

        # then
        self.assertFalse(solution.is_solved_correctly(t_values))

    def test_is_solved_correctly_True(self):
        # given
        t_values = solution.grid_values('483921657967345821251876493548132976729564138136798245372689514814253769695417382')

        # then
        self.assertTrue(solution.is_solved_correctly(t_values))

    def test_is_solved_correctly_Incorrect(self):
        # given
        t_values = solution.grid_values('483921657967345821251876493548132976729564138136798245372689514814253769695417381') # only last char is 1

        # then
        self.assertFalse(solution.is_solved_correctly(t_values))

    def test_display(self):
        # given
        t_grid_values = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

        # when
        lines = solution.display(solution.grid_values(t_grid_values))

        # then
        self.assertEquals('123456789 123456789     3     |123456789     2     123456789 |    6     123456789 123456789 ', lines[0])
        self.assertEquals('123456789 123456789     8     |    1     123456789     2     |    9     123456789 123456789 ', lines[4])
        self.assertEquals('123456789 123456789     5     |123456789     1     123456789 |    3     123456789 123456789 ', lines[10])

    def test_eliminate(self):

        # given
        t_values = solution.grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')

        # when
        result  = solution.eliminate(t_values)

        # then
        self.assertEquals('45', result['A1'])
        self.assertEquals('9', result['B1'])
        self.assertEquals('9',result['G6'])
        self.assertEquals('1', result['I5'])
        self.assertEquals('34569', result['E5'])
        self.assertEquals('24678', result['I8'])

        # print
        print()
        solution.display(result)

    def test_only_choice(self):
        # given
        t_values = solution.eliminate(solution.grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))

        # when
        print()
        lines = solution.display(solution.only_choice(t_values))

        # then
        self.assertEquals(' 345   345    8   |  1    3456   2   |  9   34567 34567 ', lines[4])
        self.assertEquals('  7     2     9   |  5   34569   4   |  1   13456   8   ', lines[5])
        self.assertEquals(' 1345 13459   6   |  7    3459   8   |  2    1345  345  ', lines[6])


    def test_reduce_puzzle(self):
        # given
        t_values = solution.grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')

        # when
        values = solution.reduce_puzzle(t_values)

        # then
        self.assertTrue(solution.is_solved_correctly(values))

        print()
        solution.display(values)


    def test_search(self):
        # given
        t_values = solution.grid_values('.....97..4..7...2...18...39.3....4...769.531...4....9.84...39...1...8..3..26.....')

        # when
        values = solution.search(t_values)

        # then
        self.assertTrue(solution.is_solved_correctly(values))

        print()
        lines = solution.display(values)


    def test_solve(self):
        # Harder sudoko
        # given
        grid = '.....97..4..7...2...18...39.3....4...769.531...4....9.84...39...1...8..3..26.....'

        # when
        values = solution.solve(grid)

        # then
        #self.assertTrue(solution.is_solved_correctly(values))

        print()
        lines = solution.display(values)


    def test_naked_twins(self):

        # given
        """
        5   367   9  | 478   2    47 | 367   1   468
        4   1237  23 | 178   5    6  | 2379 237   89
        8   1267  26 |  9    14   3  | 267  2467  5
        ---------------+---------------+---------------
        39   8    7  | 134  1349  2  |  5    36   16
        6    5    4  | 137  139  179 |  13   8    2
        23   23   1  |  5    6    8  |  4    9    7
        ---------------+---------------+---------------
        1   369   8  |  2   349   5  | 679  467  469
        7    29   25 |  6    8   149 | 129  245   3
        239   4   2356|  13   7    19 |  8   256  169
        """
        t_values = solution.eliminate(solution.grid_values('5.9.2..1.4...56...8..9.3..5.87..25..654....82..15684971.82.5...7..68...3.4..7.8..'))

        # when
        result = solution.naked_twins(t_values)

        self.assertEqual('9', result['D1'])

    def test_world_hardest_sudoku(self):

        # given See http://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html
        """
        8      1246   24569  |  2347   12357    1234  | 13569    4579  1345679
        12459    124      3    |   6     12578    1248  |  1589   45789   14579
        1456     7      456   |  348      9      1348  |   2      458    13456
        ------------------------+------------------------+------------------------
        123469    5      2469  |  2389    2368     7    |  1689    2489   12469
        12369   12368    269   |  2389     4       5    |   7      289     1269
        24679    2468   24679  |   1      268     2689  |  5689     3     24569
        ------------------------+------------------------+------------------------
        23457    234      1    | 23479    237     2349  |  359      6       8
        23467    2346     8    |   5      2367   23469  |   39      1      2379
        23567     9      2567  |  2378   123678  12368  |   4      257     2357
        """
        grid = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'

        # when
        values = solution.solve(grid)

        # then
        self.assertTrue(solution.is_solved_correctly(values))

        print()
        solution.display(values)


if __name__ == '__main__':
    unittest.main()
