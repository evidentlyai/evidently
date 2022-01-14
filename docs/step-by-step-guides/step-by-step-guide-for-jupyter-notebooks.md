---
description: How to use Evidently in Jupyter notebook or other notebook environments.
---

# Jupyter notebooks

Take the following steps to create and display a `Dashboard` in Jupyter notebook, export the report as an HTML file, or generate a JSON `Profile`.&#x20;

{% hint style="info" %}
If you want to display the dashboards in Jupyter notebook, make sure you [installed](../install-evidently.md) the Jupyter **nbextension**.
{% endhint %}

You can also use **Google Colab**, **Kaggle Kernel**, or **Deepnote**.&#x20;

If you use **Jupyter Lab**, you won't be able to explore the reports inside a Jupyter notebook. However, the report generation in a separate HTML file will work correctly.

## **1. Prepare your data as pandas `DataFrames`**&#x20;

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
| ****[**Data Drift**](../reports/data-drift.md)****                                                             | Required         | No                                | No                                | No                          |
| ****[**Numerical Target Drift**](../reports/num-target-drift.md)****                                           | Required         | Target and/or Prediction required | Target and/or Prediction required | No                          |
| ****[**Categorical Target Drift** ](../reports/categorical-target-drift.md)****                                | Required         | Target and/or Prediction required | Target and/or Prediction required | No                          |
| ****[**Regression Performance**](../reports/reg-performance.md)****                                            | Required         | Required                          | Required                          | Yes                         |
| ****[**Classification Performance**](../reports/classification-performance.md)****                             | Required         | Required                          | Required                          | Yes                         |
| ****[**Probabilistic Classification Performance**](../reports/probabilistic-classification-performance.md)**** | Required         | Required                          | Required                          | Yes                         |

### `DataFrame` requirements

Make sure the data complies with the following expectations.

1\) All column names are `string`&#x20;

2\) All feature columns that are analyzed for drift have the numerical type (`np.number)` ****&#x20;

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

Categorical features will be then treated accordingly. The [**data drift**](../reports/data-drift.md) report will use the chi-squared test by default.

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

## &#x20;**6**. **Create a JSON profile**

Alternatively, you can generate and view the output as a JSON profile.

```python
data_drift_profile = Profile(sections=[DataDriftProfileSection()])
data_drift_profile.calculate(reference_data, recent_data, 
    column_mapping=column_mapping)
data_drift_profile.json()
```

For each profile, you should specify `sections` to include. They work just like Tabs. You can choose among:

* `DataDriftProfileSection` to estimate the data drift,
* `NumTargetDriftProfileSection` to estimate target drift for numerical target,
* `CatTargetDriftProfileSection`to estimate target drift for categorical target,
* `ClassificationPerformanceProfileSection` to explore the performance of a classification model,
* `ProbClassificationPerformanceProfileSection` to explore the performance of a probabilistic classification model,
* `RegressionPerformanceProfileSection` to explore the performance of a regression model.

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
from evidently.tabs import DataDriftTab

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
