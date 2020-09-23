import numpy as np
import matplotlib.pyplot as plt
from copy import copy, deepcopy

class Piece():
    def __init__(self, picture):
        picture = np.array(picture)
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
        return (len(self.board), len(self.board[0]))


    def create_from_img(self, img):
        np.random.seed(self.seed)  # for reproducibility

        ## Crop the image for its size to be a multiple of the patch size
        height, width, _ = img.shape
        ps = self.patch_size
        n_rows, n_columns = height // ps, width // ps
        img_cropped = img[:n_rows * ps, :n_columns * ps]
    
        ## Populate the board
        self.board = [[None] * n_columns for _ in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_columns):
                self.board[i][j] = Piece(img_cropped[i*ps:(i+1)*ps, j*ps:(j+1)*ps])

    def shuffle(self):
        n_rows, n_colums = self.shape
        for i in range(n_rows):
            for j in range(n_colums):
                if self.board[i][j] != None :
                    self.bag_of_pieces.append(self.board[i][j])
                    self.board[i][j] = None
        np.random.shuffle(self.bag_of_pieces)
        
    def plot(self):
        assert self.board, "Puzzle board is empty"
        n_rows, n_columns = self.shape
        ps = self.patch_size
        vsize, hsize = n_rows * ps, n_columns * ps
        puzzle_plot = np.zeros([vsize, hsize, 3], dtype=int)
        for i in range(n_rows):
            for j in range(n_columns):
                piece = self.board[i][j]
                if piece:
                    picture = piece.picture
                else:
                    picture = np.zeros((ps, ps, 3))
                puzzle_plot[i*ps:(i+1)*ps, j*ps:(j+1)*ps, :] = picture
            #     if i == 0:
            #         plt.axvline(j*ps)
            # plt.axhline(i*ps)

        plt.title("puzzle vision")
        plt.imshow(puzzle_plot, 'gray')
        plt.show()

    def __copy__(self):
        new_puzzle = Puzzle(self.patch_size)
        new_puzzle.bag_of_pieces = copy(self.bag_of_pieces)
        new_puzzle.board = deepcopy(self.board)
        return new_puzzle