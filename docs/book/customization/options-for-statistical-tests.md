# Options for Statistical Tests

## Available Options

- `feature_stattest_func` (default: `None`): define Stat Test for features in DataDrift:
  - `None` - use default Stat Tests for all features (chosen by internal logic)
  - Redefine Stat Test for all features:
    - `str` - name of Stat Test to use across all features (available names see below)
    - `Callable[[pd.Series, pd.Series, float], Tuple[float, bool]]` - custom function (requirements for custom function for StatTest see below)
    - `StatTest` - instance of `StatTest`
  - Also, Stat Test can be set per feature, by passing `dict` object, where key is feature name and value is one from previous options (`str`, `Callable` or `StatTest`)  
- `cat_target_stattest_func` (default: `None`): defines a custom statistical test to detect target drift in the Categorical Target Drift report. Follows same logic as `feature_stattest_func`, but without `dict` option. 
- `num_target_stattest_func` (default: `None`): defines a custom statistical test to detect target drift in the Numerical Target Drift report. Follows same logic as `feature_stattest_func`, but without `dict` option.
- 

### Example:
Change Stat Test for all features if DataDrift
```python
from evidently.options.data_drift import DataDriftOptions

options = DataDriftOptions(
  feature_stattest_func="ks",
) 
```

Change Stat Test for single feature to Custom function:
```python
from evidently.options.data_drift import DataDriftOptions


def my_stat_test(reference_data, current_data, threshold):
  return 0.0, False


options = DataDriftOptions(
  feature_stattest_func={"feature_1": my_stat_test },
)
```

Change Stat Test for single feature to Custom function (using StatTest object):
```python
from evidently.analyzers.stattests import StatTest
from evidently.options.data_drift import DataDriftOptions


def _my_stat_test(reference_data, current_data, threshold):
  return 0.0, False


my_stat_test = StatTest(
  name="my_stat_test",
  display_name="My Stat Test",
  func=_my_stat_test,
  allowed_feature_types=["cat"],
)


options = DataDriftOptions(
  feature_stattest_func={"feature_1": my_stat_test },
)
```




## Stat Test function requirements:

Stat Test function should match `(reference_data: pd.Series, current_data: pd.Series, threshold: float) -> Tuple[float, bool]` signature:
- `reference_data: pd.Series` - reference data series
- `current_data: pd.Series` - current data series to compare
- `threshold: float` - Stat Test threshold for drift detection

Returns:
- `score: float` - Stat Test score (actual value)
- `drift_detected: bool` - indicates is drift detected with given threshold

### Example:

```python
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import anderson_ksamp


def anderson_stat_test(reference_data: pd.Series, current_data: pd.Series, threshold: float) -> Tuple[float, bool]:
  p_value = anderson_ksamp(np.array([reference_data, current_data]))[2]
  return p_value, p_value < threshold
```


## Stat Test Meta information (StatTest class):

For better usage of Stat Test function it is recommended to write specific instance of StatTest class for that function:

For creating instance of `StatTest` class required:
- `name: str` - short name, used for referencing this Stat Test from options by (Stat Test should be registered globally) 
- `display_name: str` - long name for displaying in Dashboard and Profile 
- `func: Callable` - Stat Test function
- `allowed_feature_types: List[str]` - list of allowed feature types to which this function can be applied (avaiable values `cat`, `num`)


### Example:
```python
from evidently.analyzers.stattests import StatTest


def example_stat_test(reference_data, current_data, threshold):
    return 0.1, False

example_stat_test = StatTest(
  name="example_test",
  display_name="Example Stat Test (score)",
  func=example_stat_test,
  allowed_feature_types=["cat"],
)
```


## Available Stat Test Functions:

- `ks` - K-S test
  - default for numerical features
  - only for numerical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `chisquare` - Chi-Square test
  - default for categorical features if amount of labels for feature > 2
  - only for categorical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `z` - Z-test
  - default for categorical features if amount of labels for feature < 2
  - only for categorical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `wasserstein` - Wasserstein distance (normed)
  - only for numerical features
  - returns `distance`
  - drift detected when `distance >= threshold`
- `kl_div` - Kullback-Leibler divergence
  - only for numerical features
  - returns `divergence`
  - drift detected when `divergence >= threshold`
- `psi` - PSI
  - only for numerical features
  - returns `psi_value`
  - drift detected when `psi_value >= threshold`
- `jensenshannon` - Jensen-Shannon distance
  - only for numerical features
  - returns `distance`
  - drift detected when `distance >= threshold`