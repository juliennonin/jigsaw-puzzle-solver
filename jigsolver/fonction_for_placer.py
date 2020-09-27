from jigsolver.puzzle import *
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

def find_place_occupied(puzzle):
    """Return a generator that yields the coordinates of pieces placed on the board
    
    (The placed pieces and their coordinanted can be stored and updated
    in an attribute of board or puzzle instead)
    """
    return (
        (i, j) for (i,j), elmt in puzzle.board.enumerate()
        if isinstance(elmt, Piece))

def position_to_place(puzzle):
    n_rows, n_cols = puzzle.board.shape
    list_number_position_to_place=[]

    for (i,j) in find_place_occupied(puzzle):

        if puzzle.board[i,j].right_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e+1])))

        if puzzle.board[i,j].left_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e-1])))

        if puzzle.board[i,j].up_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e-n_cols])))

        if puzzle.board[i,j].down_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e+n_cols])))


    return list_number_position_to_place


def find_in_board_pieces(puzzle):
    return filter(lambda piece: piece.is_placed, puzzle.bag_of_pieces)

def find_not_in_board_pieces(puzzle):
    ## [OR] return [piece for piece in puzzle.bag_of_pieces if not piece.is_placed]
    return filter(lambda piece: not piece.is_placed, puzzle.bag_of_pieces)


def find_best_one_piece_to_one_place(puzzle,position_number,Matrix):
    row = position_number//puzzle.board.shape[0]
    column = position_number % puzzle.board.shape[1]
    diss_value = []
    diss_value_list = []
    # list_place_occupied = find_place_occupied(puzzle)
    not_in_board_pieces_list = find_not_in_board_pieces(puzzle)

    n_rows, n_cols = puzzle.board.shape
#     print(not_in_space_list)

    for e in not_in_board_pieces_list:
        n_average = 0
        if column != (n_cols-1):
            if isinstance(puzzle.board[row,column+1],Piece):
                n_average=n_average+1
                diss_value = Matrix['L'][e,puzzle.board[row,column+1].number]

        if column != 0:
            if isinstance(puzzle.board[row,column-1],Piece):
                n_average = n_average + 1
                diss_value = Matrix['R'][e,puzzle.board[row,column-1].number]
        if row !=  n_rows-1:
            if isinstance(puzzle.board[row+1,column],Piece):
                n_average = n_average + 1
                diss_value = Matrix['U'][e,puzzle.board[row+1,column].number]
        if row != 0:
            if isinstance(puzzle.board[row-1,column],Piece):
                n_average = n_average + 1
                diss_value = Matrix['B'][e,puzzle.board[row-1,column].number]

        diss_value_list.append(diss_value/n_average)

    return not_in_board_pieces_list[diss_value_list.index(max(diss_value_list))], max(diss_value_list),n_average

def decide_piece_to_add(puzzle, list_number_position_to_place, Matrix):
    list_prepare_to_add=[]
    for e in list_number_position_to_place:

        list_prepare_to_add.append(find_best_one_piece_to_one_place(puzzle,e, Matrix))

    print((list_prepare_to_add))
    print('numer:',list_number_position_to_place)

    list_compatibilities_to_add = [e[1] for e in list_prepare_to_add]

    #return position number, compatibility, piece number
    return  list_number_position_to_place[list_compatibilities_to_add.index(max(list_compatibilities_to_add))], \
            max(list_compatibilities_to_add), \
            find_best_one_piece_to_one_place(puzzle,list_number_position_to_place[list_compatibilities_to_add.index(max(list_compatibilities_to_add))], Matrix)[0]

def place_piece_to_position(puzzle,position_number,piece_nunmber):
    row = position_number//puzzle.board.shape[0]
    column = position_number % puzzle.board.shape[1]

    puzzle.board[row,column] = puzzle.get_piece(piece_nunmber)

    if row == 0:
        puzzle.board[row,column].up_occu = True

    elif isinstance(puzzle.board[row-1,column],Piece):
        puzzle.board[row-1,column].down_occu = True
        puzzle.board[row, column].up_occu = True

    if column == 0:
        puzzle.board[row,column].left_occu = True

    elif isinstance(puzzle.board[row, column-1], Piece):
        puzzle.board[row, column-1].right_occu = True
        puzzle.board[row, column].left_occu = True

    if row == puzzle.shape[0]-1:
        puzzle.board[row,column].down_occu = True

    elif isinstance(puzzle.board[row+1, column], Piece):
        puzzle.board[row+1, column].up_occu = True
        puzzle.board[row, column].down_occu = True

    if column == puzzle.shape[1]-1:
        puzzle.board[row,column].right_occu = True

        print('test1')

    elif isinstance(puzzle.board[row, column+1], Piece):
        puzzle.board[row, column+1].left_occu = True
        puzzle.board[row, column].right_occu = True




    return puzzle






