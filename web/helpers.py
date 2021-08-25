import json
from random import choice

from yinsh.game import GameState, Move
from yinsh.helpers import coordinate_index
from yinsh.types import Hex, IllegalMoveError, Marker, Ring

content_index = {None: 0, Ring.WHITE: 1, Ring.BLACK: 2, Marker.WHITE: 3, Marker.BLACK: 4}
inv_content_index = {v: k for k, v in content_index.items()}


def handle_place(hex: Hex, game: GameState):
    if game.is_over() or not game.requires_setup:
        return
    move = Move.place(hex)
    try:
        game.make_move(move)
        return dump_data(game)
    except IllegalMoveError:
        return


def handle_play(src_hex: Hex, dst_hex: Hex, game: GameState):
    if game.is_over() or game.requires_setup:
        return
    move = Move.play(src_hex, dst_hex)
    try:
        game.make_move(move)
        return dump_data(game)
    except IllegalMoveError:
        return


def handle_dsts(hex: Hex, game: GameState):
    if game.is_over() or game.requires_setup:
        return
    valid_dsts = [
        coordinate_index[move.dst_hex] for move in game.legal_moves if move.src_hex == hex
    ]
    print(valid_dsts)
    if valid_dsts:
        return json.dumps(valid_dsts)


def handle_bot(game: GameState):
    game.next_player = game.next_player.other
    move = choice(list(game.legal_moves))
    game.make_move(move)
    return dump_data(game)


def parse_data(data: dict):
    hex = data.get("action")
    if hex is not None:
        hex = Hex(*hex.values())
    game = GameState.parse_state(data["state"])
    return hex, game


def parse_play_data(data: dict):
    action = data["action"]
    src_hex = Hex(*action["src"].values())
    dst_hex = Hex(*action["dst"].values())
    game = GameState.parse_state(data["state"])
    return src_hex, dst_hex, game


def dump_data(game: GameState):
    grid = {
        coordinate_index[hex]: content_index[content] for hex, content in game.board._grid.items()
    }
    data = {
        "state": {
            "grid": grid,
            "rings": {"white": game.players.white.rings, "black": game.players.black.rings},
            "requiresSetup": game.requires_setup,
        }
    }
    return json.dumps(data)
