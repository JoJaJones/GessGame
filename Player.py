from Board import Board
from Stone import Stone
from Piece import Piece
from constants import *


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

