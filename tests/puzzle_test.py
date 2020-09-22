import unittest
from jigsolver.puzzle import Puzzle
import numpy as np
from copy import copy


class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        self.img = np.arange(468).reshape(13,12,3)
        self.puzzle = Puzzle(patch_size=3)
        self.puzzle.create_from_img(self.img)

    def test_create_puzzle_crop_test(self):
        self.assertEqual(self.puzzle.shape,(4,4))

    def test_shuffle_puzzle(self):
        self.puzzle.shuffle()
        self.assertEqual(len(self.puzzle.bag_of_pieces),16)
        empty_board = [[None]*4]*4
        self.assertEqual(self.puzzle.board,empty_board)

    def test_puzzle_copy(self):
        self.puzzle_copy = copy(self.puzzle)
        self.puzzle.shuffle()
        self.assertNotEqual(self.puzzle.bag_of_pieces,self.puzzle_copy.bag_of_pieces)
        self.assertNotEqual(self.puzzle.board,self.puzzle_copy.board)


if __name__ == '__main__':
    unittest.main()