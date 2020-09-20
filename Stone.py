from Board import Board


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
