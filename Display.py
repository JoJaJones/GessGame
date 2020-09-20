from Board import Board
from constants import *


# noinspection PyMethodMayBeStatic
class Display:
    def __init__(self, board, empty, black, white):
        self._board = board
        self._board_converter = {empty: None, black: BLACK, white: WHITE}
        self._col_dict = {}
        self._init_col_dict()

    def _init_col_dict(self):
        for i in range(len(COL_STRING)):
            self._col_dict[i] = COL_STRING[i]
            self._col_dict[COL_STRING[i]] = i

    def convert_ltr_col(self, val):
        return self._col_dict[val]

    def print_board(self):
        print("\033[30;107m    ", end="")
        for i in range(20):
            print(f"   {self.convert_ltr_col(i)}  ", end="")
        print("     "+CLEAR_COLOR)

        for i in range(41):
            if i % 2:
                self.print_space_row(i//2)
            else:
                self.print_divider_row(i)

        print("\033[30;107m    ", end="")
        for i in range(20):
            print(f"   {self.convert_ltr_col(i)}  ", end="")
        print("     "+CLEAR_COLOR)

    def print_divider_row(self, row_num):
        row_str = FIRST_COLOR_SET
        for i in range(ROW_LENGTH):
            if i % JUNCTION_FREQ == 0:
                row_str += self.get_junc_type(row_num, i)
            else:
                row_str += PIPES[0]

        print("\033[30;107m    " + row_str + "\033[30;107m    " + CLEAR_COLOR)

    def print_space_row(self, num):
        piece_list = [FIRST_COLOR_SET] + [self.convert_piece_to_color(stone)
                                          for stone in self._board.get_positions()[-(num+1)]] + ["\033[30;107m"]
        piece_list = PIPES[1].join(piece_list)

        print(f"\033[30;107m {20-num:2} " + piece_list + f" {20 - num:2} ", end=CLEAR_COLOR + "\n")

    def convert_piece_to_color(self, stone):
        t = type(stone)
        if t != str and t != int and t != type(None):
            stone = stone.get_color()

        return SPACE_DICT[stone]

    def get_junc_type(self, row, col):
        if col % (ROW_LENGTH - 1) == 0 and row % (40) == 0:
            return CORNERS_DICT[(row, col)]
        elif row == 0:
            return JUNCTIONS[DOWN]
        elif col == 0:
            return JUNCTIONS[RIGHT]
        elif row == 40:
            return JUNCTIONS[UP]
        elif col == ROW_LENGTH -1:
            return JUNCTIONS[LEFT]
        else:
            return JUNCTIONS[ALL]