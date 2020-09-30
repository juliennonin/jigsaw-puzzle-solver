import numpy as np
import matplotlib.pyplot as plt

from enum import Enum
from copy import copy, deepcopy
from skimage import io, color

class Border(Enum):
    def __new__(cls, value, slice):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.slice = slice
        return obj
    TOP = (0, np.index_exp[0,:])
    RIGHT = (1, np.index_exp[:,-1])
    BOTTOM = (2, np.index_exp[-1,:])
    LEFT = (3, np.index_exp[:,0])

    @property
    def opposite(self):
        opposite_value = (self.value + 2) % 4
        if 0 <= opposite_value <= 3:
            return Border(opposite_value)
        raise NotImplementedError     


class Board():
    def __init__(self, n_rows, n_cols):
        self._grid = np.array([[Slot(i * n_cols + j) for j in range(n_cols)] for i in range(n_rows)])

    def __getitem__(self, coords):
        i, j = coords
        return self._grid[i,j]

    def __setitem__(self, coords, value):
        assert isinstance(value, Slot) or isinstance(value, Piece), (
            f"value is an instance of {type(value)} instead of Slot or Piece")
        i, j = coords
        self._grid[i,j] = value

    def __iter__(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                yield self._grid[i,j]

    def enumerate(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                yield (i, j), self._grid[i,j]

    @property
    def shape(self):
        return self._grid.shape

    def neighbors(self, i, j):
        if i > 0:
            yield Border.TOP.value, self[i-1, j]
        if j < self.shape[1]-1:
            yield Border.RIGHT.value, self[i, j+1]
        if i < self.shape[0]-1:
            yield Border.BOTTOM.value, self[i+1, j]
        if j > 0:
            yield Border.LEFT.value, self[i, j-1]


class Slot():
    def __init__(self, id):
        self._id = id
        self.available = False
    
    @property
    def id(self):
        return self._id

    @property
    def picture(self):
            return 0



class Piece():
    def __init__(self, picture, id=None):
        picture = np.array(picture, dtype=int)
        assert picture.ndim == 3, "The picture must be 3-dimensional, i.e. of shape (n,n,3)"
        assert picture.shape[2] == 3, "Each pixel of the picture must have 3 color values"
        assert picture.shape[0] == picture.shape[1], "The image must not be rectangular but squared in shape"

        self._id = id
        self.picture = picture
        self._is_placed = False

    @property
    def id(self):
        return self._id

    @property
    def is_placed(self):
        return self._is_placed

    @property
    def size(self):
        return len(self.picture)

    def get_border(self, border):
        return self.picture[border.slice]

    def rgb_to_lab(self):
        return color.rgb2lab(self.picture)

    def lab_to_rgb(self):
        return color.lab2rgb(self.picture)

    def _clean(self):
        self._is_placed = False

    def diss(self, other, p=2, q=1, lab_space=False):
        '''Return the dissimilarities between the current Piece and the other for the four sides'''

        currentPiece=self.rgb_to_lab() if lab_space else self

        diss = {}
        for border in Border:
            diss[border] = np.power(
                np.sum(np.power(self.get_border(border) - other.get_border(border.opposite), p)),q)
        return diss

    def __eq__(self, other):
        if isinstance(other, Piece):
            return np.allclose(self.picture, other.picture)
        return False


class Cho():

    def __init__(self,puzzle):
        self.puzzle=puzzle

    def set_CM(self):
        "set the compatibility matrix associated to our current puzzle - Cho paper"

        assert self.puzzle.bag_of_pieces, "A puzzle should be created"

        CM=[]

        #function enabling to jump from dissimilarities into probabilities
        h = lambda x,sigma: np.round(np.exp(-x / (2 * (sigma ** 2))),3)

        for i,Piece in enumerate(self.puzzle.bag_of_pieces):

            #We need to obtain the dissimilarities between the current
            #Piece and all the others Piece.
            f=lambda otherPiece: Piece.diss(otherPiece)
            g=lambda otherPiece: list(f(otherPiece).values())

            CM.append([f(otherPiece) for otherPiece in self.puzzle.bag_of_pieces])

            # **Normalization of dissimilarities (suggested by the Cho Paper)**

            #We don't count the current piece for the normalization
            Values = list((map(g,filter(lambda x: x!=Piece,self.puzzle.bag_of_pieces))))

            #Then, we need the two smallest dissimilarities so we can sort our list values to obtain them
            Values=np.sort(np.array(Values).reshape(-1))

            #kind of standard deviation - handling of the case where there are only two pieces
            try:
                sigma=(Values[1]-Values[0]) if (Values[1]-Values[0]!=0) else 1
            except:
                sigma=Values[0] if (Values[0]!=0) else 1

            #Normalization
            for diss in CM[-1]:
                for key in diss.keys():
                    diss[key]=h(diss[key],sigma)

            self.puzzle.CM=np.array(CM)

class Pomeranz():
    def __init__(self,puzzle,p=2,q=1):
        self.puzzle=puzzle
        self.p=p
        self.q=q

    def set_CM(self):
        "set the compatibility matrix associated to our current puzzle - Pomeranz paper"

        assert self.puzzle.bag_of_pieces, "A puzzle should be created"

        CM=[]

        #function enabling to jump from dissimilarities into probabilities
        h = lambda x,quartile: np.round(np.exp(-x/quartile),3)

        for i,Piece in enumerate(self.puzzle.bag_of_pieces):

            #We need to obtain the dissimilarities between the current
            #Piece and all the others Piece.
            f=lambda otherPiece: Piece.diss(otherPiece,p=self.p,q=self.q)

            left=lambda otherPiece: f(otherPiece)[Border.LEFT]
            right=lambda otherPiece : f(otherPiece)[Border.RIGHT]
            top=lambda otherPiece : f(otherPiece)[Border.TOP]
            bottom=lambda otherPiece : f(otherPiece)[Border.BOTTOM]

            CM.append([f(otherPiece) for otherPiece in self.puzzle.bag_of_pieces])

            # **Normalization of dissimilarities (suggested by the Cho Paper)**

            #We don't count the current piece for the normalization
            Left = list(map(left,filter(lambda x: x!=Piece,self.puzzle.bag_of_pieces)))
            Right = list((map(right, filter(lambda x: x != Piece, self.puzzle.bag_of_pieces))))
            Top = list((map(top, filter(lambda x: x != Piece, self.puzzle.bag_of_pieces))))
            Bottom = list((map(bottom, filter(lambda x: x != Piece, self.puzzle.bag_of_pieces))))

            #Then, we need the two smallest dissimilarities so we can sort our list values to obtain them
            quartiles={}
            quartiles[Border.LEFT]=np.quantile(Left,q=0.25) if np.quantile(Left,q=0.25)!=0 else 1
            quartiles[Border.RIGHT]=np.quantile(Right, q=0.25) if np.quantile(Right,q=0.25)!=0 else 1
            quartiles[Border.TOP]=np.quantile(Top, q=0.25) if np.quantile(Top,q=0.25)!=0 else 1
            quartiles[Border.BOTTOM]=np.quantile(Bottom,q=0.25) if np.quantile(Bottom,q=0.25)!=0 else 1

            #Normalization
            for diss in CM[-1]:
                for key in diss.keys():
                    diss[key]=h(diss[key],quartiles[key])

        self.puzzle.CM=np.array(CM)


class Puzzle():
    def __init__(self, patch_size=100, seed=0):
        self.patch_size = patch_size
        self.seed = seed
        self.bag_of_pieces = []
        self.board = None
        self.solver=Cho(self)

    @property
    def shape(self):
        '''Return the shape of the board of the Puzzle'''
        assert self.board, "Puzzle board is empty."
        return self.board.shape

    @property
    def pieces_placed(self):
        return filter(lambda piece: piece.is_placed, self.bag_of_pieces)

    @property
    def pieces_remaining(self):
        return [piece for piece in self.bag_of_pieces if not piece.is_placed]
        #≡ return filter(lambda piece: not piece.is_placed, self.bag_of_pieces)

    def create_from_img(self, img):
        '''Create the pieces from an img and put them in the board'''
        np.random.seed(self.seed)  # for reproducibility

        ## Crop the image for its size to be a multiple of the patch size
        height, width, _ = img.shape
        ps = self.patch_size
        n_rows, n_columns = height // ps, width // ps
        img_cropped = img[:n_rows * ps, :n_columns * ps]
    
        ## Populate the board
        self.board = Board(n_rows, n_columns)
        for i in range(n_rows):
            for j in range(n_columns):
                piece = Piece(img_cropped[i*ps:(i+1)*ps, j*ps:(j+1)*ps], i * n_columns + j)
                self.bag_of_pieces.append(piece)
                self.board[i,j] = piece
        return self

    def shuffle(self):
        '''Took all pieces from the board to the bag of pieces, and shuffle it'''
        n_rows, n_colums = self.shape
        self.board = Board(n_rows, n_colums)
        np.random.shuffle(self.bag_of_pieces)
        for i, piece in enumerate(self.bag_of_pieces):
            piece._is_placed = False
            piece._id = i

    
    def place(self, piece, coords):
        """Places a piece at the given coordinates
            * set _is_placed to True
            * make the neighboring slots available
        """
        i, j = coords
        assert isinstance(piece, Piece), "must be an instance of Piece."
        assert isinstance(self.board[i, j], Slot), f"A piece is already placed at {coords}."
        assert not piece._is_placed, "This Piece has already been placed"
        
        self.board[i,j] = piece
        piece._is_placed = True
        for position, slot in self.board.neighbors(i, j):
            if isinstance(slot, Slot):
                slot.available = True


    def display(self, show_borders=True):
        assert self.board, "Puzzle board is empty"
        n_rows, n_columns = self.shape
        ps = self.patch_size
        vsize, hsize = n_rows * ps, n_columns * ps
        puzzle_plot = np.zeros([vsize, hsize, 3], dtype=int)
        for i in range(n_rows):
            for j in range(n_columns):
                puzzle_plot[i*ps:(i+1)*ps, j*ps:(j+1)*ps, :] = self.board[i,j].picture

        if show_borders:
            for i in range(n_rows):
                plt.axhline(i*ps-.5, c="w")
            for j in range(n_columns):
                plt.axvline(j*ps-.5, c="w")
        plt.xticks(np.arange(-.5, hsize+1, ps), np.arange(0, hsize+1, ps))
        plt.yticks(np.arange(-.5, vsize+1, ps), np.arange(0, vsize+1, ps))
    
        plt.imshow(puzzle_plot)
        plt.show()

    def clean(self):
        "clean the current puzzle | Restart the party"
        self.board = Board(*self.shape)
        for piece in self.bag_of_pieces:
            piece._clean()


    def set_CM(self):
        self.solver.set_CM()

    def set_Pomeranz(self,p=2,q=1):
        self.solver=Pomeranz(self,p,q)

    def __copy__(self):
        new_puzzle = Puzzle(self.patch_size)
        new_puzzle.bag_of_pieces = copy(self.bag_of_pieces)
        new_puzzle.board = deepcopy(self.board)
        return new_puzzle
