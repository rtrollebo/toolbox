
import unittest
import numpy as np
from statistics.ml import entropy

class TestMlCore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ml_core(self):
        size = 7
        p = 1 / size
        array1 = np.array([p] * size)
        array2 = np.array(
            [0.10513192, 0.03125064, 0.2496782, 0.22240208, 0.20958976, 0.02310486, 0.15884255])
        self.assertAlmostEqual(np.sum(array1), 1.0, delta=1E-6)
        self.assertAlmostEqual(np.sum(array2), 1.0, delta=1E-6)
        e1 = entropy(array1)
        e2 = entropy(array2)
        self.assertAlmostEqual(e1, np.log2(size), delta=1E-6)
        self.assertTrue((e2 < np.log2(size)) and (e2 > 0))


if __name__ == '__main__':
    unittest.main()
