from constants import *
from Board import Board
from Player import Player
from Display import Display


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
