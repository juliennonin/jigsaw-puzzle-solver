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




some_piece = eiffel_unsolved.get_piece(1)
eiffel_unsolved.board[0,0] = some_piece
eiffel_unsolved.board[0,0].left_occu = True
eiffel_unsolved.board[0,0].up_occu = True

#
# eiffel_unsolved.display()


Matrix_L = np.random.rand(6,6)
Matrix_L[0,1] = Matrix_L[1,2] = Matrix_L[3,4]= Matrix_L[4,5] = 1
# print(Matrix_L)
Matrix_R = np.random.rand(6,6)
Matrix_R[1,0] = Matrix_R[2,1] = Matrix_R[4,3]= Matrix_R[5,4] = 1

Matrix_U = np.random.rand(6,6)
Matrix_U[0,3] = Matrix_U[1,4] = Matrix_U[2,5] = 1

Matrix_B = np.random.rand(6,6)
Matrix_B[3,0] = Matrix_B[4,1] = Matrix_B[5,2] = 1

Matrix = {'L':Matrix_L,'R':Matrix_R,'U':Matrix_U,'B':Matrix_B}


print(find_place_occupied(eiffel_unsolved))
print(position_to_place(eiffel_unsolved))
print(eiffel_unsolved.board[0,0].left_occu)

print(find_in_board_pieces(eiffel_unsolved))
print(find_not_in_board_pieces(eiffel_unsolved))
print(find_best_one_piece_to_one_place(eiffel_unsolved,1,Matrix))

# n_row = eiffel_puzzle.shape[0]
# n_column = eiffel_puzzle.shape[1]
#
# test=Board(n_row,n_column)
# #
# test.__setitem__([0,0],eiffel_puzzle.get_piece(3))

# test._grid[0][0].left_occu = True
# test._grid[0][0].up_occu = True


#
#
# print(position_to_place(test))
#
# print(eiffel_puzzle.shape)

# print(eiffel_puzzle.get_compatibilities())
#
#
#
#

# print(test)



