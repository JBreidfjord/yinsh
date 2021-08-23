from __future__ import annotations

import ast
from typing import Iterator

from yinsh.board import Board
from yinsh.helpers import display_index, inv_coordinate_index
from yinsh.types import Hex, IllegalMoveError, Outcome, Player, Players


class Move:
    def __init__(self, src_hex: Hex, dst_hex: Hex = None, is_starting: bool = False):
        if not (dst_hex is not None) ^ is_starting:
            raise ValueError("Move takes exactly 1 type of move as input")

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


class MoveGenerator:
    def __init__(self, game: GameState):
        self.game = game

    def __iter__(self):
        return self._generate_legal_moves()

    def _generate_legal_moves(self) -> Iterator[Move]:
        ...

    def count(self):
        len(list(self))


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
        if variant not in ["standard", "blitz"]:
            raise ValueError("Variant must be 'standard', 'blitz', or not given")

        players = Players()
        players.white.set_rings(0)
        players.black.set_rings(0)

        return GameState(Board.empty(), players, players.white, None, None, variant, is_setup=False)

    def is_over(self):
        return (
            self.players.white.rings == self._rings_to_win
            or self.players.black.rings == self._rings_to_win
        )

    def outcome(self):
        if self.players.white.rings == self._rings_to_win:
            return Outcome(winner=Player.WHITE)
        elif self.players.black.rings == self._rings_to_win:
            return Outcome(winner=Player.BLACK)

    def make_move(self, move: Move):
        if move.is_play and self.requires_setup:
            raise IllegalMoveError("Board requires setup")
        elif move.is_starting and not self.requires_setup:
            raise IllegalMoveError("Max rings reached")
        elif self.is_over():
            raise IllegalMoveError("Game is over")

        if move.is_starting:
            self.board.place_ring(self.next_player, move.src_hex)
            self.next_player = self.next_player.other
            white_rings, black_rings = self.board._get_ring_count()
            if white_rings == 5 and black_rings == 5:
                self.requires_setup = False

        elif move.is_play:
            self.board.move_ring(self.next_player, move.src_hex, move.dst_hex)
            self._handle_rows()
            self.next_player = self.next_player.other

    def _handle_rows(self):
        rows = self.board.get_rows()
        if rows:
            if len(rows) == 1:
                row = rows[0]
            else:
                self.display_rows(rows)
                choice = int(input("Input numeric selection: "))
                row = rows[choice]

            ring_coords = ast.literal_eval(input("Input coords for ring (x, y): "))
            ring_hex = Hex(ring_coords[0], ring_coords[1])
            self.board._complete_row(row, ring_hex)
            if self.next_player.value:
                self.players.white.rings += 1
            else:
                self.players.black.rings += 1

    @property
    def legal_moves(self):
        return MoveGenerator(self)

    def display(self):
        print(self.board)
