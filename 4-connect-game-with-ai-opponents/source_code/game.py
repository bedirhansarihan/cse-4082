import math
import random
import typing

import constants
from board import Board
from players.player import Player
from players.human import Human
from players.ai import Ai

class Game:

    def __init__(self, player_1, player_2, depth= None):

        self.board = Board()

        self.player_1 = player_1
        self.player_2 = player_2
        self.players = [self.player_1, self.player_2]
        self.ply = 0
        self.depth = depth
        self.start_game()

    def is_move_valid(self, board: Board, movement: int) -> bool:
        """
        checks if column is not full
        :return:
        """
        if board.board_matrix[0][movement] in [1, 2]:
            return False
        else:
            return True

    def is_terminal_board(self, board: Board):
        """
        Checking if terminal is reached for minimax algorithm
        :param board:
        :return:
        """
        return self.is_game_over(board, self.player_1) or self.is_game_over(board, self.player_2) or len(
            self.get_valid_locations(board)) == 0

    def get_valid_locations(self, board) -> typing.List[int]:
        """
        it lists valid moves that can be played
        :param board:
        :return:
        """
        valid_locations = []
        for col_movement in range(constants.COL_SIZE):
            if self.is_move_valid(board, col_movement):
                valid_locations.append(col_movement)
        return valid_locations

    def change_turn(self) -> None:
        for p in self.players:
            p.is_turn = not p.is_turn

    def check_any_moves_left(self) -> bool:
        """
        checks if there are any moves left to move
        :return:
        """
        if all(piece != 0 for piece in self.board.board_matrix[0]):
            return True
        else:
            return False

    def last_piece_location(self, movement) -> typing.Tuple[int, int]:
        """
        returns the coordinates of the last move
        :param movement:
        :return:
        """
        for row_idx, row in enumerate(self.board.board_matrix):
            for col_idx, piece in enumerate(row):
                if movement == col_idx:
                    if piece != 0:
                        return row_idx, col_idx

    def is_game_over(self, board: Board, player: Player) -> bool:
        """
        It scans the whole board into 4 pieces and checks whether there are 4 pieces next to each other.

        :param board:
        :param player:
        :return:
        """
        # HORIZONTAL
        for c in range(constants.COL_SIZE - 3):
            for r in range(constants.ROW_SIZE):
                if board.board_matrix[r][c] == player.piece_color and board.board_matrix[r][c+1] == player.piece_color and \
                        board.board_matrix[r][c+2] == player.piece_color and board.board_matrix[r][c+3] == player.piece_color:
                    return True

            # VERTICAL

        for c in range(constants.COL_SIZE):
            for r in range(constants.ROW_SIZE - 3):
                if board.board_matrix[r][c] == player.piece_color and board.board_matrix[r+1][c] == player.piece_color and \
                        board.board_matrix[r + 2][c] == player.piece_color and board.board_matrix[r + 3][c] == player.piece_color:
                    return True
        # POSITIVE SLOPE
        for c in range(constants.COL_SIZE - 3):
            for r in range(constants.ROW_SIZE - 3):
                if board.board_matrix[r][c] == player.piece_color and board.board_matrix[r+1][c+1] == player.piece_color and \
                        board.board_matrix[r+2][c+2] == player.piece_color and board.board_matrix[r+3][c+3] == player.piece_color:
                    return True
        # NEGATIVE SLOPE
        for c in range(constants.COL_SIZE - 3):
            for r in range(3, constants.ROW_SIZE):
                if board.board_matrix[r][c] == player.piece_color and board.board_matrix[r-1][c+1] == player.piece_color and \
                        board.board_matrix[r-2][c+2] == player.piece_color and board.board_matrix[r-3][c+3] == player.piece_color:
                    return True

        return False

    def minimax(self, board, player: Ai, opp_player: Ai, depth, alpha, beta, is_maximizer) -> typing.Tuple:
        """
        minimax works recursively until it lands on the terminal. When you go down to the terminal, 1000 or -1000 score is determined according to whether the game is over
        according to the opponent and himself. If the game is not finished at the terminal, the score is calculated and the move col index and the score itself are returned.

        :param board:
        :param player:
        :param opp_player:
        :param depth:
        :param alpha:
        :param beta:
        :param is_maximizer:
        :return:
        """
        all_possible_moves = self.get_valid_locations(board)

        is_terminal = self.is_terminal_board(board)
        if depth == 0 or is_terminal:
            if is_terminal:

                if self.is_game_over(board, player):
                    return None, 1000

                elif self.is_game_over(board, opp_player):
                    return None, -1000

                elif self.check_any_moves_left():  # true if there is no move
                    return None, 0

            else:
                return None, self.calculate_score(board, player)

        if is_maximizer:
            score = -math.inf

            best_possible_move = random.choice(all_possible_moves)
            for col_idx in all_possible_moves:

                b_copy = board.board_copy()
                player.move(movement=col_idx, board=b_copy)
                new_score = self.minimax(b_copy, player, opp_player, depth - 1, alpha, beta, False)[1]
                if new_score > score:
                    score = new_score
                    best_possible_move = col_idx
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return best_possible_move, score

        else:
            score = math.inf
            best_possible_move = random.choice(all_possible_moves)
            for col_idx in all_possible_moves:

                b_copy = board.board_copy()
                opp_player.move(movement=col_idx, board=b_copy)
                new_score = self.minimax(b_copy, player, opp_player, depth - 1, alpha, beta, True)[1]
                if new_score < score:
                    score = new_score
                    best_possible_move = col_idx
                alpha = min(alpha, score)
                if alpha >= beta:
                    break
            return best_possible_move, score

    def calculate_score(self, board: Board, player: Ai):
        """
        While calculating the score of each board, all the four combinations on the board are sent to the heuristic method as parameters
        and the score is determined according to the piece values in it.
        :param board:
        :param player:
        :return:
        """
        score = 0

        if player.difficulty == 'hard':
            # +3 score is added for each piece in the middle of the board
            for row_idx in range(constants.ROW_SIZE):

                if board.board_matrix[row_idx][constants.COL_SIZE // 2] == player.piece_color:
                    score += 3

        # VERTICAL
        for col_idx in range(constants.COL_SIZE):
            for row_idx in range(constants.ROW_SIZE - 3):
                score += self.heuristic(board.board_matrix[row_idx: row_idx + 4], player)
        # HORIZONTAL
        for row_idx in range(constants.ROW_SIZE):

            for col_idx in range(constants.COL_SIZE - 3):
                score += self.heuristic(board.board_matrix[col_idx: col_idx + 4], player)
        # POSITIVE DIAGONAL
        for row_idx in range(constants.ROW_SIZE - 3):
            for col_idx in range(constants.COL_SIZE - 3):
                score += self.heuristic([board.board_matrix[row_idx + i][col_idx + i] for i in range(4)], player)
        # NEGATIVE DIAGONAL
        for row_idx in range(constants.ROW_SIZE - 3):
            for col_idx in range(constants.COL_SIZE - 3):
                score += self.heuristic([board.board_matrix[row_idx + 3 - i][col_idx + i] for i in range(4)], player)

        # print(f"test_ {score}")
        # pprint.pprint(board.board_matrix)
        return score

    def heuristic(self, sub_board: list, player: Ai) -> int:

        score = 0
        opp_player = 2 if player.piece_color == 1 else 1


        player_count, opp_player_count = 0, 0
        for piece in sub_board:
            if piece == opp_player:
                opp_player_count += 1
            elif piece == player.piece_color:
                player_count += 1

        if player.difficulty == 'easy':
            """
            If the opponent has 3 pieces next to each other, make the score -1, otherwise the score of the board is 0 unless there is a win condition.
            """
            if opp_player_count == 3 and player_count == 0:
                score = -1


        elif player.difficulty == 'medium':
            """
            For 3 pieces next to each other, it increases the score by 5, for 2 pieces next to each other, it increases the score by 2. If the opponent's 3 pieces are next to each other, it makes the score -1.
            """


            if player_count == 3 and opp_player_count == 0:
                score += 5

            elif player_count == 2 and opp_player_count == 0:
                score +=2

            if opp_player_count == 3 and player_count == 0:
                score = -1


        elif player.difficulty == 'hard':
            """
           In addition to the medium difficulty level, +3 is added to the score for each piece in the middle of the board. It also deducts 2 from the score 
           when the opponenthas 2 pieces next to each other. (adding process is in calculate_score method)
            """

            if player_count == 3 and opp_player_count == 0:
                score += 5

            elif player_count == 2 and opp_player_count == 0:
                score += 2

            if opp_player_count == 2 and player_count == 0:
                score -=2

            if opp_player_count == 3 and player_count == 0:
                score = -1



        return score

    def start_game(self) -> None:
        while True:
            self.ply += 1
            if self.player_1.is_turn:
                print(f" PLAYER 1 TURN!!")

                if isinstance(self.player_1, Human):
                    movement = int(input(
                        "In which column are you going to put a piece? between 0-7"))
                    print(f" Player 1 Human plays column '{movement}'")
                else:
                    movement, minimax_score = self.minimax(self.board, self.player_1, self.player_2, self.depth, -math.inf, math.inf, True)
                    print(f" Player 1 Ai plays column '{movement}'")
                    print(f"minimax score for PLAYER 1:   {minimax_score}")

                if self.is_move_valid(self.board, movement):
                    self.player_1.move(movement, self.board)

                    if self.is_game_over(self.board, self.player_1):
                        print(f"GAME OVER 'Player 1' WINS")
                        print("NUMBER OF PLIES: ", self.ply)

                        self.board.print_board()

                        return

                    self.change_turn()
                    self.board.print_board()
                else:
                    print(f"COLUMN {movement} IS NOT EMPTY, SELECT ANOTHER COLUMN")

            elif self.player_2.is_turn:
                print(f" PLAYER 2 TURN!!")

                if isinstance(self.player_2, Human):
                    movement = int(input(
                        "In which column are you going to put a piece? between 0-7"))
                    print(f" Player 2 Human plays column '{movement}'")
                else:
                    movement, minimax_score = self.minimax(self.board, self.player_2, self.player_1, self.depth, -math.inf, math.inf, True)
                    print(f" Player 2 Ai plays column '{movement}'")
                    print(f"minimax score for PLAYER 2:   {minimax_score}")
                if self.is_move_valid(self.board, movement):
                    self.player_2.move(movement, self.board)

                    if self.is_game_over(self.board, self.player_2):
                        print(f"GAME OVER 'Player 2' WINS")
                        print("NUMBER OF PLIES: ", self.ply)
                        self.board.print_board()
                        return

                    self.change_turn()
                    self.board.print_board()
                else:
                    print(f"COLUMN {movement} IS NOT EMPTY, SELECT ANOTHER COLUMN")
