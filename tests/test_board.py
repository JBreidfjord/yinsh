import pytest
from yinsh.board import Board
from yinsh.types import Hex, IllegalMoveError, Marker, Player, Ring


class TestBoard:
    def test_empty(self):
        board = Board.empty()
        assert board._grid == {}

    def test_ring_count(self):
        board = Board.empty()
        assert board._get_ring_count() == (0, 0)
        board._grid[Hex(1, 0)] = Ring.WHITE
        board._grid[Hex(-2, 3)] = Ring.BLACK
        board._grid[Hex(4, 2)] = Ring.WHITE
        board._grid[Hex(3, -2)] = Ring.BLACK
        assert board._get_ring_count() == (2, 2)

    def test_place_ring(self):
        board = Board.empty()
        hex = Hex(0, 0)
        board.place_ring(Player.WHITE, hex)
        assert board._grid[hex] == Ring.WHITE

        # Test placing in occupied hex
        with pytest.raises(IllegalMoveError):
            board.place_ring(Player.BLACK, hex)

        # Test invalid hex
        with pytest.raises(IllegalMoveError):
            board.place_ring(Player.BLACK, Hex(10, 10))

        # Test placing too many rings
        board.place_ring(Player.WHITE, Hex(1, 0))
        board.place_ring(Player.WHITE, Hex(2, 0))
        board.place_ring(Player.WHITE, Hex(3, 0))
        board.place_ring(Player.WHITE, Hex(4, 0))
        board.place_ring(Player.BLACK, Hex(-1, 0))
        with pytest.raises(IllegalMoveError):
            board.place_ring(Player.WHITE, Hex(-2, 0))

    def test_valid_move(self):
        board = Board.empty()

        # Test source doesn't contain ring
        assert not board.is_valid_move(Hex(0, 0), Hex(0, 1))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(0, 0), Hex(0, 1), silent=False)

        # Test valid move
        board._grid[Hex(0, 0)] = Ring.BLACK
        assert board.is_valid_move(Hex(0, 0), Hex(0, -3))

        # Test invalid hexes
        board._grid[Hex(10, 10)] = Ring.WHITE
        assert not board.is_valid_move(Hex(10, 10), Hex(-10, -10))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(10, 10), Hex(-10, -10), silent=False)

        # Test same hex
        assert not board.is_valid_move(Hex(0, 0), Hex(0, 0))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(0, 0), Hex(0, 0), silent=False)

        # Test occupied space
        board._grid[Hex(1, 1)] = Ring.WHITE
        assert not board.is_valid_move(Hex(0, 0), Hex(1, 1))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(0, 0), Hex(1, 1), silent=False)

        # Test non-straight line
        board._grid[Hex(4, 1)] = Ring.BLACK
        assert not board.is_valid_move(Hex(4, 1), Hex(-1, 0))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(4, 1), Hex(-1, 0), silent=False)

        # Test jumping over rings
        board._grid[Hex(4, 0)] = Ring.WHITE
        assert not board.is_valid_move(Hex(4, 1), Hex(4, -5))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(4, 1), Hex(4, -5), silent=False)

        # Test vacant space handling
        board._grid[Hex(4, 0)] = None
        board._grid[Hex(4, -1)] = Marker.WHITE
        board._grid[Hex(4, -2)] = Marker.BLACK
        assert not board.is_valid_move(Hex(4, 1), Hex(4, -5))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(4, 1), Hex(4, -5), silent=False)
        board._grid[Hex(4, -3)] = Marker.WHITE
        board._grid[Hex(4, -4)] = Marker.BLACK
        assert board.is_valid_move(Hex(4, 1), Hex(4, -5))

    def test_check_rows(self):
        board = Board.empty()
        assert board._check_rows() is []

        # Test single row
        board._grid[Hex(0, 0)] == Marker.WHITE
        board._grid[Hex(0, 1)] == Marker.WHITE
        board._grid[Hex(0, 2)] == Marker.WHITE
        board._grid[Hex(0, 3)] == Marker.WHITE
        board._grid[Hex(0, 4)] == Marker.WHITE
        assert board._check_rows() == [[Hex(0, 0), Hex(0, 1), Hex(0, 2), Hex(0, 3), Hex(0, 4)]]

        # Test only single marker color
        board._grid[Hex(0, 0)] == Marker.BLACK
        assert board._check_rows() is []

        # Test only markers
        board._grid[Hex(0, 0)] == Ring.WHITE
        assert board._check_rows() is []

        # Test intersecting rows
        board._grid[Hex(0, 0)] == Marker.WHITE
        board._grid[Hex(1, 0)] == Marker.WHITE
        board._grid[Hex(2, 0)] == Marker.WHITE
        board._grid[Hex(3, 0)] == Marker.WHITE
        board._grid[Hex(4, 0)] == Marker.WHITE
        assert [Hex(0, 0), Hex(0, 1), Hex(0, 2), Hex(0, 3), Hex(0, 4)] in board._check_rows()
        assert [Hex(0, 0), Hex(1, 0), Hex(2, 0), Hex(3, 0), Hex(4, 0)] in board._check_rows()

        # Test long rows
        board._grid[Hex(0, -1)] == Marker.WHITE
        assert [Hex(0, 0), Hex(0, 1), Hex(0, 2), Hex(0, 3), Hex(0, 4)] in board._check_rows()
        assert [Hex(0, -1), Hex(0, 0), Hex(0, 1), Hex(0, 2), Hex(0, 3)] in board._check_rows()

    def test_move_ring(self):
        board = Board.empty()
        board._grid[Hex(0, 0)] = Ring.WHITE
        board._grid[Hex(0, 2)] = Marker.WHITE
        board._grid[Hex(0, 3)] = Marker.BLACK

        with pytest.raises(IllegalMoveError):
            board.move_ring(Player.BLACK, Hex(0, 0), Hex(0, 4))

        board.move_ring(Player.WHITE, Hex(0, 0), Hex(0, 4))
        assert board._grid[Hex(0, 0)] == Marker.WHITE
        assert board._grid.get(Hex(0, 1)) is None
        assert board._grid[Hex(0, 2)] == Marker.BLACK
        assert board._grid[Hex(0, 3)] == Marker.WHITE
        assert board._grid[Hex(0, 4)] == Ring.WHITE
