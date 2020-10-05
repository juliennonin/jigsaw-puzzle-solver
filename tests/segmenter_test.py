import unittest
from jigsolver.puzzle import *
from jigsolver.pomeranz_solver.segmenter import BestBuddies_matrix,segmenter,find_segment
from jigsolver.metrics import pomeranz_CM
import numpy as np
from copy import copy

class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_board_should_return_empty_segment(self):
        empty_puzzle = Puzzle(np.zeros((3,3,3)),patch(1))

        self.assertEqual(segmenter(empty_puzzle,[]),[])
        self.assertEqual(find_segment(empty_puzzle,[],(1,1),[]),[])
    
    def test_black_and_white_board(self):
        img = np.array([[[250., 250., 250.],[251., 251., 251.],[253., 253., 253.]],
                        [[  0.,   0.,   0.],[  0.,   0.,   0.],[  0.,   0.,   0.]],
                        [[  0.,   0.,   0.],[  0.,   0.,   0.],[  0.,   0.,   0.]]])
        bw_puzzle = Puzzle(img,patch(1)).ground_truth

        bw_puzzle.clean()
        print(len(bw_puzzle.bag_of_pieces))
        print(bw_puzzle.bag_of_pieces[0].picture)

        for i in range(bw_puzzle.shape[0]):
            for j in range(bw_puzzle.shape[1]):
                bw_puzzle.place(bw_puzzle.bag_of_pieces[i*bw_puzzle.shape[0]+j],(i,j))


        cm = pomeranz_CM(bw_puzzle)
        BB = BestBuddies_matrix(cm)

        segment = find_segment(bw_puzzle,[],(0,0),BB)
        self.assertEqual(len(segment),2)
    

if __name__ == '__main__':
    unittest.main()