import pytest
from yinsh.game import GameState, Move, MoveGenerator
from yinsh.types import Hex, IllegalMoveError, Player, Ring


class TestMove:
    ...


class TestMoveGenerator:
    ...


class TestGame:
    def test_new_game(self):
        game = GameState.new_game()
        assert game.board._grid == {}
        assert game.next_player == Player.WHITE
        assert game.players.white.rings == 0
        assert game.players.black.rings == 0
        assert game.previous_state == None
        assert game.last_move == None
        assert game.variant == "standard"
        assert game.requires_setup
        assert game._rings_to_win == 3

        game = GameState.new_game("blitz")
        assert game.variant == "blitz"
        assert game._rings_to_win == 1

        with pytest.raises(ValueError):
            GameState.new_game("not_a_variant")

    def test_is_over(self):
        game = GameState.new_game()
        assert not game.is_over()
        game.players.white.rings = 3
        assert game.is_over()
        game.players.white.rings = 0
        game.players.black.rings = 3
        assert game.is_over()

    def test_make_move(self):
        # See test_board.py for move validation tests
        game = GameState.new_game()

        # Test play move when requires setup
        with pytest.raises(IllegalMoveError, match="Board requires setup"):
            game.board._grid[Hex(0, 0)] = Ring.WHITE
            game.make_move(Move.play(Hex(0, 0), (Hex(0, 1))))

        # Test place move when setup is finished
        with pytest.raises(IllegalMoveError, match="Max rings reached"):
            game.requires_setup = False
            game.make_move(Move.place(Hex(0, 3)))

        # Test game over
        with pytest.raises(IllegalMoveError, match="Game is over"):
            game.players.white.rings = 3
            game.make_move(Move.play(Hex(0, 0), Hex(0, 1)))

        game = GameState.new_game()  # Fresh game state
        game.make_move(Move.place(Hex(0, 0)))
        assert game.board._grid[Hex(0, 0)] == Ring.WHITE
        assert game.next_player == Player.BLACK
        assert game.requires_setup

        game.make_move(Move.place(Hex(1, 0)))
        assert game.board._grid[Hex(1, 0)] == Ring.BLACK
        assert game.next_player == Player.WHITE
        assert game.requires_setup

        for i in range(4):  # Place rings to finish setup
            game.make_move(Move.place(Hex(i, 1)))
            game.make_move(Move.place(Hex(-1, i)))
        assert not game.requires_setup

    def test_legal_moves(self):
        game = GameState.new_game()
        assert isinstance(game.legal_moves, MoveGenerator)
