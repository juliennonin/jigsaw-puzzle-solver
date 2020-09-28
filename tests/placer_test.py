import unittest
from jigsolver import *
from jigsolver.placer import available_positions
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        img_real = plt.imread('img/eiffel.jpg')
        self.eiffel_puzzle = Puzzle(patch_size=100)
        self.eiffel_puzzle.create_from_img(img_real)
        self.eiffel_puzzle.shuffle()

    def test_find_position_to_place(self):
        self.eiffel_puzzle.place(self.eiffel_puzzle.bag_of_pieces[3], (2, 2))
        self.eiffel_puzzle.place(self.eiffel_puzzle.bag_of_pieces[2], (2, 3))
        return self.assertEqual(list(available_positions(self.eiffel_puzzle)), [18, 23, 24, 9, 10, 15])



if __name__ == '__main__':
    unittest.main()
