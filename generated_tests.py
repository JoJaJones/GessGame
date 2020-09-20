import unittest
from GessGame import GessGame


class TestGess(unittest.TestCase):
    def test_000(self):
        t = GessGame()
        self.assertTrue(t.make_move('o8','o6'))
        self.assertTrue(t.make_move('p14','m14'))
        self.assertFalse(t.make_move('o4','o8'))
        self.assertTrue(t.make_move('o4','o7'))
        self.assertTrue(t.make_move('m14','j14'))
        self.assertTrue(t.make_move('k7','l7'))
        self.assertTrue(t.make_move('j14','g14'))
        self.assertFalse(t.make_move('p7o8','p9'))
        self.assertTrue(t.make_move('p7','o8'))
        self.assertTrue(t.make_move('b14','e14'))
        self.assertTrue(t.make_move('n10','n9'))
        self.assertTrue(t.make_move('f13','f16'))
        self.assertTrue(t.make_move('n7','n16'))
        self.assertEqual(t.get_game_state(), 'BLACK_WON')
        self.assertFalse(t.make_move('l18', 'l17'))

