from enum import Enum


class Player(Enum):
    WHITE = True
    BLACK = False

    @property
    def other(self):
        return Player.BLACK if self == Player.WHITE else Player.WHITE

    def set_rings(self, num_rings: int):
        self.rings = num_rings
