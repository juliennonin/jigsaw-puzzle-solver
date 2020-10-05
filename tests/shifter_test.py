import unittest
from jigsolver.puzzle import *
from jigsolver.pomeranz_solver.shifter import shifter
from copy import copy
import numpy as np

class ShifterTestCase(unittest.TestCase):
    def setUp(self):
        img = plt.imread('img/eiffel.jpg')
        self.puzzle = Puzzle(img,patch(100)).ground_truth

    def test_should_do_nothing_when_segment_is_all(self):
        segment = []
        for i in range(self.puzzle.shape[0]):
            for j in range(self.puzzle.shape[1]):
                segment.append(self.puzzle.board[i,j])

        puzzle_copy = copy(self.puzzle)
        shifter(puzzle_copy,segment)

        for i in range(self.puzzle.shape[0]):
            for j in range(self.puzzle.shape[1]):
                self.assertTrue(puzzle_copy.board[i,j].id==self.puzzle.board[i,j].id)
    
    def test_should_remove_all_when_segment_is_empty(self):
        segment = []

        shifter(self.puzzle,segment)

        for i in range(self.puzzle.shape[0]):
            for j in range(self.puzzle.shape[1]):
                self.assertTrue(isinstance(self.puzzle.board[i,j],Slot))

    def test_should_removecols_and_roll_right(self):
        segment = []
        for i in range(self.puzzle.shape[0]):
            for j in range(self.puzzle.shape[1]-2):
                segment.append(self.puzzle.board[i,j])

        shifter(self.puzzle,segment)

        #self.assertTrue(np.all([isinstance(piece,Slot) for piece in self.puzzle.board[:,-1]])) # Right Border is empty
        self.assertTrue(np.all([isinstance(piece,Slot) for piece in self.puzzle.board[:,0]])) # Left Border is empty due to roll


if __name__ == '__main__':
    unittest.main()