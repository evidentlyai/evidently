# evidently.calculations package

## Subpackages

- [evidently.calculations.stattests package](evidently.calculations.stattests.md)

    - [Submodules](./evidently.calculations.stattests.md#submodules)

    - [evidently.calculations.stattests.anderson_darling_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.anderson_darling_stattest)

    - [evidently.calculations.stattests.chisquare_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.chisquare_stattest)

    - [evidently.calculations.stattests.cramer_von_mises_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.cramer_von_mises_stattest)

        - [`CVM_2samp()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.cramer_von_mises_stattest.CVM_2samp)

        - [`CramerVonMisesResult`](./evidently.calculations.stattests.md#evidently.calculations.stattests.cramer_von_mises_stattest.CramerVonMisesResult)

    - [evidently.calculations.stattests.energy_distance module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.energy_distance)

    - [evidently.calculations.stattests.epps_singleton_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.epps_singleton_stattest)

    - [evidently.calculations.stattests.fisher_exact_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.fisher_exact_stattest)

    - [evidently.calculations.stattests.g_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.g_stattest)

    - [evidently.calculations.stattests.hellinger_distance module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.hellinger_distance)

    - [evidently.calculations.stattests.jensenshannon module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.jensenshannon)

    - [evidently.calculations.stattests.kl_div module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.kl_div)

    - [evidently.calculations.stattests.ks_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.ks_stattest)

    - [evidently.calculations.stattests.mann_whitney_urank_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.mann_whitney_urank_stattest)

    - [evidently.calculations.stattests.psi module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.psi)

    - [evidently.calculations.stattests.registry module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.registry)

        - [`StatTest`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)

            - [`StatTest.allowed_feature_types`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.allowed_feature_types)

            - [`StatTest.default_threshold`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.default_threshold)

            - [`StatTest.display_name`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.display_name)

            - [`StatTest.func`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.func)

            - [`StatTest.name`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.name)

        - [`StatTestInvalidFeatureTypeError`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestInvalidFeatureTypeError)

        - [`StatTestNotFoundError`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestNotFoundError)

        - [`StatTestResult`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestResult)

            - [`StatTestResult.actual_threshold`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestResult.actual_threshold)

            - [`StatTestResult.drift_score`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestResult.drift_score)

            - [`StatTestResult.drifted`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestResult.drifted)

        - [`get_stattest()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.get_stattest)

        - [`register_stattest()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.registry.register_stattest)

    - [evidently.calculations.stattests.t_test module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.t_test)

    - [evidently.calculations.stattests.tvd_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.tvd_stattest)

    - [evidently.calculations.stattests.utils module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.utils)

        - [`generate_fisher2x2_contingency_table()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.utils.generate_fisher2x2_contingency_table)

        - [`get_binned_data()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.utils.get_binned_data)

        - [`get_unique_not_nan_values_list_from_series()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.utils.get_unique_not_nan_values_list_from_series)

        - [`permutation_test()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.utils.permutation_test)

    - [evidently.calculations.stattests.wasserstein_distance_norm module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.wasserstein_distance_norm)

    - [evidently.calculations.stattests.z_stattest module](./evidently.calculations.stattests.md#module-evidently.calculations.stattests.z_stattest)

        - [`proportions_diff_z_stat_ind()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.z_stattest.proportions_diff_z_stat_ind)

        - [`proportions_diff_z_test()`](./evidently.calculations.stattests.md#evidently.calculations.stattests.z_stattest.proportions_diff_z_test)

    - [Module contents](./evidently.calculations.stattests.md#module-evidently.calculations.stattests)


## Submodules

## evidently.calculations.classification_performance module


### _class_ evidently.calculations.classification_performance.ConfusionMatrix(labels: Sequence[Union[str, int]], values: list)
Bases: `object`


#### labels(_: Sequence[Union[str, int]_ )

#### values(_: lis_ )

### _class_ evidently.calculations.classification_performance.PredictionData(predictions: pandas.core.series.Series, prediction_probas: Optional[pandas.core.frame.DataFrame], labels: List[Union[str, int]])
Bases: `object`


#### labels(_: List[Union[str, int]_ )

#### prediction_probas(_: Optional[DataFrame_ )

#### predictions(_: Serie_ )

### evidently.calculations.classification_performance.calculate_confusion_by_classes(confusion_matrix: ndarray, class_names: Sequence[Union[str, int]])
Calculate metrics

    TP (true positive)
    TN (true negative)
    FP (false positive)
    FN (false negative)

for each class from confusion matrix.

Returns a dict like:
{

> “class_1_name”: {

>     “tp”: 1,
>     “tn”: 5,
>     “fp”: 0,
>     “fn”: 3,

}


### evidently.calculations.classification_performance.calculate_pr_table(binded)

### evidently.calculations.classification_performance.get_prediction_data(data: DataFrame, data_columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns), pos_label: Optional[Union[str, int]], threshold: float = 0.5)
Get predicted values and optional prediction probabilities from source data.
Also take into account a threshold value - if a probability is less than the value, do not take it into account.

Return and object with predicted values and an optional prediction probabilities.


### evidently.calculations.classification_performance.k_probability_threshold(prediction_probas: DataFrame, k: Union[int, float])

### evidently.calculations.classification_performance.threshold_probability_labels(prediction_probas: DataFrame, pos_label: Union[str, int], neg_label: Union[str, int], threshold: float)
Get prediction values by probabilities with the threshold apply

## evidently.calculations.data_drift module

Methods and types for data drift calculations


### _class_ evidently.calculations.data_drift.ColumnDataDriftMetrics(column_name: str, column_type: str, stattest_name: str, drift_score: float, drift_detected: bool, threshold: float, current_distribution: [Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution), reference_distribution: [Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution), current_small_distribution: Optional[list] = None, reference_small_distribution: Optional[list] = None, current_scatter: Optional[Dict[str, list]] = None, x_name: Optional[str] = None, plot_shape: Optional[Dict[str, float]] = None, current_correlations: Optional[Dict[str, float]] = None, reference_correlations: Optional[Dict[str, float]] = None)
Bases: `object`

One column drift metrics


#### column_name(_: st_ )

#### column_type(_: st_ )

#### current_correlations(_: Optional[Dict[str, float]_ _ = Non_ )

#### current_distribution(_: [Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution_ )

#### current_scatter(_: Optional[Dict[str, list]_ _ = Non_ )

#### current_small_distribution(_: Optional[list_ _ = Non_ )

#### drift_detected(_: boo_ )

#### drift_score(_: floa_ )

#### plot_shape(_: Optional[Dict[str, float]_ _ = Non_ )

#### reference_correlations(_: Optional[Dict[str, float]_ _ = Non_ )

#### reference_distribution(_: [Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution_ )

#### reference_small_distribution(_: Optional[list_ _ = Non_ )

#### stattest_name(_: st_ )

#### threshold(_: floa_ )

#### x_name(_: Optional[str_ _ = Non_ )

### _class_ evidently.calculations.data_drift.DatasetDrift(number_of_drifted_columns: int, dataset_drift_score: float, dataset_drift: bool)
Bases: `object`

Dataset drift calculation results


#### dataset_drift(_: boo_ )

#### dataset_drift_score(_: floa_ )

#### number_of_drifted_columns(_: in_ )

### _class_ evidently.calculations.data_drift.DatasetDriftMetrics(number_of_columns: int, number_of_drifted_columns: int, share_of_drifted_columns: float, dataset_drift: bool, drift_by_columns: Dict[str, evidently.calculations.data_drift.ColumnDataDriftMetrics], options: [evidently.options.data_drift.DataDriftOptions](./evidently.options.md#evidently.options.data_drift.DataDriftOptions), dataset_columns: [evidently.utils.data_operations.DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
Bases: `object`


#### dataset_columns(_: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns_ )

#### dataset_drift(_: boo_ )

#### drift_by_columns(_: Dict[str, ColumnDataDriftMetrics_ )

#### number_of_columns(_: in_ )

#### number_of_drifted_columns(_: in_ )

#### options(_: [DataDriftOptions](./evidently.options.md#evidently.options.data_drift.DataDriftOptions_ )

#### share_of_drifted_columns(_: floa_ )

### evidently.calculations.data_drift.ensure_prediction_column_is_string(\*, prediction_column: Optional[Union[str, Sequence]], current_data: DataFrame, reference_data: DataFrame, threshold: float = 0.5)
Update dataset by predictions type:
- if prediction column is None or a string, no dataset changes
- (binary classification) if predictions is a list and its length equals 2

> set predicted_labels column by classification_threshold

- (multy label classification) if predictions is a list and its length is greater than 2

    set predicted_labels from probability values in columns by prediction column

Returns prediction column name.


### evidently.calculations.data_drift.get_dataset_drift(drift_metrics, drift_share=0.5)

### evidently.calculations.data_drift.get_drift_for_columns(\*, current_data: DataFrame, reference_data: DataFrame, dataset_columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns), data_drift_options: [DataDriftOptions](./evidently.options.md#evidently.options.data_drift.DataDriftOptions), drift_share_threshold: Optional[float] = None, columns: Optional[List[str]] = None)

### evidently.calculations.data_drift.get_one_column_drift(\*, current_data: DataFrame, reference_data: DataFrame, column_name: str, options: [DataDriftOptions](./evidently.options.md#evidently.options.data_drift.DataDriftOptions), dataset_columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns), column_type: Optional[str] = None)
## evidently.calculations.data_integration module


### evidently.calculations.data_integration.get_number_of_all_pandas_missed_values(dataset: DataFrame)
Calculate the number of missed - nulls by pandas - values in a dataset


### evidently.calculations.data_integration.get_number_of_almost_constant_columns(dataset: DataFrame, threshold: float)
Calculate the number of almost constant columns in a dataset


### evidently.calculations.data_integration.get_number_of_almost_duplicated_columns(dataset: DataFrame, threshold: float)
Calculate the number of almost duplicated columns in a dataset


### evidently.calculations.data_integration.get_number_of_constant_columns(dataset: DataFrame)
Calculate the number of constant columns in a dataset


### evidently.calculations.data_integration.get_number_of_duplicated_columns(dataset: DataFrame)
Calculate the number of duplicated columns in a dataset


### evidently.calculations.data_integration.get_number_of_empty_columns(dataset: DataFrame)
Calculate the number of empty columns in a dataset

## evidently.calculations.data_quality module

Methods for overall dataset quality calculations - rows count, a specific values count, etc.


### _class_ evidently.calculations.data_quality.ColumnCorrelations(column_name: str, kind: str, values: [evidently.utils.visualizations.Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution))
Bases: `object`


#### column_name(_: st_ )

#### kind(_: st_ )

#### values(_: [Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution_ )

### _class_ evidently.calculations.data_quality.DataQualityGetPlotData()
Bases: `object`


#### calculate_data_by_target(curr: DataFrame, ref: Optional[DataFrame], feature_name: str, feature_type: str, target_name: str, target_type: str, merge_small_cat: Optional[int] = 5)

#### calculate_data_in_time(curr: DataFrame, ref: Optional[DataFrame], feature_name: str, feature_type: str, datetime_name: str, merge_small_cat: Optional[int] = 5)

#### calculate_main_plot(curr: DataFrame, ref: Optional[DataFrame], feature_name: str, feature_type: str, merge_small_cat: Optional[int] = 5)

### _class_ evidently.calculations.data_quality.DataQualityPlot(bins_for_hist: Dict[str, pandas.core.frame.DataFrame])
Bases: `object`


#### bins_for_hist(_: Dict[str, DataFrame_ )

### _class_ evidently.calculations.data_quality.DataQualityStats(rows_count: int, num_features_stats: Optional[Dict[str, evidently.calculations.data_quality.FeatureQualityStats]] = None, cat_features_stats: Optional[Dict[str, evidently.calculations.data_quality.FeatureQualityStats]] = None, datetime_features_stats: Optional[Dict[str, evidently.calculations.data_quality.FeatureQualityStats]] = None, target_stats: Optional[Dict[str, evidently.calculations.data_quality.FeatureQualityStats]] = None, prediction_stats: Optional[Dict[str, evidently.calculations.data_quality.FeatureQualityStats]] = None)
Bases: `object`


#### cat_features_stats(_: Optional[Dict[str, FeatureQualityStats]_ _ = Non_ )

#### datetime_features_stats(_: Optional[Dict[str, FeatureQualityStats]_ _ = Non_ )

#### get_all_features()

#### num_features_stats(_: Optional[Dict[str, FeatureQualityStats]_ _ = Non_ )

#### prediction_stats(_: Optional[Dict[str, FeatureQualityStats]_ _ = Non_ )

#### rows_count(_: in_ )

#### target_stats(_: Optional[Dict[str, FeatureQualityStats]_ _ = Non_ )

### _class_ evidently.calculations.data_quality.FeatureQualityStats(feature_type: str, number_of_rows: int = 0, count: int = 0, infinite_count: Optional[int] = None, infinite_percentage: Optional[float] = None, missing_count: Optional[int] = None, missing_percentage: Optional[float] = None, unique_count: Optional[int] = None, unique_percentage: Optional[float] = None, percentile_25: Optional[float] = None, percentile_50: Optional[float] = None, percentile_75: Optional[float] = None, max: Optional[Union[int, float, bool, str]] = None, min: Optional[Union[int, float, bool, str]] = None, mean: Optional[float] = None, most_common_value: Optional[Union[int, float, bool, str]] = None, most_common_value_percentage: Optional[float] = None, std: Optional[float] = None, most_common_not_null_value: Optional[Union[int, float, bool, str]] = None, most_common_not_null_value_percentage: Optional[float] = None, new_in_current_values_count: Optional[int] = None, unused_in_current_values_count: Optional[int] = None)
Bases: `object`

Class for all features data quality metrics store.

A type of the feature is stored in feature_type field.
Concrete stat kit depends on the feature type. Is a metric is not applicable - leave None value for it.

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

    - most_common_not_null_value - if most_common_value equals NaN - the next most common value. Otherwise - None

    - most_common_not_null_value_percentage - the percentage of most_common_not_null_value if it is defined.

        If most_common_not_null_value is not defined, equals None too.

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


#### as_dict()

#### count(_: in_ _ = _ )

#### feature_type(_: st_ )

#### infinite_count(_: Optional[int_ _ = Non_ )

#### infinite_percentage(_: Optional[float_ _ = Non_ )

#### is_category()
Checks that the object store stats for a category feature


#### is_datetime()
Checks that the object store stats for a datetime feature


#### is_numeric()
Checks that the object store stats for a numeric feature


#### max(_: Optional[Union[int, float, bool, str]_ _ = Non_ )

#### mean(_: Optional[float_ _ = Non_ )

#### min(_: Optional[Union[int, float, bool, str]_ _ = Non_ )

#### missing_count(_: Optional[int_ _ = Non_ )

#### missing_percentage(_: Optional[float_ _ = Non_ )

#### most_common_not_null_value(_: Optional[Union[int, float, bool, str]_ _ = Non_ )

#### most_common_not_null_value_percentage(_: Optional[float_ _ = Non_ )

#### most_common_value(_: Optional[Union[int, float, bool, str]_ _ = Non_ )

#### most_common_value_percentage(_: Optional[float_ _ = Non_ )

#### new_in_current_values_count(_: Optional[int_ _ = Non_ )

#### number_of_rows(_: in_ _ = _ )

#### percentile_25(_: Optional[float_ _ = Non_ )

#### percentile_50(_: Optional[float_ _ = Non_ )

#### percentile_75(_: Optional[float_ _ = Non_ )

#### std(_: Optional[float_ _ = Non_ )

#### unique_count(_: Optional[int_ _ = Non_ )

#### unique_percentage(_: Optional[float_ _ = Non_ )

#### unused_in_current_values_count(_: Optional[int_ _ = Non_ )

### evidently.calculations.data_quality.calculate_category_column_correlations(column_name: str, dataset: DataFrame, columns: List[str])
For category columns calculate cramer_v correlation


### evidently.calculations.data_quality.calculate_column_distribution(column: Series, column_type: str)

### evidently.calculations.data_quality.calculate_correlations(dataset: DataFrame, columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### evidently.calculations.data_quality.calculate_cramer_v_correlation(column_name: str, dataset: DataFrame, columns: List[str])

### evidently.calculations.data_quality.calculate_data_quality_stats(dataset: DataFrame, columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns), task: Optional[str])

### evidently.calculations.data_quality.calculate_numerical_column_correlations(column_name: str, dataset: DataFrame, columns: List[str])

### evidently.calculations.data_quality.get_features_stats(feature: Series, feature_type: str)

### evidently.calculations.data_quality.get_pairwise_correlation(df, func: Callable[[Series, Series], float])
Compute pairwise correlation of columns
:param df: initial data frame.
:param func: function for computing pairwise correlation.


* **Returns**

    Correlation matrix.



### evidently.calculations.data_quality.get_rows_count(data: Union[DataFrame, Series])
Count quantity of rows in  a dataset

## evidently.calculations.regression_performance module


### _class_ evidently.calculations.regression_performance.ErrorWithQuantiles(error, quantile_top, quantile_other)
Bases: `object`


### _class_ evidently.calculations.regression_performance.FeatureBias(feature_type: str, majority: float, under: float, over: float, range: float)
Bases: `object`


#### as_dict(prefix)

#### feature_type(_: st_ )

#### majority(_: floa_ )

#### over(_: floa_ )

#### range(_: floa_ )

#### under(_: floa_ )

### _class_ evidently.calculations.regression_performance.RegressionPerformanceMetrics(mean_error: float, mean_abs_error: float, mean_abs_perc_error: float, error_std: float, abs_error_max: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, error_bias: dict)
Bases: `object`


#### abs_error_max(_: floa_ )

#### abs_error_std(_: floa_ )

#### abs_perc_error_std(_: floa_ )

#### error_bias(_: dic_ )

#### error_normality(_: dic_ )

#### error_std(_: floa_ )

#### mean_abs_error(_: floa_ )

#### mean_abs_perc_error(_: floa_ )

#### mean_error(_: floa_ )

#### underperformance(_: dic_ )

### evidently.calculations.regression_performance.calculate_regression_performance(dataset: DataFrame, columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns), error_bias_prefix: str)

### evidently.calculations.regression_performance.error_bias_table(dataset, err_quantiles, num_feature_names, cat_feature_names)

### evidently.calculations.regression_performance.error_with_quantiles(dataset, prediction_column, target_column, quantile: float)
## Module contents
