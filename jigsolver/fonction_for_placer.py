from jigsolver.puzzle import *
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

def find_place_occupied(board):
    n_row, n_col = board.shape
    list_occupied=[]
    for i in np.arange(n_row):
        for j in np.arange(n_col):
            if isinstance(board.__getitem__([i,j]),Piece):
                list_occupied.append([i,j])

    return list_occupied

def position_to_place(board):
    list_occupied = find_place_occupied(board)
    list_number_position_to_place=[]
    n_rows, n_cols = board.shape
    for e in list_occupied:

        if board._grid[e[0]][e[1]].right_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e[0]*n_cols+e[1]+1])))

        if board._grid[e[0]][e[1]].left_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e[0]*n_cols+e[1]-1])))

        if board._grid[e[0]][e[1]].up_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([(e[0]-1)*n_cols+e[1]])))

        if board._grid[e[0]][e[1]].down_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([(e[0]+1)*n_cols+e[1]])))


    return list_number_position_to_place


def find_best_one_piece_to_one_place(board,n_row,n_column,position_number,puzzle,in_space_list):
    row = position_number//n_column
    column = position_number % n_column
    diss_value = []
    diss_value_list = []
    not_in_space_list = list(set(list(range(n_row*n_column))).difference(set(in_space_list)))
    n_average=0
    for e in not_in_space_list:
        if column != (n_column-1):
            if board[row][column+1] is not None:
                n_average=n_average+1
                diss_value = puzzle.get_piece(e).diss(board[row][column+1])['R']
        if column != 0:
            if board[row][column-1] is not None:
                n_average = n_average + 1
                diss_value = diss_value + puzzle.get_piece(e).diss(board[row][column-1])['L']
        if row !=  n_row-1:
            if board[row+1][column] is not None:
                n_average = n_average + 1
                diss_value = diss_value + puzzle.get_piece(e).diss(board[row][column])['B']
        if row != 0:
            if board[row-1][column] is not None:
                n_average = n_average + 1
                diss_value = diss_value + puzzle.get_piece(e).diss(board[row][column])['U']

        diss_value_list.append(diss_value/n_average)

    return not_in_space_list[diss_value_list.index(min(diss_value_list))], min(diss_value_list)

# def decide_piece_to_add():
#
#
#     return




