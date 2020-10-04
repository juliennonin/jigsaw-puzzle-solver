import unittest
from jigsolver import Puzzle, Board,Piece
from jigsolver.segmenter import segmenter,find_segment
from jigsolver.metrics import pomeranz_CM,BestBuddies_matrix
import numpy as np
from copy import copy

class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_board_should_return_empty_segment(self):
        empty_puzzle = Puzzle(patch_size=1)
        empty_puzzle.create_from_img(np.zeros((3,3,3)))
        empty_puzzle.shuffle()

        self.assertEqual(segmenter(empty_puzzle,[]),[])
        self.assertEqual(find_segment(empty_puzzle,[],(1,1),[]),[])
    
    def test_black_and_white_board(self):
        img = np.array([[[250., 250., 250.],[251., 251., 251.],[253., 253., 253.]],[[  0.,   0.,   0.],[  0.,   0.,   0.],[  0.,   0.,   0.]],[[  0.,   0.,   0.],[  0.,   0.,   0.],[  0.,   0.,   0.]]])
        bw_puzzle = Puzzle(patch_size=1)

        bw_puzzle.create_from_img(img)
        bw_puzzle.clean()
        for i in range(bw_puzzle.shape[0]):
            for j in range(bw_puzzle.shape[1]):
                bw_puzzle.place(bw_puzzle.bag_of_pieces[i*bw_puzzle.shape[0]+j],(i,j))

        cm = pomeranz_CM(bw_puzzle)
        BB = BestBuddies_matrix(cm)

        segment = find_segment(bw_puzzle,[],(0,0),BB)
        self.assertEqual(len(segment),2)
    

if __name__ == '__main__':
    unittest.main()