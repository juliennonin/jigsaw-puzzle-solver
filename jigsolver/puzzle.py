import numpy as np
import matplotlib.pyplot as plt
from copy import copy, deepcopy
from skimage import io, color

class Board():
    def __init__(self, n_rows, n_cols, patch_size=100):
        self._grid = [[Slot(patch_size) for j in range(n_cols)] for i in range(n_rows)]

    def __getitem__(self, coords):
        i, j = coords
        return self._grid[i][j]

    def __setitem__(self, coords, piece):
        i, j = coords
        assert isinstance(piece, Piece), "set value must be an instance of Piece"
        
        if isinstance(self._grid[i][j], Piece):
            raise IndexError("A piece is already placed here.")
        self._grid[i][j] = piece
        piece._is_placed = True

    def __iter__(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                yield self._grid[i][j]

    def enumerate(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                yield (i, j), self._grid[i][j]

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
    def __init__(self, picture, id):
        picture = np.array(picture, dtype=int)
        assert picture.ndim == 3, "The picture must be 3-dimensional, i.e. of shape (n,n,3)"
        assert picture.shape[2] == 3, "Each pixel of the picture must have 3 color values"
        assert picture.shape[0] == picture.shape[1], "The image must not be rectangular but squared in shape"

        self._id = id
        self.picture = picture
        self._is_placed = False

        self.right_occu = False
        self.left_occu = False
        self.up_occu = False
        self.down_occu = False
        self.in_space = False
        self.number = 0

    @property
    def is_placed(self):
        return self._is_placed

    @property
    def size(self):
        return len(self.picture)

    def set_number(self, number):
        self.number = number

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

    def __eq__(self, other):
        if isinstance(other, Piece):
            return np.allclose(self.picture, other.picture)
        return False



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
                piece = Piece(img_cropped[i*ps:(i+1)*ps, j*ps:(j+1)*ps], i * n_columns + j)
                self.bag_of_pieces.append(piece)
                self.board[i,j] = piece
        return self



    def shuffle(self):
        '''Took all pieces from the board to the bag of pieces, and shuffle it'''
        n_rows, n_colums = self.shape
        self.board = Board(n_rows, n_colums, self.patch_size)
        np.random.shuffle(self.bag_of_pieces)
        for i, piece in enumerate(self.bag_of_pieces):
            piece._is_placed = False
            piece._id = i

    # def get_piece(self,number): --> Puzzle.bag_of_pieces[number]
    #     return [e for e in filter(lambda x: x.number == number, self.bag_of_pieces)][0]

    def set_piece_in_space(self,number):
        for i in np.arange(len(self.bag_of_pieces)):
            if number == self.bag_of_pieces[i].number:
                self.bag_of_pieces[i].in_space = True

    def set_right_side_occupied(self,number_piece):
        for i in np.arange(len(self.bag_of_pieces)):
            if number_piece == self.bag_of_pieces[i].number:
                self.bag_of_pieces[i].right_occu = True

    def set_left_side_occupied(self,number_piece):
        for i in np.arange(len(self.bag_of_pieces)):
            if number_piece == self.bag_of_pieces[i].number:
                self.bag_of_pieces[i].left_occu = True

    def set_up_side_occupied(self,number_piece):
        for i in np.arange(len(self.bag_of_pieces)):
            if number_piece == self.bag_of_pieces[i].number:
                self.bag_of_pieces[i].up_occu = True

    def set_down_side_occupied(self,number_piece):
        for i in np.arange(len(self.bag_of_pieces)):
            if number_piece == self.bag_of_pieces[i].number:
                self.bag_of_pieces[i].down_occu = True


    def place_piece_to_position(self,position,number_piece_to_place,side,number_piece_near):
        self.board_space[position[0]][position[1]] = self.get_piece(number_piece_to_place)
        self.set_piece_in_space(number_piece_to_place,position)

        if position[0] == 0:
            self.set_up_side_occupied(number_piece_to_place)

        if position[1] == 0:
            self.set_left_side_occupied(number_piece_to_place)

        if position[0] == self.shape[0]-1:
            self.set_down_side_occupied(number_piece_to_place)

        if position[1] == self.shape[1]-1:
            self.set_right_side_occupied(number_piece_to_place)

        for i in np.arange(len(number_piece_near)):

            if side[i] == 'right':
                self.set_right_side_occupied(number_piece_near[i])
            elif side[i] == 'left':
                self.set_left_side_occupied(number_piece_near[i])

            elif side[i] == 'up':
                self.set_up_side_occupied(number_piece_near[i])

            elif side[i] == 'down':
                self.set_down_side_occupied(number_piece_near[i])

            else:
                return "error to place"


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
