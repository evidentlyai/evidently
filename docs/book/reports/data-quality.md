**TL;DR:** You can explore and track various dataset and feature statistics.

For Reports, you can use the `DataQualityPreset`. For Test Suites, you can use the `DataQualityTestPreset`or `DataStabilityTestPreset`.  

# Use Cases

You might need to track and evaluate data quality and integrity in different scenarios.

1. **Data quality tests in production.** You can check the quality and stability of the input data before you generate the predictions, every time you perform a certain transformation, add a new data source, etc. 

2. **Data profiling in production.** You can log and store JSON snapshots of your production data stats for future analysis and visualization. 

3. **Exploratory data analysis.** You can use the visual report to explore your training dataset and understand which features are stable and useful enough to use in modeling. 

4. **Dataset comparison.** You can use the report to compare two datasets to confirm similarities or understand the differences. For example, you might compare training and test dataset, subgroups in the same dataset (e.g., customers from Region 1 and Region 2), or current production data against training.

5. **Production model debugging.** If your model is underperforming, you can use this report to explore and interpret the details of changes in the input data or debug the quality issues.

For production pipeline tests, use Test Suites. For exploratory analysis and debugging, use Report.

# Data Quality Report 

If you want to get a visual report, you can create a new Report object and use the `DataQualityPreset`.

## Code example

```python
data_quality_report = Report(metrics=[
    DataQualityPreset(),
])

data_quality_report.run(reference_data=adult_ref, current_data=adult_cur)
data_quality_report
```

## How it works

The Data Quality report provides detailed feature statistics and a feature behavior overview. 

* The report works for a **single dataset** or **compares the two**. 
* Calculates base **statistics** for numerical, categorical and datetime features 
* Displays **interactive plots** with data distribution and behavior in time
* Plots **interactions and correlations** between features and target


## Data Requirements 

You need to pass only the input features. Target and prediction are optional. If you want to perform a side-by-side comparison, pass two datasets with identical schema. You can also pass a single dataset. 

You might need to specify additional column mapping:
* If you have a **datetime** column and want to learn how features change with time, specify the datetime column in the `column_mapping` parameter.
* If you have a **target** column and want to see features distribution by target, specify the target column in the `column_mapping` parameter. 

Feature types (numerical, categorical, datetime) will be parsed based on pandas column type. If you want to specify a different feature mapping strategy, you can explicitly set the feature type using `column_mapping`.

The report contains the section that plots interactions between the features and the target. It will look slightly different for classification and regression tasks. By default, if the target has a numeric type and has >5 unique values, Evidently will treat it as a regression problem. Everything else is treated as a classification problem. If you want to explicitly define your task as `regression` or `classification`, you should set the `task` parameter in the `column_mapping` object. 

{% hint style="info" %}
You can read more to understand [column mapping](../tests-and-reports/column-mapping.md) and [data requirements](../tests-and-reports/input-data.md) for Evidently reports in the corresponding sections of documentation.  
{% endhint %}

## How it looks

The default report includes 3 widgets. All plots are interactive.

### 1. Summary widget

The table gives an overview of the dataset, including missing or empty features and other general information. It also shows the share of almost empty and almost constant features. This applies to cases when 95% or more features are missing or constant.

![](../.gitbook/assets/reports_data_quality_summary.png)

### 2. Features widget

For each feature, this widget generates a set of visualizations. They vary depending on the feature type. There are 3 components:

#### 2.1. Feature overview table

The table shows relevant statistical summaries for each feature based on its type and a visualization of feature distribution. 

##### Example for a categorical feature:

![](../.gitbook/assets/reports_data_quality_overview_cat.png)

##### Example for a numerical feature:

![](../.gitbook/assets/reports_data_quality_overview_num.png)

##### Example for a datetime feature:

![](../.gitbook/assets/reports_data_quality_overview_datetime.png)

#### 2.2. Feature in time

If you click on "details", each feature would include additional visualization to show feature behavior in time.

##### Example for a categorical feature:

![](../.gitbook/assets/reports_data_quality_in_time_cat.png)

##### Example for a numerical feature:

![](../.gitbook/assets/reports_data_quality_in_time_num.png)

##### Example for a datetime feature:

![](../.gitbook/assets/reports_data_quality_in_time_datetime.png)

#### 2.3. Feature by target 

Categorical and numerical features include an additional visualization that plots the interaction between a given feature and the target. 

##### Example for a categorical feature:

![](../.gitbook/assets/reports_data_quality_by_target_cat.png)

##### Example for a numerical feature:

![](../.gitbook/assets/reports_data_quality_by_target_num.png)

### 3. Correlation widget

This widget shows the correlations between different features. 

#### 3.1. Insights

This table shows a summary of pairwise feature correlations.  

For a single dataset, it lists the top-5 highly correlated variables from Cramer's v correlation matrix (categorical features) and from Spearman correlation matrix (numerical features).

For two datasets, it lists the top-5 pairs of variables **where correlation changes** the most between the reference and current datasets. Similarly, it uses categorical features from Cramer's v correlation matrix and numerical features from Spearman correlation matrix.

