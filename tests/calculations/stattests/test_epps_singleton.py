import pandas as pd
import numpy as np
from evidently.calculations.stattests.epps_singleton import epps_singleton_test

def test_epps_singleton_detects_drift():
    np.random.seed(42)
    ref = pd.Series(np.random.normal(loc = 0, scale = 1, size=1000))
    curr = pd.Series(np.random.normal(scale = 1.5, size=1000))

    p_val, drift = epps_singleton_test.func(ref, curr, feature_type="num", threshold=0.05)

    assert drift 
    assert p_val < 0.05
