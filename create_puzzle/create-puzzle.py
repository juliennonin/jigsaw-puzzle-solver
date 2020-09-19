import cv2
import numpy as np
import random
from matplotlib import pyplot as plt

img = cv2.imread('../img/eiffel.jpg', 0)


class piece_puzzle:
    def __init__(self, data):
        self.data = data

    def right_side(self):
        return self.data[:, -1]

    def left_side(self):
        return self.data[:, 0]

    def up_side(self):
        return self.data[0, :]

    def down_side(self):
        return self.data[-1, :]


def create_puzzle(img,patch_size=100):
    puzzle_img = img[:(img.shape[0]//patch_size)*patch_size,:(img.shape[1]//patch_size)*patch_size]

    plt.title("original image")
    plt.imshow(puzzle_img, 'gray')
    plt.show()

    list_pieces = []
    for i in np.arange(0,puzzle_img.shape[0],patch_size):
        for j in np.arange(0, puzzle_img.shape[1], patch_size):
            list_pieces.append(piece_puzzle(puzzle_img[i:i+patch_size,j:j+patch_size]))

    random.shuffle(list_pieces)

    return list_pieces, (img.shape[0]//patch_size)*patch_size, (img.shape[1]//patch_size)*patch_size


list_pieces_random, row, column = create_puzzle(img,100)


def plot_list_pieces(list_pieces, row, colume,patch_size=100):
    puzzle_img_random = np.zeros([row,colume])
    for i in np.arange(0,row,patch_size):
        for j in np.arange(0,colume,patch_size):
            puzzle_img_random[i:i+patch_size,j:j+patch_size] = list_pieces[((colume//patch_size)*i+j)//patch_size].data
    plt.title("puzzle vision")
    plt.imshow(puzzle_img_random, 'gray')
    plt.show()


plot_list_pieces(list_pieces_random, row, column)


