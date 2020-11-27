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

## More details
`Dashboard` generate interactive report, which consists from selected `Tabs`. Currently there is on `DriftTab` for data drift estimation, however, later on more tabs will be avaliable.
To generate `Dashbord` you have to do the following steps:
1. Prepare your data as pandas DataFrames. 
For data drift estimation you will need two datasets: reference data and the most recent data. Data drift will be estimated as a difference of the most recent data comparing to the reference dataset.
We expect DataFrames:
- Have `string` column names only;
- Have only numerical (`np.number`) types for feture columns that are supposed to be analysed for data drift. **All columns, which have non numerical types will be ignored**. The datetime column is the only exception, if you have time scale in your data, it can be used as x axis in the data plots. 

2. Pass `column_mapping` into `Dashboard`. 
If `column_mapping` is `None`, we use default column mapping strategy:
- All features will be treated as numerical ones
- Column with 'id' name will be treated as an ID column
- Column with 'datetime' name will be treated as a datetime 
- Column with 'target' name will be treated as a target function
- Column with 'prediction' name will be treated as a model prediction

ID, datetime, target and prediction are utility columns. It is not necessery to have them for drift calculation. Moreover, target and prediction columns will be excluded from the report if you specify them, datetime will be used for data plots, if ypu specify it. 

You can create a `column_mapping` to specify, wether you have utility columns in your dataset and split features into numerical and categorical types. 

`Column_mapping` is a python `dictionry` with the following format:
```python
column_mapping = {}

column_mapping['target'] = 'y' #'y' is the name of the column with target function
column_mapping['prediction'] = 'pred' #'pred' is the name of the column with the model predictions
column_mapping['id'] = None #there is no ID column in the dataset
column_mapping['datetime'] = 'date' #the 'datetime' is in the 'date' column

column_mapping['numerical_features'] = ['temp', 'atemp', 'humidity'] #list of the numerical features
test_column_mapping['categorical_features'] = ['season', 'holiday'] #list of the categorical features
```

Despite the fact, that the tool works only with numerical data, you can estimate data drift for categorical features. To do that you need first encode categorigal data with [numerical labels](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) or use any other strategy you like to to represent categorical data as a numerical ones, for instance [OneHotEncoding](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html) Then you need to create `column_mapping` `dict` and list all your encoded categorical features in the `categorical_feature` section, like:
```python
column_mapping['categorical_features'] = ['encoded_cat_feature_1', 
'encoded_cat_feature_2']
```
After that categorical features will be actually treated as categorical, meanly chi-squared test will be used for data drift estimation.

3. Generate report.
You can gererate report without `column_mapping` specification:
```python
drift_dashboard = Dashboard(reference_data, recent_data, 
	column_mapping = None, tabs=[DriftTab])
```
And with `column_mapping` specificatin:
```python
drift_dashboard_with_mapping = Dashboard(reference_data, recent_data, 
	column_mapping = column_mapping, tabs=[DriftTab])
```

3. Explore report inside your jupyter notebook.
```python
drift_dashboard.show()
```

4. Export report as html file and explore it in your browser.
```python
drift_dashboard.save("reports/my_report.html")
```
Note, that you need to specify path where to save your report and report name. 
Report will not be opened automatically, so to explore it you need to open it.

## How it works
To calculate data drift two datasets are needed: reference dataset and the most recent dataset. The idea here is that we use reference dataset as en etalone and estimate data drift as a shift of the most resent data comparing to the etalone data. Suretainly, you can use any datasets you like as a reference and most recent ones, but be aware that reference one will serve as an etalone for comparison.
To estimate drift we compare distribution for each feature in reference dataset with distribution of the corresponding feature from the most recent dataset. We detect if distribution has changed signifivantly using statistical tests. 
For numerical features we use [two-sample Kolmogorov-Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test), for categorical features we use [chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test), for both tests 0.95 confidence level is used. 

Currently we analyze data drift individually for each feature, integral data drift estimation is not prodided.
