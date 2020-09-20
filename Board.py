from constants import *


# noinspection PyRedundantParentheses,PyMethodMayBeStatic
class Board:
    def __init__(self):
        self._positions = []
        self._col_dict = {}
        self._init_board()
        self._col_dict = {}
        self._init_col_dict()

    def _init_col_dict(self):
        for i in range(len(COL_STRING)):
            self._col_dict[i] = COL_STRING[i]
            self._col_dict[COL_STRING[i]] = i

    def _init_board(self):
        for i in range(20):
            self._positions.append([])
            for j in range(20):
                self._positions[i].append(None)

    def convert_ltr_col(self, val):
        return self._col_dict[val]

    def convert_to_pos(self, coord: str):
        return (int(coord[1:]) - 1, self.convert_ltr_col(coord[0]))

    def convert_to_coord(self, pos: tuple):
        return self.convert_ltr_col(pos[1]) + str(pos[0]+1)

    def get_piece_at_pos(self, pos: tuple):
        row, col = pos
        return self._positions[row][col]

    def get_positions(self):
        return self._positions

    def get_direction(self, start: tuple, end: tuple):
        s_row, s_col = start
        e_row, e_col = end
        direction = [None, None]

        if s_row != e_row:
            if s_row < e_row:
                direction[0] = UP
            else:
                direction[0] = DOWN

        if s_col != e_col:
            if s_col < e_col:
                direction[1] = RIGHT
            else:
                direction[1] = LEFT

        if direction[0] is not None and direction[1] is not None:
            if abs(s_row - e_row) != abs(s_col - e_col):
                return None

        return (DIR_DICT[direction[0]], DIR_DICT[direction[1]])

    def add_stone(self, stone, pos: tuple):
        row, col = pos
        self._positions[row][col] = stone

    def update_pos(self, pos: tuple,  stone=None):
        row, col = pos
        self._positions[row][col] = stone

    def find_empty_neighbors(self, pos: tuple):
        empty_list = []
        row, col = pos
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and self.get_piece_at_pos((row + i, col + j)) is None:
                    empty_list.append((row + i, col + j))

        return empty_list

    def is_valid_pos(self, pos: tuple, piece: bool = True):
        row, col = pos
        if not piece:
            min_pos = 1
            max_pos = NUM_ROWS - 2
        else:
            min_pos = 0
            max_pos = NUM_ROWS - 1

        if row < min_pos or row > max_pos:
            return False

        if col < min_pos or col > max_pos:
            return False

        return True

    def is_unobstructed(self, start, dest):
        direction = self.get_direction(start, dest)
        cur_row, cur_col = start
        e_row, e_col = dest

        cur_row += direction[0]
        cur_col += direction[1]
        while cur_row != e_row or cur_col != e_col:
            if self.get_piece_at_pos((cur_row, cur_col)) is not None:
                return False
            cur_row += direction[0]
            cur_col += direction[1]

        return True
