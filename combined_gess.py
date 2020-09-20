BLACK = "BLACK"
WHITE = "WHITE"

UNFINISHED = 'UNFINISHED'
BLACK_WON = 'BLACK_WON'
WHITE_WON = 'WHITE_WON'
WIN_STATES = [WHITE_WON, BLACK_WON]

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
ALL = "ALL"

NUM_ROWS = 20

COLOR_DICT = {BLACK: 0, 0: BLACK, WHITE: 1, 1: WHITE}

FIRST_COLOR_SET = "\033[43;90m"
BLACK_PIECE = f" \033[30;107m   {FIRST_COLOR_SET} "
WHITE_PIECE = f" \033[97;40m   {FIRST_COLOR_SET} "
BLANK_PIECE = "     "
CLEAR_COLOR = "\033[0m"

# noinspection SpellCheckingInspection
COL_STRING = "abcdefghijklmnopqrst"

SPACE_DICT = {None: BLANK_PIECE, WHITE: WHITE_PIECE, BLACK: BLACK_PIECE}

DIR_DICT = {UP: 1, DOWN: -1, RIGHT: 1, LEFT: -1, None: 0}

ROW_LENGTH = 121
JUNCTION_FREQ = (ROW_LENGTH - 1) // 20

CORNERS = [chr(9472+84), chr(9472+87), chr(9472+90), chr(9472+93)]
JUNCTIONS = {RIGHT: chr(9472+96), LEFT: chr(9472+99), UP: chr(9472+105), DOWN: chr(9472+102), ALL: chr(9472+108)}
PIPES = [chr(9472+80), chr(9472+81)]

CORNERS_DICT = {(0, 0): CORNERS[0], (0, ROW_LENGTH-1): CORNERS[1], (40, 0): CORNERS[2], (40, ROW_LENGTH-1): CORNERS[3]}


# noinspection SpellCheckingInspection
class GessGame:
    def __init__(self):
        self._board = Board()
        self._players = [Player(self._board, BLACK), Player(self._board, WHITE)]
        self._cur_turn = 0
        self._board_printer = Display(self._board, None, BLACK, WHITE)
        self._game_state = UNFINISHED
        self._board_printer.print_board()

    def ring_at_coord(self, coord, color):
        pos = self._board.convert_to_pos(coord)
        return self._players[COLOR_DICT[color]].pos_is_ring(pos)

    def get_game_state(self):
        return self._game_state

    def resign_game(self):
        self._game_state = WIN_STATES[self._cur_turn]

    def make_move(self, start: str, end: str):
        if start == end:
            return False

        if not (start[0].isalpha() and start[1:].isnumeric()):
            return False

        if not (end[0].isalpha() and end[1:].isnumeric()):
            return False

        if self._game_state != UNFINISHED:
            return False

        start = self._board.convert_to_pos(start)
        end = self._board.convert_to_pos(end)
        result = self._players[self._cur_turn].move_piece(start, end)
        self._players[self._cur_turn].find_rings()

        if not result:
            return False

        self._cur_turn ^= 1
        self._players[self._cur_turn].update_stones()
        self._players[self._cur_turn].find_rings()
        self._board_printer.print_board()

        if not self._players[self._cur_turn].has_rings():
            self._game_state = WIN_STATES[self._cur_turn]

        return True

    def is_valid_piece(self, coord):
        if type(coord) == str:
            coord = self._board.convert_to_pos(coord)
        piece = self._players[self._cur_turn].make_piece(coord)
        if piece and piece.is_valid():
            return True

        return False

    def check_move(self, start, end):
        if type(start) == str:
            start = self._board.convert_to_pos(start)

        if type(end) == str:
            end = self._board.convert_to_pos(end)

        piece = self._players[self._cur_turn].make_piece(start)
        if piece is None:
            return False

        return self._players[self._cur_turn].check_move(start, end)

    def piece_is_ringlocked(self, coord):
        if type(coord) == str:
            coord = self._board.convert_to_pos(coord)
        piece = self._players[self._cur_turn].make_piece(coord)
        return self._players[self._cur_turn].moving_breaks_rings(piece)

    def convert_input(self, data):
        if type(data) == str:
            return self._board.convert_to_pos(data)
        else:
            return self._board.convert_to_coord(data)


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


