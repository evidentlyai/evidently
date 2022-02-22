# Data Quality

**TL;DR:** The report for exploratory data analysis

* Calculate base statistics for numerical, categorical and datetime features
* Displays interactive plots with data distribution
* Plots interactions for features and target
* Highlite behaviour of features in time 
* Can compare two datasets

## Summary

**Data Quality** report can be use for exploration your data and undefstanding which features are stabel and useful enought for using it for modeling. Moreower 
it can helps to compare two datasets: 
* train and test
* referense and current 
* subgroups of one dataset (for example your customers from Europe and from Asia)

## Requirements

If you wanr to run this report for one dataset you need padndas DataFrame with features you want to explore. Pass it as reference_data.
* if you have datetime column and want to learn how features change with time - specify datetime column in the Column Mapping parameter.
* if you have a target column and want to see features distribution by target - specify target column in the Column Mapping parameter.
For two dataset comparison you need two pandas DataFrame. The schema of both datasets should be identical.

## How it looks

## JSON Profile

If you choose to generate a JSON profile, it will contain the following information:&#x20;

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
        'reference': {
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
            }
          }
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
    'datetime': '2022-02-22 16:35:15.529404',
    'name': 'data_quality'
    },
  'timestamp': 'timestamp'
}
```

## Examples
