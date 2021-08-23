from yinsh.helpers import (
    distance,
    hex_lerp,
    hex_linedraw,
    hex_round,
    lerp,
    neighbour,
    straight_line,
)
from yinsh.types import Direction, Hex


def test_neighbour():
    assert neighbour(Hex(0, 0), Direction.N) == Hex(0, -1)
    assert neighbour(Hex(-2, -3), Direction.SE) == Hex(-1, -3)


def test_distance():
    assert distance(Hex(0, 0), Hex(0, 4)) == 4
    assert distance(Hex(-2, -3), Hex(4, 1)) == 10


def test_lerp():
    assert lerp(0, 10, 0.5) == 5
    assert lerp(-10, 10, 0.25) == -5


def test_hex_lerp():
    assert hex_lerp(Hex(0, 0), Hex(0, 4), 0.5) == Hex(0, 2)
    assert hex_lerp(Hex(-2, -3), Hex(4, 1), 0.5) == Hex(1, -1)


def test_hex_round():
    assert hex_round(Hex(0.34, -0.28)) == Hex(0, 0)
    assert hex_round(Hex(-2.5, 4.99)) == Hex(-3, 5)


def test_hex_linedraw():
    assert hex_linedraw(Hex(0, 0), Hex(0, 4)) == [
        Hex(0, 0),
        Hex(0, 1),
        Hex(0, 2),
        Hex(0, 3),
        Hex(0, 4),
    ]
    assert hex_linedraw(Hex(-2, -3), Hex(4, 1)) == [
        Hex(-2, -3),
        Hex(-1, -3),
        Hex(-1, -2),
        Hex(0, -2),
        Hex(0, -1),
        Hex(1, -1),
        Hex(2, -1),
        Hex(2, 0),
        Hex(3, 0),
        Hex(3, 1),
        Hex(4, 1),
    ]


def test_straight_line():
    assert straight_line(Hex(0, 0), Hex(0, 4)) == [
        Hex(0, 0),
        Hex(0, 1),
        Hex(0, 2),
        Hex(0, 3),
        Hex(0, 4),
    ]
    assert straight_line(Hex(-2, -3), Hex(4, 1)) is None
