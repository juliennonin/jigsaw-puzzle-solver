import unittest
from jigsolver.puzzle import *
import numpy as np
from copy import copy
import matplotlib.pyplot as plt
from jigsolver.fonction_for_placer import *



img_real = plt.imread('../img/eiffel.jpg')
eiffel_puzzle = Puzzle()
eiffel_puzzle.create_from_img(img_real)
eiffel_puzzle.shuffle()

n_row = eiffel_puzzle.shape[0]
n_column = eiffel_puzzle.shape[1]

test=Board(n_row,n_column)

test.__setitem__([2,3],eiffel_puzzle.get_piece(3))
test.__setitem__([2,4],eiffel_puzzle.get_piece(4))

test._grid[2][3].right_occu = True
test._grid[2][4].left_occu = True

print(position_to_place(test))

print(eiffel_puzzle.get_compatibilities())
#
# print(find_best_one_piece_to_one_place(test,n_row,n_column,18,eiffel_puzzle,in_space_list=[2,3]))
#
#

# print(test)



