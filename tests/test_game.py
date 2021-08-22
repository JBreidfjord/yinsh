import pytest
from yinsh.game import GameState, Move, MoveGenerator
from yinsh.helpers import valid_hexes
from yinsh.types import Hex, IllegalMoveError, Marker, Player, Ring


class TestMove:
    def test_init(self):
        with pytest.raises(ValueError):
            Move(Hex(0, 0), dst_hex=Hex(0, 1), is_starting=True)

    def test_play(self):
        move = Move.play(Hex(0, 0), Hex(0, 1))
        assert isinstance(move, Move)
        assert move.src_hex == Hex(0, 0)
        assert move.dst_hex == Hex(0, 1)
        assert move.is_play
        assert not move.is_starting

    def test_place(self):
        move = Move.place(Hex(0, 0))
        assert isinstance(move, Move)
        assert move.src_hex == Hex(0, 0)
        assert move.dst_hex is None
        assert not move.is_play
        assert move.is_starting


class TestMoveGenerator:
    def generate_valid(game: GameState):
        """Iterate through rings then check all hexes for valid moves"""
        valid = []
        for point, content in game.board.get_rings():
            if content.value == game.next_player.value:
                for hex in valid_hexes:
                    if game.board.is_valid_move(point, hex, True):
                        valid.append(Move.play(point, hex))
        return valid

    def test_move_generator(self):
        game = GameState.new_game()
        assert list(MoveGenerator(game)) == [Move.place(hex) for hex in valid_hexes]

        game.make_move(Move.place(Hex(0, 0)))
        assert list(MoveGenerator(game)) == [
            Move.place(hex) for hex in valid_hexes if hex != Hex(0, 0)
        ]

        # Place rings to finish setup
        game.make_move(Move.place(Hex(1, 0)))
        for i in range(4):
            game.make_move(Move.place(Hex(-1, i)))
            game.make_move(Move.place(Hex(i, 1)))

        # Test for no place moves
        assert MoveGenerator(game).count() > 0
        for move in MoveGenerator(game):
            assert move.is_play

        assert set(MoveGenerator(game)) == set(self.generate_valid(game))

        game.make_move(Move.play(Hex(0, 0), Hex(3, -3)))
        assert set(MoveGenerator(game)) == set(self.generate_valid(game))

        game.make_move(Move.play(Hex(0, 1), Hex(0, -1)))
        assert set(MoveGenerator(game)) == set(self.generate_valid(game))


class TestGameState:
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

    def test_outcome(self):
        game = GameState.new_game()
        assert game.outcome() is None
        game.players.white.rings = 3
        assert game.outcome().winner == Player.WHITE
        game.players.white.rings = 0
        game.players.black.rings = 3
        assert game.outcome().winner == Player.BLACK

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
            game.make_move(Move.place(Hex(-1, i)))
            game.make_move(Move.place(Hex(i, 1)))
        assert not game.requires_setup

        game.make_move(Move.play(Hex(0, 0), Hex(0, -4)))
        assert game.board._grid[Hex(0, 0)] == Marker.WHITE
        assert game.board._grid[Hex(0, -4)] == Ring.WHITE
        assert game.next_player == Player.BLACK
        assert not game.requires_setup

        game.make_move(Move.play(Hex(0, 1), Hex(0, -1)))
        assert game.board._grid[Hex(0, 1)] == Marker.BLACK
        assert game.board._grid[Hex(0, -1)] == Ring.BLACK
        assert game.next_player == Player.WHITE
        assert game.board._grid[Hex(0, 0)] == Marker.BLACK  # Flipped marker

    def test_legal_moves(self):
        game = GameState.new_game()
        assert isinstance(game.legal_moves, MoveGenerator)
