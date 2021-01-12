# evidently
## What is it?
Evidently helps analyze machine learning models during development, validation, or production monitoring. The tool generates interactive reports from pandas `DataFrame`.
Currently 3 reports are available.  

### 1. Data Drift
Detects changes in feature distribution. 
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_github.png)

### 2. Numerical Target Drift
Detects changes in numerical target (see example below) and feature behavior.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_num_target_drift_github.png)

### 3. Categorical Target Drift
Detects changes in categorical target and feature behavior (see example below).
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_cat_target_drift_github.png)

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
To start, prepare your data as two pandas DataFrames. The first should include your reference data, the second -  most recent production data. The structure should be identical. For Target Drift report, include the column with Target and/or Prediction:

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.tabs import DriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

To generate the Data Drift report, run:
```python
iris_data_drift_report = Dashboard(iris_frame[:100], iris_frame[100:], tabs = [DriftTab])
iris_data_drift_report.save("reports/my_report.html")
```

To generate the Data Drift and the Categorical Target Drift reports, run:
```python
iris_data_drift_report = Dashboard(iris_frame[:100], iris_frame[100:], tabs = [DriftTab, CatTargetDriftTab])
iris_data_drift_report.save("reports/my_report_with_2_tabs.html")
```

If you get a security alert, press "trust html".
Report will not open automatically, to explore it, you should open it.

## More details
`Dashboard` generates an interactive report that includes the selected `Tabs`. 
Currently, you can choose the following Tabs:
- `DriftTab` to estimate the data drift.
- `NumTargetDrift` to estimate target drift for numerical target. It is an option for a problem statement with a numerical target function: regression, probabilistic classification or ranking, etc.
- `CatTargetDrift` to estimate target drift for categorical target. It is an option for a problem statement with a categorical target function: binary classification, multi-class classification, etc.
We will be adding more tabs soon!

To create a `Dashboard`, take the following steps:

1. **Prepare your data as two pandas DataFrames**. 
To estimate data drift, you will need two datasets. The first one is the “reference” dataset. It can include training or earlier production data. The second dataset should include the most recent production data. Data drift will be evaluated by comparing the recent data to the reference data. 

We expect that DataFrames:
- Have only `string` column names;
- Have only numerical type (`np.number`) for feature columns that are analyzed for data drift. **All non-numerical columns will be ignored**. The datetime column is the only exception. If available, it will be used as the x-axis in the data plots. 

**Note**: you can also prepare a single pandas DataFrame. When calling the dashboard, you can specify the rows that belong to the reference dataset, and rows that belong to the production dataset. See Boston housing and Breast Cancer notebooks for examples. 

2. **Pass `column_mapping` into `Dashboard`**. 
If the `column_mapping` is not specified or set as `None`, we use the default mapping strategy:
- All features will be treated as numerical.
- Column with 'id' name will be treated as an ID column.
- Column with 'datetime' name will be treated as a datetime column. 
- Column with 'target' name will be treated as a target function.
- Column with 'prediction' name will be treated as a model prediction.

ID, datetime, target and prediction are utility columns. They are not required to calculate data drift. If you specify the datetime, it will be used in data plots. If you specify id, target and prediction, they will be excluded from the data drift report.

For target drift reports, either target or prediction column (or both) are needed. 

You can create a `column_mapping` to specify if your dataset includes utility columns, and split features into numerical and categorical types. 

`Column_mapping` is a python `dictionary` with the following format:
```python
column_mapping = {}

column_mapping['target'] = 'y' #'y' is the name of the column with the target function
column_mapping['prediction'] = 'pred' #'pred' is the name of the column with model predictions
column_mapping['id'] = None #there is no ID column in the dataset
column_mapping['datetime'] = 'date' #'date' is the name of the column with datetime 

column_mapping['numerical_features'] = ['temp', 'atemp', 'humidity'] #list of numerical features
column_mapping['categorical_features'] = ['season', 'holiday'] #list of categorical features
```

Though the tool works only with numerical data, you can also estimate drift for categorical features. To do that, you should encode the categorical data with [numerical labels](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html). You can use other strategies to represent categorical data as numerical, for instance [OneHotEncoding](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html). Then you should create `column_mapping` `dict` and list all encoded categorical features in the `categorical_feature` section, like:
```python
column_mapping['categorical_features'] = ['encoded_cat_feature_1', 
'encoded_cat_feature_2']
```
Categorical features will be actually treated as categorical. Data drift estimation will use chi-squared test.

