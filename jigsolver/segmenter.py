from .puzzle import Piece,Puzzle,Board,Border,Slot
import numpy as np

def find_segment(puzzle,segment,pos):
    '''
    test if all neighbors of a piece are part of its segment, add them into the segment if so and recursively call the function
    :puzzle:
    '''

    for neighbor in puzzle.board.neighbors(pos[0],pos[1]): # Iter on each neighbor

        if (not isinstance(neighbor,Slot)) and (neighbor not in segment) and (puzzle.board[pos[0],pos[1]].BestBuddies(neighbor)) : ## If neighbor is a Piecen not already in segment and is best best buddies
            
            segment.append(neighbor)
            segment = find_segment(puzzle,segment,neighbor._is_placed) 
            #._is_placed attribute not yet created -> may change name
    return segment


def segmenter(puzzle,n_iter=10):
    '''Find the biggest segment of the Puzzle'''

    segments = [] # list of segments 

    for i in range(n_iter): # iterate n_iter times

        # Choose randomly first piece
        init_col = np.random.randint(0,puzzle.shape[0])
        init_row = np.random.randint(0,puzzle.shape[1])

        # Find the segment
        current_segment = find_segment(puzzle,[],(init_col,init_row))

        segments.append(current_segment)

    ## find biggest segment
    biggest_segment = max(segments,key=len)
    return biggest_segment
