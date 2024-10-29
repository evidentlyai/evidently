import numpy as np
import torch


def test_torch_to_numpy():
    array = torch.tensor([1, 2, 3]).numpy()
    assert np.array_equal(array, np.array([1, 2, 3]))
