MODE_NO_DIAGONAL = 1
MODE_WITH_DIAGONAL = 2

DIGITS = '123456789'
ROWS = 'ABCDEFGHI'
COLS = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

BOXES = cross(ROWS, COLS)
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COLUMN_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
DIAGONAL_UNITS = [[row+col for (row,col) in zip(ROWS, COLS[::step])] for step in [-1,1]]

def get_units_peers(mode):

    if mode == MODE_NO_DIAGONAL:
        unitlist = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS
    elif mode == MODE_WITH_DIAGONAL:
        unitlist = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAGONAL_UNITS
    else:
        raise Exception('Unknown mode.')

    units = dict((s, [u for u in unitlist if s in u]) for s in BOXES)
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in BOXES)

    return unitlist, units, peers

