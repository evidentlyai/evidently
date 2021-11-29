import unittest

import numpy as np

from evidently.utils import NumpyEncoder


class TestNumpyEncoder(unittest.TestCase):

    def setUp(self) -> None:
        self.encoder = NumpyEncoder()

    def test_int_convert(self):
        for _type in (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32,
                      np.int64, np.uint8, np.uint16, np.uint32, np.uint64):
            self.assertEqual(self.encoder.default(_type(55)), 55)

    def test_float_convert(self):
        np.testing.assert_almost_equal(self.encoder.default(np.float16(1.5)), 1.5)
        for _type in (np.float, np.float_, np.float32, np.float64):
            np.testing.assert_almost_equal(self.encoder.default(_type(.2)), .2)

    def test_bool_covert(self):
        self.assertEqual(self.encoder.default(np.bool(1)), True)
        self.assertEqual(self.encoder.default(np.bool(0)), False)
        self.assertEqual(self.encoder.default(np.bool_(1)), True)
        self.assertEqual(self.encoder.default(np.bool_(0)), False)

    def test_array_covert(self):
        self.assertEqual(self.encoder.default(np.array([0, 1, 2.1])), [0, 1, 2.1])
        self.assertEqual(self.encoder.default(np.empty((0, 0))), [])
        self.assertEqual(self.encoder.default(
            np.array([[0, 1, 2.1], [0, 1, 2.1], [0, 1, 2.1]])),
            [[0, 1, 2.1], [0, 1, 2.1], [0, 1, 2.1]])
        self.assertEqual(self.encoder.default(np.ones((2, 3))), [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])

    def test_none_covert(self):
        self.assertIsNone(self.encoder.default(np.void(3)))
