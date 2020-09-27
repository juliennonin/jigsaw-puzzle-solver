import unittest
from jigsolver.puzzle import Piece,Puzzle, Board, Slot
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        self.img = np.arange(468).reshape(13,12,3)
        self.puzzle = Puzzle(patch_size=3)
        self.puzzle.create_from_img(self.img)

        img_real = plt.imread('img/eiffel.jpg')
        self.eiffel_puzzle = Puzzle(patch_size=100)
        self.eiffel_puzzle.create_from_img(img_real)
    
    def test_puzzle_create_piece_size(self):
        return self.assertEqual(self.eiffel_puzzle.board[0,0].size, 100)

    def test_create_puzzle_crop_test(self):
        self.assertEqual(self.puzzle.shape,(4,4))

    def test_create_puzzle_crop_test_real_img(self):
        self.assertEqual(self.eiffel_puzzle.shape,(4,7))

    def test_shuffle_puzzle(self):
        self.puzzle.shuffle()
        self.assertEqual(len(self.puzzle.bag_of_pieces), 16)
        empty_board = Board(4, 4, None)
        self.assertEqual(self.puzzle.board.shape,empty_board.shape)

    def test_shuffle_puzzle_real_img(self):
        self.eiffel_puzzle.shuffle()
        self.assertEqual(len(self.eiffel_puzzle.bag_of_pieces), 28)
        empty_board = Board(4, 7, None)
        self.assertEqual(self.eiffel_puzzle.board.shape,empty_board.shape)

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

    def test_piece_compatibility_matrix_cho(self):
            P = Puzzle(patch_size=2)

            # creating very simple pieces
            A = np.zeros((2, 2, 3)).astype(int)
            B = A.copy()

            A[:, 0] = 1
            A[:, 1] = 2
            A = Piece(A)

            B[:, 0] = 5
            B[:, 1] = 1
            B = Piece(B)

            P.bag_of_pieces = [A, B]

            P.set_CM_Cho()

            #these two pieces should have a perfect compatibility for one side
            # (left of right depending of the piece considered as a reference)

            self.assertEqual((P.CM)[0,1]['L'],1)
            self.assertEqual((P.CM)[1,0]['R'], 1)

    def test_piece_compatibility_matrix_pomeranz(self):
            P = Puzzle(patch_size=2)

            # creating very simple pieces
            A = np.zeros((2, 2, 3)).astype(int)
            B = A.copy()

            A[:, 0] = 1
            A[:, 1] = 2
            A = Piece(A)

            B[:, 0] = 5
            B[:, 1] = 1
            B = Piece(B)

            P.bag_of_pieces = [A, B]

            P.set_CM_Pomeranz()

            #these two pieces should have a perfect compatibility for one side
            # (left of right depending of the piece considered as a reference)

            self.assertEqual((P.CM)[0,1]['L'],1)
            self.assertEqual((P.CM)[1,0]['R'], 1)

if __name__ == '__main__':
    unittest.main()