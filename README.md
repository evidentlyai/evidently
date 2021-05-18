<h1 align="center">Evidently</h1>

![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_4_reports_preview_small.png)
 
<p align="center"><b>Interactive reports to analyze, monitor and debug machine learning models.</b></p>

<p align="center">
  <a href="https://evidentlyai.gitbook.io/docs/">Docs</a>
  |
  <a href="https://discord.gg/xZjKRaNp8b">Join Discord</a>
  |
  <a href="https://evidentlyai.com/sign-up">Newsletter</a>
  | 
  <a href="https://evidentlyai.com/blog">Blog</a>
  | 
  <a href="https://twitter.com/EvidentlyAI">Twitter</a>
</p>


## What is it?
Evidently helps analyze machine learning models during validation or production monitoring. The tool generates interactive reports from pandas `DataFrame` or `csv` files.
Currently 6 reports are available.  

### 1. Data Drift
Detects changes in feature distribution. 
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_github.png)

### 2. Numerical Target Drift
Detects changes in numerical target and feature behavior.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_num_target_drift_github.png)

### 3. Categorical Target Drift
Detects changes in categorical target and feature behavior.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_cat_target_drift_github.png)

### 4. Regression Model Performance
Analyzes the performance of a regression model and model errors.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_regression_performance_report_github.png)

### 5. Classification Model Performance
Analyzes the performance and errors of a classification model. Works both for binary and multi-class models.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_classification_performance_report_github.png)

### 6. Probabilistic Classification Model Performance
Analyzes the performance of a probabilistic classification model, quality of model calibration, and model errors. Works both for binary and multi-class models.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_prob_classification_performance_report_github.png)

## Installing from PyPI
### MAC OS and Linux
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```

The tool allows building interactive reports both inside a Jupyter notebook and as a separate .html file. If you only want to generate interactive reports as .html files, the installation is now complete.

To enable building interactive reports inside a Jupyter notebook, we use jupyter nbextension. If you want to create reports inside a Jupyter notebook, then after installing `evidently` you should run the two following commands in the terminal from evidently directory.

To install jupyter nbextention, run:
```sh
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```
To enable it, run:
```sh
jupyter nbextension enable evidently --py --sys-prefix
```
That's it!

**Note**: a single run after the installation is enough. No need to repeat the last two commands every time.

**Note 2**: if you use Jupyter Lab, you may experience difficulties with exploring report inside a Jupyter notebook. However, the report generation in a separate .html file will work correctly.

### Windows
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```
The tool allows building interactive reports both inside a Jupyter notebook and as a separate .html file. Unfortunately, building reports inside a Jupyter notebook is not yet possible for Windows. The reason is Windows requires administrator privileges to create symlink. In later versions we will address this issue.

## Getting started

### Jupyter Notebook
To start, prepare your data as two pandas `DataFrames`. The first should include your reference data, the second - current production data. The structure of both datasets should be identical. 

* For **Data Drift** report, include the input features only.
* For **Target Drift** reports, include the column with Target and/or Prediction.
* For **Model Performance** reports, include the columns with Target and Prediction.

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.tabs import DriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

To generate the **Data Drift** report, run:
```python
iris_data_drift_report = Dashboard(iris_frame[:100], iris_frame[100:], tabs = [DriftTab])
iris_data_drift_report.save("reports/my_report.html")
```

To generate the **Data Drift** and the **Categorical Target Drift** reports, run:
```python
iris_data_drift_report = Dashboard(iris_frame[:100], iris_frame[100:], tabs = [DriftTab, CatTargetDriftTab])
iris_data_drift_report.save("reports/my_report_with_2_tabs.html")
```

If you get a security alert, press "trust html".
Html report does not open automatically. To explore it, you should open it from the destination folder.

To generate the **Regression Model Performance** report, run:
```python
regression_model_performance = Dashboard(reference_data, current_data,  column_mapping = column_mapping, tabs=[RegressionPerfomanceTab]) 
```

You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
```python
regression_single_model_performance = Dashboard(reference_data, None, column_mapping=column_mapping, tabs=[RegressionPerformanceTab])
```

