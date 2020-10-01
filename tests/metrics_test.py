import unittest
from jigsolver import cho_CM,pomeranz_CM,BestBuddies_matrix
from jigsolver import puzzle
import numpy as np

class BorderTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_BestBuddies_simplecase(self):
        cm = np.array([[[0., 0., 0., 0.], [0.79, 0.16, 0.81, 0.79], [0.61, 0.15, 0.26, 0.65]],[[0.76, 0.88, 0.79, 0.83], [0., 0., 0., 0.], [0.88, 0.08, 0.44, 0.4 ]],[[0.64, 0.16, 0.92, 0.21], [0.87, 0.81, 0.6 , 0.1 ], [0., 0., 0., 0.]]])

        BB = BestBuddies_matrix(cm)

        self.assertEqual(BB[0,1,0],1)
        self.assertEqual(BB[0,1,1],1)
        self.assertEqual(BB[0,1,3],1)
        self.assertEqual(BB[1,0,1],1)
        self.assertEqual(BB[1,0,3],1)

    def test_BestBuddies_none(self):
        cm = np.array([[[0,0,0,0],[1,1,1,1],[2,2,2,2]],[[2,2,2,2],[0,0,0,0],[1,1,1,1]],[[1,1,1,1],[2,2,2,2],[0,0,0,0]]])

        BB = BestBuddies_matrix(cm)

        self.assertTrue( (BB== np.zeros((3,3,4))).all() )



if __name__ == '__main__':
    unittest.main()