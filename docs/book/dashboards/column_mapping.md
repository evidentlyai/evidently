---
description: How to use column_mapping in Evidently.
---

This section applies both to Dashboards and Profiles.

If you prefer a video version, watch this tutorial:

{% embed url="https://www.youtube.com/watch?v=MiSl73LRj5I&t=7s&ab_channel=EvidentlyAI" %}

## Column mapping 

If the `column_mapping` is not specified or set as `None`, we use the default mapping strategy:

* All features with numeric types (np.number) will be treated as numerical. All datetime features (np.datetime64) will be treated as datetimes. All others will be treated as categorical.  
* The column with **'id'** name will be treated as an ID column.
* The column with **'datetime'** name will be treated as a datetime column.
* The column with **'target'** name will be treated as a target function.
* The column with **'prediction'** name will be treated as a model prediction.

ID, datetime, target, and prediction are utility columns. Requirements are different depending on the report type:

* For the **Data Drift** report, these columns are not required. If you specify id, target, and prediction, they will be excluded from the data drift report. If you specify the datetime, it will be used in data plots.
* For the **Target Drift** reports, we expect either the target or the prediction column or both. ID and datetime are optional.
* For **Model Performance** reports, both the target and the prediction column are required. ID and datetime are optional.
* For **Data Quality** report, these columns are not required. If you you specify target and datetime they will be used in data plots.

You can create a `ColumnMapping` object to specify whether your dataset includes the utility columns and split the features into numerical and categorical types. Also you could specify datetime types. If **datetime** expects that you pass main datetime column bounded with objects, **datetime_feature_names** expects all others date columns (example churn task: datetime: 'date_of_curn', datetime_feature_names = ['lust_call_date', 'join_date']) 

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

