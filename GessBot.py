from GessGame import GessGame
from constants import UNFINISHED
from random import choice
from time import sleep


class GessBot:
    def __init__(self):
        self._game = GessGame()
        self._cur_test = 0
        with open("test_no.txt", "r") as infile:
            self._cur_test = int(infile.readline().strip())


    def restart_game(self):
        self._game = GessGame()

    def run_round(self):
        self.restart_game()
        count = 0
        with open("bot_gen_tests.py", "a+") as outfile:
            outfile.write(f"    def test_{self._cur_test:03}(self):\n")
            outfile.write(f"        t = GessGame()\n")
            self._cur_test += 1
            while self._game.get_game_state() == UNFINISHED:
                pieces = self.get_valid_pieces()
                piece = choice(pieces)
                moves = self.get_valid_moves(piece)
                if len(moves) > 0:
                    move = choice(moves)
                    print(f"{piece} => {move}")
                    if self._game.make_move(piece, move):
                        count += 1
                        outfile.write(f"        self.assertTrue(t.make_move('{piece}','{move}'))\n")
                    else:
                        outfile.write(f"        self.assertFalse(t.make_move('{piece}','{move}'))\n")

            print(" ".join(self._game.get_game_state().lower().capitalize().split("_"))+f" in {count} rounds!\n\n")
            outfile.write(f"        self.assertEqual(t.get_game_state(), '{self._game.get_game_state()}')\n\n")

        return count

    def run(self, min_val, max_val):
        while min_val < self.run_round() < max_val:
            sleep(1)

        with open("test_no.txt", "w") as save_num:
            save_num.write(str(self._cur_test))


    def get_valid_pieces(self):
        valid_pieces = []
        for i in range(1, 19):
            for j in range(1,19):
                coord = self._game.convert_input((i, j))
                if self._game.is_valid_piece(coord) and not self._game.piece_is_ringlocked(coord):
                    valid_pieces.append(coord)

        return valid_pieces

    def get_valid_moves(self, piece):
        row, col = self._game.convert_input(piece)
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if j != 0 or i != 0:
                    cur_row, cur_col = row, col
                    cur_row += i
                    cur_col += j
                    while self._game.check_move((row, col), (cur_row, cur_col)):
                        moves.append(self._game.convert_input((cur_row, cur_col)))
                        cur_row += i
                        cur_col += j

        return moves

g = GessBot()
g.run_round()
# g.run(12, 398)


# TODO ****************************************************************************
# tests needing adding:
#       test for moving ring off board and destroying it
# bug fix:
#       one legal move is considered illegal in current iteration
#               000OOO      000OO
#               000O O  =>  000 O
#               000OOO      000OO

# TODO best: 12 moves (6 rounds) worst: 343 moves