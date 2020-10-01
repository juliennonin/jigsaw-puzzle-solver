import unittest
from jigsolver import Board, Border, Piece, Puzzle, Slot
from jigsolver.metrics import *
import numpy as np
from copy import copy,deepcopy
import matplotlib.pyplot as plt

class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        self.img = np.arange(468).reshape(13,12,3)
        self.puzzle = Puzzle(patch_size=3)
        self.puzzle.create_from_img(self.img)

        
        img_real = plt.imread('img/eiffel.jpg')
        self.eiffel_puzzle = Puzzle(patch_size=100)
        self.eiffel_puzzle.create_from_img(img_real)
        self.eiffel_puzzle_copy = copy(self.eiffel_puzzle)

        # creating a very simple puzzle
        A = np.zeros((2, 2, 3)).astype(int)
        B = A.copy()
        C = B.copy()


        A[:, 0] = 5
        A[:, 1] = 1
        A = Piece(A, 0)

        B[:, 0] = 1
        B[:, 1] = 2
        B = Piece(B, 1)

        C[:, 0] = 20
        C[:, 1] = 50
        C = Piece(C, 2)

        D=B.copy()

        P = Puzzle(patch_size=2)
        P.bag_of_pieces = [A, B, C, D]

        P_board = Board(1, 4)
        P.board=P_board
        P.place(A,(0,0))
        P.place(B,(0,1))
        P.place(C,(0,2))
        P.place(D,(0,3))

        Q=deepcopy(P)
        Q.board[0,0]=B
        Q.board[0,1]=A


        self.simple_puzzle=P
        self.inferred_puzzle=Q
    
    def test_puzzle_create_piece_size(self):
        self.assertEqual(self.eiffel_puzzle.board[0,0].size, 100)

    def test_create_puzzle_crop_test(self):
        self.assertEqual(self.puzzle.shape,(4,4))

    def test_create_puzzle_crop_test_real_img(self):
        self.assertEqual(self.eiffel_puzzle.shape,(4,7))

    def test_shuffle_puzzle(self):
        self.puzzle.shuffle()
        self.assertEqual(len(self.puzzle.bag_of_pieces), 16)
        empty_board = Board(4, 4)
        self.assertEqual(self.puzzle.board.shape,empty_board.shape)

    def test_shuffle_puzzle_real_img(self):
        self.eiffel_puzzle.shuffle()
        self.assertEqual(len(self.eiffel_puzzle.bag_of_pieces), 28)
        empty_board = Board(4, 7)
        self.assertEqual(self.eiffel_puzzle.board.shape,empty_board.shape)

    def test_puzzle_copy(self):
        self.puzzle_copy = copy(self.puzzle)
        self.puzzle.shuffle()
        self.assertNotEqual(self.puzzle.bag_of_pieces,self.puzzle_copy.bag_of_pieces)
        self.assertNotEqual(self.puzzle.board,self.puzzle_copy.board)


    def test_puzzle_copy_real_img(self):
        self.eiffel_puzzle.shuffle()
        self.assertNotEqual(self.eiffel_puzzle.bag_of_pieces,self.eiffel_puzzle_copy.bag_of_pieces)
        self.assertNotEqual(self.eiffel_puzzle.board,self.eiffel_puzzle_copy.board)

    def test_puzzle_compatibility_matrix_cho(self):
        CM = cho_CM(self.simple_puzzle)

        # these two pieces should have a perfect compatibility for one side
        # (left of right depending of the piece considered as a reference)

        self.assertEqual(CM[0, 1, Border.RIGHT.value], 1)
        self.assertEqual(CM[1, 0, Border.LEFT.value], 1)

    def test_puzzle_compatibility_matrix_pomeranz(self):
        CM = pomeranz_CM(self.simple_puzzle)

        # these two pieces should have a perfect compatibility for one side
        # (left of right depending of the piece considered as a reference)

        self.assertEqual(CM[0, 1, Border.RIGHT.value], 1)
        self.assertEqual(CM[1, 0, Border.LEFT.value], 1)


    def test_puzzle_simple_evaluation(self):
        # Case where the puzzle is perfectly solved
        self.assertEqual(simple_evaluation(self.eiffel_puzzle,self.eiffel_puzzle_copy),1)

        #Case where the puzzle is completely not solved
        self.assertEqual(simple_evaluation(self.simple_puzzle,self.inferred_puzzle),0.5)


    def test_puzzle_fraction_of_correct_neighbors(self):
        self.assertEqual(fraction_of_correct_neighbors((0, 0), self.simple_puzzle, self.inferred_puzzle), 0)
        self.assertEqual(fraction_of_correct_neighbors((0, 1), self.simple_puzzle, self.inferred_puzzle), 0)
        self.assertEqual(fraction_of_correct_neighbors((0,2),self.simple_puzzle,self.inferred_puzzle), 0.5)
        self.assertEqual(fraction_of_correct_neighbors((0, 3), self.simple_puzzle, self.inferred_puzzle), 1)


    # def test_puzzle_neighbor_comparison(self):
    #         # Case where the puzzle is perfectly solved
    #         self.assertEqual(neighbor_comparison(self.eiffel_puzzle, self.eiffel_puzzle_copy), 1)
    #
    #         # Case where the puzzle is not completely solved
    #         self.assertEqual(neighbor_comparison(self.simple_puzzle, self.inferred_puzzle), 0.25)


if __name__ == '__main__':
    unittest.main()