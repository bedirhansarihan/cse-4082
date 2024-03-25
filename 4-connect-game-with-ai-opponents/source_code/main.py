from game import Game
from players.human import Human
from players.ai import Ai
from constants import *

# CONSTANTS
RED = 2
BLUE = 1

"""
YASİN ALPER BİNGÜL 170517033
BEDİRHAN SARIHAN   150119692
"""





def run():
    game_type = input("Would you like to play with\n"
                        "1 - Human vs Human\n"
                        "2 - Human vs Ai\n"
                        "3 - Ai vs Ai\n"
                        "Type (1 or 2 or 3): ")


    if game_type == "1":        # human vs human
        game = Game(player_1=Human(piece_color=BLUE, is_turn=True),
                    player_2=Human(piece_color=RED, is_turn=False)
                )

    elif game_type == "2":      # human vs ai
        difficulty_input = input("Select difficulty for AI (easy, medium, hard): ")
        depth_input = int(input("Select depth: "))

        game = Game(player_1=Human(piece_color=BLUE, is_turn=True),
                    player_2=Ai(piece_color=RED, is_turn=False, difficulty= difficulty_input),
                    depth=depth_input
                )

    elif game_type == "3":      # ai vs ai
        difficulty_input_1 = input("Select difficulty for first AI (easy, medium, hard): ")
        difficulty_input_2 = input("Select difficulty for second AI (easy, medium, hard): ")
        depth_input = int(input("Select depth: "))

        game = Game(player_1=Ai(piece_color=BLUE, is_turn=True, difficulty= difficulty_input_1),
                    player_2=Ai(piece_color=RED, is_turn=False, difficulty= difficulty_input_2),
                    depth=depth_input
                )


if __name__ == '__main__':
    run()
