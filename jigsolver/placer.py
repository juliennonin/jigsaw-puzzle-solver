from .puzzle import *
import numpy as np
from copy import copy
import matplotlib.pyplot as plt


def naiv_greedy_placer(puzzle, compatibilities, display=False):
    n_pieces = len(puzzle.pieces_placed)
    for _ in range(n_pieces):
        position, piece = decide_piece_to_add(puzzle, compatibilities)
        puzzle.place(piece, position)
        if display:
            puzzle.display()


def decide_piece_to_add(puzzle, compatibilities):
    best_value = 0
    best_position = None
    best_piece = None

    for slot_coord in available_positions(puzzle):
        piece, value = find_best_piece_for_slot(puzzle,slot_coord,compatibilities)
        if value > best_value:
            best_value = value
            best_position = slot_coord
            best_piece = piece
    return best_position, piece


def find_best_piece_for_slot(puzzle, slot_coord, compatibilities):
    best_diss_value = 0
    best_piece = None

    for piece in puzzle.pieces_remaining:
        diss_value = []
        for position,neigh in puzzle.board.neighbors(*slot_coord):
            if isinstance(neigh,Piece):
                diss_value.append(compatibilities[position][piece.id, neigh.id])

        diss_value_avg = (sum(diss_value) / len(diss_value))
        if diss_value_avg > best_diss_value:
            best_diss_value = diss_value_avg
            best_piece = piece

    return best_piece, best_diss_value


def available_positions(puzzle):
    """Return a generator that yields the coordinates of "available" place"""
    return (
        (i, j) for (i,j), elmt in puzzle.board.enumerate()
        if isinstance(elmt, Slot) and elmt.available
    )

