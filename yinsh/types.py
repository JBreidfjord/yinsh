from dataclasses import dataclass
from enum import Enum

from yinsh.board import Hex


class Player(Enum):
    WHITE = True
    BLACK = False

    @property
    def other(self):
        return Player.BLACK if self == Player.WHITE else Player.WHITE

    def set_rings(self, num_rings: int):
        self.rings = num_rings


@dataclass
class Players:
    white = Player.WHITE
    black = Player.BLACK


class Direction(Enum):
    N = Hex(0, -1)
    NE = Hex(1, -1)
    SE = Hex(1, 0)
    S = Hex(0, 1)
    SW = Hex(-1, 1)
    NW = Hex(-1, 0)


class IllegalMoveError(Exception):
    ...
