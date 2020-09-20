from Board import Board


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
