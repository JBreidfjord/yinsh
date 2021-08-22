from __future__ import annotations

from yinsh.board import Board
from yinsh.types import Hex, IllegalMoveError, Player, Players


class Move:
    def __init__(self, src_hex: Hex, dst_hex: Hex = None, is_starting: bool = False):
        # Replace with proper exception
        assert (dst_hex is not None) ^ is_starting, "Move takes exactly 1 type of move as input"

        self.src_hex = src_hex
        self.dst_hex = dst_hex

        self.is_play = dst_hex is not None
        self.is_starting = is_starting

    @classmethod
    def play(cls, src_hex: Hex, dst_hex: Hex):
        return Move(src_hex, dst_hex)

    @classmethod
    def place(cls, hex: Hex):
        return Move(hex, is_starting=True)

    def __repr__(self):
        if self.is_play:
            return f"Move.play({self.src_hex}, {self.dst_hex})"
        else:
            return f"Move.place({self.src_hex})"


class GameState:
    def __init__(
        self,
        board: Board,
        players: Players,
        next_player: Player,
        previous: GameState,
        move: Move,
        variant: str,
        is_setup: bool = True,
    ):
        self.board = board
        self.players = players
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move
        self.variant = variant

        self.requires_setup = not is_setup
        self._rings_to_win = 1 if self.variant == "blitz" else 3

    @classmethod
    def new_game(cls, variant: str = "standard"):
        """
        Initializes a new game of YINSH
        
        Pass variant argument "blitz" for a shorter game,
        otherwise standard game length will be used
        """
        # Replace with proper exception
        assert variant in [
            "standard",
            "blitz",
        ], "Variant must be 'standard', 'blitz', or not given"

        players = Players()
        players.white.set_rings(0)
        players.black.set_rings(0)

        return GameState(Board.empty(), players, players.white, None, None, variant, is_setup=False)

    def is_over(self, outcome: bool = False):
        # Return Outcome object if True
        return (
            self.players.white.rings == self._rings_to_win
            or self.players.black.rings == self._rings_to_win
        )

    def make_move(self, move: Move):
        if move.is_play and self.requires_setup:
            raise IllegalMoveError("Board requires setup")
        elif move.is_starting and not self.requires_setup:
            raise IllegalMoveError("Max rings reached")
        elif self.is_over():
            raise IllegalMoveError("Game is over")

        if move.is_starting:
            raise NotImplementedError
        elif move.is_play:
            raise NotImplementedError

    def legal_moves(self):
        if self.requires_setup:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def display(self):
        print(self.board)
