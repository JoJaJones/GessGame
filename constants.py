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


if __name__ == "__main__":

    print(COL_STRING[-1:0:-1])

    print(FIRST_COLOR_SET, BLACK_PIECE, WHITE_PIECE, CLEAR_COLOR, "Hello, world!")
    print("|" + chr(9472+80) + f" : {80:3}|")
    for i in range(9472+81, 9472+109, 3):
        print("|"+chr(i)+f" : {i-9472:3}|")
        if i%20 == 0:
            print()
    print()
    for i in range(40, 56):
        if i > 47:
            i += 52
        for j in range(30, 46):
            if j > 37:
                j += 52
            print (f"\033[{j};{i}m {j:3}, {i:3}", end=" ")
            if j % 10 == 7:
                print(CLEAR_COLOR)