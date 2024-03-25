
from players.player import Player


class Ai(Player):

    def __init__(self, piece_color, is_turn, difficulty):
        super().__init__(piece_color=piece_color, is_turn=is_turn)


        self.difficulty = difficulty

