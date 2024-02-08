---
description: How to implement a new drift detection method. 
---

**Pre-requisites**:
* You know how to set custom drift methods and which methods are available in the library.

If you do not find a suitable drift detection method, you can implement a custom function.


# Code example

Notebook example with custom data drift function example:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_specify_stattest_for_a_testsuite.ipynb" %}

# Custom StatTest function requirements:

The StatTest function should match `(reference_data: pd.Series, current_data: pd.Series, threshold: float) -> Tuple[float, bool]` signature:
- `reference_data: pd.Series` - reference data series
- `current_data: pd.Series` - current data series to compare
- `feature_type: str` - feature type
- `threshold: float` - Stat Test threshold for drift detection

Returns:
- `score: float` - Stat Test score (actual value)
- `drift_detected: bool` - indicates is drift detected with given threshold

## Example:

```python
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import anderson_ksamp


def anderson_stat_test(reference_data: pd.Series, current_data: pd.Series, _feature_type: str, threshold: float) -> Tuple[float, bool]:
  p_value = anderson_ksamp(np.array([reference_data, current_data]))[2]
  return p_value, p_value < threshold
```

# StatTest meta information (StatTest class):

To use the StatTest function, we recommended writing a specific instance of the StatTest class for that function:

To create the instance of the `StatTest` class, you need:
- `name: str` - a short name used to reference the Stat Test from the options (the StatTest should be registered globally) 
- `display_name: str` - a long name displayed in the Dashboard and Profile 
- `func: Callable` - a StatTest function
- `allowed_feature_types: List[str]` - the list of allowed feature types to which this function can be applied (available values: `cat`, `num`)


## Example:

```python
from evidently.calculations.stattests import StatTest


def example_stat_test(reference_data, current_data, feature_type, threshold):
  return 0.1, False


example_stat_test = StatTest(
  name="example_test",
  display_name="Example Stat Test (score)",
  func=example_stat_test,
  allowed_feature_types=["cat"],
)
```
