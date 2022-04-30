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
column_mapping.prediction = 'pred' # predictions
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
from evidently.dashboard.tabs import DataDriftTab

my_dashboard = Dashboard(tabs=[DataDriftTab()])
my_dashboard.calculate(reference_data, current_data)
my_dashboard.show()
```
You can set the custom options for the following Reports: 
* num_target_drift_tab (Numerical Target Drift)
* cat_target_drift_tab (Categorical Target Drift)
* data_drift_tab (Data Drift)
See the example [here](how_to_questions/drift_dashboard_with_options_california_housing.ipynb).

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
from evidently.model_profile.sections import DataDriftProfileSection

my_profile = Profile(sections=[DataDriftProfileSection()])
my_profile.calculate(reference_data, current_data) 
my_profile.json()
```
# Examples

### Sample notebooks
Here you can find simple examples on toy datasets to quickly explore what Evidently can do right out of the box.

Report | Jupyter notebook | Colab notebook | Data source 
--- | --- | --- | --- 
Data Drift + Categorical Target Drift (Multiclass) | [link](sample_notebooks/multiclass_target_and_data_drift_iris.ipynb) | [link](https://colab.research.google.com/drive/1Dd6ZzIgeBYkD_4bqWZ0RAdUpCU0b6Y6H) | Iris plants sklearn.datasets 
Data Drift + Categorical Target Drift (Binary) | [link](sample_notebooks/binary_target_and_data_drift_breast_cancer.ipynb) | [link](https://colab.research.google.com/drive/1gpzNuFbhoGc4-DLAPMJofQXrsX7Sqsl5) | Breast cancer sklearn.datasets
Data Drift + Numerical Target Drift | [link](sample_notebooks/numerical_target_and_data_drift_california_housing.ipynb) | [link](https://colab.research.google.com/drive/1TGt-0rA7MiXsxwtKB4eaAGIUwnuZtyxc) | California housing sklearn.datasets 
Regression Performance | [link](sample_notebooks/regression_performance_bike_sharing_demand.ipynb) | [link](https://colab.research.google.com/drive/1ONgyDXKMFyt9IYUwLpvfxz9VIZHw-qBJ) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
Classification Performance (Multiclass) | [link](sample_notebooks/classification_performance_multiclass_iris.ipynb) | [link](https://colab.research.google.com/drive/1pnYbVJEHBqvVmHUXzG-kw-Fr6PqhzRg3) | Iris plants sklearn.datasets 
Probabilistic Classification Performance (Multiclass) | [link](sample_notebooks/probabilistic_classification_performance_multiclass_iris.ipynb) | [link](https://colab.research.google.com/drive/1UkFaBqOzBseB_UqisvNbsh9hX5w3dpYS) | Iris plants sklearn.datasets 
Classification Performance (Binary) | [link](sample_notebooks/classification_performance_breast_cancer.ipynb) | [link](https://colab.research.google.com/drive/1b2kTLUIVJkKJybYeD3ZjpaREr_9dDTpz) | Breast cancer sklearn.datasets
Probabilistic Classification Performance (Binary) | [link](sample_notebooks/probabilistic_classification_performance_breast_cancer.ipynb) | [link](https://colab.research.google.com/drive/1sE2H4mFSgtNe34JZMAeC3eLntid6oe1g) | Breast cancer sklearn.datasets
Data Quality | [link](sample_notebooks/data_quality_bike_sharing_demand.ipynb) | [link](https://colab.research.google.com/drive/1XDxs4k2wNHU9Xbxb9WI2rOgMkZFavyRd) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)

### How-to notebooks
These examples answer “how-to” questions - they help you to adjust evidently as you need

How to | Jupyter notebook | Colab notebook | Data source 
--- | --- | --- | --- 
How to customize drift dashboards? (set confidence level, number of bins in a histogram and statistical test) | [link](how_to_questions/drift_dashboard_with_options_california_housing.ipynb) | [link](https://colab.research.google.com/drive/1roAyq4DdxBSGyzp0XmmH0zqOHso6Fd6y) | California housing sklearn.datasets 
How to change classification threshold? How to cut outliers from the histagram plot? How to define the width of confidence interval depicted on plots?| [link](how_to_questions/quality_metrics_options_wine.ipynb) | [link](https://colab.research.google.com/drive/1W7l3iAILkMti-3qcBLrU5JrW24lSOMR3) | Wine Quality openml
How to add your own widget or create your own report? | [link](how_to_questions/custom_widget_and_tab_example/) | [link](https://colab.research.google.com/drive/1ZYhokqQupQVX0n2boRjyr5cpg_WgFJoL) | California housing sklearn.datasets 
How to specify a colour scheme for the Dashboard?|[link](how_to_questions/colour_options_data_drift_iris.ipynb) | [link](https://colab.research.google.com/drive/1wjEsHHfspk3b4wtYV_rVEo1dkiVEPDTF)| Iris plants sklearn.datasets
How to create a text annotation in the Dashboard? | [link](how_to_questions/text_widget_usage_iris.ipynb)| [link](https://colab.research.google.com/drive/1cSXkLLVGJMBR5m_Crf93SsH9Y6K8ztdP)|Iris plants sklearn.datasets
How to assign a particular stattest from the evidently library for a feature or features?|[link](how_to_questions/stat_test_specification_for_data_drift_adult.ipynb)| [link](https://colab.research.google.com/drive/1GmJI4_DeFa2N2xcZ2uW9iKS2CFXPBh0D)|Adult Data Set sklearn.datasets openml

### Data Stories
To better understand potential use cases (such as model evaluation and monitoring), refer to the detailed tutorials accompanied by the blog posts.

Title | Jupyter notebook | Colab notebook | Blog post | Data source 
--- | --- | --- | --- | --- 
Monitor production models | [link](data_stories/bicycle_demand_monitoring.ipynb) | [link](https://colab.research.google.com/drive/1xjAGInfh_LDenTxxTflazsKJp_YKmUiD) | [How to break a model in 20 days](https://evidentlyai.com/blog/tutorial-1-model-analytics-in-production) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
Compare two models | [link](data_stories/ibm_hr_attrition_model_validation.ipynb) | [link](https://colab.research.google.com/drive/12AyNh3RLSEchNx5_V-aFJ1_EnLIKkDfr) | [What Is Your Model Hiding?](https://evidentlyai.com/blog/tutorial-2-model-evaluation-hr-attrition) | HR Employee Attrition: [link](https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset)
Custom tab and PSI widget | [link](data_stories/california_housing_custom_PSI_widget_and_tab.ipynb) | [link](https://colab.research.google.com/drive/1FuXId8p-lCP9Ho_gHeqxAdoxHRuvY9d0) | --- | California housing sklearn.datasets 

### Integrations
To see how to integrate Evidently in your prediction pipelines and use it with other tools, refer to the integrations. 

Title | link to tutorial
--- | ---
Real-time ML monitoring with Grafana | [Evidently + Grafana](integrations/grafana_monitoring_service/)
Batch ML monitoring with Airflow | [Evidently + Airflow](integrations/airflow_drift_detection/)
Log Evidently metrics in MLflow UI | [Evidently + MLflow](integrations/mlflow_logging/)
