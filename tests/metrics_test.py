import unittest
from jigsolver.pomeranz_solver.segmenter import BestBuddies_matrix
from jigsolver.metrics import *
from jigsolver.puzzle import *
import numpy as np

class BorderTestCase(unittest.TestCase):
    def setUp(self):
        self.cm1=np.array([[[0., 0., 0., 0.], [0.79, 0.16, 0.81, 0.79], [0.61, 0.15, 0.26, 0.65]],
                          [[0.76, 0.88, 0.79, 0.83], [0., 0., 0., 0.], [0.88, 0.08, 0.44, 0.4 ]],
                          [[0.64, 0.16, 0.92, 0.21],[0.87, 0.81, 0.6 , 0.1 ], [0., 0., 0., 0.]]])

        self.cm2=np.array([[[0,0,0,0],[1,1,1,1],[2,2,2,2]],
                           [[2,2,2,2],[0,0,0,0],[1,1,1,1]],
                           [[1,1,1,1],[2,2,2,2],[0,0,0,0]]])


    def test_BestBuddies_simplecase(self):

        BB = BestBuddies_matrix(self.cm1)

        self.assertEqual(BB[0,1,0],1)
        self.assertEqual(BB[0,1,1],1)
        self.assertEqual(BB[0,1,3],1)
        self.assertEqual(BB[1,0,1],1)
        self.assertEqual(BB[1,0,3],1)
        self.assertEqual(BB[1,0,2], 1)


    def test_BestBuddies_none(self):

        BB = BestBuddies_matrix(self.cm2)

        self.assertTrue(np.sum(BB==1)==0)

    def test_BestBuddies_metric(self):
        P=Puzzle()
        P.board=Board(3,3)
        BB1 = BestBuddies_matrix(self.cm1)
        BB2 = BestBuddies_matrix(self.cm2)


        print(BestBuddies_metric(P,self.cm1))

        self.assertEqual(BestBuddies_metric(P,BB1),0.21)
        self.assertEqual(BestBuddies_metric(P,BB2), 0)




if __name__ == '__main__':
    unittest.main()