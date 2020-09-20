import numpy as np


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