import numpy as np
import matplotlib.pyplot as plt
from copy import copy, deepcopy
from skimage import io, color

class Board():
    def __init__(self, n_rows, n_cols, patch_size):
        self._grid = [[Slot(patch_size) for j in range(n_cols)] for i in range(n_rows)]

    def __getitem__(self, coords):
        i, j = coords
        return self._grid[i][j]

    def __setitem__(self, coords, value):
        i, j = coords
        if isinstance(value, Slot) or isinstance(value, Piece):
            self._grid[i][j] = value
        else:
            raise AttributeError("value must be an instance of Slot or Piece")

    def __iter__(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                yield self._grid[i][j]

    @property
    def shape(self):
        return (len(self._grid), len(self._grid[0]))

    def neighbors(self, i, j):
        #up
        if i > 0:
            yield self[i-1, j]
        #right
        if j < self.shape[1]-1:
            yield self[i, j+1]
        #down
        if i < self.shape[0]-1:
            yield self[i+1, j]
        #left
        if j > 0:
            yield self[i, j-1]


class Slot():
    def __init__(self, patch_size):
        self.patch_size = patch_size

    @property
    def picture(self):
            return np.zeros((self.patch_size, self.patch_size, 3))



class Piece():
    def __init__(self, picture):
        picture = np.array(picture, dtype=int)
        assert picture.ndim == 3, "The picture must be 3-dimensional, i.e. of shape (n,n,3)"
        assert picture.shape[2] == 3, "Each pixel of the picture must have 3 color values"
        assert picture.shape[0] == picture.shape[1], "The image must not be rectangular but squared in shape"

        self.picture = picture

    @property
    def size(self):
        return len(self.picture)

    @property
    def right(self):
        return self.picture[:,-1,:].reshape(self.size,1,3)

    @property
    def left(self):
        return self.picture[:,0,:].reshape(self.size,1,3)

    @property
    def up(self):
        return self.picture[0,:,:].reshape(1,self.size,3)
        
    @property
    def bottom(self):
        return self.picture[-1,:,:].reshape(1,self.size,3)

    def rgb_to_lab(self):
        return color.rgb2lab(self.picture)

    def lab_to_rgb(self):
        return color.lab2rgb(self.picture)

    def diss(self,otherPiece,lab_space=False):
        '''Return the dissimilarities between the current Piece and the otherPiece for the four sides'''

        currentPiece=self.rgb_to_lab() if lab_space else self

        dict={}
        dict['L']=np.sum(np.power((otherPiece.right-currentPiece.left),2))
        dict['R']=np.sum(np.power((currentPiece.right-otherPiece.left),2))
        dict['U']=np.sum(np.power((otherPiece.bottom-currentPiece.up),2))
        dict['B'] = np.sum(np.power((currentPiece.bottom - otherPiece.up), 2))

        return dict

    def __eq__(self, otherPiece):
        return np.allclose(Piece.picture,otherPiece.picture)




class Puzzle():
    def __init__(self, patch_size=100, seed=0):
        self.patch_size = patch_size
        self.seed = seed
        self.bag_of_pieces = []
        self.board = None

    @property
    def shape(self):
        '''Return the shape of the board of the Puzzle'''
        assert self.board, "Puzzle board is empty."
        return self.board.shape


    def create_from_img(self, img):
        '''Create the pieces from an img and put them in the board'''
        np.random.seed(self.seed)  # for reproducibility

        ## Crop the image for its size to be a multiple of the patch size
        height, width, _ = img.shape
        ps = self.patch_size
        n_rows, n_columns = height // ps, width // ps
        img_cropped = img[:n_rows * ps, :n_columns * ps]
    
        ## Populate the board
        self.board = Board(n_rows, n_columns, ps)
        for i in range(n_rows):
            for j in range(n_columns):
                self.board[i,j] = Piece(img_cropped[i*ps:(i+1)*ps, j*ps:(j+1)*ps])
        return self


    def shuffle(self):
        '''Took all pieces from the board to the bag of pieces, and shuffle it'''
        n_rows, n_colums = self.shape
        for i in range(n_rows):
            for j in range(n_colums):
                self.bag_of_pieces.append(self.board[i,j])
        self.board = Board(n_rows, n_colums, self.patch_size)
        np.random.shuffle(self.bag_of_pieces)


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

    def get_compatibilities(self):
        "Return the compatibility matrix associated to our current puzzle"

        assert self.bag_of_pieces, "A puzzle should be created"

        CM=[]


        for i,Piece in enumerate(self.bag_of_pieces):

            bag_of_pieces=self.bag_of_pieces.copy()

            f=lambda otherPiece: Piece.diss(otherPiece)
            g=lambda otherPiece: list(Piece.diss(otherPiece).values())

            CM.append([f(otherPiece) for otherPiece in bag_of_pieces])

            #We don't count the current piece for the normalization
            del bag_of_pieces[i]
            Values = np.sort(list(map(g,bag_of_pieces))).reshape(-1)

            sigma=Values[1]-Values[0]
            h = lambda x: np.exp(-x/ (2 * (sigma ** 2)))

            #Normalization
            for diss in CM[-1]:
                for key in ('L','R','U','B'):
                    diss[key]=h(diss[key])


        return np.array(CM)


    def __copy__(self):
        new_puzzle = Puzzle(self.patch_size)
        new_puzzle.bag_of_pieces = copy(self.bag_of_pieces)
        new_puzzle.board = deepcopy(self.board)
        return new_puzzle