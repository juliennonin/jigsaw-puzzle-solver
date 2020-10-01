
from jigsolver.puzzle import Border,Puzzle
import numpy as np


def dissimilarity(piece1, piece2, p=2, q=1, lab_space=False):
    """Return the dissimilarities between the current Piece and the other for the four sides"""
    piece1 = piece1.rgb_to_lab() if lab_space else piece1
    piece2 = piece2.rgb_to_lab() if lab_space else piece2

    diss = [0] * len(Border)
    for border in Border:
        diss[border.value] = np.power(
            np.sum(np.power(piece1.get_border(border) - piece2.get_border(border.opposite), p)),q)
    return diss


def cho_CM(puzzle):
    """Set the compatibility matrix associated to our current puzzle - Cho paper"""

    assert puzzle.bag_of_pieces, "A puzzle should be created"

    CM=[]

    #function enabling to jump from dissimilarities into probabilities
    h = lambda x,sigma: np.round(np.exp(-x / (2 * (sigma ** 2))),3)

    for i, piece in enumerate(puzzle.bag_of_pieces):

        #We need to obtain the dissimilarities between the current
        #Piece and all the others Piece.
        f = lambda other_piece: dissimilarity(piece, other_piece)
        # g = lambda other_piece: list(f(otherPiece).values())

        CM.append([f(otherPiece) for otherPiece in puzzle.bag_of_pieces])

        # **Normalization of dissimilarities (suggested by the Cho Paper)**

        #We don't count the current piece for the normalization
        Values = list((map(f,filter(lambda x: x!=piece,puzzle.bag_of_pieces))))

        #Then, we need the two smallest dissimilarities so we can sort our list values to obtain them
        Values=np.sort(np.array(Values).reshape(-1))

        #kind of standard deviation - handling of the case where there are only two pieces
        try:
            sigma=(Values[1]-Values[0]) if (Values[1]-Values[0]!=0) else 1
        except:
            sigma=Values[0] if (Values[0]!=0) else 1

        #Normalization
        for diss in CM[-1]:
            for i in range(len(diss)):
                diss[i] = h(diss[i],sigma)

    return np.array(CM)


def pomeranz_CM(puzzle, p=2, q=1):
    """Set the compatibility matrix associated to our current puzzle - Pomeranz paper"""

    assert puzzle.bag_of_pieces, "A puzzle should be created"

    CM=[]

    #function enabling to jump from dissimilarities into probabilities
    h = lambda x,quartile: np.round(np.exp(-x/quartile),3)

    for i, piece in enumerate(puzzle.bag_of_pieces):

        #We need to obtain the dissimilarities between the current
        #Piece and all the others Piece.
        f = lambda other_piece: dissimilarity(piece, other_piece, p=p, q=q)

        left=lambda otherPiece: f(otherPiece)[Border.LEFT.value]
        right=lambda otherPiece : f(otherPiece)[Border.RIGHT.value]
        top=lambda otherPiece : f(otherPiece)[Border.TOP.value]
        bottom=lambda otherPiece : f(otherPiece)[Border.BOTTOM.value]

        CM.append([f(otherPiece) for otherPiece in puzzle.bag_of_pieces])

        # **Normalization of dissimilarities (suggested by the Cho Paper)**

        #We don't count the current piece for the normalization
        Left = list(map(left, filter(lambda p: p.id != piece.id, puzzle.bag_of_pieces)))
        Right = list((map(right, filter(lambda p: p.id != piece.id, puzzle.bag_of_pieces))))
        Top = list((map(top, filter(lambda p: p.id != piece.id, puzzle.bag_of_pieces))))
        Bottom = list((map(bottom, filter(lambda p: p.id != piece.id, puzzle.bag_of_pieces))))

        #Then, we need the two smallest dissimilarities so we can sort our list values to obtain them
        quartiles={}
        quartiles[Border.LEFT.value] = np.quantile(Left,q=0.25) if np.quantile(Left,q=0.25)!=0 else 1
        quartiles[Border.RIGHT.value] = np.quantile(Right, q=0.25) if np.quantile(Right,q=0.25)!=0 else 1
        quartiles[Border.TOP.value] = np.quantile(Top, q=0.25) if np.quantile(Top,q=0.25)!=0 else 1
        quartiles[Border.BOTTOM.value] = np.quantile(Bottom,q=0.25) if np.quantile(Bottom,q=0.25)!=0 else 1

        #Normalization
        for diss in CM[-1]:
            for i in range(len(diss)):
                diss[i]=h(diss[i], quartiles[i])

    return np.array(CM)

def simple_evaluation(ground_truth,solver_output):
    """Count the fraction of correct pieces in the solver's output"""
     assert isinstance(ground_truth,Puzzle) and isinstance(solver_output,Puzzle), 'The two input should be instances of Puzzle'
     assert (ground_truth.board.shape==solver_output.board.shape), "You can't compare two inputs of different shape"
     assert (ground_truth.board and solver_output.board), "At least one input has no Board"

     n,m = ground_truth.board.shape

     return np.mean([ground_truth.board[i,j] == solver_output.board[i,j] for i in range(n) for j in range(m)])

def fraction_of_correct_neighbors(true_pos,ground_truth,solver_output):
    """For the piece located at the position pos in the solved puzzle, we compute the fraction of correct neighbors
    in the solver's output for this same piece"""

    assert isinstance(ground_truth, Puzzle) and isinstance(solver_output,Puzzle), 'The two input should be instances of Puzzle'
    assert (ground_truth.board.shape == solver_output.board.shape), "You can't compare two inputs of different shape"
    assert (ground_truth.board and solver_output.board), "At least one input has no Board"


    i,j=true_pos

    correct_neighbors={}

    for border,neighbor in ground_truth.board.neighbors(i,j):
        correct_neighbors[border]=neighbor


    current_Piece=ground_truth.board[i,j]

    #we need to find the position of the current piece in the solver's output
    inferred_pos=solver_output.find_position(current_Piece.id)
    r,s=inferred_pos

    nb_incorrect_neighbors=0
    nb_neigbors=0

    for border, neighbor in solver_output.board.neighbors(r,s):
            nb_neigbors+=1
            # if there is a neighbor that shouldn't exist then, it's a wrong neighbor
            if not(border) in correct_neighbors:
                nb_incorrect_neighbors+=1
            else:
                nb_incorrect_neighbors+=not((correct_neighbors[border]==neighbor))

    return np.round((nb_neigbors-nb_incorrect_neighbors)/nb_neigbors,2)

def neighbor_comparison(ground_truth,solver_output):
    """Return the average fraction of correct neighbors - Cho Paper"""
    assert isinstance(ground_truth, Puzzle) and isinstance(solver_output,Puzzle), 'The two input should be instances of Puzzle'
    assert (ground_truth.board.shape == solver_output.board.shape), "You can't compare two inputs of different shape"
    assert (ground_truth.board and solver_output.board), "At least one input has no Board"

    n, m = ground_truth.board.shape

    return np.mean([fraction_of_correct_neighbors((i,j),ground_truth,solver_output) for i in range(n) for j in range(m)])




















































