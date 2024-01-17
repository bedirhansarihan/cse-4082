import collections
import pprint
import time
import typing
import logging

from board import Board

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log', encoding='utf8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class BreadthFirstSearch:


    def __init__(self):
        self.frontier= []

        self.max_frontier_count = 0

        self.no_of_expanded_board = 0
        self.initial_board = Board()
        self.frontier.append(self.initial_board)
        self.best_board: Board = self.initial_board
        self.search()

    def check_solution(self,board_obj: Board):
        """
               it checks whether board is goal state or not
               :param board_obj:
               :return:
        """
        if board_obj.number_of_peg == 1 and board_obj.board[3][3] == 1:
            return True
        else:
            return False

    def search(self):

        logger.info("----------Breadth First Search Starts")

        while True:
                try:
                    board_obj = self.frontier[0]



                    if len(self.frontier) == 0:
                        logger.info(f"Explored count: {self.no_of_expanded_board}, Frontier count: {len(self.frontier)}, Max frontier count: {self.max_frontier_count}  ")
                        return "There is no Solution"

                    # check whether solution is optimal or not
                    elif self.check_solution(board_obj):
                        print(f"Board id: {board_obj.node_id}, BOARD_DEPTH: {board_obj.depth}, PEG_COUNT: {board_obj.number_of_peg} length of frontier: {len(self.frontier)}")
                        logger.info(f"Explored count: {self.no_of_expanded_board}, Frontier count: {len(self.frontier)}, Max frontier count: {self.max_frontier_count}, "
                                    f"Best Solution: {self.best_board.number_of_peg} Best Board: {self.best_board.board}")
                        return board_obj

                    child_board_obj: typing.List[Board]= board_obj.create_childrens()       # creates childrens
                    # if board_obj has childrens, extends them into frontier and pop first element
                    if child_board_obj is not None:
                        self.no_of_expanded_board += 1
                        self.frontier.extend(child_board_obj)
                        if self.max_frontier_count < len(self.frontier):
                            self.max_frontier_count = len(self.frontier)

                        if self.best_board.number_of_peg > board_obj.number_of_peg:
                            self.best_board = board_obj


                        explored_board = self.frontier.pop(0)
                        explored_board.is_visited = True
                    #if there is no any childrens, just pop first element
                    else:

                        if self.max_frontier_count < len(self.frontier):
                            self.max_frontier_count = len(self.frontier)
                        # if board is not optimal, check whether it is suboptimal or not
                        if self.best_board.number_of_peg > board_obj.number_of_peg:
                            self.best_board = board_obj

                        explored_board = self.frontier.pop(0)
                        explored_board.is_visited = True
                except KeyboardInterrupt:
                    logger.info(
                        f" Frontier count: {len(self.frontier)}, Max frontier count: {self.max_frontier_count}, Best Solution: {self.best_board.number_of_peg}, Best Board: {self.best_board.board}", )
                except MemoryError as e:
                    logger.error("OUT OF MEMORY!!")
                    logger.info(f" Frontier count: {len(self.frontier)}, Max frontier count: {self.max_frontier_count}, Best Solution: {self.best_board}", )
                    break
if __name__ == '__main__':

    BreadthFirstSearch()