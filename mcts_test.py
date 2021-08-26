from random import choice

from yinsh import mcts
from yinsh.game import GameState

game = GameState.new_game()
turn = True
while not game.is_over():
    if turn:
        game.make_move(mcts.search(game, 6400, 3600, 1.41))
    else:
        game.make_move(choice(list(game.legal_moves)))
    turn = not turn

    # Handle rows
    rows = game.board.get_rows(game.next_player.other)  # Player who moved last
    if rows:
        game.complete_row(choice(rows))
        game.remove_ring(
            choice(
                [
                    hex
                    for hex, ring in game.board.rings.items()
                    if ring.value == game.next_player.other.value
                ]
            )
        )
        # Check if this ended the game
        if (game.next_player.other.value and game.rings.white == game._rings_to_win) or (
            not game.next_player.other.value and game.rings.black == game._rings_to_win
        ):
            break

    op_rows = game.board.get_rows(game.next_player)
    if op_rows:
        game.complete_row(choice(op_rows))
        game.remove_ring(
            choice(
                [
                    hex
                    for hex, ring in game.board.rings.items()
                    if ring.value == game.next_player.value
                ]
            )
        )
print(game.outcome())
