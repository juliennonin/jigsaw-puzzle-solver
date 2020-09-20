import numpy as np
from .puzzle import Piece

def random_solver(puzzle,plotsteps=True):

    # Random solver
    pieces_random_idx = np.arange(len(puzzle.pieces))
    np.random.shuffle(pieces_random_idx)
    solved_puzzle = np.copy(np.array(puzzle.pieces)[pieces_random_idx])

    empty_piece = Piece(np.zeros((puzzle.patch_size,puzzle.patch_size,3)))
    empty_puzzle = np.repeat(empty_piece,puzzle.vsize*puzzle.hsize/(puzzle.patch_size**2)) ## void image, with same size as puzzle image
    puzzle.pieces = empty_puzzle

    # Simulate solver step by step
    for i in range(len(solved_puzzle)):
        puzzle.pieces[i] = solved_puzzle[i]

        if plotsteps == True :
            puzzle.plot()

    return