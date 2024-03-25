import pprint

import constants


class Board:

    def __init__(self, board= None):
        self.board_matrix =[
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],

    ]  if board == None else board


        self.depth = 0
        self.score = 0

    def print_board(self) -> None:

        pprint.pprint(self.board_matrix)
        print('\n')


    def board_copy(self):
        board_copy = [[piece for piece in row] for row in self.board_matrix]

        return Board(board_copy)