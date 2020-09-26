import unittest
from jigsolver.puzzle import *
import numpy as np
from copy import copy
import matplotlib.pyplot as plt
from jigsolver.fonction_for_placer import *

class PuzzleTestCase(unittest.TestCase):
    def setUp(self):
        img_real = plt.imread('../img/eiffel.jpg')
        self.eiffel_puzzle = Puzzle(patch_size=100)
        self.eiffel_puzzle.create_from_img(img_real)
        self.eiffel_puzzle.shuffle()

        self.test = [[None] * self.eiffel_puzzle.shape[1] for _ in range(self.eiffel_puzzle.shape[0])]

        self.test[2][2]=self.eiffel_puzzle.get_piece(3)
        self.test[2][3]=self.eiffel_puzzle.get_piece(2)

        self.test[2][3].left_occu = True
        self.test[2][2].right_occu = True

    def test_find_position_to_place(self):
        return self.assertEqual(position_to_place(self.test,self.eiffel_puzzle.shape[0],self.eiffel_puzzle.shape[1]), [18, 23, 24, 9, 10, 15])








