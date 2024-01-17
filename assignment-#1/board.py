import copy
import pprint
import random
import typing
import itertools

class Board():

    new_id = itertools.count()

    def __init__(self, board= None, heuristic_type= "ordered"):
        self.heuristic_type = heuristic_type

        self.board: typing.List[list] = [
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
        ] if board == None else board


        self.number_of_peg: int = self.peg_count()
        self.possible_moves = self.all_possible_moves()

        self.node_id = next(Board.new_id)
        self.depth = 0

        self.is_visited = False
        self.parent = None
        self.childrens  = None


    def find_depth(self, board_obj):
        """ calculates current board depth"""
        depth = board_obj.depth + 1
        return depth

    def __repr__(self):

        return repr(f"object node:  {self.node_id} ")

    def all_possible_moves(self):
        """
        it calculates for all possible moves and stores them. DOES NOT MOVE! only possible moves coordinates
        :return:
        """
        possible_moves = []
        OFFSET = [(2, 0), (-2, 0), (0, -2), (0, 2)]

        for x, row in enumerate(self.board):
            for y,  peg in enumerate(row):

                if self.board[x][y] == 1:

                    for mx, my in OFFSET:
                        if 6 >= x + mx >= 0 and 6 >= y + my >= 0:
                            if self.board[x + mx][y + my] == 0:
                                if self.board[(x*2 + mx)//2 ][(y*2 + my)//2] == 1:
                                    possible_moves.append(((x, y), (x + mx, y + my)))

        return possible_moves

    # it calculates number of pegs for current board
    def peg_count(self)-> int:
        count = 0
        for row in self.board:
            for peg in row:
                if peg == 1:
                    count += 1
        return count


    def copy(self):
        """
        deep copy of current board
        :return:
        """
        board_copy = [[peg for peg in row] for row in self.board]

        return Board(board_copy, self.heuristic_type)

    def create_childrens(self):
        """
        it creates current board obj's childrens as a list according
        sorting styles: random, ordered, heuristic
        :return:
        """

        childrens: typing.List[Board] = []

        if len(self.possible_moves) != 0:
            for (x,y), (new_x,new_y) in self.possible_moves:
                new_board_obj = self.copy()
                new_board_obj.board[x][y] = 0
                new_board_obj.board[(x+new_x)//2 ][(y +new_y)//2] = 0  # todo check
                new_board_obj.board[new_x][new_y] = 1
                new_board_obj.parent = self

                childrens.append(new_board_obj)
                new_board_obj.depth = self.find_depth(self)


        if len(childrens) == 0:
            return None
        # ordered
        elif self.heuristic_type == "ordered":
            childrens.sort(key=lambda board: board.number_of_peg)
            return childrens
        # it shuffles list
        elif self.heuristic_type == "random":

            random.shuffle(childrens)
            return childrens

        # branches from the beginning and then the end of the list
        elif self.heuristic_type == "heuristic":
            # total = 0
            # for child in childrens:
            #     total += child.number_of_peg
            #
            # avg = total // len(childrens)
            #
            # for id, child in enumerate(childrens):
            #     #print(f" avg: {avg}, children_id: {child.node_id},    children_peg_coun:  {child.number_of_peg}")
            #     distance = abs(avg - child.number_of_peg)
            #     if distance != 0:
            #         print(print(f" avg: {avg}, children_id: {child.node_id},    children_peg_coun:  {child.number_of_peg}")

               # print(distance)
            #print("*********************************************")

            if self.node_id // 2 == 0:
                childrens.sort(key=lambda board: board.number_of_peg)
                return childrens
            else:
                childrens.sort(key=lambda board: board.number_of_peg, reverse=True)  # sort according to peg numbers
                return childrens


"""
[2,2,1,1,1,2,2]
[2,2,1,1,1,2,2]
[1,1,1,1,1,1,1]
[1,1,1,0,1,1,1]
[1,1,1,1,1,1,1]
[2,2,1,1,1,2,2]
[2,2,1,1,1,2,2]

Step 1. Borad'da 1 var mı yok mu kontrol et
        - 1 varsa:
            - İlgili pegin sağında, solunda, yukarısında, aşağısında 1 var mı kontrol et
            - İlgili pegin 2 sağında, 2 solunda, 2 yukarısında, 2 aşağısında 0 var mı kontrol et

            - İki karşılaştırma sağlanıyorsa:
                - Listeye atlanmış halini ekle
                - Parent board'daki dizilimden başka bir atlama komnbinasyonu aramaya devam et

        - 1 yoksa:
            - 1 aramaya devam et

Step 2.


"""