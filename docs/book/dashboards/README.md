---
description: How to use Evidently in Jupyter notebook or other notebook environments.
---

# Jupyter notebooks

Take the following steps to create and display a `Dashboard` in Jupyter notebook, export the report as an HTML file, or generate a JSON `Profile`.&#x20;

{% hint style="info" %}
If you want to display the dashboards in Jupyter notebook, make sure you [installed](../get-started/install-evidently.md) the Jupyter **nbextension**.
{% endhint %}

You can also use **Google Colab**, **Kaggle Kernel**, or **Deepnote**.

If you use **Jupyter Lab**, you won't be able to explore the reports inside a Jupyter notebook. However, the report generation in a separate HTML file will work correctly.

## **1. Prepare your data as pandas `DataFrames`**

To analyze data or target drift, you always need two datasets. For the model performance reports, the second dataset is optional.&#x20;

* The first dataset is the **reference**. This can be training or earlier production data.&#x20;
* The second dataset is **current**. It should include the recent production data. &#x20;

You can prepare the datasets as **two** pandas `DataFrames`. The structure of both datasets should be identical. Performance or drift will be evaluated by comparing the current data to the reference data.

![](<../.gitbook/assets/two\_datasets\_classification (1).png>)

You can also prepare a **single** pandas DataFrame to generate a comparative report. When calling the dashboard, you should specify the rows that belong to the reference and production dataset accordingly.&#x20;

Model Performance reports can be generated for a **single** dataset, with no comparison performed. In this case, you can simply pass a single `DataFrame`.&#x20;

### Dataset structure

The data structure is different depending on the report type.

* For the **Data Drift** report, include the input features only.&#x20;
* For the **Target Drift** reports, include the input features and the column with the Target and/or the Prediction.&#x20;
* For the **Model Performance** reports, include the input features, the column with the Target, and the column with the Prediction.

If you include more columns than needed for a given report, they will be ignored. &#x20;

Below is a summary of the data requirements:

| Report Type                                                                                                    | Feature columns  | Target column                     | Prediction column                 | Works with a single dataset |
| -------------------------------------------------------------------------------------------------------------- | ---------------- | --------------------------------- | --------------------------------- | --------------------------- |
| ****[**Data Drift**](../get-started/reports/data-drift.md)****                                                             | Required         | No                                | No                                | No                          |
| ****[**Numerical Target Drift**](../get-started/reports/num-target-drift.md)****                                           | Required         | Target and/or Prediction required | Target and/or Prediction required | No                          |
| ****[**Categorical Target Drift** ](../get-started/reports/categorical-target-drift.md)****                                | Required         | Target and/or Prediction required | Target and/or Prediction required | No                          |
| ****[**Regression Performance**](../get-started/reports/reg-performance.md)****                                            | Required         | Required                          | Required                          | Yes                         |
| ****[**Classification Performance**](../get-started/reports/classification-performance.md)****                             | Required         | Required                          | Required                          | Yes                         |
| ****[**Probabilistic Classification Performance**](../get-started/reports/probabilistic-classification-performance.md)**** | Required         | Required                          | Required                          | Yes                         |

### `DataFrame` requirements

Make sure the data complies with the following expectations.

1\) All column names are `string`&#x20;

2\) All feature columns that are analyzed for drift have the numerical type `(np.number)`&#x20;

* **All non-numerical columns will be ignored**. Categorical data can be encoded as numerical labels and specified in the column mapping
* **The datetime column is the only exception.** If available, it will be used as the x-axis in the data plots.&#x20;

## **2. Pass the `column_mapping` into `Dashboard`**&#x20;

If the `column_mapping` is not specified or set as `None`, we use the default mapping strategy:

* All features will be treated as numerical.
* The column with **'id'** name will be treated as an ID column.
* The column with **'datetime'** name will be treated as a datetime column.
* The column with **'target'** name will be treated as a target function.
* The column with **'prediction'** name will be treated as a model prediction.

ID, datetime, target, and prediction are utility columns. Requirements are different depending on the report type:

* For the **Data Drift** report, these columns are not required. If you specify id, target, and prediction, they will be excluded from the data drift report. If you specify the datetime, it will be used in data plots.
* For the **Target Drift** reports, we expect either the target or the prediction column or both. ID and datetime are optional.
* For **Model Performance** reports, both the target and the prediction column are required. ID and datetime are optional.

