import numpy as np
import unittest
from jigsolver import Border

class BorderTestCase(unittest.TestCase):
    def setUp(self):
        self.grid = np.array([
            [11, 21, 31],
            [12, 22, 32],
            [13, 23, 33],
        ])

    def test_border_top_should_return_top_border(self):
        top = [11, 21, 31]
        self.assertListEqual(list(self.grid[Border.TOP.slice]), top)
    
    def test_border_bottom_should_return_bottom_border(self):
        bottom = [13, 23, 33]
        self.assertListEqual(list(self.grid[Border.BOTTOM.slice]), bottom)
    
    def test_border_right_should_return_right_border(self):
        right = [31, 32, 33]
        self.assertListEqual(list(self.grid[Border.RIGHT.slice]), right)
    
    def test_border_left_should_return_left_border(self):
        left = [11, 12, 13]
        self.assertListEqual(list(self.grid[Border.LEFT.slice]), left)

class OppositeBorderTestCase(unittest.TestCase):
    def test_border_top_opposite_should_return_bottom(self):
        self.assertEqual(Border.TOP.opposite, Border.BOTTOM)
    
    def test_border_bottom_opposite_should_return_top(self):
        self.assertEqual(Border.BOTTOM.opposite, Border.TOP)
    
    def test_border_right_opposite_should_return_left(self):
        self.assertEqual(Border.RIGHT.opposite, Border.LEFT)
    
    def test_border_left_opposite_should_return_right(self):
        self.assertEqual(Border.LEFT.opposite, Border.RIGHT)

    def test_border_opposite_twice_should_return_same_border(self):
        self.assertEqual(Border.RIGHT.opposite.opposite, Border.RIGHT) 


if __name__ == '__main__':
    unittest.main()