# noinspection PyMethodMayBeStatic
class Piece:
    def __init__(self, pos: tuple, color: str, board: Board):
        self._pos = pos
        self._board = board
        self._color = color
        self._stones = {}
        self._num_stones = 0
        self._center_stone = False
        self._max_move = 0
        self.load_stones()
        self._is_valid = True

    def get_pos(self):
        return self._pos

    def load_stones(self):
        row, col = self._pos
        for i in range(-1, 2):
            for j in range(-1, 2):
                stone = self._board.get_piece_at_pos((row + i, col + j))
                if stone:
                    if stone.get_color() == self._color:
                        self._num_stones += 1
                        if i == 0 and j == 0:
                            self._center_stone = True
                            self._max_move = 20
                        self._stones[(i, j)] = stone
                    else:
                        self._is_valid = False
                        return

        if not self._center_stone:
            self._max_move = 3

    def is_ring(self):
        return self._num_stones == 8 and not self._center_stone

    def get_members_at_edge(self, direction: tuple):
        stones = []
        c_shift, r_shift = direction
        row, col = direction

        c_shift = abs(c_shift)
        r_shift = abs(r_shift)

        for i in range(-1, 2):
            stones.append((row + r_shift * i, col + c_shift * i))

        return stones

    def check_move(self, dest):
        e_row, e_col = dest
        s_row, s_col = self._pos
        direction = self._board.get_direction(self._pos, dest)
        if direction is None:
            return False

        stones = []
        if direction[0]:
            stones += self.get_members_at_edge((direction[0], 0))

        if direction[1]:
            stones += self.get_members_at_edge((0, direction[1]))

        if (direction[0], direction[1]) not in self._stones:
            return False

        if max(abs(e_row - s_row), abs(e_col - s_col)) > self._max_move:
            return False

        stones = set(stones)
        for stone_pos in stones:
            r_shift, c_shift = stone_pos
            s_start = s_row + r_shift, s_col + c_shift
            s_end = e_row + r_shift, e_col + c_shift

            if stone_pos in self._stones and not self._stones[stone_pos].check_move(s_end):
                return False
            elif not self._board.is_unobstructed(s_start, s_end):
                return False

        return True

    def perform_move(self, dest: tuple):
        self.update_board(dest)

    def update_board(self, dest):
        stone_positions = self.get_stone_pos().union(self.get_stone_pos(dest))
        row, col = dest

        for pos in stone_positions:
            stone = self._board.get_piece_at_pos(pos)
            if stone:
                stone.update_pos()

        for stone_pos in self._stones:
            r_shift, c_shift = stone_pos
            stone = self._stones[stone_pos]
            stone.update_pos((row + r_shift, col + c_shift))

    def get_stone_pos(self, pos = None):
        stones = []
        if pos:
            row, col = pos
        else:
            row, col = self._pos

        for i in range(-1,2):
            for j in range(-1,2):
                stones.append((row + i, col + j))

        stones = set(stones)
        return stones

    def is_valid(self):
        if self._is_valid:
            if self._num_stones > 1:
                return True

            if self._num_stones == 1 and not self._center_stone:
                return True

        return False


class Stone:
    def __init__(self, pos: tuple, color: str, board: Board):
        self._pos = pos
        self._color = color
        self._board = board

    def check_move(self, dest: tuple):
        if not self._board.is_valid_pos(dest):
            return False

        return True

    def get_pos(self):
        return self._pos

    def update_pos(self, end_pos=None):
        if self._pos:
            self._board.update_pos(self._pos)

        if end_pos and self._board.is_valid_pos(end_pos):
            self._board.update_pos(end_pos, self)
            self._pos = end_pos
        else:
            self._pos = None

    def get_color(self):
        return self._color


