import unittest
import numpy as np
from jigsolver import Border, Piece, Puzzle

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

        diss = {
            Border.TOP: 51,
            Border.BOTTOM: 51,
            Border.RIGHT: 54,
            Border.LEFT: 0
        }
        self.assertDictEqual(A.diss(B), diss)

        diss[Border.TOP], diss[Border.BOTTOM] = diss[Border.BOTTOM], diss[Border.TOP]
        diss[Border.LEFT], diss[Border.RIGHT] = diss[Border.RIGHT], diss[Border.LEFT]
        self.assertDictEqual(B.diss(A), diss)


if __name__ == '__main__':
    unittest.main()