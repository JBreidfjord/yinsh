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
        board.rings[Hex(1, 0)] = Ring.WHITE
        board.rings[Hex(-2, 3)] = Ring.BLACK
        board.rings[Hex(4, 2)] = Ring.WHITE
        board.rings[Hex(3, -2)] = Ring.BLACK
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
        board.rings[Hex(0, 0)] = Ring.BLACK
        assert board.is_valid_move(Hex(0, 0), Hex(0, -3))

        # Test invalid hexes
        board._grid[Hex(10, 10)] = Ring.WHITE
        board.rings[Hex(10, 10)] = Ring.WHITE
        assert not board.is_valid_move(Hex(10, 10), Hex(-10, -10))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(10, 10), Hex(-10, -10), silent=False)

        # Test same hex
        assert not board.is_valid_move(Hex(0, 0), Hex(0, 0))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(0, 0), Hex(0, 0), silent=False)

        # Test occupied space
        board._grid[Hex(1, 1)] = Ring.WHITE
        board.rings[Hex(1, 1)] = Ring.WHITE
        assert not board.is_valid_move(Hex(0, 0), Hex(1, 1))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(0, 0), Hex(1, 1), silent=False)

        # Test non-straight line
        board._grid[Hex(4, 1)] = Ring.BLACK
        board.rings[Hex(4, 1)] = Ring.BLACK
        assert not board.is_valid_move(Hex(4, 1), Hex(-1, 0))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(4, 1), Hex(-1, 0), silent=False)

        # Test jumping over rings
        board._grid[Hex(4, 0)] = Ring.WHITE
        board.rings[Hex(4, 0)] = Ring.WHITE
        assert not board.is_valid_move(Hex(4, 1), Hex(4, -5))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(4, 1), Hex(4, -5), silent=False)

        # Test vacant space handling
        board._grid[Hex(4, 0)] = None
        board._grid[Hex(4, -1)] = Marker.WHITE
        board._grid[Hex(4, -2)] = Marker.BLACK
        board.markers[Hex(4, -1)] = Marker.WHITE
        board.markers[Hex(4, -2)] = Marker.BLACK
        assert not board.is_valid_move(Hex(4, 1), Hex(4, -5))
        with pytest.raises(IllegalMoveError):
            board.is_valid_move(Hex(4, 1), Hex(4, -5), silent=False)
        board._grid[Hex(4, -3)] = Marker.WHITE
        board._grid[Hex(4, -4)] = Marker.BLACK
        board.markers[Hex(4, -3)] = Marker.WHITE
        board.markers[Hex(4, -4)] = Marker.BLACK
        assert board.is_valid_move(Hex(4, 1), Hex(4, -5))

    def test_get_rows(self):
        board = Board.empty()
        assert board.get_rows(Player.WHITE) == []
        assert board.get_rows(Player.BLACK) == []

        # Test single row
        hexes = [Hex(0, 0), Hex(0, 1), Hex(0, 2), Hex(0, 3), Hex(0, 4)]
        board.markers = {hex: Marker.WHITE for hex in hexes}
        assert board.get_rows(Player.WHITE) == [
            [Hex(0, 4), Hex(0, 3), Hex(0, 2), Hex(0, 1), Hex(0, 0)]
        ]
        assert board.get_rows(Player.BLACK) == []

        # Test only single marker color
        board.markers[Hex(0, 0)] = Marker.BLACK
        assert board.get_rows(Player.WHITE) == []
        assert board.get_rows(Player.BLACK) == []

        # Test only markers
        board.markers[Hex(0, 0)] == Ring.WHITE
        assert board.get_rows(Player.WHITE) == []
        assert board.get_rows(Player.BLACK) == []

        # Test intersecting rows
        hexes = [Hex(0, 0), Hex(1, 0), Hex(2, 0), Hex(3, 0), Hex(4, 0)]
        for hex in hexes:
            board.markers[hex] = Marker.WHITE
        rows = board.get_rows(Player.WHITE)
        assert [Hex(0, 4), Hex(0, 3), Hex(0, 2), Hex(0, 1), Hex(0, 0)] in rows
        assert [Hex(0, 0), Hex(1, 0), Hex(2, 0), Hex(3, 0), Hex(4, 0)] in rows
        assert board.get_rows(Player.BLACK) == []

        # Test long rows
        board.markers[Hex(0, -1)] = Marker.WHITE
        rows = board.get_rows(Player.WHITE)
        assert [Hex(0, 4), Hex(0, 3), Hex(0, 2), Hex(0, 1), Hex(0, 0)] in rows
        assert [Hex(0, 3), Hex(0, 2), Hex(0, 1), Hex(0, 0), Hex(0, -1)] in rows
        assert board.get_rows(Player.BLACK) == []

    def test_move_ring(self):
        board = Board.empty()
        board._grid[Hex(0, 0)] = Ring.WHITE
        board.rings[Hex(0, 0)] = Ring.WHITE
        board._grid[Hex(0, 2)] = Marker.WHITE
        board._grid[Hex(0, 3)] = Marker.BLACK
        board.markers[Hex(0, 2)] = Marker.WHITE
        board.markers[Hex(0, 3)] = Marker.BLACK

        with pytest.raises(IllegalMoveError):
            board.move_ring(Player.BLACK, Hex(0, 0), Hex(0, 4))

        board.move_ring(Player.WHITE, Hex(0, 0), Hex(0, 4))
        assert board._grid[Hex(0, 0)] == Marker.WHITE
        assert board._grid.get(Hex(0, 1)) is None
        assert board._grid[Hex(0, 2)] == Marker.BLACK
        assert board._grid[Hex(0, 3)] == Marker.WHITE
        assert board._grid[Hex(0, 4)] == Ring.WHITE

    def test_rings(self):
        board = Board.empty()
        assert board.rings == {}

        board.place_ring(Player.WHITE, Hex(0, 0))
        board.place_ring(Player.BLACK, Hex(1, 1))
        assert set(board.rings.items()) == set([(Hex(0, 0), Ring.WHITE), (Hex(1, 1), Ring.BLACK)])

        board.move_ring(Player.WHITE, Hex(0, 0), Hex(0, -1))
        board.move_ring(Player.BLACK, Hex(1, 1), Hex(1, 3))
        assert set(board.rings.items()) == set([(Hex(0, -1), Ring.WHITE), (Hex(1, 3), Ring.BLACK)])

    def test_markers(self):
        board = Board.empty()
        assert board.markers == {}

        board.place_ring(Player.WHITE, Hex(0, 0))
        board.place_ring(Player.BLACK, Hex(1, 0))

        # Test placement
        board.move_ring(Player.WHITE, Hex(0, 0), Hex(0, -1))
        assert set(board.markers.items()) == set([(Hex(0, 0), Marker.WHITE)])

        # Test flip
        board.move_ring(Player.BLACK, Hex(1, 0), Hex(-1, 0))
        assert set(board.markers.items()) == set(
            [(Hex(0, 0), Marker.BLACK), (Hex(1, 0), Marker.BLACK)]
        )
