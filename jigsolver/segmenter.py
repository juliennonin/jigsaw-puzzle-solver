from .puzzle import Piece,Puzzle,Board,Border
import numpy as np

def find_segment(puzzle,segment,pos):

    for neighbor in puzzle.board.neighbors(pos[0],pos[1]): # Iter on each neighbor

        if (neighbor not in segment) and (puzzle.board[pos[0],pos[1]].BestBuddies(neighbor)): ## If neighbor not already in segment and is best best buddies

            segment.append(neighbor)
            segment = find_segment(puzzle,segment,neighbor.position) # 
    return segment


def segmenter(puzzle,n_iter=10):
    segments = [] # list of segments 

    for i in range(n_iter): # iterate n_iter times

        # Choose randomly first piece
        init_col = np.random.randint(0,puzzle.shape[0])
        init_row = np.random.randint(0,puzzle.shape[1])

        # Find the segment
        current_segment = find_segment(puzzle,[],(init_col,init_row))

        segments.append(current_segment)

    ## find biggest segment and return it
    return segments