You can create a `ColumnMapping` object to specify whether your dataset includes the utility columns and split the features into numerical and categorical types.

```python
from evidently.pipeline.column_mapping import ColumnMapping

column_mapping = ColumnMapping()

column_mapping.target = 'y' #'y' is the name of the column with the target function
column_mapping.prediction = 'pred' #'pred' is the name of the column(s) with model predictions
column_mapping.id = None #there is no ID column in the dataset
column_mapping.datetime = 'date' #'date' is the name of the column with datetime 

column_mapping.numerical_features = ['temp', 'atemp', 'humidity'] #list of numerical features
column_mapping.categorical_features = ['season', 'holiday'] #list of categorical features
```

#### **NOTE: Categorical features in Data Drift**

Though the data drift tool works only with numerical data, you can also estimate drift for categorical features. To do that, you should encode the categorical data with [numerical labels](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html). You can use other strategies to represent categorical data as numerical, for instance, [OneHotEncoding](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get\_dummies.html).&#x20;

Then you should create `ColumnMapping` object and list all encoded categorical features in the `categorical_feature` section, like:

```python
column_mapping = ColumnMapping()

column_mapping.categorical_features = ['encoded_cat_feature_1', 
    'encoded_cat_feature_2']
```

Categorical features will be then treated accordingly. The [**data drift**](../get-started/reports/data-drift.md) report will use the chi-squared test by default.

**NOTE: Column names in Probabilistic Classification**

The tool expects your `DataFrame(s)` to contain columns with the names matching the ones from the ‘prediction’ list. Each column should include information about the predicted probability \[0;1] for the corresponding class.

```python
column_mapping = ColumnMapping()

column_mapping.prediction = ['class_name1', 'class_name2', 'class_name3',]
```

**NOTE: Column order in Binary Classification**

For binary classification, class order matters. The tool expects that the target (so-called positive) class is the **first** in the `column_mapping.prediction` list.

#### If you are unsure how to use column mapping, watch this video tutorial:

{% embed url="https://www.youtube.com/watch?v=MiSl73LRj5I&t=7s&ab_channel=EvidentlyAI" %}

## **3. Generate the report**

You can choose one or several of the following **Tabs**.

* `DataDriftTab` to estimate the **data drift**
* `NumTargetDriftTab` to estimate **target drift** for the numerical **** target (for problem statements with the numerical target function: regression, probabilistic classification or ranking, etc.)
* `CatTargetDriftTab` to estimate **target drift** for the categorical target (for problem statements with the categorical target function: binary classification, multi-class classification, etc.)
* `RegressionPerformanceTab` to explore the **performance** of a regression model.
* `ClassificationPerformanceTab` to explore the **performance** of a classification **** model
* `ProbClassificationPerformanceTab` to explore the **performance** of a probabilistic classification model and the quality of the model calibration

You can generate the report without specifying the `ColumnMapping`:

```python
drift_dashboard = Dashboard(tabs=[DataDriftTab()])
drift_dashboard.calculate(reference_data, recent_data)
```

And with the `column_mapping` specification:

```python
drift_dashboard_with_mapping = Dashboard(tabs=[DataDriftTab()])
drift_dashboard_with_mapping.calculate(reference_data, recent_data, 
    column_mapping=column_mapping)
```

### Generating dashboards and HTML reports

After installing the tool, import `evidently` and the required tabs:

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import (
    DataDriftTab,
    CatTargetDriftTab,
    RegressionPerformanceTab,
    ClassificationPerformanceTab,
    ProbClassificationPerformanceTab,
)
```

Create a `Pandas DataFrame` with the dataset to analyze:

```python
iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

`Dashboard` generates an interactive report that includes the selected `Tabs`.&#x20;

You can choose the following **Tabs**:

* `DataDriftTab` to estimate the **data drift**
* `NumTargetDriftTab` to estimate **target drift** for the numerical **** target&#x20;
* `CatTargetDriftTab` to estimate **target drift** for the categorical target&#x20;
* `RegressionPerformanceTab` to explore the **performance** of a regression model
* `ClassificationPerformanceTab` to explore the **performance** of a classification **** model
* `ProbClassificationPerformanceTab` to explore the **performance** of a probabilistic classification model&#x20;

