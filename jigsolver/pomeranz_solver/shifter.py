import numpy as np
from jigsolver.puzzle import Slot

def update_pieces_positions(puzzle):
    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            puzzle.board[i,j].position = (i,j)

def remove_all_but_segment(puzzle,segment):
    ''' 
    Remove all Pieces from board exect those in the segment 
    @segment: segment to keep in the board (normally keep the biggest segment)
    '''

    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            if puzzle.board[i,j] not in segment:
                puzzle.board[i,j]._is_placed = False
                s = Slot(i*puzzle.shape[0]+j)
                puzzle.board[i,j] = s

def shifter(puzzle,segment):
    '''Remove pieces not in the segment and roll the board if a the pieces touch the border on one side and if opposite border is available'''

    remove_all_but_segment(puzzle,segment)

    # Roll the board if necessary
    puzzle_left_border_isempty = np.all([isinstance(piece,Slot) for piece in puzzle.board[:,0]])
    puzzle_right_border_isempty = np.all([isinstance(piece,Slot) for piece in puzzle.board[:,-1]])
    puzzle_top_border_isempty = np.all([isinstance(piece,Slot) for piece in puzzle.board[0,:]])
    puzzle_bottom_border_isempty = np.all([isinstance(piece,Slot) for piece in puzzle.board[-1,:]])

    if puzzle_left_border_isempty and not puzzle_right_border_isempty : 
        puzzle.board._grid = np.roll(puzzle.board._grid, -1, axis=1)

    elif puzzle_right_border_isempty and not puzzle_left_border_isempty :
        puzzle.board._grid = np.roll(puzzle.board._grid, 1, axis=1)

    if puzzle_top_border_isempty and not puzzle_bottom_border_isempty : 
        puzzle.board._grid = np.roll(puzzle.board._grid, -1, axis=0)

    elif puzzle_bottom_border_isempty and not puzzle_top_border_isempty :
        puzzle.board._grid = np.roll(puzzle.board._grid, 1, axis=0)
    
    update_pieces_positions(puzzle)
