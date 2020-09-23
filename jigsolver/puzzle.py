import numpy as np
import matplotlib.pyplot as plt
from copy import copy, deepcopy
from skimage import io, color

class Piece():
    def __init__(self, picture):
        picture = np.array(picture)
        assert picture.ndim == 3, "The picture must be 3-dimensional, i.e. of shape (n,n,3)"
        assert picture.shape[2] == 3, "Each pixel of the picture must have 3 color values"
        assert picture.shape[0] == picture.shape[1], "The image must not be rectangular but squared in shape"

        self.picture = picture
        self.right_occu = False
        self.left_occu = False
        self.up_occu = False
        self.down_occu = False
        self.in_space = False
        self.number = 0

    @property
    def size(self):
        return len(self.picture)

    def set_number(self, number):
        self.number = number

    @property
    def right(self):
        return self.picture[:,-1,:].reshape(3,1,3)

    @property
    def left(self):
        return self.picture[:,0,:].reshape(3,1,3)

    @property
    def up(self):
        return self.picture[0,:,:].reshape(1,3,3)
        
    @property
    def bottom(self):
        return self.picture[-1,:,:].reshape(1,3,3)

    def rgb_to_lab(self):
        return color.rgb2lab(self.picture)

    def lab_to_rgb(self):
        return color.lab2rgb(self.picture)

    def diss(self,otherPiece,lab_space=False):

        if lab_space:
            currentPiece=self.rgb_to_lab()
        else:
            currentPiece=self

        dict={}
        dict['L']=np.sum(np.power((otherPiece.left-currentPiece.right),2))
        dict['R']=np.sum(np.power((currentPiece.right-otherPiece.left),2))
        dict['U']=np.sum(np.power((otherPiece.bottom-currentPiece.up),2))
        dict['B'] = np.sum(np.power((currentPiece.bottom - otherPiece.up), 2))

        return dict


class Puzzle():
    def __init__(self, patch_size=100, seed=0):
        self.patch_size = patch_size
        self.seed = seed
        self.bag_of_pieces = []
        self.board = None
        self.board_space = None
        # hsize=0
        # self.vsize=0
        # self.puzzle_img=None

    @property
    def shape(self):
        '''Return the shape of the board of the Puzzle'''
        assert self.board, "Puzzle board is empty."
        return (len(self.board), len(self.board[0]))


    def create_from_img(self, img):
        '''Create the pieces from an img and put them in the board'''
        np.random.seed(self.seed)  # for reproducibility

        ## Crop the image for its size to be a multiple of the patch size
        height, width, _ = img.shape
        ps = self.patch_size
        n_rows, n_columns = height // ps, width // ps
        img_cropped = img[:n_rows * ps, :n_columns * ps]
    
        ## Populate the board
        self.board = [[None] * n_columns for _ in range(n_rows)]
        self.board_space = self.board
        for i in range(n_rows):
            for j in range(n_columns):
                self.board[i][j] = Piece(img_cropped[i*ps:(i+1)*ps, j*ps:(j+1)*ps])


    def shuffle(self):
        '''Took all pieces from the board to the bag of pieces, and shuffle it'''
        n_rows, n_colums = self.shape
        for i in range(n_rows):
            for j in range(n_colums):
                if self.board[i][j] != None :
                    self.bag_of_pieces.append(self.board[i][j])
                    self.board[i][j] = None
                    self.bag_of_pieces[-1].set_number(7*i+j)
        np.random.shuffle(self.bag_of_pieces)

    def get_piece(self,number):
        return [e for e in filter(lambda x: x.number == number, self.bag_of_pieces)][0]
        
    def plot(self):
        '''Plot the Board of the Puzzle'''
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
