from __future__ import annotations

from copy import deepcopy
from math import log, sqrt
from random import choice
from yinsh.game import GameState, Move
from yinsh.types import Player


class Node:
    def __init__(
        self,
        color: Player,
        c: float,
        state: GameState = None,
        move: Move = None,
        parent: Node = None,
    ):
        self.color = color
        self.state = state
        self.move = move
        self.parent = parent
        self.c = c
        self.wins = 0
        self.visits = 1
        self.children: dict[Move, Node] = {}
        self.expanded = False

    def q(self):
        return self.wins / self.visits

    def u(self):
        return sqrt(log(self.parent.visits) / self.visits)

    def select_leaf(self):
        node = self
        while node.expanded:
            node = node.select_child()
        if node.state is None:
            node.state = deepcopy(node.parent.state)
            node.state.make_move(node.move)
        return node

    def select_child(self):
        return max(self.children.values(), key=lambda node: node.q() + node.c * node.u())

    def expand(self):
        self.children = {
            move: Node(self.color.other, self.c, move=move, parent=self)
            for move in self.state.legal_moves
        }
        self.expanded = True

    def simulate(self):
        state = deepcopy(self.state)
        while not state.is_over():
            state.make_move(choice(list(state.legal_moves)))
        outcome = state.outcome()
        # Random result if drawn
        if outcome.winner == "DRAW":
            outcome.winner = choice((Player.WHITE, Player.BLACK))
        return outcome

    def backpropagate(self, winner: Player):
        node = self
        while node.parent is not None:
            node.visits += 1
            node.wins += 1 if node.color.value == winner.value else 0
            node = node.parent
