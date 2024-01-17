import time
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
class IterativeDeepeningSearch:

    def __init__(self, max_depth_limit):


        self.frontier= [] # LIFO
        self.explored = []
        self.initial_board = Board()
        self.frontier.append(self.initial_board)

        self.max_frontier_count = 0
        self.best_board = self.initial_board
        self.max_depth_limit = max_depth_limit

        self.search()


    def check_solution(self,board_obj: Board):

        if board_obj.number_of_peg == 1 and board_obj.board[3][3] == 1:
            return True
        else:
            return False

    def search(self):
        logger.info("DEPTH LIMITED SEARCH STARTS")
        try:
            while True:
                current_board: Board = self.frontier[-1]
                if self.max_frontier_count < len(self.frontier):
                    self.max_frontier_count = len(self.frontier)


                if current_board.depth == self.max_depth_limit:
                    popped_board = self.frontier.pop()
                    if  popped_board.parent is None:
                        logger.info("DEPTH LIMITED SEARCH COMPLETED")
                        logger.info(
                            f"DEPTH_LIMIT: {self.max_depth_limit},best solution: {self.best_board.number_of_peg} board_scheme = {self.best_board.board}, max frontier: {self.max_frontier_count}")
                        return

                    if self.check_solution(popped_board):
                        logger.info("BEST SOLUTION FOUND ")
                        logger.info(f"frontier_size: {self.frontier} ")
                        return "SOLUTION FOUND"

                    else:
                        if self.best_board.number_of_peg >  popped_board.number_of_peg:
                            self.best_board = popped_board

                        popped_board.is_visited = True
                        parent_board = popped_board.parent


                        for child in parent_board.childrens:

                            if child.is_visited == False:
                                self.frontier.append(child)
                                break
                        else:
                            if self.check_solution(parent_board):
                                logger.info("BEST SOLUTION FOUND ")
                                logger.info(f"frontier_size: {self.frontier} ")
                                return "SOLUTION FOUND"
                            else:

                                self.frontier.pop()
                                if len(self.frontier) == 0:
                                    logger.info("DEPTH LIMITED SEARCH COMPLETED")
                                    logger.info(
                                        f"DEPTH_LIMIT: {self.max_depth_limit},best solution: {self.best_board.number_of_peg} board_scheme = {self.best_board.board}, max frontier: {self.max_frontier_count}")
                                    return
                else:           # karşılamıyorsa

                    if current_board.childrens is None:
                        current_board.childrens = current_board.create_childrens()

                    if current_board.childrens is not None:
                        for child in current_board.childrens:

                            if child.is_visited == False:
                                self.frontier.append(child)
                                break
                        else:

                            current_board.is_visited = True
                            self.frontier.pop()
                            if len(self.frontier) == 0:
                                logger.info("DEPTH LIMITED SEARCH COMPLETED")
                                logger.info(f"DEPTH_LIMIT: {self.max_depth_limit},best solution: {self.best_board.number_of_peg}, max frontier: {self.max_frontier_count} board_scheme = {self.best_board.board}")
                                return

        except KeyboardInterrupt:
            logger.error("KEYBOARD INTERRUPT")
            logger.info(f"DEPTH_LIMIT: {self.max_depth_limit},best solution: {self.best_board.number_of_peg}, max frontier: {self.max_frontier_count} board_scheme = {self.best_board.board}")

        except Exception as e:
            logger.error("ERROR")
            logger.info(f"DEPTH_LIMIT: {self.max_depth_limit}, best solution: {self.best_board.number_of_peg}, max frontier: {self.max_frontier_count} board_scheme = {self.best_board.board}")

"""
Depth First Search:
- Frontier'e ilk board'u ekle, iterasyona başla,
    a - Depth limitini karşılıyor mu onu kontrol et:
        - Karşılıyorsa:
            - Expanded node'a ekle, frontier'den çıkart
            - Parent'ı varsa parent'ına git.
                -Eğer child'ı varsa:
                    - Sıradaki child'ı frontier'e ekle
                -Eğer child'ı yoksa:
                    - İlgili seçili olan parent'ı explored'a ekle
                    - Seçili olan parent'ın parent'ına git.

            - a'ya dön.
        - Karşılamıyorsa:
            - DFS'e devam et (childlarını oluştur, child'ı varsa sıradakinden devam et)
                -Child varsa:
                    -sıradaki child'ı frontier'e ekle
                -Child yoksa:
                    - Expand et
                    - 0. depth'te miyiz kontrol et.
                        -Öyleyse programı durdur.
            - a'ya dön
"""




if __name__ == '__main__':
    MAX_DEPTH = 10

    for i in range(1,MAX_DEPTH):
        IterativeDeepeningSearch(max_depth_limit=i)















