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
        piece = Piece(picture, 0)
        self.assertEqual(piece.size, 3)

    def test_piece_with_rectangular_picture_should_raise_error(self):
        picture = np.zeros((4, 5, 3))  # RGB picture of shape 4×5
        with self.assertRaises(AssertionError):
            piece = Piece(picture, 0)

    def test_piece_without_colored_picture_should_raise_error(self):
        picture = np.zeros((3, 3, 2))
        with self.assertRaises(AssertionError):
            piece = Piece(picture, 0)

    def test_piece_without_three_dimensional_picture_should_raise_error(self):
        picture = np.zeros((5, 5))
        with self.assertRaises(AssertionError):
            piece = Piece(picture, 0)

    def test_piece_dissimilarity(self):
        #creating very simple pieces
        A = np.zeros((3, 3, 3))
        A[:, 0] = 100
        A[:, -1] = 200
        A[0, :] = 200
        A[-1, :] = 100
        A = Piece(A, 0)

        B = np.ones((3, 3, 3))
        B[1, 0] = 150
        B[1, 2] = 200
        B=Piece(B, 0)

        self.assertEqual(A.diss(B), {'L': 178206, 'R': 155706, 'U': 356409, 'B': 88209})
        self.assertEqual(B.diss(A), {'L': 155706, 'R': 178206, 'U': 88209, 'B': 356409})


if __name__ == '__main__':
    unittest.main()