To generate the **Data Drift** report and save it as HTML, run:

```python
iris_data_drift_report = Dashboard(tabs=[DataDriftTab])
iris_data_drift_report.calculate(iris_frame[:75], iris_frame[75:], 
    column_mapping = None)
iris_data_drift_report.save("reports/my_report.html")
```

To generate the **Data Drift** and the **Categorical Target Drift** reports, first add a target (and/or prediction) column to the initial dataset:&#x20;

```python
iris_frame['target'] = iris.target
```

Then run:

```python
iris_data_and_target_drift_report = Dashboard(tabs=[DataDriftTab, CatTargetDriftTab])
iris_data_and_target_drift_report.calculate(iris_frame[:75], iris_frame[75:], 
    column_mapping=None)
iris_data_and_target_drift_report.save("reports/my_report_with_2_tabs.html")
```

If you get a security alert, press "trust html". The HTML report does not open automatically. To explore it, you should open it from the destination folder.

To generate the **Regression Model Performance** report, run:

```python
regression_model_performance = Dashboard(tabs=[RegressionPerfomanceTab]) 
regression_model_performance.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
regression_model_performance.show()
```

For **Regression Model Performance report** from a single`DataFrame` , run:

```python
regression_single_model_performance = Dashboard(tabs=[RegressionPerfomanceTab])
regression_single_model_performance.calculate(reference_data, None, 
    column_mapping=column_mapping)
regression_single_model_performance.show()
```

To generate the **Classification Model Performance report**, run:

```python
classification_performance_report = Dashboard(tabs=[ClassificationPerformanceTab])
classification_performance_report.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
classification_performance_report.show()
```

For **Probabilistic Classification Model Performance report**, run:

```python
classification_performance_report = Dashboard(tabs=[ProbClassificationPerformanceTab])
classification_performance_report.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
classification_performance_report.show()
```

For a **classification reports** from a single `DataFrame`, run:

```python
classification_single_model_performance = Dashboard(tabs=[ClassificationPerformanceTab])
classification_single_model_performance.calculate(reference_data, None, 
    column_mapping=column_mapping) 
classification_single_model_performance.show()
```

For a **probabilistic classification report** from a single `DataFrame`, run:

```python
prob_classification_single_model_performance = Dashboard(tabs=[ProbClassificationPerformanceTab])
prob_classification_single_model_performance.calculate(reference_data, None, 
    column_mapping=column_mapping)
prob_classification_single_model_performance.show()
```

{% hint style="info" %}
**It might take some time to display the report. If it does not show, this might be due to the dataset size.** The dashboard contains the data necessary to generate interactive plots and can become large. The limitation depends on infrastructure. In this case, we suggest applying sampling to your dataset. In Jupyter notebook, that can be done directly with pandas. You can also generate a JSON profile instead 👇🏼
{% endhint %}

## 4. **Explore the dashboard in the Jupyter notebook**

You can display the chosen Tabs in a single Dashboard directly in the notebook.&#x20;

```python
drift_dashboard.show()
```

{% hint style="info" %}
**If the report is not displayed, this might be due to the dataset size.** The dashboard contains the data necessary to generate interactive plots and can become large. The limitation depends on infrastructure. In this case, we suggest applying sampling to your dataset. In Jupyter notebook, that can be done directly with pandas. You can also generate JSON instead 👇🏼
{% endhint %}

## 5. **Export the report as an HTML file**

You can save the report as an HTML file, and open it in your browser.

```python
drift_dashboard.save("reports/my_report.html")
```

If you get a security alert, press "trust HTML".

You will need to specify the path where to save your report and the report name. The report will not open automatically. To explore it, you should open it from the destination folder.


### Google Colab, Kaggle Kernel, Deepnote

To install `evidently`, run the following command in the notebook cell:

```
!pip install evidently
```

To build a `Dashboard` or a `Profile` in Google Colab, Kaggle Notebook or Deepnote, simply repeat the steps described above.&#x20;

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


# Command line interface

To start, prepare your data as `csv`  files. Follow the same data requirements as described in the [Jupyter notebook](step-by-step-guide-for-jupyter-notebooks.md) guide.

If you prefer a video version, here is 7-min Quick Start on how to use Evidently using CLI. &#x20;

