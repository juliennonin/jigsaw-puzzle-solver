import unittest
import numpy as np
from jigsolver.puzzle import Piece
import matplotlib.pyplot as plt
import jigsolver



class PieceTestCase(unittest.TestCase):
    def setUp(self):
        img = plt.imread('../img/eiffel.jpg')
        eiffel_puzzle = jigsolver.Puzzle(patch_size=50)
        eiffel_puzzle.create_from_img(img)
        self.eiffel_puzzle = eiffel_puzzle

    def test_piece_size_should_return_size(self):
        picture = np.array([
            [[1, 1, 1], [1, 2, 3], [4, 5, 6]], 
            [[0, 1, 2], [5, 3, 0], [0, 1, 4]],
            [[8, 5, 1], [4, 5, 0], [8, 5, 1]]
        ])
        piece = Piece(picture)
        return self.assertEqual(piece.size, 3)

    def test_piece_size_should_return_size_with_real_piece(self):
        return self.assertEqual(self.eiffel_puzzle.board[0][0].size, 50)

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



if __name__ == '__main__':
    unittest.main()