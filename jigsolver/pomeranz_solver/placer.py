from jigsolver.puzzle import *
import numpy as np

'''
The role of the placer is simply to place the remaining pieces from the bag of pieces into the board.
His role is ended when all the pieces are placed on the board.

'''

def naiv_greedy_placer(puzzle, compatibilities, display=False):
    ''' 
    Place the pieces in greedy way 
    @compatibilities: compatibility matrix
    @display: set up if it will display the process of place step by step

    '''
    n_pieces = len(list(puzzle.pieces_remaining))
    
    ## INIT: no piece
    if all(not piece._is_placed for piece in puzzle.bag_of_pieces):
        n_rows, n_cols = puzzle.shape
        puzzle.place(puzzle.bag_of_pieces[0], (n_rows//2, n_cols//2))
        n_pieces -= 1
        if display:
            puzzle.display()
    for _ in range(n_pieces):
        position, piece = decide_piece_to_add(puzzle, compatibilities)
        puzzle.place(piece, position)
        if display:
            puzzle.display()


def decide_piece_to_add(puzzle, compatibilities):
    '''
    Find the best piece to add to best position in curent puzzle (means have the best compatibility)
    @compatibilities: compatibility matrix
    '''
    positions = list(available_positions(puzzle))
    assert len(positions) != 0, "No empty slot left!"
    best_value = -1
    best_position = None
    best_piece = None
    for slot_coord in positions:
        piece, value = find_best_piece_for_slot(puzzle,slot_coord,compatibilities)
        if value >= best_value:
            best_value = value
            best_position = slot_coord
            best_piece = piece
    return best_position, best_piece


def find_best_piece_for_slot(puzzle, slot_coord, compatibilities):
    '''
    Find the best piece to add to one designated slot (best means have the highest compatibility)
    @slot_coord: position of the designated slot
    @compatibilities: compatibility matrix
    '''
    best_diss_value = -1
    best_piece = None

    for piece in puzzle.pieces_remaining:
        diss_value = []
        for position,neigh in puzzle.board.neighbors(*slot_coord):
            if isinstance(neigh,Piece):
                diss_value.append(compatibilities[piece.id, neigh.id, position])

        diss_value_avg = np.mean(diss_value)
        if diss_value_avg >= best_diss_value:
            best_diss_value = diss_value_avg
            best_piece = piece

    return best_piece, best_diss_value


def available_positions(puzzle):
    """Return a generator that yields the coordinates of "available" place"""
    return (
        (i, j) for (i,j), elmt in puzzle.board.enumerate()
        if isinstance(elmt, Slot) and elmt.available
    )

