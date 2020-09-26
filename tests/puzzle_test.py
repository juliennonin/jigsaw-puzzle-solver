import unittest
from jigsolver.puzzle import Puzzle
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        self.img = np.arange(468).reshape(13,12,3)
        self.puzzle = Puzzle(patch_size=3)
        self.puzzle.create_from_img(self.img)

        img_real = plt.imread('../img/eiffel.jpg')
        self.eiffel_puzzle = Puzzle(patch_size=100)
        self.eiffel_puzzle.create_from_img(img_real)
    
    def test_puzzle_create_piece_size(self):
        return self.assertEqual(self.eiffel_puzzle.board[0][0].size, 100)

    def test_create_puzzle_crop_test(self):
        self.assertEqual(self.puzzle.shape,(4,4))

    def test_create_puzzle_crop_test_real_img(self):
        self.assertEqual(self.eiffel_puzzle.shape,(4,7))

    def test_shuffle_puzzle(self):
        self.puzzle.shuffle()
        self.assertEqual(len(self.puzzle.bag_of_pieces),16)
        empty_board = [[None]*4]*4
        self.assertEqual(self.puzzle.board,empty_board)

    def test_shuffle_puzzle_real_img(self):
        self.eiffel_puzzle.shuffle()
        self.assertEqual(len(self.eiffel_puzzle.bag_of_pieces),28)
        empty_board = [[None]*7]*4
        self.assertEqual(self.eiffel_puzzle.board,empty_board)

    def test_puzzle_copy(self):
        self.puzzle_copy = copy(self.puzzle)
        self.puzzle.shuffle()
        self.assertNotEqual(self.puzzle.bag_of_pieces,self.puzzle_copy.bag_of_pieces)
        self.assertNotEqual(self.puzzle.board,self.puzzle_copy.board)


    def test_puzzle_copy_real_img(self):
        self.eiffel_puzzle_copy = copy(self.eiffel_puzzle)
        self.eiffel_puzzle.shuffle()
        self.assertNotEqual(self.eiffel_puzzle.bag_of_pieces,self.eiffel_puzzle_copy.bag_of_pieces)
        self.assertNotEqual(self.eiffel_puzzle.board,self.eiffel_puzzle_copy.board)


if __name__ == '__main__':
    unittest.main()