To generate the **Classification Model Performance** report, run:
```python
classification_performance_report = Dashboard(reference_data, current_data, column_mapping = column_mapping,
                   	tabs=[ClassificationPerformanceTab])
```
 
For **Probabilistic Classification Model Performance** report, run:
```python
classification_performance_report = Dashboard(reference_data, current_data, column_mapping = column_mapping,
                   	tabs=[ProbClassificationPerformanceTab])
```
 
You can also generate either of the **Classification** reports for a single `DataFrame`. In this case, run:
```python
classification_single_model_performance = Dashboard(reference_data, None, column_mapping=column_mapping, tabs=[ClassificationPerformanceTab])
```
or
```python
prob_classification_single_model_performance = Dashboard(reference_data, None, column_mapping=column_mapping, tabs=[ProbClassificationPerformanceTab])
```

### Terminal
You can run a report generation directly from the bash shell. To do this, prepare your data as two `csv` files. In case you run one of the performance reports, you can have only one file. The first one should include your reference data, the second - current production data. The structure of both datasets should be identical. 

To generate reportm run the following command in bash:

```bash
python -m evidently analyze --config config.json 
--reference reference.csv --current current.csv --output output_folder
```
Here:
- `reference` is the path to the reference data, 
- `current` is the path to the current data, 
- `output` is the path to the output folder,
- `config` is the path to the configuration file.

Currently, you can choose the following Tabs:
- `drift` to estimate the data drift,
- `num_target_drift` to estimate target drift for numerical target,
- `cat_target_drift` to estimate target drift for categorical target,
- `classification_performance` to explore the performance of a classification model,
- `prob_classification_performance` to explore the performance of a probabilistic classification model,
- `regression_performance` to explore the performance of a regression model.

To configure the report you need to create the `config.json` file. This file configures the way of reading your input data and the type of the report. 

Here is an example of a simple configuration, where we have comma separated `csv` files with headers and there is no `date` column in the data.

```bash
{
  "data_format": {
    "separator": ",",
    "header": true,
    "date_column": null
  },
  "dashboard_tabs": ["cat_target_drift"]
}
```

Here is an example of a more complicated configuration, where we have comma separated `csv` files with headers and `datetime` column. We also specified the `column_mapping` dictionary to add information about `datetime`, `target` and `numerical_features`. 

```bash
{
  "data_format": {
    "separator": ",",
    "header": true,
    "date_column": "datetime"
  },
  "column_mapping" : {
  	"datetime":"datetime",
  	"target":"target",
  	"numerical_features": ["mean radius", "mean texture", "mean perimeter", 
  		"mean area", "mean smoothness", "mean compactness", "mean concavity", 
  		"mean concave points", "mean symmetry"]},
  "dashboard_tabs": ["cat_target_drift"]
}
```
## Documentation

For more information, refer to a complete <a href="https://evidentlyai.gitbook.io/docs/">Documentation</a>.

## Examples
- See Iris **Data Drift**, **Categorical Target Drift** and **Classification Performance** report generation to explore the reports both inside a Jupyter notebook and as a separate .html file: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/iris_data_drift.ipynb) 
- See Boston Housing **Data Drift** and **Numerical Target Drift** report generation to explore the reports with and without column mapping: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/boston_data_drift.ipynb)
- See Breast cancer **Data Drift** and **Probabilistic Classification Performance** report generation to explore the reports with and without datetime specification: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/breast_cancer_data_drift.ipynb)
- See Bike Demand Prediction **Regression Model Performance** report with datetime and column mapping inside a Jupyter notebook: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/bike_sharing_demand_regression_performance.ipynb)

## Stay updated
We will be releasing more reports soon. If you want to receive updates, follow us on [Twitter](https://twitter.com/EvidentlyAI), or sign up for our [newsletter](https://evidentlyai.com/sign-up). You can also find more tutorials and explanations in our [Blog](https://evidentlyai.com/blog). If you want to chat and connect, join our [Discord community](https://discord.gg/xZjKRaNp8b)!
