import time
import logging
from board import Board
"""
Depth First Search:
1- Frontier'e ilk board'u ekle, İterasyona başla:
    a- Eklenen node'un childlarını oluştur.
       - Eğer child yoksa frontier'den çıkar, explore'a ekle,
       - Frontier'den çıkarılan child'ın parentına git
       - c'den devam et.

    b- Child'ları aralarında sırala (peg sayılarına göre)
    c- Sıralanmış child'lardan visited olmayan ilkini frontier'e ekle
    d- a'ya dön
"""
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
class DepthFirstSearch:


    def __init__(self, heuristic_type= "ordered"):
        self.frontier= [] # LIFO
        self.initial_board = Board(heuristic_type= heuristic_type)
        self.frontier.append(self.initial_board)

        self.max_frontier_count = 0
        self.best_board: Board = self.initial_board
        self.nof_expanded_board = 0
        self.explored_board_count = 0
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

        logger.info("---------- DEPTH FIRST SEARCH starts")
        try:
            while True:

                current_board = self.frontier[-1]
                current_board.childrens = current_board.create_childrens()

                if len(self.frontier) == 0:

                    logger.info(
                        f"explored count: {self.explored_board_count}, expanded node count: {self.nof_expanded_board} Frontier count: {len(self.frontier)}, Max frontier count: {self.max_frontier_count}  FRONTIER HAS NO ANY ITEM ")
                    return

                # if current_board's childrens are None, it checks whether current board is goal state or not
                elif current_board.childrens is None:
                    self.explored_board_count += 1

                    if self.check_solution(current_board):
                        logger.info("SOLUTION FOUND")
                        logger.info(f"explored count: {self.explored_board_count}, expanded node count: {self.nof_expanded_board} Frontier count: {len(self.frontier)}, Max frontier count: {self.max_frontier_count}, "
                                    f"Best Solution: {self.best_board.number_of_peg}, Best board: {self.best_board.board}")
                        return

                    # if board is not optimal, check whether it is suboptimal or not
                    else:
                        if self.best_board.number_of_peg > current_board.number_of_peg:
                            self.best_board = current_board

                        current_board.is_visited = True
                        self.frontier.pop()

                # if current_board has childrens,append the smallest unvisited board to the frontier
                elif (current_board.childrens is not None) and len(current_board.childrens) > 0:
                    self.nof_expanded_board+= 1
                    for child in current_board.childrens:
                            if child.is_visited == False:
                                self.frontier.append(child)
                                if self.max_frontier_count < len(self.frontier):
                                    self.max_frontier_count = len(self.frontier)

                                current_board.childrens.remove(child)
                                break
        except KeyboardInterrupt:
            logger.error("KEYBOARD INTERRUPT")
            logger.info(f"explored count: {self.explored_board_count}, expanded node count: {self.nof_expanded_board} Frontier count: {len(self.frontier)}, Max frontier count: {self.max_frontier_count}, "
                        f" Best Solution: {self.best_board.number_of_peg} Best board: {self.best_board.board}")


if __name__ == '__main__':

    # DFS with ordered childrens
    # DepthFirstSearch(heuristic_type= "ordered")

    # # DFS with random childrens
    # DepthFirstSearch(heuristic_type= "random")

    # DFS with heuristic
    DepthFirstSearch(heuristic_type="heuristic")
