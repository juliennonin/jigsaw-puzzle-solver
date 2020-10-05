from jigsolver.pomeranz_solver.placer import greedy_placer
from jigsolver.pomeranz_solver.segmenter import segmenter,BestBuddies_matrix
from jigsolver.metrics import pomeranz_CM
#,BestBuddies_metric
from jigsolver.pomeranz_solver.shifter import shifter


import numpy as np
def BestBuddies_metric(solver_output,BB):
    """
        Return the ratio between the number of neighbors who are said to be best buddies and the total number
        of neighbors. - Pomeranz Paper
        @solver_output: The position/arrangement of the output of the solver
        @BB : The best buddies matrix
        N.B. : This metric can be computed without knowing at all the solved puzzle
    """
    nb_pieces_height,nb_pieces_width=solver_output.shape
    nb_neigbors=4*(nb_pieces_height-1)*(nb_pieces_width-1)+8+2*(nb_pieces_width+nb_pieces_height-4)
    return np.round(np.sum(BB==1)/nb_neigbors,2)

def solve(puzzle, compatibility_metric=pomeranz_CM, placer=greedy_placer, n_iter_max = 5, acceptable_score =0.98, display=True):
    '''Solve a puzzle'''

    CM = compatibility_metric(puzzle)
    BB = BestBuddies_matrix(CM)
    
    placer(puzzle,CM,rolling=True)
    score = BestBuddies_metric(puzzle,BB)

    if display :
        puzzle.display()  

    i = 0
    while (i < n_iter_max) and (score < acceptable_score):
        
        segment = segmenter(puzzle,BB,n_iter=4)
        shifter(puzzle,segment)
        placer(puzzle,CM,rolling=True)

        score = BestBuddies_metric(puzzle,BB)
        i += 1

        if display :
            puzzle.display() 
