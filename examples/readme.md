<h1 align="center">10 minutes to Evidently</h1>

This is a short introduction to Evidently. 

# Input Data

You should prepare the data as pandas DataFrames. It could be two datasets - reference data and current production data. Or just one - you will need to identify rows that refer to reference and current data. If you do not want to perform a comparison, you can also pass a single dataset.

If you deal with large datasets, you can take a sample from it:

```python
df.sample(1000, random_state=0) 
```
# Column mapping
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
from evidently import ColumnMapping

column_mapping = ColumnMapping()

column_mapping.target = 'y'
column_mapping.prediction = 'pred' # predictions
column_mapping.id = None 
column_mapping.datetime = 'date' 
column_mapping.numerical_features = ['temp', 'atemp', 'humidity'] 
column_mapping.categorical_features = ['season', 'holiday'] 
```

# Choose a Report

A report evaluates a specific aspect of the model or data performance.

You can choose one or several Metric Presets to generate a pre-built report:

* `DataQualityPreset` to explore the dataset and evaluate its quality
* `DataDriftPreset` to estimate the data drift in the input feature
* `TargetDriftPreset` to estimate target (prediction) drift
* `RegressionPerformancePreset` to explore the performance of a regression model
* `ClassificationPerformancePreset` to explore the performance of a classification model

## Generate the Report

To generate the chosen report and explore it in the Jupyter notebook run these commands:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metric_preset import TargetDriftPreset

drift_report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
drift_report.run(reference_data=reference, current_data=current)
drift_report
```

## Export the Report in different formats

To save the Drift report as an HTML file, run:

```python
drift_report.save_html("file.html")
```

You can also get the output as a JSON or Python dictionary if you want to integrate the calculated metrics and statistical test results into external pipelines and visualization tools.

To get the output as a JSON, run:

```python
drift_report.json()
```

To get the output as a Python dictionary, run:

```python
drift_report.as_dict()
```

# Test Suites 

You can also run the Test Suites. This is an alternative interface that helps perform an explicit comparison of each metric against a defined condition and returns a pass or fail result.

You can choose one or several of the several Test Presets to run the pre-built Test Suites.
* `NoTargetPerformanceTestPreset` to evaluate the model performance without ground truth labels
* `DataStabilityTestPreset`to compare descriptive stats and similarity between the two data batches
* `DataQualityTestPreset`to check the data for issues like missing values or duplicates
* `DataDriftTestPreset` to compare the column distribution
* `RegressionTestPreset` to test the quality of a regression model
* `MulticlassClassificationTestPreset` to test the quality of a multi-class classification model
* `BinaryClassificationTopKTestPreset` to test the quality of a binary classification model at K
* `BinaryClassificationTestPreset` to test the quality of a binary classification model

To run the NoTargetPerformanceTestPreset and get the visual report with the result of the tests:

```python
no_target_performance = TestSuite(tests=[
NoTargetPerformanceTestPreset(),
])
no_target_performance.run(reference_data=ref,current_data=curr)
no_target_performance
```
To get the output as a JSON, run:

```python
no_target_performance.json()
```

# Customization

You can also build a custom Report from individual Metrics or a Test Suite from individual Tests. Evidently has 50+ inidvidual metrics and tests to choose from. All you need is to list which metrics or tests to include. 

Here is how you build a custom Test Suite from individual tests:

```python
feature_suite = TestSuite(tests=[
    TestColumnShareOfMissingValues(column_name='hours-per-week'),
    TestColumnValueDrift(column_name='education'),
    TestMeanInNSigmas(column_name='hours-per-week')
])
```

