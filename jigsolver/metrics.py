from jigsolver.puzzle import Border,Puzzle
import numpy as np

'''
This library contains metrics useful for different purposes.

Firstly, we have metrics which enable to judge if two pieces are compatible relatively to a border.
They are called 'compatibility metrics' (CM) and are useful for choosing how to place the pieces in the board.
Concretely, we store them using matrix of dimension (n,n,4).
For instance, CM[i,j,Border.Left] means that we are trying 
to access to the compatibility between the i-th Piece and the j-th Piece when the j-th Piece is placed to the left of 
the i-th Piece.

There are several ways to choose compatibility metrics and here we've tested a few of them based on our intuition and
paper we have read.

Then, we have also performance metrics enable to assess the solving quality for different solvers.

'''

def dissimilarity(piece1, piece2, p=2, q=1, lab_space=False):
    """
    Return the dissimilarities between the current Piece and the other for the four sides
    @piece1,piece2: two pieces to compute dissimilarity
    @p,q: To set up the dissimilarity value is compute by L_(p,q) norms of difference between two pieces
    @lab_space: To set up the dissimilarity value is compute by Lab or RGB color space

    """
    piece1 = piece1.rgb_to_lab() if lab_space else piece1 
    piece2 = piece2.rgb_to_lab() if lab_space else piece2

    diss = [0] * len(Border)
    for border in Border:
        diss[border.value] = np.power(
            np.sum(np.power(piece1.get_border(border) - piece2.get_border(border.opposite), p)),q)

    piece1 = piece1.lab_to_rgb() if lab_space else piece1
    piece2 = piece2.lab_to_rgb() if lab_space else piece2

    return diss

def cho_CM(puzzle,lab_space=False):
    """Set the compatibility matrix associated to our current puzzle - Cho paper"""

    assert puzzle.bag_of_pieces, "A puzzle should be created"

    N = len(puzzle.bag_of_pieces)

    assert N>=2, f"There are only {N} pieces and you call that a puzzle ??"

    CM = np.zeros((N, N, 4))

    # function enabling to jump from dissimilarities into probabilities
    h = lambda x, sigma: np.round(np.exp(-x / (2 * (sigma ** 2))), 3)

    #populate the CM with dissimilarities
    for i, piece1 in enumerate(puzzle.bag_of_pieces):
        for j, piece2 in enumerate(puzzle.bag_of_pieces[:i]):
            for border in Border:
                CM[i, j, border.value] = dissimilarity(piece1,piece2,lab_space=lab_space)[border.value]
                CM[j, i, border.opposite.value] = CM[i, j, border.value]

    #turning dissimilarities into compatibilities
    for i in range(N):
        for border in Border:
            compatibilities_without_current_piece = np.sort(np.concatenate([CM[i, 0:i, border.value], CM[i, i + 1:, border.value]]))
            sigma=compatibilities_without_current_piece[1]-compatibilities_without_current_piece[0]
            sigma = sigma if sigma>0 else 1
            CM[i, :, border.value] = h(CM[i, :, border.value],sigma)

    return CM


def pomeranz_CM(puzzle, p=2, q=1,lab_space=False):

    """Set the compatibility matrix associated to our current puzzle - Pomeranz paper
    @p,q: To set up the dissimilarity value is compute by L_(p,q) norms of difference between two pieces
    """
    

    assert puzzle.bag_of_pieces, "A puzzle should be created"
    N=len(puzzle.bag_of_pieces)


    assert N>=4, f"There are only {N} pieces and you call that a puzzle ??"


    CM=np.zeros((N,N,4))

    #function enabling to jump from dissimilarities into probabilities
    h = lambda x,quartile: np.round(np.exp(-x/quartile),3)

    # populate the CM with dissimilarities
    for i, piece1 in enumerate(puzzle.bag_of_pieces):
        for j,piece2 in enumerate(puzzle.bag_of_pieces[:i]):
            for border in Border:
                CM[i,j,border.value]=dissimilarity(piece1,piece2,p=p,q=q,lab_space=lab_space)[border.value]
                CM[j,i,border.opposite.value]=CM[i,j,border.value]

    # turning dissimilarities into compatibilities
    for i in range(N):
        for border in Border:
            compatibilities_without_current_piece=np.concatenate([CM[i,0:i,border.value],CM[i,i+1:,border.value]])
            current_quartile=np.quantile(compatibilities_without_current_piece,q=0.25)
            current_quartile = current_quartile if current_quartile>0 else 1
            CM[i,:,border.value]=h(CM[i,:,border.value],current_quartile)
        CM[i][i]=0

    return CM
  
def simple_evaluation(ground_truth,solver_output):
    """
    Compare the correct position/arrangement of pieces with the arrangement of the output of the solver
    Count the fraction of correct pieces in the solver's output
    @ground_truth: The puzzle in right position/arrangement or the answer of the puzzle
    @solver_output: The position/arrangement of the output of the solver
    Return
    The right arrangement should return 1, means all pieces in the board are placed correctly
    """

    assert (isinstance(ground_truth,Puzzle) and isinstance(solver_output,Puzzle)), 'The two input should be instances of Puzzle'
    assert (ground_truth.board.shape==solver_output.board.shape), "You can't compare two inputs of different shape"
    assert (ground_truth.board and solver_output.board), "At least one input has no Board"

    n,m = ground_truth.board.shape

    return np.mean([ground_truth.board[i,j] == solver_output.board[i,j] for i in range(n) for j in range(m)])

 
def fraction_of_correct_neighbors(true_pos,ground_truth,solver_output):
    """
    For the piece located at the position pos in the solved puzzle, we compute the fraction of correct neighbors
    in the solver's output for this same piece
    @true_pos: position of piece given, to compare if it has right neighbors
    @ground_truth: The puzzle in right position/arrangement or the answer of the puzzle
    @solver_output: The position/arrangement of the output of the solver
    Return
    The right arrangement should return 1, means all neighbors of the given position are correct
    """

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
    """
    Return the average fraction of correct neighbors - Cho Paper
    @ground_truth: The puzzle in right position/arrangement or the answer of the puzzle
    @solver_output: The position/arrangement of the output of the solver
    """

    assert isinstance(ground_truth, Puzzle) and isinstance(solver_output,Puzzle), 'The two input should be instances of Puzzle'
    assert (ground_truth.board.shape == solver_output.board.shape), "You can't compare two inputs of different shape"
    assert (ground_truth.board and solver_output.board), "At least one input has no Board"

    n, m = ground_truth.board.shape

    return np.round(np.mean([fraction_of_correct_neighbors((i,j),ground_truth,solver_output) for i in range(n) for j in range(m)]),2)

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
