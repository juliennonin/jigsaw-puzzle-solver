from jigsolver.puzzle import Slot,Border
import numpy as np

'''
The role of the segmenter is to identify sets of pieces for which it seems that they are well matched.
When this is done, following the idea of Pomeranz, we kept the segment with the highest size in the board 
and, we restart to place the pieces with this new configuration.
'''

def BestBuddies_matrix(CM,diag=True):
    '''Compute the Best Buddies matrix based on the compatibility matrix'''
    if diag :
        for k in range(CM.shape[2]):
            np.fill_diagonal(CM[:,:,k],0) # Put compatibility between same pieces at 0

    #Initialize Best Buddies matrix
    BB = np.zeros(CM.shape)

    for i in range(CM.shape[0]):
        for b in Border :
            best_neighbour = np.argmax(CM[i,:,b.value])
            if np.argmax(CM[best_neighbour,:,b.opposite.value]) == i:
                BB[i,best_neighbour,b.value] = 1
                #BB[best_neighbour,i,b.opposite.value] = 1

    return BB


def find_segment(puzzle,segment,pos,BB):
    '''
    test if all neighbors of a piece are part of its segment, add them into the segment if so and recursively call the function
    '''
    if isinstance(puzzle.board[pos[0],pos[1]],Slot): # If initial piece is empty -> return 
        return segment

    for border,neighbor in puzzle.board.neighbors(pos[0],pos[1]): # Iter on each neighbor
        if (not isinstance(neighbor,Slot)) and (neighbor not in segment) and (BB[puzzle.board[pos[0],pos[1]].id,neighbor.id,border]) : ## If neighbor is a Piecen not already in segment and is best best buddies
            
            segment.append(neighbor) ## Add neighbor to segment
            segment = find_segment(puzzle,segment,neighbor.position,BB) 
    return segment


def segmenter(puzzle,BB,n_iter=False):
    '''Find the biggest segment of the Puzzle'''

    segments = [] # list of segments 

    if not n_iter : 
        n_iter = max(5,int((puzzle.shape[0] * puzzle.shape[1]) /5))

    for i in range(n_iter): # iterate n_iter times, #TODO make it dependant of size of the board 

        # Choose randomly first piece
        init_col = np.random.randint(0,puzzle.shape[0])
        init_row = np.random.randint(0,puzzle.shape[1])

        # Find the segment
        current_segment = find_segment(puzzle,[],(init_col,init_row),BB)

        segments.append(current_segment)

    ## find biggest segment
    biggest_segment = max(segments,key=len)
    return biggest_segment

def remove_all_but_segment(puzzle,segment):
    ''' Remove all Pieces from board exect those in the segment '''
    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            if puzzle.board[i,j] not in segment:
                puzzle.board[i,j]._is_placed = False
                puzzle.board[i,j]=Slot(i*puzzle.shape[0]+j)