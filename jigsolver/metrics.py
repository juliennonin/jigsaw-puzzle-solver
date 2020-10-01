
from jigsolver.puzzle import Border
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