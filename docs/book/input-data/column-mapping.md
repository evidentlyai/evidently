---
description: How to use column mapping in Evidently.
---

**TL;DR:** Evidently expects a certain dataset structure and input column names. You can specify any differences by creating a `ColumnMapping` object. It works the same way for Test Suites and Reports. 

# Default mapping strategy

Column mapping helps correctly process the input data. 

If the `column_mapping` is not specified or set as `None`, Evidently will use the default mapping strategy.

**Column types**:
* All columns with numeric types (np.number) will be treated as Numerical. 
* All columns with DateTime format (np.datetime64) will be treated as DateTime. 
* All other columns will be treated as Categorical.

**Dataset structure**:
* The column named **“id“**  will be treated as an ID column. 
* The column named **“datetime”** will be treated as a DateTime column. 
* The column named **“target”** will be treated as a target function.
* The column named **“prediction”** will be treated as a model prediction.
 
ID, DateTime, target, and prediction are utility columns. If provided, the **“datetime”** column will be used as an index for some plots. The **“ID”** column will be excluded from drift analysis. 

Data structure requirements depend on the type of analysis. Here are example requirements:

| Report/Test Suite | Feature columns  | Prediction column | Target column  | ID column | Datetime column |
|---|---|---|---|---|---|
| Data Quality | Required | Optional | Optional | Optional | Optional |
| Data Drift | Required | Optional | Optional | Optional | Optional |
| Target Drift | Optional | Target and/or prediction required | Target and/or prediction required | Optional | Optional |
| Classification Performance | Optional | Required | Required | Optional | Optional |
| Regression Performance | Optional | Required | Required | Optional | Optional |

{% hint style="info" %} 
**We recommend specifying column mapping manually**. Evidently applies different heuristics and rules to map the input data automatically. To avoid errors, it is always best to set column mapping manually. For example, numerical columns with only 3 different values in the reference data might be incorrectly parsed as categorical features.
{% endhint %}

# Primary mapping options

You can create a `ColumnMapping` object to map your column names and feature types. 

## Dataset structure

To specify the column names for target, prediction, ID or DateTime: 

```python
from evidently import ColumnMapping

column_mapping = ColumnMapping()

column_mapping.target = 'y' #'y' is the name of the column with the target function
column_mapping.prediction = 'pred' #'pred' is the name of the column(s) with model predictions
column_mapping.id = None #there is no ID column in the dataset
column_mapping.datetime = 'date' #'date' is the name of the column with datetime
```

## Categorical and numerical features

To split the features into numerical and categorical types: 

```python
column_mapping.numerical_features = ['temp', 'atemp', 'humidity'] #list of numerical features
column_mapping.categorical_features = ['season', 'holiday'] #list of categorical features
```

{% hint style="info" %} 
**Why map them:** the column types affect some of the tests, metrics and visualizations. For example, the [drift algorithm](../reference/data-drift-algorithm.md) selects a statistical test based on the column type and ignores DateTime features. Some of the data quality visualizations are different for specific feature types. Some of the tests (e.g. on value ranges) only considers numeral columns, etc.
{% endhint %}

## Text data 

To specify that columns contain raw text data: 

```python
column_mapping.text_features = ['email_subject', 'email_body']
```

{% hint style="info" %} 
**Why map them:** if you want to apply text-specific drift detection methods or call other metrics relevant to text data, you should specify them explicitly. Text columns are also excluded from certain tests and metrics similar to ID column.
{% endhint %}

## Embeddings features

To specify which columns in your dataset contain embeddings, you can pass a dictionary where keys are embedding names and values are lists of columns. 

Here is an example of how you point to the earlier defined list of columns that contain embeddings:

```python
column_mapping = ColumnMapping()
column_mapping.embeddings = {'small_subset': embeddings_data.columns[:10]}
```

{% hint style="info" %} 
**Why map them:** to apply embeddings-specific data drift detection methods. 
{% endhint %}

# Additional mapping options

There are additional mapping options that apply to specific test suites and reports.

## DateTime features 

You might have temporal features in your dataset. For example, “date of the last contact.” 
 
To map them, define: 

```python
column_mapping = ColumnMapping()
column_mapping.datetime_features = ['last_call_date', 'join_date'] #list of DateTime features
```

**Default**: Evidently treats columns with DateTime format (np.datetime64) as DateTime features.
 
**Note**: do not confuse DateTime features with the DateTime column, which is used as the x-axis in some plots. You will typically use the DateTime column as a prediction timestamp. 

