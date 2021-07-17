from __future__ import annotations


class Hex:
    def __init__(self, q: int, r: int, s: int = None):
        """Data structure representing a hex coordinate using a cube/axial system"""
        self.s = s if s is not None else -q - r
        if q + r + self.s != 0:
            raise ValueError("Coordinates must sum to 0")
        self.q = q
        self.r = r
        self.cube = (self.q, self.r, self.s)
        self.axial = (self.q, self.r)

        self._neighbours = []

    def neighbours(self):
        from yinsh.helpers import Direction, neighbour, valid_hexes

        if self._neighbours == []:
            for direction in Direction:
                possible_neighbour = neighbour(self, direction)
                if possible_neighbour in valid_hexes:
                    self._neighbours.append(possible_neighbour)
        return self._neighbours

    def __repr__(self):
        return f"Hex{self.axial}"

    def __eq__(self, other: Hex):
        return self.cube == other.cube

    def __hash__(self):
        return hash(self.axial)

    def __add__(self, other: Hex):
        if not isinstance(other, Hex):
            raise TypeError(f"Invalid type {type(other)}")
        return Hex(self.q + other.q, self.r + other.r)

    def __sub__(self, other: Hex):
        if not isinstance(other, Hex):
            raise TypeError(f"Invalid type {type(other)}")
        return Hex(self.q - other.q, self.r - other.r)

    def __len__(self):
        return int((abs(self.q) + abs(self.r) + abs(self.s)) / 2)


class Board:
    from yinsh.types import Player

    def __init__(self):
        self._grid = {}

    def place_ring(self, player: Player, hex: Hex):
        """Place a ring during setup of starting position"""
        raise NotImplementedError

    def move_ring(self, player: Player, src_hex: Hex, dst_hex: Hex):
        """Move a ring from source to destination"""
        raise NotImplementedError

    @classmethod
    def empty(cls):
        """Initializes a new empty YINSH board"""
        return Board()

