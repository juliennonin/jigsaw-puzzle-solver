from jigsolver.puzzle import *
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

def find_place_occupied(puzzle):
    list_place_occupied=[]
    n_rows, n_cols = puzzle.board.shape
    for i in np.arange(n_rows):
        for j in np.arange(n_cols):
            if isinstance(puzzle.board.__getitem__([i,j]),Piece):
                list_place_occupied.append(i*puzzle.board.shape[1]+j)

    return list_place_occupied

def position_to_place(puzzle):
    n_rows, n_cols = puzzle.board.shape
    list_place_occupied = find_place_occupied(puzzle)
    list_number_position_to_place=[]

    for e in list_place_occupied:

        if puzzle.board[e//n_cols,e%n_cols].right_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e+1])))

        if puzzle.board[e//n_cols,e%n_cols].left_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e-1])))

        if puzzle.board[e//n_cols,e%n_cols].up_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e-n_cols])))

        if puzzle.board[e//n_cols,e%n_cols].down_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e+n_cols])))


    return list_number_position_to_place


def find_in_board_pieces(puzzle):
    list_in_board_pieces = []
    for i in np.arange(puzzle.board.shape[0]):
        for j in np.arange(puzzle.board.shape[1]):
            if isinstance(puzzle.board[i,j],Piece):
                list_in_board_pieces.append(i*puzzle.board.shape[0]+j)
    return list_in_board_pieces

def find_not_in_board_pieces(puzzle):

    return list(set(list(range(puzzle.board.shape[0]*puzzle.board.shape[1]))).difference(set(find_in_board_pieces(puzzle))))



# def find_best_one_piece_to_one_place(puzzle,position_number):
#     row = position_number//puzzle.board.shape[0]
#     column = position_number % puzzle.board.shape[1]
#     diss_value = []
#     diss_value_list = []
#     list_place_occupied = find_place_occupied(puzzle)
#     not_in_space_pieces_list = list(set(list(range(puzzle.board.shape[0]*puzzle.board.shape[1]))).difference(set(list_occupied)))
#     n_average=0
#     print(not_in_space_list)

    # for e in not_in_space_list:
    #     if column != (n_column-1):
    #         if board[row][column+1] is not None:
    #             n_average=n_average+1
    #             diss_value = puzzle.get_piece(e).diss(board[row][column+1])['R']
    #     if column != 0:
    #         if board[row][column-1] is not None:
    #             n_average = n_average + 1
    #             diss_value = diss_value + puzzle.get_piece(e).diss(board[row][column-1])['L']
    #     if row !=  n_row-1:
    #         if board[row+1][column] is not None:
    #             n_average = n_average + 1
    #             diss_value = diss_value + puzzle.get_piece(e).diss(board[row][column])['B']
    #     if row != 0:
    #         if board[row-1][column] is not None:
    #             n_average = n_average + 1
    #             diss_value = diss_value + puzzle.get_piece(e).diss(board[row][column])['U']
    #
    #     diss_value_list.append(diss_value/n_average)
    #
    # return not_in_space_list[diss_value_list.index(min(diss_value_list))], min(diss_value_list)

# def decide_piece_to_add():
#
#
#     return