3. **Generate the report**.
You can generate the report without specifying the `column_mapping`:
```python
drift_dashboard = Dashboard(reference_data, recent_data, tabs=[DriftTab])
```
And with `column_mapping` specification:
```python
drift_dashboard_with_mapping = Dashboard(reference_data, recent_data, 
	column_mapping = column_mapping, tabs=[DriftTab])
```

4. **Explore the report inside the Jupyter notebook**.
```python
drift_dashboard.show()
```

5. **Export the report as an html file and open it in your browser**.
```python
drift_dashboard.save("reports/my_report.html")
```
If you get security alert, press "trust html".

You will need to specify the path where to save your report and the report name. 
Report will not open automatically. To explore it, you should open it.

## How it works
To calculate target or data drift, we need two datasets. The reference dataset will serve as a benchmark. We estimate drift by comparing the most recent data to the reference data. 

You can potentially choose any two datasets for comparison. But keep in mind that only “reference” dataset will be used as a basis for comparison. 

### Data Drift
To estimate the data drift, we compare distributions of each individual feature in the two datasets. We use statistical tests to detect if the distribution has changed significantly. For numerical features, we use [two-sample Kolmogorov-Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test). For categorical features, we will use [chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test). Both tests use 0.95 confidence level. We will add some levers later on, but this is a good enough default approach.

Currently, we estimate data drift for each feature individually. Integral data drift is not evaluated.

By clicking on each feature, you can explore the values mapped in a plot. The dark green line is the mean, as seen in the reference dataset. The green area covers one standard deviation from the mean. You can also zoom on distributions to understand what has changed.

### Numerical Target Drift
We estimate the drift for the target (actual values) and predictions in the same manner. If both columns are passed to the dashboard, we build two sets of plots. If only one of them (either target or predictions) is provided, we build one set of plots. If neither target nor predictions column is available, you will get an error.

To estimate the numerical target drift, we compare the distribution of the target in the two datasets. We use the Kolmogorov-Smirnov statistical test with a 0.95 confidence level to detect if the distribution has changed significantly.

We also calculate the Pearson correlation between the target and each individual feature in the two datasets. We create a plot with correlations to show correlation changes between the reference and the current dataset. 

We visualize the target values by index or time (if `datetime` column is available or defined in the `column_mapping` dictionary). This plot helps explore the target behavior and compare it between datasets.

Finally, we generate an interactive table with the visualizations of dependencies between the target and each feature. These plots help analyze how feature values relate to the target values and identify the differences between the datasets. We recommend paying attention to the behavior of the most important features since significant changes might confuse the model and cause higher errors.

### Categorical Target Drift
Just as above, we estimate the drift for the target and predictions in the same manner. If both columns are passed to the dashboard, we build two sets of plots. If only one of them (either target or predictions) is provided, we build one set of plots. If neither target nor predictions column is available, you will get an error.

To estimate the categorical target drift, we compare the distribution of the target in the two datasets. We use chi-squared statistical test with 0.95 confidence level to detect if the distribution has changed significantly.

We also generate an interactive table with the visualizations of each feature distribution for different the target labels. These plots help analyze how feature values relate to the target labels and identify the differences between the datasets. We recommend paying attention to the behavior of the most important features since significant changes might confuse the model and cause higher errors.

## Examples
- See Iris **Data Drift** and **Categorical Target Drift** report generation to explore the report both inside a Jupyter notebook and as a separate .html file: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/iris_data_drift.ipynb) 
- See Boston **Data Drift** and **Numerical Target Drift** report generation to explore the report with and without column mapping: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/boston_data_drift.ipynb)
- See Breast cancer **Data Drift** report generation to explore the report with and without datetime specification: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/breast_cancer_data_drift.ipynb)

## Stay updated
We will be releasing more reports soon. If you want to receive updates, follow us on [Twitter](https://twitter.com/EvidentlyAI), or sign up for our [newsletter](https://evidentlyai.com/sign-up). You can also find more tutorials and explanations in our [Blog](https://evidentlyai.com/blog).
