from jigsolver.puzzle import *
import numpy as np
# from copy import copy
import matplotlib.pyplot as plt
from jigsolver.fonction_for_placer import *



img_real = plt.imread('../img/eiffel.jpg')
eiffel_puzzle = Puzzle(patch_size=200)
eiffel_puzzle.create_from_img(img_real)
# eiffel_puzzle.display()

eiffel_unsolved = copy(eiffel_puzzle)
eiffel_unsolved.shuffle()


eiffel_unsolved.bag_of_pieces[0].left_occu = True
eiffel_unsolved.bag_of_pieces[0].up_occu = True

some_piece = eiffel_unsolved.bag_of_pieces[0]
eiffel_unsolved.board[0,0] = some_piece

eiffel_unsolved.display()

# n_row = eiffel_puzzle.shape[0]
# n_column = eiffel_puzzle.shape[1]
#
# test=Board(n_row,n_column)
# #
# test.__setitem__([0,0],eiffel_puzzle.get_piece(3))

# test._grid[0][0].left_occu = True
# test._grid[0][0].up_occu = True
#
print(find_place_occupied(eiffel_unsolved))

print(position_to_place(eiffel_unsolved))
# print(position_to_place(test))
#
# print(eiffel_puzzle.shape)

# print(eiffel_puzzle.get_compatibilities())
#
# print(find_best_one_piece_to_one_place(test,n_row,n_column,18,eiffel_puzzle,in_space_list=[2,3]))
#
#

# print(test)



