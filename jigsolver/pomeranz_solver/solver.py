from enum import auto
from jigsolver.pomeranz_solver.placer import greedy_placer
from jigsolver.pomeranz_solver.segmenter import segmenter,BestBuddies_matrix
from jigsolver.metrics import pomeranz_CM,BestBuddies_metric
from jigsolver.pomeranz_solver.shifter import shifter
from jigsolver.metrics import *
import matplotlib.pyplot as plt
import numpy as np

def solve(puzzle, compatibility_metric=pomeranz_CM, placer=greedy_placer, n_iter_max = 5, acceptable_score =0.98, display=True, lab_space_set = False, Auto_chose = False):
    '''
    Solve a puzzle with different color space and output the best result automatically.
    The best result means biggest sum of the score of evaluations.
    The color space can also be set manually.
    '''

    Simple_eval=[]
    Neighbor_eval=[]
    BB_eval=[]
    CM = compatibility_metric(puzzle,lab_space = lab_space_set)
    BB = BestBuddies_matrix(CM)
    puzzle.clean() 
    placer(puzzle,CM,rolling=True)
    score = BestBuddies_metric(puzzle,BB)

    Simple_eval = simple_evaluation(puzzle.ground_truth,puzzle)
    Neighbor_eval = neighbor_comparison(puzzle.ground_truth,puzzle)
    BB_eval = BestBuddies_metric(puzzle,BB)

    if Auto_chose == True:
        Simple_eval_compare=[]
        Neighbor_eval_compare=[]
        BB_eval_compare=[]
        CM_compare = compatibility_metric(puzzle,lab_space = not lab_space_set)
        BB_compare = BestBuddies_matrix(CM)
        puzzle.clean() 
        placer(puzzle,CM_compare,rolling=True)
        score_compare = BestBuddies_metric(puzzle,BB_compare)

        Simple_eval_compare = simple_evaluation(puzzle.ground_truth,puzzle)
        Neighbor_eval_compare = neighbor_comparison(puzzle.ground_truth,puzzle)
        BB_eval_compare = BestBuddies_metric(puzzle,BB_compare)
        if (Simple_eval_compare+Neighbor_eval_compare+BB_eval_compare) > (Simple_eval+Neighbor_eval+BB_eval):
            simple_eval,Neighbor_eval,BB_eval,score = Simple_eval_compare,Neighbor_eval_compare,BB_eval_compare,score_compare
            CM, BB = CM_compare, BB_compare
            puzzle.clean() 
            placer(puzzle,CM,rolling=True)
            score = BestBuddies_metric(puzzle,BB)

        else:
            puzzle.clean() 
            placer(puzzle,CM,rolling=True)
            score = BestBuddies_metric(puzzle,BB)
            

    i = 0
    while (i < n_iter_max) and (score < acceptable_score):
        
        segment = segmenter(puzzle,BB,n_iter=4)
        shifter(puzzle,segment)
        placer(puzzle,CM,rolling=True)

        score = BestBuddies_metric(puzzle,BB)
        i += 1

    if display :
        if Auto_chose == True:
            plt.title(f'NB_Pieces:{len(puzzle.bag_of_pieces)},Color space: Auto')
        elif lab_space_set == True:
            plt.title(f'NB_Pieces:{len(puzzle.bag_of_pieces)},Color space: Lab')
        else: plt.title(f'NB_Pieces:{len(puzzle.bag_of_pieces)},Color space: RGB')
        puzzle.display()



