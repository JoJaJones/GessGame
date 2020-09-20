
import sys

sys.path.insert(0, "D:/PycharmProjects/GessGame/subdir/")
from constants import SPACE_DICT, WHITE, BLACK
from GessGame import GessGame

class Converter:
    def __init__(self, board):
        self._letter_converter = board.convert_to_pos

    def convert(self, value_to_vert):
        pass

class ValueConverter(Converter):
    def __init__(self, value_converter: dict, example_value, processing_func: list):
        super().__init__(None)
        self._value_converter = value_converter
        self._proc_funcs = processing_func

    def convert(self, value_to_vert):
        idx = 0
        while value_to_vert not in self._value_converter and idx < len(self._proc_func):
            value_to_vert = self._proc_funcs[idx](value_to_vert)
            idx += 1

        return value_to_vert

class ListConverter(Converter):
    def __init__(self, target_value:tuple, example_value, inner_converter: Converter = None):
        super().__init__(None)
        self._inner_converter = inner_converter

    def convert(self, value_to_vert):
        result = []
        for item in value_to_vert:
            result.append(self._inner_converter.convert(item))

class DictConverter(Converter):
    def __init__(self, board, example_key, inner_converter: Converter = None):
        super().__init__(board)
        self._inner_converter = inner_converter
        self._key_converter = self._load_key_converter(example_key)

    def _load_key_converter(self, ex_key):
        pass

    def create_alpha_to_num(self, is_letters = True):
        def alpha_to_num(ltr):
            return COL_STRING.index(ltr)

        def str_to_num(num):
            return int(num)

        if is_letters:
            return alpha_to_num
        else:
            return str_to_num

    def create_tuple_maker(self, key_type):

        if key_type == str:
            begin = self.create_aplha_to_num()



    def convert(self, value_to_vert):
        result = []
        for i in range(20):
            result.append([])
            for j in range(20):
                result[i].append(None)

        for key in value_to_vert:
            row, col = self.convert_key(key)
            result[row][col] = self._inner_converter.convert(value_to_vert)

        return result

    def convert_key(self, key) -> tuple:
        new_key = None

CONVERTER_DICT = {dict: DictConverter, list: ListConverter, str: ValueConverter, int: ValueConverter, tuple: ValueConverter}


class BoardAdaptor:
    def __init__(self, board, empty_value, white_value, black_value):
        self._board = board
        self._value_to_space = {}
        self.load_value_to_space(empty_value, white_value, black_value)
        self._converter = None
        self._load_converter(board)

    def load_value_to_space(self, empty, white, black):
        self._value_to_space[empty] = None
        self._value_to_space[white] = WHITE
        self._value_to_space[black] = BLACK

    def get_positions(self):
        return self._board

    def load_converter(self, convert_type):
        pass

g = GessGame()
d = DictConverter(g._board, (1,2))
arr = [(3,4), (10,15), (11,3), (4,8), (9,1)]
for key in arr:
    print(d.convert_key(key))