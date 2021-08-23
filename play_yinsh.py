import ast
import sys
from random import choice

from yinsh.game import GameState, Move
from yinsh.types import Hex, Player


def run(color: bool = True):
    human = Player.WHITE if color else Player.BLACK
    game = GameState.new_game()
    while not game.is_over():
        while game.requires_setup:
            if game.next_player == human:
                while True:
                    try:
                        game.display()
                        coords = ast.literal_eval(input("Coordinates (x, y): "))
                        move = Move.place(Hex(*coords))
                        print(move)
                        game.make_move(move)
                        break
                    except KeyboardInterrupt:
                        sys.exit()
                    except:
                        continue
            else:
                game.display()
                move = choice(list(game.legal_moves))
                print(move)
                game.make_move(move)

        if game.next_player == human:
            while True:
                try:
                    game.display()
                    src_hex = Hex(*ast.literal_eval(input("Ring Coordinates (x, y): ")))
                    valid_targets = list(
                        enumerate(
                            sorted(
                                [
                                    move.dst_hex.axial
                                    for move in game.legal_moves
                                    if move.src_hex == src_hex
                                ]
                            )
                        )
                    )
                    target_fmt = [f"{i}) {t}" for i, t in valid_targets]
                    print(" | ".join(target_fmt))
                    dst_idx = int(input("Target Choice (i): "))
                    dst_hex = valid_targets[dst_idx][1]
                    move = Move.play(src_hex, dst_hex)
                    print(move)
                    game.make_move(move)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    continue
        else:
            game.display()
            move = choice(list(game.legal_moves))
            print(move)
            game.make_move(move)

    print(game.outcome())


if __name__ == "__main__":
    color_input = input("(W)hite or (B)lack? ").lower()
    if color_input.startswith("w"):
        color = True
    elif color_input.startswith("b"):
        color = False
    else:
        color = choice([True, False])

    run(color)
