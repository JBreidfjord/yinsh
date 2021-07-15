from yinsh.board import Hex

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

directions = [Hex(0, -1), Hex(1, -1), Hex(1, 0,), Hex(0, 1,), Hex(-1, 1), Hex(-1, 0)]
diagonals = [Hex(1, -2), Hex(2, -1), Hex(1, 1), Hex(-1, 2), Hex(-2, 1), Hex(-1, -1)]


def distance(a: Hex, b: Hex):
    """Calculates the distance between two hexes"""
    return len(a - b)


def direction(direction: int):
    """Returns a Hex corresponding to the given integer direction"""
    return directions[direction]


def neighbour(hex: Hex, direction: int):
    """Returns the neighbour Hex in the given direction"""
    return hex + directions[direction]


def diagonal_direction(direction: int):
    """Returns a Hex corresponding to the given integer direction"""
    return diagonals[direction]


def diagonal_neighbour(hex: Hex, direction: int):
    """Returns the diagonal neighbour Hex in the given direction"""
    return hex + diagonals[direction]