Each metric and test has parameters that you can pass to modify how the metric is calculated or to define a custom condition of the test. You can consult these documentation pages for reference:
* [All tests](https://docs.evidentlyai.com/reference/all-tests): all individual tests and parameters
* [All metrics](https://docs.evidentlyai.com/reference/all-metrics): all individual metrics and parameters

# Sample notebooks

Here you can find simple examples on toy datasets to quickly explore what Evidently can do right out of the box.

Report | Jupyter notebook | Colab notebook 
--- | --- | --- 
Evidently Metrics| [link](sample_notebooks/evidently_metrics.ipynb) | [link](https://colab.research.google.com/drive/1IpfQsq5dmjuG_Qbn6BNtghq6aubZBP5A) | Adult data set openml
Evidently Metric Presets| [link](sample_notebooks/evidently_metric_presets.ipynb) | [link](https://colab.research.google.com/drive/1wmHWipPd6iEy9Ce8NWBcxs_BSa9hgKgk) 
Evidently Tests| [link](sample_notebooks/evidently_tests.ipynb) | [link](https://colab.research.google.com/drive/1nQhfXft4VZ3G7agvXgH_LqVHdCh-WaMl) 
Evidently Test Presets| [link](sample_notebooks/evidently_test_presets.ipynb) | [link](https://colab.research.google.com/drive/1CBAFY1qmHHV_72SC7YBeaD4c6LLpPQan) 

### How-to notebooks
These examples answer “how-to” questions - they help you to adjust evidently as you need

How to | Jupyter notebook | Colab notebook | Data source 
--- | --- | --- | --- 
How to customize drift dashboards? (set confidence level, number of bins in a histogram and statistical test) | [link](how_to_questions/drift_dashboard_with_options_california_housing.ipynb) | [link](https://colab.research.google.com/drive/1roAyq4DdxBSGyzp0XmmH0zqOHso6Fd6y) | California housing sklearn.datasets 
How to change classification threshold? How to cut outliers from the histagram plot? How to define the width of confidence interval depicted on plots?| [link](how_to_questions/quality_metrics_options_wine.ipynb) | [link](https://colab.research.google.com/drive/1W7l3iAILkMti-3qcBLrU5JrW24lSOMR3) | Wine Quality openml
How to add your own widget or create your own report? | [link](how_to_questions/custom_widget_and_tab_example/) | [link](https://colab.research.google.com/drive/1ZYhokqQupQVX0n2boRjyr5cpg_WgFJoL) | California housing sklearn.datasets 
How to specify a colour scheme for the Dashboard?|[link](how_to_questions/colour_options_data_drift_iris.ipynb) | [link](https://colab.research.google.com/drive/1wjEsHHfspk3b4wtYV_rVEo1dkiVEPDTF)| Iris plants sklearn.datasets
How to create a text annotation in the Dashboard? | [link](how_to_questions/text_widget_usage_iris.ipynb)| [link](https://colab.research.google.com/drive/1cSXkLLVGJMBR5m_Crf93SsH9Y6K8ztdP)|Iris plants sklearn.datasets
How to assign a particular stattest from the evidently library for a feature or features?|[link](how_to_questions/stat_test_specification_for_data_drift_adult.ipynb)| [link](https://colab.research.google.com/drive/1GmJI4_DeFa2N2xcZ2uW9iKS2CFXPBh0D)|Adult data set openml

### Data Stories
To better understand potential use cases (such as model evaluation and monitoring), refer to the detailed tutorials accompanied by the blog posts.

Title | Jupyter notebook | Colab notebook | Blog post | Data source 
--- | --- | --- | --- | --- 
Monitor production models | [link](data_stories/bicycle_demand_monitoring.ipynb) | [link](https://colab.research.google.com/drive/1xjAGInfh_LDenTxxTflazsKJp_YKmUiD) | [How to break a model in 20 days](https://evidentlyai.com/blog/tutorial-1-model-analytics-in-production) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
Compare two models | [link](data_stories/ibm_hr_attrition_model_validation.ipynb) | [link](https://colab.research.google.com/drive/12AyNh3RLSEchNx5_V-aFJ1_EnLIKkDfr) | [What Is Your Model Hiding?](https://evidentlyai.com/blog/tutorial-2-model-evaluation-hr-attrition) | HR Employee Attrition: [link](https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset)
Custom tab and PSI widget | [link](data_stories/california_housing_custom_PSI_widget_and_tab.ipynb) | [link](https://colab.research.google.com/drive/1FuXId8p-lCP9Ho_gHeqxAdoxHRuvY9d0) | --- | California housing sklearn.datasets 
Default stat test for data drift | [link](data_stories/default_stattest_adult.ipynb) | [link](https://colab.research.google.com/drive/1MqG9QqtwHXqCesAow3l4b9czkeLFuOpF) | --- | Adult Data Set openml 

### Integrations
To see how to integrate Evidently in your prediction pipelines and use it with other tools, refer to the integrations. 

Title | link to tutorial
--- | ---
Real-time ML monitoring with Grafana | [Evidently + Grafana](integrations/grafana_monitoring_service/)
Batch ML monitoring with Airflow | [Evidently + Airflow](integrations/airflow_drift_detection/)
Log Evidently metrics in MLflow UI | [Evidently + MLflow](integrations/mlflow_logging/)
