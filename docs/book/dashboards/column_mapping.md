---
description: How to use column_mapping in Evidently.
---

This section applies both to Dashboards and Profiles.

If you prefer a video version, watch this tutorial:

{% embed url="https://www.youtube.com/watch?v=MiSl73LRj5I&t=7s&ab_channel=EvidentlyAI" %}

## Column mapping 

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

