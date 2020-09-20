import numpy as np
import cv2
import numpy as np
import matplotlib.pyplot as plt

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

    def right_side(self):
        return self.data[:, -1]

    def left_side(self):
        return self.data[:, 0]

    def up_side(self):
        return self.data[0, :]

    def down_side(self):
        return self.data[-1, :]

class Puzzle():
    def __init__(self,img,patch_size=100,seed=0):
        self.img = img
        self.patch_size=patch_size
        self.seed=0
        self.pieces=[]
        self.hsize=0
        self.vsize=0
        self.puzzle_img=None


    def create(self):
        #for reproducibility
        np.seed(self.seed)

        puzzle_img = img[:(img.shape[0] // self.patch_size) * self.patch_size, :(img.shape[1] // self.patch_size) * self.patch_size]

        plt.title("original image")
        plt.imshow(puzzle_img, 'gray')
        plt.show()

        list_pieces = []
        for i in np.arange(0, puzzle_img.shape[0], self.patch_size):
            for j in np.arange(0, puzzle_img.shape[1], self.patch_size):
                list_pieces.append(Piece(puzzle_img[i:i + self.patch_size, j:j + self.patch_size]))

        np.random.shuffle(list_pieces)

        self.pieces=list_pieces
        self.hsize=(img.shape[0] // self.patch_size) * self.patch_size
        self.vsize=(img.shape[1] // self.patch_size) * self.patch_size

        pass

    def plot(self):

        if len(self.pieces) == 0:
            raise Exception("You should create puzzle before plotting it")

        puzzle_img_random = np.zeros([self.hsize, self.vsize, 3], dtype=int)
        for i in np.arange(0, self.hsize, self.patch_size):
            for j in np.arange(0, self.vsize, self.patch_size):
                puzzle_img_random[i:i + self.patch_size, j:j + self.patch_size, :] = \
                    self.pieces[((self.vsize // self.patch_size) * i + j) // self.patch_size].picture
        plt.title("puzzle vision")
        plt.imshow(puzzle_img_random, 'gray')
        plt.show()
        self.puzzle_img=puzzle_img_random


if __name__ == '__main__':
    import os
    from os.path import dirname, join

    img_folder = join(dirname(dirname(__file__)), 'img')

    img = cv2.imread(join(img_folder, 'eiffel.jpg'))
    Example=Puzzle(img,100)
    Example.create()
    Example.plot()