import pytest
from yinsh.types import Hex, IllegalMoveError


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
