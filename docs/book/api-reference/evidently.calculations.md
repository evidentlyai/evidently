# Table of Contents

* [evidently.calculations](#evidently.calculations)
* [evidently.calculations.classification\_performance](#evidently.calculations.classification_performance)
  * [calculate\_confusion\_by\_classes](#evidently.calculations.classification_performance.calculate_confusion_by_classes)
  * [get\_prediction\_data](#evidently.calculations.classification_performance.get_prediction_data)
  * [threshold\_probability\_labels](#evidently.calculations.classification_performance.threshold_probability_labels)
* [evidently.calculations.data\_drift](#evidently.calculations.data_drift)
  * [ColumnDataDriftMetrics](#evidently.calculations.data_drift.ColumnDataDriftMetrics)
  * [DatasetDrift](#evidently.calculations.data_drift.DatasetDrift)
  * [ensure\_prediction\_column\_is\_string](#evidently.calculations.data_drift.ensure_prediction_column_is_string)
* [evidently.calculations.data\_integration](#evidently.calculations.data_integration)
  * [get\_number\_of\_all\_pandas\_missed\_values](#evidently.calculations.data_integration.get_number_of_all_pandas_missed_values)
  * [get\_number\_of\_empty\_columns](#evidently.calculations.data_integration.get_number_of_empty_columns)
  * [get\_number\_of\_duplicated\_columns](#evidently.calculations.data_integration.get_number_of_duplicated_columns)
  * [get\_number\_of\_almost\_duplicated\_columns](#evidently.calculations.data_integration.get_number_of_almost_duplicated_columns)
  * [get\_number\_of\_constant\_columns](#evidently.calculations.data_integration.get_number_of_constant_columns)
  * [get\_number\_of\_almost\_constant\_columns](#evidently.calculations.data_integration.get_number_of_almost_constant_columns)
* [evidently.calculations.data\_quality](#evidently.calculations.data_quality)
  * [get\_rows\_count](#evidently.calculations.data_quality.get_rows_count)
  * [FeatureQualityStats](#evidently.calculations.data_quality.FeatureQualityStats)
    * [is\_datetime](#evidently.calculations.data_quality.FeatureQualityStats.is_datetime)
    * [is\_numeric](#evidently.calculations.data_quality.FeatureQualityStats.is_numeric)
    * [is\_category](#evidently.calculations.data_quality.FeatureQualityStats.is_category)
  * [get\_pairwise\_correlation](#evidently.calculations.data_quality.get_pairwise_correlation)
  * [calculate\_category\_column\_correlations](#evidently.calculations.data_quality.calculate_category_column_correlations)
* [evidently.calculations.regression\_performance](#evidently.calculations.regression_performance)
* [evidently.calculations.stattests.anderson\_darling\_stattest](#evidently.calculations.stattests.anderson_darling_stattest)
* [evidently.calculations.stattests.chisquare\_stattest](#evidently.calculations.stattests.chisquare_stattest)
* [evidently.calculations.stattests.cramer\_von\_mises\_stattest](#evidently.calculations.stattests.cramer_von_mises_stattest)
  * [CVM\_2samp](#evidently.calculations.stattests.cramer_von_mises_stattest.CVM_2samp)
* [evidently.calculations.stattests.energy\_distance](#evidently.calculations.stattests.energy_distance)
* [evidently.calculations.stattests.epps\_singleton\_stattest](#evidently.calculations.stattests.epps_singleton_stattest)
* [evidently.calculations.stattests.fisher\_exact\_stattest](#evidently.calculations.stattests.fisher_exact_stattest)
* [evidently.calculations.stattests.g\_stattest](#evidently.calculations.stattests.g_stattest)
* [evidently.calculations.stattests.hellinger\_distance](#evidently.calculations.stattests.hellinger_distance)
* [evidently.calculations.stattests.jensenshannon](#evidently.calculations.stattests.jensenshannon)
* [evidently.calculations.stattests.kl\_div](#evidently.calculations.stattests.kl_div)
* [evidently.calculations.stattests.ks\_stattest](#evidently.calculations.stattests.ks_stattest)
* [evidently.calculations.stattests.mann\_whitney\_urank\_stattest](#evidently.calculations.stattests.mann_whitney_urank_stattest)
* [evidently.calculations.stattests.psi](#evidently.calculations.stattests.psi)
* [evidently.calculations.stattests.registry](#evidently.calculations.stattests.registry)
* [evidently.calculations.stattests.tvd\_stattest](#evidently.calculations.stattests.tvd_stattest)
* [evidently.calculations.stattests.t\_test](#evidently.calculations.stattests.t_test)
* [evidently.calculations.stattests.utils](#evidently.calculations.stattests.utils)
  * [get\_unique\_not\_nan\_values\_list\_from\_series](#evidently.calculations.stattests.utils.get_unique_not_nan_values_list_from_series)
  * [get\_binned\_data](#evidently.calculations.stattests.utils.get_binned_data)
  * [permutation\_test](#evidently.calculations.stattests.utils.permutation_test)
  * [generate\_fisher2x2\_contingency\_table](#evidently.calculations.stattests.utils.generate_fisher2x2_contingency_table)
* [evidently.calculations.stattests.wasserstein\_distance\_norm](#evidently.calculations.stattests.wasserstein_distance_norm)
* [evidently.calculations.stattests.z\_stattest](#evidently.calculations.stattests.z_stattest)
* [evidently.calculations.stattests](#evidently.calculations.stattests)

<a id="evidently.calculations"></a>

# evidently.calculations

<a id="evidently.calculations.classification_performance"></a>

# evidently.calculations.classification\_performance

<a id="evidently.calculations.classification_performance.calculate_confusion_by_classes"></a>

#### calculate\_confusion\_by\_classes

```python
def calculate_confusion_by_classes(
    confusion_matrix: np.ndarray, class_names: Sequence[Union[str, int]]
) -> Dict[Union[str, int], Dict[str, int]]
```

Calculate metrics
    TP (true positive)
    TN (true negative)
    FP (false positive)
    FN (false negative)
for each class from confusion matrix.

Returns a dict like:
{
    "class_1_name": {
        "tp": 1,
        "tn": 5,
        "fp": 0,
        "fn": 3,
    },
    ...
}

<a id="evidently.calculations.classification_performance.get_prediction_data"></a>

#### get\_prediction\_data

```python
def get_prediction_data(data: pd.DataFrame,
                        data_columns: DatasetColumns,
                        pos_label: Optional[Union[str, int]],
                        threshold: float = 0.5) -> PredictionData
```

Get predicted values and optional prediction probabilities from source data.
Also take into account a threshold value - if a probability is less than the value, do not take it into account.

Return and object with predicted values and an optional prediction probabilities.

<a id="evidently.calculations.classification_performance.threshold_probability_labels"></a>

#### threshold\_probability\_labels

```python
def threshold_probability_labels(prediction_probas: pd.DataFrame,
                                 pos_label: Union[str,
                                                  int], neg_label: Union[str,
                                                                         int],
                                 threshold: float) -> pd.Series
```

Get prediction values by probabilities with the threshold apply

<a id="evidently.calculations.data_drift"></a>

# evidently.calculations.data\_drift

Methods and types for data drift calculations

<a id="evidently.calculations.data_drift.ColumnDataDriftMetrics"></a>

## ColumnDataDriftMetrics Objects

```python
@dataclass
class ColumnDataDriftMetrics()
```

One column drift metrics

<a id="evidently.calculations.data_drift.DatasetDrift"></a>

## DatasetDrift Objects

```python
@dataclass
class DatasetDrift()
```

Dataset drift calculation results

<a id="evidently.calculations.data_drift.ensure_prediction_column_is_string"></a>

#### ensure\_prediction\_column\_is\_string

```python
def ensure_prediction_column_is_string(
        *,
        prediction_column: Optional[Union[str, Sequence]],
        current_data: pd.DataFrame,
        reference_data: pd.DataFrame,
        threshold: float = 0.5) -> Optional[str]
```

Update dataset by predictions type:
- if prediction column is None or a string, no dataset changes
- (binary classification) if predictions is a list and its length equals 2
    set predicted_labels column by `classification_threshold`
- (multy label classification) if predictions is a list and its length is greater than 2
    set predicted_labels from probability values in columns by prediction column

Returns prediction column name.

<a id="evidently.calculations.data_integration"></a>

# evidently.calculations.data\_integration

<a id="evidently.calculations.data_integration.get_number_of_all_pandas_missed_values"></a>

#### get\_number\_of\_all\_pandas\_missed\_values

```python
def get_number_of_all_pandas_missed_values(dataset: pd.DataFrame) -> int
```

Calculate the number of missed - nulls by pandas - values in a dataset

<a id="evidently.calculations.data_integration.get_number_of_empty_columns"></a>

#### get\_number\_of\_empty\_columns

```python
def get_number_of_empty_columns(dataset: pd.DataFrame) -> int
```

Calculate the number of empty columns in a dataset

<a id="evidently.calculations.data_integration.get_number_of_duplicated_columns"></a>

#### get\_number\_of\_duplicated\_columns

```python
def get_number_of_duplicated_columns(dataset: pd.DataFrame) -> int
```

Calculate the number of duplicated columns in a dataset

<a id="evidently.calculations.data_integration.get_number_of_almost_duplicated_columns"></a>

#### get\_number\_of\_almost\_duplicated\_columns

```python
def get_number_of_almost_duplicated_columns(dataset: pd.DataFrame,
                                            threshold: float) -> int
```

Calculate the number of almost duplicated columns in a dataset

<a id="evidently.calculations.data_integration.get_number_of_constant_columns"></a>

#### get\_number\_of\_constant\_columns

```python
def get_number_of_constant_columns(dataset: pd.DataFrame) -> int
```

Calculate the number of constant columns in a dataset

<a id="evidently.calculations.data_integration.get_number_of_almost_constant_columns"></a>

#### get\_number\_of\_almost\_constant\_columns

```python
def get_number_of_almost_constant_columns(dataset: pd.DataFrame,
                                          threshold: float) -> int
```

Calculate the number of almost constant columns in a dataset

<a id="evidently.calculations.data_quality"></a>

# evidently.calculations.data\_quality

Methods for overall dataset quality calculations - rows count, a specific values count, etc.

<a id="evidently.calculations.data_quality.get_rows_count"></a>

#### get\_rows\_count

```python
def get_rows_count(data: Union[pd.DataFrame, pd.Series]) -> int
```

Count quantity of rows in  a dataset

<a id="evidently.calculations.data_quality.FeatureQualityStats"></a>

## FeatureQualityStats Objects

```python
@dataclasses.dataclass
class FeatureQualityStats()
```

Class for all features data quality metrics store.

A type of the feature is stored in `feature_type` field.
Concrete stat kit depends on the feature type. Is a metric is not applicable - leave `None` value for it.

Metrics for all feature types:
    - feature type - cat for category, num for numeric, datetime for datetime features
    - count - quantity of a meaningful values (do not take into account NaN values)
    - missing_count - quantity of meaningless (NaN) values
    - missing_percentage - the percentage of the missed values
    - unique_count - quantity of unique values
    - unique_percentage - the percentage of the unique values
    - max - maximum value (not applicable for category features)
    - min - minimum value (not applicable for category features)
    - most_common_value - the most common value in the feature values
    - most_common_value_percentage - the percentage of the most common value
    - most_common_not_null_value - if `most_common_value` equals NaN - the next most common value. Otherwise - None
    - most_common_not_null_value_percentage - the percentage of `most_common_not_null_value` if it is defined.
        If `most_common_not_null_value` is not defined, equals None too.

Metrics for numeric features only:
    - infinite_count - quantity infinite values (for numeric features only)
    - infinite_percentage - the percentage of infinite values (for numeric features only)
    - percentile_25 - 25% percentile for meaningful values
    - percentile_50 - 50% percentile for meaningful values
    - percentile_75 - 75% percentile for meaningful values
    - mean - the sum of the meaningful values divided by the number of the meaningful values
    - std - standard deviation of the values

Metrics for category features only:
    - new_in_current_values_count - quantity of new values in the current dataset after the reference
        Defined for reference dataset only.
    - new_in_current_values_count - quantity of values in the reference dataset that not presented in the current
        Defined for reference dataset only.

<a id="evidently.calculations.data_quality.FeatureQualityStats.is_datetime"></a>

#### is\_datetime

```python
def is_datetime()
```

Checks that the object store stats for a datetime feature

<a id="evidently.calculations.data_quality.FeatureQualityStats.is_numeric"></a>

#### is\_numeric

```python
def is_numeric()
```

Checks that the object store stats for a numeric feature

<a id="evidently.calculations.data_quality.FeatureQualityStats.is_category"></a>

#### is\_category

```python
def is_category()
```

Checks that the object store stats for a category feature

<a id="evidently.calculations.data_quality.get_pairwise_correlation"></a>

#### get\_pairwise\_correlation

```python
def get_pairwise_correlation(
        df, func: Callable[[pd.Series, pd.Series], float]) -> pd.DataFrame
```

Compute pairwise correlation of columns

**Arguments**:

- `df` - initial data frame.
- `func` - function for computing pairwise correlation.

**Returns**:

  Correlation matrix.

<a id="evidently.calculations.data_quality.calculate_category_column_correlations"></a>

#### calculate\_category\_column\_correlations

```python
def calculate_category_column_correlations(
        column_name: str, dataset: pd.DataFrame,
        columns: List[str]) -> Dict[str, ColumnCorrelations]
```

For category columns calculate cramer_v correlation

<a id="evidently.calculations.regression_performance"></a>

# evidently.calculations.regression\_performance

<a id="evidently.calculations.stattests.anderson_darling_stattest"></a>

# evidently.calculations.stattests.anderson\_darling\_stattest

<a id="evidently.calculations.stattests.chisquare_stattest"></a>

# evidently.calculations.stattests.chisquare\_stattest

<a id="evidently.calculations.stattests.cramer_von_mises_stattest"></a>

# evidently.calculations.stattests.cramer\_von\_mises\_stattest

<a id="evidently.calculations.stattests.cramer_von_mises_stattest.CVM_2samp"></a>

#### CVM\_2samp

```python
def CVM_2samp(x: np.ndarray,
              y: np.ndarray,
              method: str = "auto") -> CramerVonMisesResult
```

Perform the two-sample Cram├⌐r-von Mises test

**Arguments**:

  x : array_like
  y : array_like
  method : {'auto', 'asymptotic', 'exact'}, optional

**Returns**:

  res : object with attributes
  statistic : Cram├⌐r-von Mises statistic.
  pvalue : float

<a id="evidently.calculations.stattests.energy_distance"></a>

# evidently.calculations.stattests.energy\_distance

<a id="evidently.calculations.stattests.epps_singleton_stattest"></a>

# evidently.calculations.stattests.epps\_singleton\_stattest

<a id="evidently.calculations.stattests.fisher_exact_stattest"></a>

# evidently.calculations.stattests.fisher\_exact\_stattest

<a id="evidently.calculations.stattests.g_stattest"></a>

# evidently.calculations.stattests.g\_stattest

<a id="evidently.calculations.stattests.hellinger_distance"></a>

# evidently.calculations.stattests.hellinger\_distance

<a id="evidently.calculations.stattests.jensenshannon"></a>

# evidently.calculations.stattests.jensenshannon

<a id="evidently.calculations.stattests.kl_div"></a>

# evidently.calculations.stattests.kl\_div

<a id="evidently.calculations.stattests.ks_stattest"></a>

# evidently.calculations.stattests.ks\_stattest

<a id="evidently.calculations.stattests.mann_whitney_urank_stattest"></a>

# evidently.calculations.stattests.mann\_whitney\_urank\_stattest

<a id="evidently.calculations.stattests.psi"></a>

# evidently.calculations.stattests.psi

<a id="evidently.calculations.stattests.registry"></a>

# evidently.calculations.stattests.registry

<a id="evidently.calculations.stattests.tvd_stattest"></a>

# evidently.calculations.stattests.tvd\_stattest

<a id="evidently.calculations.stattests.t_test"></a>

# evidently.calculations.stattests.t\_test

<a id="evidently.calculations.stattests.utils"></a>

# evidently.calculations.stattests.utils

<a id="evidently.calculations.stattests.utils.get_unique_not_nan_values_list_from_series"></a>

#### get\_unique\_not\_nan\_values\_list\_from\_series

```python
def get_unique_not_nan_values_list_from_series(
        current_data: pd.Series, reference_data: pd.Series) -> list
```

Get unique values from current and reference series, drop NaNs

<a id="evidently.calculations.stattests.utils.get_binned_data"></a>

#### get\_binned\_data

```python
def get_binned_data(reference_data: pd.Series,
                    current_data: pd.Series,
                    feature_type: str,
                    n: int,
                    feel_zeroes: bool = True)
```

Split variable into n buckets based on reference quantiles

**Arguments**:

- `reference_data` - reference data
- `current_data` - current data
- `feature_type` - feature type
- `n` - number of quantiles

**Returns**:

- `reference_percents` - % of records in each bucket for reference
- `current_percents` - % of records in each bucket for current

<a id="evidently.calculations.stattests.utils.permutation_test"></a>

#### permutation\_test

```python
def permutation_test(reference_data,
                     current_data,
                     observed,
                     test_statistic_func,
                     iterations=100)
```

Perform a two-sided permutation test

**Arguments**:

- `reference_data` - reference data
- `current_data` - current data
- `observed` - observed value
- `test_statistic_func` - the test statistic function
- `iterations` - number of times to permute

**Returns**:

- `p_value` - two-sided p_value

<a id="evidently.calculations.stattests.utils.generate_fisher2x2_contingency_table"></a>

#### generate\_fisher2x2\_contingency\_table

```python
def generate_fisher2x2_contingency_table(
        reference_data: pd.Series, current_data: pd.Series) -> np.ndarray
```

Generate 2x2 contingency matrix for fisher exact test

**Arguments**:

- `reference_data` - reference data
- `current_data` - current data

**Raises**:

- `ValueError` - if reference_data and current_data are not of equal length

**Returns**:

- `contingency_matrix` - contingency_matrix for binary data

<a id="evidently.calculations.stattests.wasserstein_distance_norm"></a>

# evidently.calculations.stattests.wasserstein\_distance\_norm

<a id="evidently.calculations.stattests.z_stattest"></a>

# evidently.calculations.stattests.z\_stattest

<a id="evidently.calculations.stattests"></a>

# evidently.calculations.stattests

