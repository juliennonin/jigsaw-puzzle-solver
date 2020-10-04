import unittest
import numpy as np
from jigsolver import Border, Piece, Puzzle
from jigsolver.metrics import dissimilarity

class PieceTestCase(unittest.TestCase):
    def setUp(self):
        # creating very simple pieces
        A = np.zeros((2, 2, 3)).astype(int)
        B = A.copy()

        A[:, 0] = 1
        A[:, 1] = 2
        A = Piece(A)

        B[:, 0] = 5
        B[:, 1] = 1
        B = Piece(B)

        self.A=A
        self.B=B

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

        diss = [0] * len(Border)
        diss[Border.TOP.value] = 51
        diss[Border.BOTTOM.value] = 51
        diss[Border.RIGHT.value] = 54
        diss[Border.LEFT.value] = 0

        #Testing of the symetry

        self.assertListEqual(dissimilarity(self.A, self.B), diss)

        diss[Border.TOP.value], diss[Border.BOTTOM.value] = diss[Border.BOTTOM.value], diss[Border.TOP.value]
        diss[Border.LEFT.value], diss[Border.RIGHT.value] = diss[Border.RIGHT.value], diss[Border.LEFT.value]

        self.assertListEqual(dissimilarity(self.B, self.A), diss)




if __name__ == '__main__':
    unittest.main()