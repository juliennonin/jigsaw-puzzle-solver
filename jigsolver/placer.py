from .puzzle import *
import numpy as np
from copy import copy
import matplotlib.pyplot as plt


def greedy_placer(puzzle, compatibilites, display=False):
    n, m = puzzle.shape
    n_pieces = n * m
    M = np.zeros((n_pieces, n, m)) 
    ## M[p,i,j] is the avg compatibility if piece #p was placed at (i,j) in the board 

    def update_M(piece_id, slot_coords):
        ## Remove the placed piece and the filled slot from matrix M
        M[piece_id] = 0
        M[:, slot_coords[0], slot_coords[1]] = 0

        ## Update the scores (of all remaining pieces) for all neighboring slots
        for i, j in puzzle.board.adjacent_empty_slots(*slot_coords):  # fore each neighboring slot
            adjacent_pieces = [(position, piece) for position, piece in puzzle.board.neighbors(i,j) if isinstance(piece, Piece)]
            for piece in puzzle.pieces_remaining:
                scores = [compatibilites[piece.id, adjacent.id, position] for position, adjacent in adjacent_pieces]
                M[piece.id, i, j] = sum(scores) / len(scores)

    ## Main loop: find the best piece-slot pair and place it
    for _ in range(len(list(puzzle.pieces_remaining))):
        piece_id, *coords = np.unravel_index(np.argmax(M), M.shape)
        piece = puzzle.bag_of_pieces[piece_id]
        puzzle.place(piece, coords)
        update_M(piece_id, coords)


# %%
def naiv_greedy_placer(puzzle, compatibilities, display=False):
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

