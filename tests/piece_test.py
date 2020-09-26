import unittest
import numpy as np
from jigsolver.puzzle import Piece,Puzzle

class PieceTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_piece_size_should_return_size(self):
        picture = np.array([
            [[1, 1, 1], [1, 2, 3], [4, 5, 6]],
            [[0, 1, 2], [5, 3, 0], [0, 1, 4]],
            [[8, 5, 1], [4, 5, 0], [8, 5, 1]]
        ])
        piece = Piece(picture)
        self.assertEqual(piece.size, 3)

    def test_piece_with_rectangular_picture_should_raise_error(self):
        picture = np.zeros((4, 5, 3))  # RGB picture of shape 4×5
        with self.assertRaises(AssertionError):
            piece = Piece(picture)

    def test_piece_without_colored_picture_should_raise_error(self):
        picture = np.zeros((3, 3, 2))
        with self.assertRaises(AssertionError):
            piece = Piece(picture)

    def test_piece_without_three_dimensional_picture_should_raise_error(self):
        picture = np.zeros((5, 5))
        with self.assertRaises(AssertionError):
            piece = Piece(picture)

    def test_piece_dissimilarity(self):
        #creating very simple pieces
        A = np.zeros((2, 2, 3)).astype(int)
        B = A.copy()

        A[:, 0] = 1
        A[:, 1] = 2
        A=Piece(A)

        B[:, 0] = 5
        B[:, 1] = 1
        B=Piece(B)

        self.assertEqual(A.diss(B), {'L': 0, 'R': 54, 'U': 51, 'B': 51})
        self.assertEqual(B.diss(A), {'L': 54, 'R': 0, 'U': 51, 'B': 51})



if __name__ == '__main__':
    unittest.main()