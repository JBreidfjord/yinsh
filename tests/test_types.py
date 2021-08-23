import pytest
from yinsh.types import Direction, Hex, Marker, Player, Ring


class TestHex:
    def test_construction(self):
        with pytest.raises(ValueError):
            Hex(1, 0, 0)

    def test_addition(self):
        x = Hex(1, 0, -1)
        y = Hex(2, -2, 0)
        assert x + y == Hex(3, -2, -1)
        with pytest.raises(TypeError):
            x + 4

    def test_subtraction(self):
        x = Hex(1, 0, -1)
        y = Hex(2, -2, 0)
        assert x - y == Hex(-1, 2, -1)
        with pytest.raises(TypeError):
            x - 4

    def test_scale(self):
        x = Hex(1, 0, -1)
        assert x.scale(4) == Hex(4, 0, -4)

    def test_len(self):
        assert len(Hex(1, 0, -1)) == 1
        assert len(Hex(-4, 2, 2)) == 4

    def test_comparison(self):
        x = Hex(1, 0, -1)
        y = Hex(2, -2, 0)
        z = Hex(-2, 4, -2)
        assert x < y < z
        assert not x <= Hex(0, 0)
        assert z > x
        assert z >= Hex(0, 0)
        assert x == Hex(1, 0)
        assert not x == Hex(0, 1)

    def test_neighbours(self):
        x = Hex(0, 0)
        assert set(x.neighbours()) == set(
            [Hex(1, 0), Hex(-1, 0), Hex(-1, 1), Hex(0, -1), Hex(1, -1), Hex(0, 1)]
        )
        y = Hex(1, -5)
        assert set(y.neighbours()) == set([Hex(0, -4), Hex(1, -4), Hex(2, -5)])


class TestPlayer:
    def test_enum(self):
        assert Player.WHITE.value
        assert not Player.BLACK.value

    def test_other(self):
        assert not Player.WHITE.other.value
        assert Player.BLACK.other.value

    def test_rings(self):
        player = Player.WHITE
        player.set_rings(0)
        assert player.rings == 0

        player.rings += 1
        assert player.rings == 1


class TestRing:
    def test_enum(self):
        assert Ring.WHITE.value
        assert not Marker.BLACK.value

    def test_other(self):
        assert not Ring.WHITE.other.value
        assert Ring.BLACK.other.value

    def test_str(self):
        assert str(Ring.WHITE) == "◎"
        assert str(Ring.BLACK) == "⊚"


class TestMarker:
    def test_enum(self):
        assert Marker.WHITE.value
        assert not Marker.BLACK.value

    def test_other(self):
        assert not Marker.WHITE.other.value
        assert Marker.BLACK.other.value

    def test_str(self):
        assert str(Marker.WHITE) == "◈"
        assert str(Marker.BLACK) == "◇"


class TestDirection:
    def test_enum(self):
        assert Direction.N.value == Hex(0, -1)
        assert Direction.NE.value == Hex(1, -1)
        assert Direction.SE.value == Hex(1, 0)
        assert Direction.S.value == Hex(0, 1)
        assert Direction.SW.value == Hex(-1, 1)
        assert Direction.NW.value == Hex(-1, 0)
