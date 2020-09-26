import unittest
from jigsolver.puzzle import *
import numpy as np
from copy import copy
import matplotlib.pyplot as plt
from jigsolver.fonction_for_placer import *



img_real = plt.imread('../img/eiffel.jpg')
eiffel_puzzle = Puzzle(patch_size=100)
eiffel_puzzle.create_from_img(img_real)
eiffel_puzzle.shuffle()

n_row = eiffel_puzzle.shape[0]
n_column = eiffel_puzzle.shape[1]

test = [[None] * n_column for _ in range(n_row)]

test[2][2]=eiffel_puzzle.get_piece(3)
test[2][3]=eiffel_puzzle.get_piece(2)

test[2][3].left_occu = True
test[2][2].right_occu = True

print(n_row,n_column)

print(position_to_place(test,n_row,n_column))

print(find_best_one_piece_to_one_place(test,n_row,n_column,18,eiffel_puzzle,in_space_list=[2,3]))



# print(test)



