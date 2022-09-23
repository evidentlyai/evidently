---
description: How to use column mapping in Evidently..
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

Why map them: the column types affect some of the tests, metrics and visualizations. For example, the drift algorithm selects a statistical test based on the column type and ignores DateTime features. Some of the data quality visualizations are different for specific feature types. Some of the tests (e.g. on value ranges) only considers numeral columns, etc. 


**NOTE: Column names in Probabilistic Classification**

The tool expects your `DataFrame(s)` to contain columns with the names matching the ones from the ‘prediction’ list. Each column should include information about the predicted probability \[0;1] for the corresponding class.

```python
column_mapping = ColumnMapping()

column_mapping.prediction = ['class_name1', 'class_name2', 'class_name3',]
```

**NOTE: Column order in Binary Classification**

For binary classification, class order matters. The tool expects that the target (so-called positive) class is the **first** in the `column_mapping.prediction` list.


**NOTE: task parameter in Data Quality**

To build the report correctly we should define classification from regression problem. There is a case when we can’t do it for sure: multiclass problem with a lot of classes encoded by numbers looks like regression problem too. In such cases, you should specify the **task** parameter. It accepts two values: 'regression' and 'classification'.


```python
column_mapping = ColumnMapping()

column_mapping.target = 'y'
column_mapping.task = 'classification'
```

If you don't specify it we use a simple strategy: 

if the target has a numeric type and number of unique values > 5: task == ‘regression’

in all other cases task == ‘classification’