{% hint style="info" %} 
**Why map them:** if you specify DateTime features, they will be ignored in data drift calculation. Evidently will also calculate appropriate statistics and generate different visualizations for DateTime features in the data quality report.
{% endhint %}

## Task parameter for target function

In many cases, it is important to differentiate between continuous and discrete targets. This applies to multiple reports and tests, including Data Quality and Target Drift. 
 
To define it explicitly, specify the task parameter:

```python
column_mapping = ColumnMapping()
column_mapping.target = 'y'
column_mapping.task = 'regression'
```
It accepts two values: 'regression' and 'classification'. 
 
**Default**: If you don't specify the task, Evidently will use a simple strategy: if the target has a numeric type and the number of unique values > 5: task == ‘regression.’ In all other cases, the task == ‘classification’.

{% hint style="info" %} 
**Why map it:**  If you have a multi-class problem where classes are encoded as numbers, it might look the same way as a regression problem. Thus it is best to explicitly specify it. It will affect how the target (prediction) is visualized and help pick the correct statistical tests for the target (prediction) drift detection. It will also affect the calculation of statistics and tests that differ for numerical and categorical data types.
{% endhint %} 

## Prediction column(s) in classification 

To evaluate the classification performance, you need both true labels and prediction. Depending on the classification type (e.g., binary, multi-class, probabilistic), you have different options of how to pass the predictions.

### Multiclass classification, option 1

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

If you pass the target names, they will appear on the visualizations. 

### Multiclass classification, option 2

Target: labels, Preds: labels. 

| target | prediction |
|---|---|
| ‘Versicolour’ | ‘Versicolour’ |
| ‘Setosa’ | ‘Virginica’ |
| … | … |
| ‘Virginica’ | ‘Virginica’ |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
```

### Multiclass probabilistic classification

Target: labels, Preds: columns named after labels.

| target | ‘Versicolour’ | ‘Setosa’ | ‘Virginica’ |
|---|---|---|---|
| ‘Setosa’ | 0.98 | 0.01 | 0.01 |
| ‘Virginica’ | 0.5 | 0.2 | 0.3 |
| … | … |  |  |
| ‘Virginica’ | 0.2 | 0.7 | 0.1 |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = ['Setosa', 'Versicolour', 'Virginica']

```

Naming the columns after the lables is a requirement. You cannot pass a custom list.

### Binary classification, option 1

Target: encoded labels, Preds: encoded labels + pos_label + Optional[target_names]

| target | prediction |
|---|---|
| 1 | 1 |
| 0 | 1 |
| … | … |
| 1 | 0 |

By default, Evidently expects the positive class to be labeled as ‘1’. If you have a different label, specify it explicitly.

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
column_mapping.target_names = ['churn', 'not_churn']
pos_label = 0

```

If you pass the target names, they will appear on the visualizations. 

### Binary classification, option 2 

Target: labels, Preds: labels + pos_label

| target | prediction |
|---|---|
| ‘churn’ | ‘churn’ |
| ‘not_churn’ | ‘churn’ |
| … | … |
| ‘churn’ | ‘not_churn’ |

Passing the name of the positive class is a requirement in this case.

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
pos_label = 'churn'

```

### Binary probabilistic classification, option 1 

Target: labels, Preds: columns named after labels + pos_label

| target | ‘churn’ | ‘not_churn’ |
|---|---|---|
| ‘churn’ | 0.9 | 0.1 |
| ‘churn’ | 0.7 | 0.3 |
| … | … |  |
| ‘not_churn’ | 0.5 | 0.5 |

Passing the name of the positive class is a requirement in this case.

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = ['churn', 'not_churn']
pos_label = 'churn'

```

### Binary probabilistic classification, option 2 

Target: labels, Preds: a column named like one of the labels + pos_label

| target | ‘not_churn’ |
|---|---|
| ‘churn’ | 0.5 |
| ‘not_churn’ | 0.1 |
| … | … |
| ‘churn’ | 0.9 |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'not_churn'
pos_label = 'churn'

```
Both naming the column after one of the labels and passing the name of the positive class are requirements.

### Binary probabilistic classification, option 3

Target: encoded labels, Preds: one column with any name + pos_label

| target | prediction |
|---|---|
| 1 | 0.5 |
| 1 | 0.1 |
| … | … |
| 0 | 0.9 |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
pos_label = 1
column_mapping.target_names = ['churn', 'not_churn']

```
If you pass the target names, they will appear on the visualizations.
