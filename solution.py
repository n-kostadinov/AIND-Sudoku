from sudoku_env import *
import itertools
# change between MODE_NO DIAGONAL AND MODE_WITH_DIAGONAL
UNITLIST, UNITS, PEERS = get_units_peers(MODE_WITH_DIAGONAL)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    for unit in UNITLIST:
        unsolved = [box for box in unit if len(values[box]) > 1]
        pairs = list(itertools.combinations(unsolved, 2)) # indices of all pairs (0, 1), (0, 2), (0, 3), (0, 4),
        for i,j in pairs:
            chars1, chars2 = values[i], values[j] # the characters in each pair
            if len(chars1) ==  2 and chars1 == chars2: # if characters match, i.e. chars1 = '34' and chars2 = '34' they are twins
                not_twins = [box for box in unsolved if values[box] != chars1] # all boxes that are not the twins
                for box in not_twins:
                    for char in chars1: # remove the characters of the twins for each box that is not one of the twins
                        val = values[box].replace(char, '')
                        values = assign_value(values, box, val)

    return values

def hidden_twins(values):
    """Eliminate values using the hidden twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked hidden eliminated from peers.
    """
    # some help functions
    box_intersection = lambda small_box, big_box, vals: set(vals[small_box]).intersection(set(vals[big_box]))
    box_difference = lambda small_box, big_box, vals: set(vals[big_box]).difference(set(vals[small_box]))

    for unit in UNITLIST:
        unsolved = [box for box in unit if len(values[box]) > 1]

        for small_box in unsolved:
            if len(values[small_box]) == 2: # box containing exactly two vlaues
                for big_box in unsolved:
                    if len(values[big_box]) > 2: # box containing more than two vlaues
                        if box_intersection(small_box, big_box, values) == set(values[small_box]): # those are potential hidden twins
                            other_boxes = [box for box in unsolved if box != small_box and box != big_box] # all unsolved boxes that are not the small and big box
                            # no intersection between the small box and the other boxes -> big and small boxes are indeed hidden twins BINGO!
                            if len(other_boxes) > 0 and sum([len(box_intersection(small_box, box, values)) for box in other_boxes]) == 0:
                                # update all units where big box is in
                                for unit in UNITS[big_box]:
                                    # all boxes that are unsolved and may be updated
                                    all_unsolved_boxes = [box for box in unit if len(values[box]) > 1 and box != big_box]
                                    # get a string that is all digits if all unsolved boxes
                                    all_unsolved_digits = ''.join([values[box] for box in all_unsolved_boxes])
                                    for digit in box_difference(small_box, big_box, values):
                                        if all_unsolved_digits.count(digit) == 1: # there is a "lonely" digit that is found only in the big box and one other box
                                            for box in all_unsolved_boxes: # update the value of that box to be the digit
                                                if digit in values[box]:
                                                    values = assign_value(values, box, digit)

    return values

def grid_values(grid):

    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    grid = [DIGITS if value == '.' else value for value in grid]
    return dict(zip(cross(ROWS, COLS), grid))
    pass


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    grid_lines = []
    width = 1+max(len(values[s]) for s in BOXES)
    delimitter_line = '+'.join(['-'*(width*3)]*3)
    for r in ROWS:
        line = ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in COLS)
        grid_lines.append(line)
        print(line)
        if r in 'CF':
            grid_lines.append(delimitter_line)
            print(delimitter_line)

    return grid_lines

def only_choice_rule(values):
    for box in BOXES:
        all_values = set(values[peer] for peer in PEERS[box])
        if len(all_values) == 8:
            values = assign_value(values, box, list(set(DIGITS).difference(all_values))[0])
    return values


def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
       values: Sudoku in dictionary form.
    Returns:
       Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in PEERS[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):

    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in UNITLIST:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Hidden Twins Strategy
        values = hidden_twins(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in BOXES):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in BOXES if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def is_solved_correctly(values):
    """
    Input: A sudoku in dictionary form.
    Output: True if the sudoko is solved correctly, False ortherwise
    """
    for unit in UNITLIST:
        # the sum will be less then zero if there is a box that does not contain a single character
        unit_sum = sum([ int(values[box]) if len(values[box]) == 1 else -100 for box in unit])
        # if the sudoko is solved correctly the sum will be 45 as 1+2...+9 is 45
        if 45 != unit_sum:
            return False

    return True

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
