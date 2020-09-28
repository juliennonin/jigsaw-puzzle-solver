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
    """Return a generator that yields the coordinates of "available" place"""
    return (
        (i, j) for (i,j), elmt in puzzle.board.enumerate()
        if isinstance(elmt, Slot) and elmt.available
    )

def find_in_board_pieces(puzzle):
    return filter(lambda piece: piece.is_placed, puzzle.bag_of_pieces)

def find_not_in_board_pieces(puzzle):
    return [piece for piece in puzzle.bag_of_pieces if not piece.is_placed]
    # return filter(lambda piece: not piece.is_placed, puzzle.bag_of_pieces)


def find_best_one_piece_to_one_place(puzzle,slot_coord,Matrix):
    row,column = slot_coord

    best_diss_value = 0

    # list_place_occupied = find_place_occupied(puzzle)
    not_in_board_pieces_list = find_not_in_board_pieces(puzzle)
    best_piece = not_in_board_pieces_list[0]
    n_rows, n_cols = puzzle.board.shape
#     print(not_in_space_list)

    for piece in not_in_board_pieces_list:
        diss_value = []
        for position,neigh in puzzle.board.neighbors(row,column):
            if isinstance(neigh,Piece):
                diss_value.append(Matrix[position][piece.id, neigh.id])
        diss_value_avg = (sum(diss_value) / len(diss_value))
        if diss_value_avg > best_diss_value:
            best_diss_value = diss_value_avg
            best_piece = piece

    return best_piece, best_diss_value


def decide_piece_to_add(puzzle, Matrix):
    best_value = 0
    best_position = None
    best_piece = None

    for slot_coord in position_to_place(puzzle):
        piece, value = find_best_one_piece_to_one_place(puzzle,slot_coord,Matrix)
        if value > best_value:
            best_value = value
            best_position = slot_coord
            best_piece = piece
    return best_position, piece



def place_piece_to_position(puzzle,piece,coords):
    """Places a piece at the given coordinates
        * set _is_placed to True
        * make the neighboring slots available
    """
    i, j = coords
    puzzle.board[i,j] = piece
    piece._is_placed = True
    for slot in puzzle.board.neighbor(i, j):
        if isinstance(slot, Slot):
            slot.available = True
    return puzzle