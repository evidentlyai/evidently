---
description: How to use Evidently in different notebook environments.
---

## Google Colab, Kaggle Kernel, Deepnote

To install `evidently`, run the following command in the notebook cell:

```
!pip install evidently
```

To build a `Dashboard` or a `Profile` in Google Colab, Kaggle Notebook or Deepnote, simply repeat the steps described above.

For example, to build the **Data Drift** dashboard, run:

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)

iris_data_drift_report = Dashboard(tabs=[DataDriftTab()])
iris_data_drift_report.calculate(iris_frame[:100], iris_frame[100:])
```

To display the dashboard in the Google Colab, Kaggle Kernel, Deepnote, run:

```python
iris_data_drift_report.show()
```

The `show()` method has the argument `mode` which can take the following options:

* **auto** - the default option. Ideally, you will not need to specify the value for `mode` and can use the default. But if it does not work (in case we failed to determine the environment automatically), consider setting the correct value explicitly.
* **nbextention** - to show the UI using nbextension. Use this option to display dashboards in Jupyter notebooks (it should work automatically).
* **inline** - to insert the UI directly into the cell. Use this option for Google Colab, Kaggle Kernels, and Deepnote. For Google Colab, this should work automatically. For **Kaggle Kernels** and **Deepnote** the option should be specified explicitly:

```
iris_data_drift_report.show(mode='inline')
```
