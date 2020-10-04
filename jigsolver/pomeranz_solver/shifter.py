from jigsolver.pomeranz_solver.placer import greedy_placer
from jigsolver.pomeranz_solver.segmenter import segmenter,remove_all_but_segment,BestBuddies_matrix
from jigsolver.metrics import pomeranz_CM,cho_CM

def shifter(puzzle,cm = pomeranz_CM):

    
    CM = cm(puzzle)
    BB = BestBuddies_matrix(CM)

    for k in range(10):
        greedy_placer(puzzle, CM, rolling=True)
        puzzle.display()

        ## Put correct position in every pieces
        for i in range(puzzle.shape[0]):
            for j in range(puzzle.shape[1]):
                puzzle.board[i,j].position = (i,j)
        
        #roll(puzzle)

        segment = segmenter(puzzle,BB,n_iter=10)
        remove_all_but_segment(puzzle,segment)
        puzzle.display()
