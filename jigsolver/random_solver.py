import numpy as np
from jigsolver.puzzle import Piece
from jigsolver.fonction_for_placer import *

def random_solver(puzzle,plotsteps=True):
    '''Solve a puzzle randomly'''

    # Random solver
    np.random.shuffle(puzzle.bag_of_pieces)

    # Simulate solver step by step
    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            if puzzle.board[i][j] == None: ## If location empty
                puzzle.board[i][j] = puzzle.bag_of_pieces[0]
                puzzle.bag_of_pieces = puzzle.bag_of_pieces[1:]

                if plotsteps == True : # Plot puzzle at step
                    puzzle.plot()

    return

def place_pieces(puzzle,matrix):



    return puzzle_all_placed



