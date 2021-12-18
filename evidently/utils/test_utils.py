import pytest

import numpy as np

from evidently.utils import NumpyEncoder


@pytest.fixture
def numpy_encoder() -> NumpyEncoder:
    return NumpyEncoder()


def test_int_convert(numpy_encoder: NumpyEncoder) -> None:
    for _type in (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32,
                  np.int64, np.uint8, np.uint16, np.uint32, np.uint64):
        assert numpy_encoder.default(_type(55)) == 55


def test_float_convert(numpy_encoder: NumpyEncoder) -> None:
    np.testing.assert_almost_equal(numpy_encoder.default(np.float16(1.5)), 1.5)
    for _type in (np.float, np.float_, np.float32, np.float64):
        np.testing.assert_almost_equal(numpy_encoder.default(_type(.2)), .2)


def test_bool_covert(numpy_encoder: NumpyEncoder) -> None:
    assert numpy_encoder.default(np.bool(1)) is True
    assert numpy_encoder.default(np.bool(0)) is False
    assert numpy_encoder.default(np.bool_(1)) is True
    assert numpy_encoder.default(np.bool_(0)) is False


def test_array_covert(numpy_encoder: NumpyEncoder) -> None:
    assert numpy_encoder.default(np.array([0, 1, 2.1])) == [0, 1, 2.1]
    assert numpy_encoder.default(np.empty((0, 0))) == []
    assert numpy_encoder.default(
        np.array([[0, 1, 2.1], [0, 1, 2.1], [0, 1, 2.1]])
    ) == [[0, 1, 2.1], [0, 1, 2.1], [0, 1, 2.1]]
    assert numpy_encoder.default(np.ones((2, 3))) == [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]


def test_none_covert(numpy_encoder: NumpyEncoder) -> None:
    assert numpy_encoder.default(np.void(3)) is None
