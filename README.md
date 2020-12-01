# evidently
## What is it?
Evidently helps analyze machine learning models during development, validation, or production monitoring. The tool generates interactive reports from pandas `DataFrame`. Currently, the Data Drift report is available.

![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/iris_data_drift_report_picture.png)

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
The tool allows building interactive reports both inside a Jupyter notebook and as a separate .html file. Unfortunately, building interactive reports inside a Jupyter notebook is not yet possible for Windows. The reason is that Windows requires administrator privileges to create symlink. In later versions we will address this issue.

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

To generate the Data Drift report, run:
```python
iris_data_drift_report = Dashboard(iris_frame[:100], iris_frame[100:], tabs = [DriftTab])
iris_data_drift_report.save("reports/my_report.html")
```
If you get a security alert, press "trust html".
Report will not open automatically, to explore it, you should open it.

## More details
`Dashboard` generates an interactive report that includes the selected `Tabs`. Currently, you can choose only the `DriftTab` to estimate the data drift. We will be adding more tabs soon!

To create a `Dashboard`, take the following steps:

1. **Prepare your data as two pandas DataFrames**. 
To estimate data drift, you will need two datasets. The first one is the “reference” dataset. It can include training or earlier production data. The second dataset should include the most recent production data. Data drift will be evaluated by comparing the recent data to the reference data. 

We expect that DataFrames:
- Have only `string` column names;
- Have only numerical type (`np.number`) for feature columns that are analyzed for data drift. **All non-numerical columns will be ignored**. The datetime column is the only exception. If available, it can be used as the x-axis in the data plots. 

**Note**: you can also prepare a single pandas DataFrame. When calling the dashboard, you can specify the rows that belong to the reference dataset, and rows that belong to the production dataset. See Boston housing and Breast Cancer notebooks for examples. 

2. **Pass `column_mapping` into `Dashboard`**. 
If the `column_mapping` is not specified or set as `None`, we use the default mapping strategy:
- All features will be treated as numerical.
- Column with 'id' name will be treated as an ID column.
- Column with 'datetime' name will be treated as a datetime column. 
- Column with 'target' name will be treated as a target function.
- Column with 'prediction' name will be treated as a model prediction.

ID, datetime, target and prediction are utility columns. They are not required to calculate drift. If you specify the datetime, it will be used in data plots. If you specify id, target and prediction, they will be excluded from the data drift report.  

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

Though the tool works only with numerical data, you can also estimate drift for categorical features. To do that, you should first encode the categorical data with [numerical labels](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html). You can use other strategies to represent categorical data as numerical, for instance [OneHotEncoding](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html). Then you should create `column_mapping` `dict` and list all encoded categorical features in the `categorical_feature` section, like:
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
To calculate the data drift, we need two datasets. The reference dataset will serve as a benchmark. We estimate drift by comparing the most recent data to the reference data. 

You can potentially choose any two datasets for comparison. But keep in mind that only “reference” dataset will be used as a basis for comparison. 

To estimate the drift, we compare distributions of each individual feature in the two datasets. We use statistical tests to detect if the distribution has changed significantly. For numerical features, we use [two-sample Kolmogorov-Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test). For categorical features, we will use [chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test). Both tests use 0.95 confidence level. We will add some levers later on, but this is a good enough default approach.

Currently, we estimate data drift for each feature individually. Integral data drift is not evaluated.

By clicking on each feature, you can explore the values mapped in a plot. The green area covers one standard deviation from the mean, as seen in the reference dataset. Or, you can zoom on distributions to understand what has changed.

## Examples
- See Iris report generation to explore the report both inside a Jupyter notebook and as a separate .html file: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/iris_data_drift.ipynb) 
- See Boston report generation to explore the report with and without column mapping: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/boston_data_drift.ipynb)
- See Breast cancer report generation to explore the report with and without datetime specification: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/breast_cancer_data_drift.ipynb)