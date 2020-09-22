import numpy as np
import matplotlib.pyplot as plt
from copy import copy, deepcopy

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
    def right_side(self):
        return self.data[:, -1]

    @property
    def left_side(self):
        return self.data[:, 0]

    @property
    def up_side(self):
        return self.data[0, :]
        
    @property
    def down_side(self):
        return self.data[-1, :]


class Puzzle():
    def __init__(self, patch_size=100, seed=0):
        self.patch_size = patch_size
        self.seed = seed
        self.bag_of_pieces = []
        self.board = None
        # hsize=0
        # self.vsize=0
        # self.puzzle_img=None

    @property
    def shape(self):
        assert self.board, "Puzzle board is empty."
        return self.board.shape


    def create_from_img(self, img):
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
        n_rows, n_colums = self.shape
        for i in range(n_rows):
            for j in range(n_colums):
                self.bag_of_pieces.append(self.board[i,j])
        self.board = Board(n_rows, n_colums, self.patch_size)
        np.random.shuffle(self.bag_of_pieces)


    def display(self):
        assert self.board, "Puzzle board is empty"
        n_rows, n_columns = self.shape
        ps = self.patch_size
        vsize, hsize = n_rows * ps, n_columns * ps
        puzzle_plot = np.zeros([vsize, hsize, 3], dtype=int)
        for i in range(n_rows):
            for j in range(n_columns):
                puzzle_plot[i*ps:(i+1)*ps, j*ps:(j+1)*ps, :] = self.board[i,j].picture
                
        plt.imshow(puzzle_plot)
        plt.show()


    def __copy__(self):
        new_puzzle = Puzzle(self.patch_size)
        new_puzzle.bag_of_pieces = copy(self.bag_of_pieces)
        new_puzzle.board = deepcopy(self.board)
        return new_puzzle