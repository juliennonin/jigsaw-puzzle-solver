import unittest
from jigsolver import Puzzle, Board,Piece
from jigsolver.segmenter import segmenter,find_segment
import numpy as np
from copy import copy

class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_board_should_return_empty_segment(self):
        empty_puzzle = Puzzle(patch_size=1)
        empty_puzzle.create_from_img(np.zeros((3,3,3)))
        empty_puzzle.shuffle

        self.assertEqual(segmenter(empty_puzzle),[])
        self.assertEqual(find_segment(empty_puzzle,[],(1,1)),[])

    def test_black_and_white_board(self):
        bw_puzzle = Puzzle(patch_size=1)
        img = np.zeros((3,3,3))
        img[0,:] = np.ones(3)
        bw_puzzle.create_from_img(img)

        segment = find_segment(bw_puzzle,[],(0,0))
        self.assertEqual(len(segment),3)


if __name__ == '__main__':
    unittest.main()