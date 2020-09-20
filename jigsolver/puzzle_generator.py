import cv2
import numpy as np
import matplotlib.pyplot as plt
from .puzzle import Piece


def create_puzzle(img,patch_size=100):
    puzzle_img = img[:(img.shape[0]//patch_size)*patch_size,:(img.shape[1]//patch_size)*patch_size]

    plt.title("original image")
    plt.imshow(puzzle_img, 'gray')
    plt.show()

    list_pieces = []
    for i in np.arange(0,puzzle_img.shape[0],patch_size):
        for j in np.arange(0, puzzle_img.shape[1], patch_size):
            list_pieces.append(Piece(puzzle_img[i:i+patch_size,j:j+patch_size]))

    np.random.shuffle(list_pieces)

    return list_pieces, (img.shape[0]//patch_size)*patch_size, (img.shape[1]//patch_size)*patch_size


def plot_list_pieces(list_pieces, row, colume, patch_size=100):
    puzzle_img_random = np.zeros([row,colume,3], dtype=int)
    for i in np.arange(0,row,patch_size):
        for j in np.arange(0,colume,patch_size):
            puzzle_img_random[i:i+patch_size,j:j+patch_size,:] = list_pieces[((colume//patch_size)*i+j)//patch_size].picture
    plt.title("puzzle vision")
    plt.imshow(puzzle_img_random, 'gray')
    plt.show()
    return puzzle_img_random



if __name__ == '__main__':
    import os
    from os.path import dirname, join

    img_folder = join(dirname(dirname(__file__)), 'img')
    
    img = cv2.imread(join(img_folder, 'eiffel.jpg'))
    list_pieces_random, n_row, n_column = create_puzzle(img, 100)
    puzzle = plot_list_pieces(list_pieces_random, n_row, n_column)