![](../.gitbook/assets/reports_data_quality_correlations.png)

#### 3.2. Correlation heatmaps

This section includes four heatmaps. 

For categorical features, Evidently calculates the [Cramer's v](https://en.wikipedia.org/wiki/Cramér%27s_V) correlation matrix.
For numerical features, Evidently calculates the [Pearson](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient), [Spearman](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient) and [Kendall](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient) matrices. 

If your dataset includes the target, the target will be also shown in the matrix according to its type. 

![](../.gitbook/assets/reports_data_quality_correlation_heatmaps.png)

## JSON Profile

If you choose to generate a JSON profile, it will contain the following information:

```yaml
{
  'data_quality': {
    'data': {
      'cat_feature_names': [],
      'datetime_feature_names': [],
      'metrics': {
        'current': {
          'feature_name': {
            'count': count,
            'feature_type': 'num',
            'infinite_count': 0,
            'infinite_percentage': 0.0,
            'max': max,
            'mean': mean,
            'min': min,
            'missing_count': 0,
            'missing_percentage': 0.0,
            'most_common_value': most_common_value,
            'most_common_value_percentage': most_common_value_percentage,
            'percentile_25': percentile_25,
            'percentile_50': percentile_50,
            'percentile_75': percentile_75,
            'std': std,
            'unique_count': unique_count,
            'unique_percentage': unique_percentage
            },
          },
        },
        'num_feature_names': [],
        'target_names': None,
        'utility_columns': {
          'date': 'dteday',
          'id': None,
          'prediction': 'prediction',
          'target': 'target'
          }
        },
      'correlations': {
        'current': {
          'pearson': {
            'feature_name_1': {
              'feature_name_2': value,
              'feature_name_3': value
              },
            'feature_name_2': {
              'feature_name_1': value,
              'feature_name_3': value
              },
            'feature_name_3': {
              'feature_name_1': value,
              'feature_name_2': value
              }
            },
          'spearman': {
            'feature_name_1': {
              'feature_name_2': value,
              'feature_name_3': value
              },
            'feature_name_2': {
              'feature_name_1': value,
              'feature_name_3': value
              },
            'feature_name_3': {
              'feature_name_1': value,
              'feature_name_2': value
              }
            },
          'kendall': {
            'feature_name_1': {
              'feature_name_2': value,
              'feature_name_3': value
              },
            'feature_name_2': {
              'feature_name_1': value,
              'feature_name_3': value
              },
            'feature_name_3': {
              'feature_name_1': value,
              'feature_name_2': value
              }
            },
          'cramer_v': {
            'feature_name_4': {
              'feature_name_5': value
              },
            'feature_name_5': {
              'feature_name_4': value
              }
            }  
          }
        }  
    'datetime': '2022-02-22 16:35:15.529404',
    'name': 'data_quality'
    },
  'timestamp': 'timestamp'
}
```

## When to use it?

You can use the `DataStabilityTestPreset` when you receive a new batch of input data and want to compare it to the previous one. 

It will help compare the key descriptive statistics and the overall data shape between two batches you expect to be similar. For example, you can detect the appearance of new categorical values, new values, or a significant difference in the number of rows. 

### Code example

```python
data_stability = TestSuite(tests=[
   DataStabilityTestPreset(),
])
 
data_stability.run(reference_data=ref, current_data=curr)
data_stability
```

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

### Preset contents

The preset contains the following tests:


```python
TestNumberOfRows(),
TestNumberOfColumns(),
TestColumnsType(),
TestColumnShareOfMissingValues(column=’all’),
TestShareOfOutRangeValues(column=numerical_columns)
TestShareOfOutListValues(column=categorical_columns)
TestMeanInNSigmas(column=numerical_columns, n=2)
```

Unless specified otherwise, the default settings are applied. 

Head here to the [All tests](../reference/all-tests.md) table to see the description of individual tests and default parameters. 

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All tests" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}


## When to use it?

You can use the `DataQualityTestPreset` when you want to evaluate the data quality, even without a reference dataset.

It will help assess whether a data batch is e.g. suitable for training or retraining. It can detect issues like missing data, duplicates, or constant and almost constant features.  

### Code example

```python
data_quality = TestSuite(tests=[
   DataQualityTestPreset(),
])
 
data_quality.run(reference_data=ref,current_data=curr)
data_quality
```

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

### Preset contents

The preset contains the following tests:


```python
TestColumnShareOfMissingValues(column="all"),
TestMostCommonValueShare(column="all")
TestNumberOfConstantColumns(),
TestNumberOfDuplicatedColumns(),
TestNumberOfDuplicatedRows(),
TestHighlyCorrelatedColumns(),

```

Unless specified otherwise, the default settings are applied. 

Head here to the [All tests](../reference/all-tests.md) table to see the description of individual tests and default parameters. 

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All tests" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}


## Data Quality Report Examples

* Browse our [example](../get-started/examples.md) notebooks to see sample Reports.