{% embed url="https://www.youtube.com/watch?v=3j3NwIkhmTs" %}

## Generate HTML report or JSON Profile

To generate the HTML report, run the following command in bash:

```bash
$ python -m evidently calculate dashboard --config config.json 
--reference reference.csv --current current.csv --output output_folder --report_name output_file_name
```

To generate a JSON profile, run the following command in bash:

```bash
$ python -m evidently calculate profile --config config.json 
--reference reference.csv --current current.csv --output output_folder --report_name output_file_name
```

Here:

* `reference` is the path to the reference data,
* `current` is the path to the current data,
* `output` is the path to the output folder,
* `config` is the path to the configuration file,
* `pretty_print` to print the JSON profile with indents (for profile only).

You can choose the following **Tabs**:

* `data_drift` to estimate the **data drift**,
* `num_target_drift` to estimate **target drift** for the numerical target
* `cat_target_drift` to estimate target drift for the categorical target
* `regression_performance` to explore the **performance** of a regression model
* `classification_performance` to explore the **performance** of a classification model
* `prob_classification_performance` to explore the **performance** of a probabilistic classification model

To configure the report you need to create the `config.json` file or a `config.yaml` file. This file configures the way of reading your input data and the type of the report.

## Configuration examples

Here is an example of a simple configuration, where we have comma-separated `csv` files with headers and there is no `date` column in the data.

**Dashboard**:

```yaml
{
  "data_format":{
    "separator":",",
    "header":true,
    "date_column":null
  },
  "column_mapping":{},
  "dashboard_tabs":["cat_target_drift"]
}
```

**Profile**:

```yaml
{
  "data_format":{
    "separator":",",
    "header":true,
    "date_column":null
  },
  "column_mapping":{},
  "profile_sections":["data_drift"],
  "pretty_print":true
}
```

Here is an example for a more complicated configuration, where we have comma-separated `csv` files with headers and `datetime` column. We also specified the `column_mapping` dictionary, where we added information about the `datetime`, `target` and `numerical_features`.

**Dashboard**:

```yaml
{
  "data_format":{
    "separator":",",
    "header":true,
    "date_column":"datetime"
  },
  "column_mapping":{
    "datetime":"datetime",
    "target":"target",
    "numerical_features":["mean radius", "mean texture", "mean perimeter", 
      "mean area", "mean smoothness", "mean compactness", "mean concavity", 
      "mean concave points", "mean symmetry"]},
  "dashboard_tabs":["cat_target_drift"],
  "sampling": {
      "reference": {
      "type": "none"
    },
      "current": {
      "type": "nth",
      "n": 2
    }
  }
}
```

**Profile**:

```yaml
{
  "data_format":{
    "separator":",",
    "header":true,
    "date_column":null
  },
  "column_mapping":{
    "target":"target",
    "numerical_features":["mean radius", "mean texture", "mean perimeter", 
      "mean area", "mean smoothness", "mean compactness", "mean concavity", 
      "mean concave points", "mean symmetry"]},
  "profile_sections":["data_drift", "cat_target_drift"],
  "pretty_print":true,
  "sampling": {
    "reference": {
      "type": "none"
    },
    "current": {
      "type": "random",
      "ratio": 0.8
    }
  }
}
```

## Telemetry

Telemetry is collected in Evidently starting from version 0.1.21.dev0.

When you use Evidently in the command-line interface, we collect some basic telemetry. It includes data on the environment (e.g. Python version) and usage (type of report or profile generated). You can read more about what we collect [here](../support/telemetry.md).

You can opt-out from telemetry collection by setting the environment variable:

```yaml
 EVIDENTLY_DISABLE_TELEMETRY=1
```

## Sampling for large datasets

As shown in the configuration example above, you can specify **sampling** parameters for large files. You can use different sampling strategies for the reference and current data, or apply sampling only to one of the files.

Currently, you can choose from the following options:

* `none`- **no sampling** will be applied
* `nth` - each **Nth row** of the file will be taken. This option works together with the `n` parameter (see the example with the Dashboard above)
* `random` - **random sampling** will be applied. This option works together with `ratio` parameter (see the example with the Profile above)

If you do not specify the sampling parameters in the configuration, it will be treated as none and no sampling will be applied.

