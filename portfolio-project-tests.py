import unittest
from GessGame import GessGame


class TestGessGame(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_1(self):
        """Make a couple of moves, check the state, black resigns"""
        game = GessGame()
        self.assertTrue(game.make_move('m3', 'm6'))
        self.assertTrue(game.make_move('e14', 'g14'))
        self.assertEqual(game.get_game_state(), 'UNFINISHED')
        game.resign_game()
        self.assertEqual(game.get_game_state(), 'WHITE_WON')
 
 
    def test_2(self):
        """black attempts perform_move that destroys their own only ring"""
        game = GessGame()
        self.assertFalse(game.make_move('j3','j4'))
    
    
    def test_3(self):  # illegal per rules
        """perform_move a piece whose footprint goes off the edge of the board"""
        game = GessGame()
        game.make_move('q6','r7')
        game.make_move('l15','l12')
        self.assertTrue(game.make_move('t7','q10'))
        game.make_move('l12','l9')
        self.assertTrue(game.make_move('p10','p13'))
    
    
    def test_4(self):
        """attempt to perform_move pieces that contains stones belonging to the other player"""
        game = GessGame()
        game.make_move('i6','i9')
        game.make_move('i15','i12')
        self.assertFalse(game.make_move('h10','j10'))
        self.assertFalse(game.make_move('i18','i17'))
    
    
    def test_5(self):
        """attempt to perform_move legal pieces in illegal ways"""
        game = GessGame()
        self.assertFalse(game.make_move('q3','q4'))
        self.assertTrue(game.make_move('m6','j9'))
        game.make_move('f15','f14')
        self.assertFalse(game.make_move('l3','l10'))
        self.assertTrue(game.make_move('l3', 'l5'))
    
    
    def test_6(self):
        """Attempt illegal capturing perform_move"""
        game = GessGame()
        game.make_move('j6','g9')
        game.make_move('o15','o12')
        self.assertFalse(game.make_move('i3','i14'))
    
    
    def test_7(self):
        """black makes moves that capture black stones, which is allowed"""
        game = GessGame()
        self.assertTrue(game.make_move('e3','d3'))
        game.make_move('l15','l12')
        self.assertTrue(game.make_move('d3','d6'))
        game.make_move('l12','l9')
        self.assertTrue(game.make_move('d6','d9'))

    
    def test_8(self):
        """win for White"""
        game = GessGame()
        self.assertTrue(game.make_move('m6','j9'))
        self.assertTrue(game.make_move('j15','g12'))
        self.assertTrue(game.make_move('j10','g10'))
        self.assertTrue(game.make_move('i18','i8'))
        self.assertTrue(game.make_move('e10','g10'))
        self.assertEqual(game.get_game_state(), 'UNFINISHED')
        self.assertTrue(game.make_move('i8','l5'))
        self.assertEqual(game.get_game_state(), 'WHITE_WON')
        self.assertFalse(game.make_move('r6','r7'))
    
    
    def test_9(self):
        """Black forms a second ring, white breaks one of them"""
        game = GessGame()
        self.assertTrue(game.make_move('e6','g8'))
        self.assertTrue(game.make_move('b15','e12'))
        self.assertTrue(game.make_move('i8','g10'))
        self.assertTrue(game.make_move('c18','c8'))
        self.assertTrue(game.make_move('e3','e6'))
        self.assertTrue(game.make_move('i18','i15'))
        self.assertTrue(game.make_move('b3','e3'))
        self.assertTrue(game.make_move('i15','i7'))
        self.assertTrue(game.make_move('f9','g9'))
        self.assertEqual(game.get_game_state(), 'UNFINISHED')
        self.assertTrue(game.make_move('i7','k5'))
        self.assertEqual(game.get_game_state(), 'UNFINISHED')


    def test_10(self):
        """Attempt to pass through other stones"""
        game = GessGame()
        self.assertFalse(game.make_move('i3','b10'))


    def test_11(self):
        """Attempt to perform_move center of piece out of bounds"""
        game = GessGame()
        self.assertFalse(game.make_move('r3','t3'))


    def test_12(self):
        """Move edge of piece off board, then check whether the edge stone was removed"""
        game = GessGame()
        self.assertTrue(game.make_move('r3','s3'))
        game.make_move('f15','f14')
        self.assertTrue(game.make_move('s3','r3'))
        game.make_move('f14','f13')
        self.assertFalse(game.make_move('r3','s3'))


    def test_13(self):
        """Attempt two moves in a row by same player"""
        game = GessGame()
        self.assertTrue(game.make_move('i6','i7'))
        self.assertFalse(game.make_move('i7','i8'))
