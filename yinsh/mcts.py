from __future__ import annotations

from math import log, sqrt
from random import choice
from timeit import default_timer as timer

from tqdm.auto import trange

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
        while node.expanded and node.children:
            node = node.select_child()
        if node.state is None:
            node.state = node.parent.state.copy()
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
        state = self.state.copy()
        while not state.is_over():
            state.make_move(choice(list(state.legal_moves)))

            # Handle rows
            rows = state.board.get_rows(state.next_player.other)  # Player who moved last
            if rows:
                state.complete_row(choice(rows))
                state.remove_ring(
                    choice(
                        [
                            hex
                            for hex, ring in state.board.rings.items()
                            if ring.value == state.next_player.other.value
                        ]
                    )
                )
                # Check if this ended the game
                if (state.next_player.other.value and state.rings.white == state._rings_to_win) or (
                    not state.next_player.other.value and state.rings.black == state._rings_to_win
                ):
                    break

            op_rows = state.board.get_rows(state.next_player)
            if op_rows:
                state.complete_row(choice(op_rows))
                state.remove_ring(
                    choice(
                        [
                            hex
                            for hex, ring in state.board.rings.items()
                            if ring.value == state.next_player.value
                        ]
                    )
                )
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


def search(state: GameState, nodes: int, time: float, temperature: float):
    root = Node(state.next_player, temperature, state)
    start = timer()
    for _ in trange(nodes, ncols=100):
        node = root.select_leaf()
        node.expand()
        outcome = node.simulate()
        node.backpropagate(outcome.winner)

        if timer() - start >= time:
            break
    # Select by max visits, q value as tiebreak
    return max(root.children.items(), key=lambda item: (item[1].visits, item[1].q()))[0]
