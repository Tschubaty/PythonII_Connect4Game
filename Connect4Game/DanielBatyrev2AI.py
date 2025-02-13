import Connect4Game as Game
import random


class RandomStrategy2(Game.Connect4GameStrategy):
    def __init__(self, name="Daniel Batyrev 2"):
        self.name = name

    @classmethod
    def strategy(cls, game_safety_copy):
        valid_moves = list()
        for col in range(7):
            if game_safety_copy.is_valid_move(col):
                valid_moves.append(col)
        return min(valid_moves)
