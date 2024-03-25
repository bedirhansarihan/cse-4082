from abc import ABC, abstractmethod

import constants
from board import Board


class Player(ABC):


    def __init__(self, piece_color: int, is_turn: bool):

        self.piece_color: int = piece_color
        self.is_turn: bool = is_turn

    def move(self, movement: int, board: Board, *args, **kwargs):

        for row_idx, row_list in enumerate(board.board_matrix):
            for col_idx, piece in enumerate(row_list):
                if col_idx == movement:
                    if board.board_matrix[row_idx][col_idx] in [1,2] or all(row[col_idx] == 0 for row in board.board_matrix):
                        board.board_matrix[row_idx - 1][col_idx] = self.piece_color
                        return None
