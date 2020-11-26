# evidently
## What is it?
Evidently generates interactive reports from a pandas `DataFrame`. Currently Data Drift report is avaliable.
## Installing from PyPI
We establish Evidently as `evidently` package in PyPI.
You can install using the pip package manager by running:
```sh
$ pip install evidently
```
 The tool allows building interactive reports both inside a Jupyter notebook and as a separate .html file. To enable this, we use jupyter nbextension. After installing `evidently` you should run the two following commands in the terminal from evidently directory

To install jupyter nbextention run:
```sh
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```
And to eneble it run:
```sh
jupyter nbextension enable evidently --py --sys-prefix
```
Thats it!

**Note**: there is no need to run two last command every time you run jupyter notebook, single run after installation is enough.
## Getting started
To start, prepare your datasets as two pandas DataFrames: DataFrame with your reference data and DataFrame with your most recent data. For example, you can do it as the following:

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.tabs import DriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

Finally, to generate Data Drift report, run:
```python
iris_data_drift_report = Dashboard(iris_frame[:100], iris_frame[100:], column_mapping = None, tabs = [DriftTab])
iris_data_drift_report.show()
```

