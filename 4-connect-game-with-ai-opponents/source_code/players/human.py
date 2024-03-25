from abc import ABC

from players.player import Player


class Human(Player):

    def __init__(self, piece_color, is_turn):
        super().__init__(piece_color=piece_color, is_turn= is_turn)


