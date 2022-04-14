# Options for Statistical Tests

## Available Options

- `feature_stattest_func` (default: `None`): define the Statistical Test for features in the DataDrift Dashboard or Profile:
  - `None` - use default Statistical Tests for all features (based on internal logic)
  - You can define a Statistical Test to be used for all the features in the dataset:
    - `str` - the name of StatTest to use across all features (see the available names below)
    - `Callable[[pd.Series, pd.Series, float], Tuple[float, bool]]` - custom StatTest function added (see the requirements for the custom StatTest function below)
    - `StatTest` - an instance of `StatTest`
  - You can define a Statistical Test to be used for individual features by passing a `dict` object where the key is a feature name and the value is one from the previous options (`str`, `Callable` or `StatTest`)  
- `cat_target_stattest_func` (default: `None`): defines a custom statistical test to detect target drift in the Categorical Target Drift report. It follows the same logic as the `feature_stattest_func`, but without the `dict` option. 
- `num_target_stattest_func` (default: `None`): defines a custom statistical test to detect target drift in the Numerical Target Drift report. It follows the same logic as the `feature_stattest_func`, but without the `dict` option.
- 

### Example:
Change the StatTest for all the features in the Data Drift report:
```python
from evidently.options.data_drift import DataDriftOptions

options = DataDriftOptions(
  feature_stattest_func="ks",
) 
```

Change the StatTest for a single feature to a Custom (user-defined) function:
```python
from evidently.options.data_drift import DataDriftOptions


def my_stat_test(reference_data, current_data, threshold):
  return 0.0, False


options = DataDriftOptions(
  feature_stattest_func={"feature_1": my_stat_test },
)
```

Change the StatTest for a single feature to Custom function (using a StatTest object):
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


## Custom StatTest function requirements:

The StatTest function should match `(reference_data: pd.Series, current_data: pd.Series, threshold: float) -> Tuple[float, bool]` signature:
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


## StatTest meta information (StatTest class):

To use the StatTest function, we recommended writing a specific instance of the StatTest class for that function:

To create the instance of the `StatTest` class, you need:
- `name: str` - a short name used to reference the Stat Test from the options (the StatTest should be registered globally) 
- `display_name: str` - a long name displayed in the Dashboard and Profile 
- `func: Callable` - a StatTest function
- `allowed_feature_types: List[str]` - the list of allowed feature types to which this function can be applied (available values: `cat`, `num`)


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


## Available StatTest Functions:

- `ks` - Kolmogorov–Smirnov (K-S) test
  - default for numerical features
  - only for numerical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `chisquare` - Chi-Square test
  - default for categorical features if the number of labels for feature > 2
  - only for categorical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `z` - Z-test
  - default for categorical features if the number of labels for feature <= 2
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
- `psi` - Population Stability Index (PSI)
  - only for numerical features
  - returns `psi_value`
  - drift detected when `psi_value >= threshold`
- `jensenshannon` - Jensen-Shannon distance
  - only for numerical features
  - returns `distance`
  - drift detected when `distance >= threshold`