class Player:
    def __init__(self, board: Board, color: str):
        self._board = board
        self._color = color
        self._stones = {}
        self._init_stones()
        self._rings = {}
        self.find_rings()

    def _init_stones(self):
        if self._color == BLACK:
            row_mod = 1
            base_row = 0
        else:
            row_mod = -1
            base_row = 19

        for i in range(3):
            for j in range(18):
                pos = base_row + row_mod * (i+1), j + 1
                self._stones[pos] = Stone(pos, self._color, self._board)
                self._board.add_stone(self._stones[pos], pos)

        for i in range(2, 18, 3):
            pos = base_row + row_mod * 6, i
            self._stones[pos] = Stone(pos, self._color, self._board)
            self._board.add_stone(self._stones[pos], pos)

        for i in range(1, 4, 2):
            row = base_row + row_mod * i
            for j in range(1, 4):
                col = 2 * j - 1
                self._board.update_pos((row, col))
                del self._stones[row, col]
                self._board.update_pos((row, 19-col))
                del self._stones[row, 19 - col]

        # noinspection SpellCheckingInspection
        spots_to_remove = "eglnp"
        for spot in spots_to_remove:
            row = base_row + row_mod * 2
            col = self._board.convert_ltr_col(spot)
            self._board.update_pos((row, col))
            del self._stones[row, col]

    def pos_is_ring(self, pos: tuple):
        return pos in self._rings

    def make_piece(self, pos: tuple, end: bool = False):
        if self._board.is_valid_pos(pos, end):
            return Piece(pos, self._color, self._board)
        else:
            return None

    def find_rings(self):
        empty_list = []
        self._rings = {}
        for piece_pos in self._stones:
            row, col = piece_pos
            if 1 < row < 18 and 1 < col < 18:
                empty_list += self._board.find_empty_neighbors(piece_pos)

        empty_list = set(empty_list)
        for spot in empty_list:
            piece = self.make_piece(spot)
            if piece.is_ring():
                self._rings[spot] = piece

    def has_rings(self):
        return len(self._rings) > 0

    def get_ring_stone_pos(self):
        stones = set()
        stones_loaded = False
        for ring in self._rings.values():
            if not stones_loaded:
                stones = set(ring.get_stone_pos())
            else:
                stones = stones.union(set(ring.get_stone_pos()))

        return stones

    def check_move(self, start, end):
        piece = self.make_piece(start)
        end_piece = self.make_piece(end)

        if piece is None or end_piece is None:
            return False

        if not piece.is_valid():
            return False

        if self.moving_breaks_rings(piece, end_piece):
            return False

        if not piece.check_move(end):
            return False

        return True

    def moving_breaks_rings(self, piece, end_piece = None):  # todo moves that replace ring pieces, moves that break 1 self ring but not all
        danger_stones = self.get_ring_stone_pos()

        move_stones = piece.get_stone_pos()
        if end_piece:
            move_stones = move_stones.union(end_piece.get_stone_pos())

        danger_stones = danger_stones.intersection(move_stones)
        if len(danger_stones) > 0 and not piece.is_ring():
            return True
        elif end_piece and piece.is_ring():
            end_pos = end_piece.get_pos()
            e_row, e_col = end_pos
            return e_row < 2 or e_col < 2 or e_row > 17 or e_col > 17

        return False

    def move_piece(self, start_pos, end_pos):
        if not self.check_move(start_pos, end_pos):
            return False

        piece = self.make_piece(start_pos)
        piece.perform_move(end_pos)
        self.update_stones()

        return True

    def update_stones(self):
        stone_key = self._stones.keys()
        to_update  = []
        for key in list(stone_key):
            stone_pos = self._stones[key].get_pos()
            if stone_pos is None:
                del self._stones[key]
            elif not self._board.is_valid_pos(stone_pos, False):
                del self._stones[key]
                self._board.update_pos(stone_pos)
            elif key != stone_pos:
                to_update.append(self._stones[key])
                del self._stones[key]

        for stone in to_update:
            self._stones[stone.get_pos()] = stone


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