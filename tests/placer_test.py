import unittest
from jigsolver import Puzzle
import matplotlib.pyplot as plt

class PlacePieceTestCase(unittest.TestCase):
    def setUp(self):
        img = plt.imread('img/peppers.png')[:,:,:3]
        self.puzzle = Puzzle(patch_size=28)
        self.puzzle.create_from_img(img)
        self.puzzle.shuffle()
        # puzzle of size 4 × 4

    def test_place_piece_should_update_is_placed_attribute(self):
        piece = self.puzzle.bag_of_pieces[3]
        self.puzzle.place(piece, (2, 2))
        self.assertTrue(piece._is_placed, True)
        
    def test_place_piece_twice_should_raise_error(self):
        piece = self.puzzle.bag_of_pieces[3]
        self.puzzle.place(piece, (2, 2))
        with self.assertRaises(AssertionError):
            self.puzzle.place(piece, (3, 3))

    def test_place_piece_in_occupied_slot_should_raise_error(self):
        piece = self.puzzle.bag_of_pieces[3]
        self.puzzle.place(piece, (2, 2))
        with self.assertRaises(AssertionError):
            piece2 = self.puzzle.bag_of_pieces[4]
            self.puzzle.place(piece, (2, 2))

    # test for the OLDER version
    # def test_place_pieces_should_update_available_slots(self):
    #     piece = self.puzzle.bag_of_pieces[1]
    #     self.puzzle.place(piece, (1, 1))
    #     piece = self.puzzle.bag_of_pieces[2]
    #     self.puzzle.place(piece, (1, 2))
    #
    #     computed_available_coords = set(available_positions(self.puzzle))
    #     true_available_coords = set([(0,1), (0,2), (1,0), (1,3), (2,1), (2,2)])
    #
    #     self.assertEqual(len(computed_available_coords), 6)
    #     self.assertSetEqual(computed_available_coords, true_available_coords)


if __name__ == '__main__':
    unittest.main()
