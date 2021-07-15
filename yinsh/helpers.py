from enum import Enum

from yinsh.board import Hex


class Direction(Enum):
    N = Hex(0, -1)
    NE = Hex(1, -1)
    SE = Hex(1, 0)
    S = Hex(0, 1)
    SW = Hex(-1, 1)
    NW = Hex(-1, 0)


def distance(a: Hex, b: Hex):
    """Calculates the distance between two hexes"""
    return len(a - b)


def neighbour(hex: Hex, direction: Direction) -> Hex:
    """Returns the neighbour Hex in the given direction"""
    return hex + direction


inv_coordinate_index = {}

inv_coordinate_index[0] = Hex(0, 0)
idx = 1
for q in range(-5, 6):
    for r in range(-5, 6):
        if -5 <= -q - r <= 5 and not (
            (abs(q) == 5 or q == 0) and (abs(r) == 5 or r == 0)
        ):
            inv_coordinate_index[idx] = Hex(q, r)
            idx += 1

coordinate_index = {coord: i for i, coord in inv_coordinate_index.items()}
