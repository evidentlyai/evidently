<h1 align="center">10 minutes to Evidently</h1>

This is a short introduction to Evidently. 

## Input Data

You should prepare the data as pandas DataFrames. It could be two datasets - reference data and current production data. Or just one - you will need to identify rows that refer to reference and production data. If you want to generate reports with no comparison performed, you will need one dataset also.
If you deal with large datasets, you can take a sample from it:

```python
df.sample(1000, random_state=0) 
```
## Column mapping
To create column mapping, you need to specify the following parameters:
* `target` - the name of the column with the target function
* `prediction` - the name of the column(s) with model predictions
* `id` - ID column in the dataset
* `datetime` - the name of the column with datetime
* `numerical_features` - list of numerical features
* `categorical_features` - list of categorical features

If the column_mapping is not specified or set as None, we use the default mapping strategy:
* All features will be treated as numerical.
* The column with 'id' name will be treated as an ID column.
* The column with 'datetime' name will be treated as a datetime column.
* The column with 'target' name will be treated as a target function.
* The column with 'prediction' name will be treated as a model prediction.

Example 
```python
from evidently.pipeline.column_mapping import ColumnMapping

column_mapping = ColumnMapping()

column_mapping.target = 'y'
column_mapping.prediction = 'pred' predictions
column_mapping.id = None 
column_mapping.datetime = 'date' 
column_mapping.numerical_features = ['temp', 'atemp', 'humidity'] 
column_mapping.categorical_features = ['season', 'holiday'] 
```

## Choose The Tabs
You can choose one or several of the following Tabs.
* DataDriftTab to estimate the data drift
* NumTargetDriftTab to estimate target drift for the numerical target (for problem statements with the numerical target function: regression, probabilistic classification or ranking, etc.)
* CatTargetDriftTab to estimate target drift for the categorical target (for problem statements with the categorical target function: binary classification, multi-class classification, etc.)
* RegressionPerformanceTab to explore the performance of a regression model
* ClassificationPerformanceTab to explore the performance of a classification model
* ProbClassificationPerformanceTab to explore the performance of a probabilistic classification model and the quality of the model calibration
For each tab, you can specify the following parameters:
* `verbose_level` - you can get the short version of the tab (verbose_level == 0) and the full version (verbose_level == 1) 
* `Include_widgets` - You can list all the widgets from the particular report you want to include, and they will appear in the specified order
You can explore short and long versions of our custom Evidently report in the Example section

## Create Your Dashboard
To generate the report and explore it in the Jupyter notebook run these commands:
```python
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab

my_dashboard = Dashboard(tabs=[DataDriftTab()])
my_dashboard.calculate(reference_data, current_data)
my_dashboard.show()
```
You can set the custom options for the following Reports: 
num_target_drift_tab (Numerical Target Drift)
cat_target_drift_tab (Categorical Target Drift)
data_drift_tab (Data Drift)
See the example [here](link)

## Export the report as an HTML file
To save the Data Drift report as HTML, run:

```python
drift_dashboard.save("reports/my_report.html")
```

## Profiles

You can generate JSON profiles if you want to integrate the calculated metrics and statistical test results into external pipelines and visualization tools. You can include several analyses in a single JSON output. You specify each as a section in a profile: just like you choose tabs in the visual dashboards.
You can choose one or several of the following profiles:
* DataDriftProfileSection to estimate the data drift
* NumTargetDriftProfileSection to estimate target drift for the numerical target (for problem statements with the numerical target function: regression, probabilistic classification or ranking, etc.)
* CatTargetDriftProfileSection to estimate target drift for the categorical target (for problem statements with the categorical target function: binary classification, multi-class classification, etc.)
* RegressionPerformanceProfileSection to explore the performance of a regression model.
* ClassificationPerformanceProfileSection to explore the performance of a classification model
* ProbClassificationPerformanceProfileSection to explore the performance of a probabilistic classification model and the quality of the model calibration

To generate the Data Drift profile, run:

```python
from evidently.model_profile import Profile
from evidently.profile_sections import DataDriftProfileSection

my_profile = Profile(sections=[DataDriftProfileSection()])
my_profile.calculate(reference_data, current_data) 
my_profile.json()
```
# Examples

### Sample notebooks
Here you can find simple examples on toy datasets to quickly explore what Evidently can do right out of the box.

Report | Jupyter notebook | Colab notebook | Data source 
--- | --- | --- | --- 
Data Drift + Categorical Target Drift (Multiclass) | link | link | Iris plants sklearn.datasets 
Data Drift + Categorical Target Drift (Binary) | link | link | Breast cancer sklearn.datasets
Data Drift + Numerical Target Drift | link | link | California housing sklearn.datasets 
Regression Performance | link | link | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
Classification Performance (Multiclass) | link | link | Iris plants sklearn.datasets 
Probabilistic Classification Performance (Multiclass) | link | link | Iris plants sklearn.datasets 
Classification Performance(Binary) | link | link | Breast cancer sklearn.datasets
Probabilistic Classification Performance (Binary) | link | link | Breast cancer sklearn.datasets

### How-to notebooks
These examples answer “how-to” questions - they help you to adjust evidently as you need
