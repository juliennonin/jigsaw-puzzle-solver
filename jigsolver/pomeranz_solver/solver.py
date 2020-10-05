from jigsolver.pomeranz_solver.placer import greedy_placer
from jigsolver.pomeranz_solver.segmenter import segmenter,BestBuddies_matrix
from jigsolver.metrics import pomeranz_CM,BestBuddies_metric
from jigsolver.pomeranz_solver.shifter import shifter


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
