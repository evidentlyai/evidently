---
description: How to use column mapping in Evidently.
---

**TL;DR:** Evidently expects a certain dataset structure and input column names. You can specify any differences by creating a ColumnMapping object.
 
Column mapping works identically for Test Suites and Reports. 

# Default mapping strategy

Column mapping helps correctly process the input data. 

If the `column_mapping` is not specified or set as `None`, Evidently will use the default mapping strategy.

**Column types**:
* All columns with numeric types (np.number) will be treated as Numerical. 
* All columns with DateTime format (np.datetime64) will be treated as DateTime. 
* All other columns will be treated as Categorical.

**Dataset structure**:
The column named **“id“**  will be treated as an ID column. 
The column named **“datetime”** will be treated as a DateTime column. 
The column named **“target”** will be treated as a target function.
The column named **“prediction”** will be treated as a model prediction.
 
ID, DateTime, target, and prediction are utility columns. If provided, the **“datetime”** column will be used as an index for some plots. The **“ID”** column will be excluded from drift analysis. 

ID, datetime, target, and prediction are utility columns. Requirements are different depending on the report type:

Data structure requirements depend on the type of analysis. Here are example requirements:

| Report/Test Suite | Feature columns  | Prediction column | Target column  | ID column | Datetime column |
|---|---|---|---|---|---|
| Data Quality | Required | Optional | Optional | Optional | Optional |
| Data Drift | Required | Optional | Optional | Optional | Optional |
| Target Drift | Optional | Target and/or prediction required | Target and/or prediction required | Optional | Optional |
| Classification Performance | Optional | Required | Required | Optional | Optional |
| Regression Performance | Optional | Required | Required | Optional | Optional |

# ColumnMapping Object

## Primary mapping

If you use different column names for target, prediction, ID or DateTime, you can create a `ColumnMapping` object to specify them: 

```python
from evidently.pipeline.column_mapping import ColumnMapping

column_mapping = ColumnMapping()

column_mapping.target = 'y' #'y' is the name of the column with the target function
column_mapping.prediction = 'pred' #'pred' is the name of the column(s) with model predictions
column_mapping.id = None #there is no ID column in the dataset
column_mapping.datetime = 'date' #'date' is the name of the column with datetime
```

To split the features into numerical and categorical types: 

```python
column_mapping.numerical_features = ['temp', 'atemp', 'humidity'] #list of numerical features
column_mapping.categorical_features = ['season', 'holiday'] #list of categorical features
```

{% hint style="info" %} **Why map them:** the column types affect some of the tests, metrics and visualizations. For example, the [drift algorithm](../reference/data-drift-algorithm.md) selects a statistical test based on the column type and ignores DateTime features. Some of the data quality visualizations are different for specific feature types. Some of the tests (e.g. on value ranges) only considers numeral columns, etc.{% endhint %}

## Additional mapping

There are additional mapping options that apply to specific Test Suites and Reports.

### DateTime features 

You might have temporal features in your dataset. For example, “date of the last contact.” 
 
To map them, define: 

```python
column_mapping = ColumnMapping()
column_mapping.datetime_features = ['last_call_date', 'join_date'] #list of DateTime features
```

Default: by default, Evidently only treats columns with DateTime format (np.datetime64) as DateTime features.
 
Note: do not confuse DateTime features with the DateTime column, which is used as the x-axis in some plots. You will typically use the DateTime column as a prediction timestamp. 

{% hint style="info" %} **Why map them:** if you specify DateTime features, they will be ignored in data drift calculation. Evidently will also calculate appropriate statistics and generate different visualizations for DateTime features in the data quality report.{% endhint %}

### Task parameter for target function

In many cases, it is important to differentiate between continuous and discrete targets. This applies to multiple reports and tests, including Data Quality and Target Drift. 
 
To define it explicitly, specify the task parameter:

```python
column_mapping = ColumnMapping()
column_mapping.target = 'y'
column_mapping.task = 'regression'
```
It accepts two values: 'regression' and 'classification'. 
 
**Default**: If you don't specify the task, Evidently will use a simple strategy: if the target has a numeric type and the number of unique values > 5: task == ‘regression.’ In all other cases, the task == ‘classification’.

{% hint style="info" %} **Why map it:**  If you have a multi-class problem where classes are encoded as numbers, it might look the same way as a regression problem. Thus it is best to explicitly specify it. It will affect how the target (prediction) is visualized and help pick the correct statistical tests for the target (prediction) drift detection. It will also affect the calculation of statistics and tests that differ for numerical and categorical data types.{% endhint %} 

### Prediction column(s) in classification 

To evaluate the classification performance, you need both true labels and prediction. Depending on the classification type (e.g., binary, multi-class, probabilistic), you have different options of how to pass the predictions.

**Multiclass classification**, option 1.

Target: encoded labels, Preds: encoded labels + Optional[target_names].

| target | prediction |
|---|---|
| 1 | 1 |
| 0 | 2 |
| … | … |
| 2 | 2 |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
column_mapping.target_names = ['Setosa', 'Versicolour', 'Virginica']
```

