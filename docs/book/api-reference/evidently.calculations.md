# evidently.calculations package

## Subpackages

- [evidently.calculations.stattests package](evidently.calculations.stattests.md)

    - [Submodules](evidently.calculations.stattests.md#module-evidently.calculations.stattests.anderson_darling_stattest)

        - [`CVM_2samp()`](evidently.calculations.stattests.md#evidently.calculations.stattests.cramer_von_mises_stattest.CVM_2samp)

        - [`CramerVonMisesResult`](evidently.calculations.stattests.md#evidently.calculations.stattests.cramer_von_mises_stattest.CramerVonMisesResult)

        - [`StatTest`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)

            - [`StatTest.allowed_feature_types`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.allowed_feature_types)

            - [`StatTest.default_threshold`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.default_threshold)

            - [`StatTest.display_name`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.display_name)

            - [`StatTest.func`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.func)

            - [`StatTest.name`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest.name)

        - [`StatTestInvalidFeatureTypeError`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestInvalidFeatureTypeError)

        - [`StatTestNotFoundError`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestNotFoundError)

        - [`StatTestResult`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestResult)

            - [`StatTestResult.actual_threshold`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestResult.actual_threshold)

            - [`StatTestResult.drift_score`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestResult.drift_score)

            - [`StatTestResult.drifted`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTestResult.drifted)

        - [`get_stattest()`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.get_stattest)

        - [`register_stattest()`](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.register_stattest)

        - [`generate_fisher2x2_contingency_table()`](evidently.calculations.stattests.md#evidently.calculations.stattests.utils.generate_fisher2x2_contingency_table)

        - [`get_binned_data()`](evidently.calculations.stattests.md#evidently.calculations.stattests.utils.get_binned_data)

        - [`get_unique_not_nan_values_list_from_series()`](evidently.calculations.stattests.md#evidently.calculations.stattests.utils.get_unique_not_nan_values_list_from_series)

        - [`permutation_test()`](evidently.calculations.stattests.md#evidently.calculations.stattests.utils.permutation_test)

        - [`proportions_diff_z_stat_ind()`](evidently.calculations.stattests.md#evidently.calculations.stattests.z_stattest.proportions_diff_z_stat_ind)

        - [`proportions_diff_z_test()`](evidently.calculations.stattests.md#evidently.calculations.stattests.z_stattest.proportions_diff_z_test)

    - [Module contents](evidently.calculations.stattests.md#module-evidently.calculations.stattests)


## Submodules


### _class _ ConfusionMatrix(labels: Sequence[Union[str, int]], values: list)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; labels _: Sequence[Union[str, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; values _: list_ 

#### Methods: 

### _class _ DatasetClassificationQuality(accuracy: float, precision: float, recall: float, f1: float, roc_auc: Optional[float] = None, log_loss: Optional[float] = None, tpr: Optional[float] = None, tnr: Optional[float] = None, fpr: Optional[float] = None, fnr: Optional[float] = None, rate_plots_data: Optional[Dict] = None, plot_data: Optional[Dict] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; accuracy _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; f1 _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; fnr _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; fpr _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; log_loss _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; plot_data _: Optional[Dict]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; precision _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; rate_plots_data _: Optional[Dict]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; recall _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; roc_auc _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; tnr _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; tpr _: Optional[float]_ _ = None_ 

#### Methods: 

### _class _ PredictionData(predictions: pandas.core.series.Series, prediction_probas: Optional[pandas.core.frame.DataFrame], labels: List[Union[str, int]])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; labels _: List[Union[str, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; prediction_probas _: Optional[DataFrame]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; predictions _: Series_ 

#### Methods: 

### calculate_confusion_by_classes(confusion_matrix: ndarray, class_names: Sequence[Union[str, int]])
Calculate metrics:
- TP (true positive)
- TN (true negative)
- FP (false positive)
- FN (false negative)
for each class from confusion matrix.


* **Returns**

    a dict like:

    ```default
    {
        "class_1_name": {
            "tp": 1,
            "tn": 5,
            "fp": 0,
            "fn": 3,
        },
        "class_1_name": {
            "tp": 1,
            "tn": 5,
            "fp": 0,
            "fn": 3,
        },
    }
    ```




### calculate_matrix(target: Series, prediction: Series, labels: List[Union[str, int]])

### calculate_metrics(column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), confusion_matrix: ConfusionMatrix, target: Series, prediction: PredictionData)

### calculate_pr_table(binded)

### collect_plot_data(prediction_probas: DataFrame)

### get_prediction_data(data: DataFrame, data_columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), pos_label: Optional[Union[str, int]], threshold: float = 0.5)
Get predicted values and optional prediction probabilities from source data.
Also take into account a threshold value - if a probability is less than the value, do not take it into account.

Return and object with predicted values and an optional prediction probabilities.


### k_probability_threshold(prediction_probas: DataFrame, k: Union[int, float])

### threshold_probability_labels(prediction_probas: DataFrame, pos_label: Union[str, int], neg_label: Union[str, int], threshold: float)
Get prediction values by probabilities with the threshold apply

Methods and types for data drift calculations.


### _class _ ColumnDataDriftMetrics(column_name: str, column_type: str, stattest_name: str, drift_score: float, drift_detected: bool, threshold: float, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), current_small_distribution: Optional[list] = None, reference_small_distribution: Optional[list] = None, current_scatter: Optional[Dict[str, list]] = None, x_name: Optional[str] = None, plot_shape: Optional[Dict[str, float]] = None, current_correlations: Optional[Dict[str, float]] = None, reference_correlations: Optional[Dict[str, float]] = None)
Bases: `object`

One column drift metrics.


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_type _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_correlations _: Optional[Dict[str, float]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_distribution _: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_scatter _: Optional[Dict[str, list]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_small_distribution _: Optional[list]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; drift_detected _: bool_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; drift_score _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; plot_shape _: Optional[Dict[str, float]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_correlations _: Optional[Dict[str, float]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_distribution _: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_small_distribution _: Optional[list]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; stattest_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; threshold _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; x_name _: Optional[str]_ _ = None_ 

#### Methods: 

### _class _ DatasetDrift(number_of_drifted_columns: int, dataset_drift_score: float, dataset_drift: bool)
Bases: `object`

Dataset drift calculation results


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; dataset_drift _: bool_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; dataset_drift_score _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_drifted_columns _: int_ 

#### Methods: 

### _class _ DatasetDriftMetrics(number_of_columns: int, number_of_drifted_columns: int, share_of_drifted_columns: float, dataset_drift: bool, drift_by_columns: Dict[str, ColumnDataDriftMetrics], options: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions), dataset_columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; dataset_columns _: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; dataset_drift _: bool_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; drift_by_columns _: Dict[str, ColumnDataDriftMetrics]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_drifted_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; share_of_drifted_columns _: float_ 

#### Methods: 

### ensure_prediction_column_is_string(\*, prediction_column: Optional[Union[str, Sequence]], current_data: DataFrame, reference_data: DataFrame, threshold: float = 0.5)
Update dataset by predictions type:

- if prediction column is None or a string, no dataset changes

- (binary classification) if predictions is a list and its length equals 2

    set predicted_labels column by threshold

- (multy label classification) if predictions is a list and its length is greater than 2

    set predicted_labels from probability values in columns by prediction column


* **Returns**

    prediction column name.



### get_dataset_drift(drift_metrics, drift_share=0.5)

### get_drift_for_columns(\*, current_data: DataFrame, reference_data: DataFrame, dataset_columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), data_drift_options: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions), drift_share_threshold: Optional[float] = None, columns: Optional[List[str]] = None)

### get_one_column_drift(\*, current_data: DataFrame, reference_data: DataFrame, column_name: str, options: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions), dataset_columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), column_type: Optional[str] = None)

### get_number_of_all_pandas_missed_values(dataset: DataFrame)
Calculate the number of missed - nulls by pandas - values in a dataset


### get_number_of_almost_constant_columns(dataset: DataFrame, threshold: float)
Calculate the number of almost constant columns in a dataset


### get_number_of_almost_duplicated_columns(dataset: DataFrame, threshold: float)
Calculate the number of almost duplicated columns in a dataset


### get_number_of_constant_columns(dataset: DataFrame)
Calculate the number of constant columns in a dataset


### get_number_of_duplicated_columns(dataset: DataFrame)
Calculate the number of duplicated columns in a dataset


### get_number_of_empty_columns(dataset: DataFrame)
Calculate the number of empty columns in a dataset

Methods for overall dataset quality calculations - rows count, a specific values count, etc.


### _class _ ColumnCorrelations(column_name: str, kind: str, values: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution))
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; kind _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; values _: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ 

#### Methods: 

### _class _ DataQualityGetPlotData()
Bases: `object`


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate_data_by_target(curr: DataFrame, ref: Optional[DataFrame], feature_name: str, feature_type: str, target_name: str, target_type: str, merge_small_cat: Optional[int] = 5)

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate_data_in_time(curr: DataFrame, ref: Optional[DataFrame], feature_name: str, feature_type: str, datetime_name: str, merge_small_cat: Optional[int] = 5)

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate_main_plot(curr: DataFrame, ref: Optional[DataFrame], feature_name: str, feature_type: str, merge_small_cat: Optional[int] = 5)

### _class _ DataQualityPlot(bins_for_hist: Dict[str, pandas.core.frame.DataFrame])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; bins_for_hist _: Dict[str, DataFrame]_ 

#### Methods: 

### _class _ DataQualityStats(rows_count: int, num_features_stats: Optional[Dict[str, FeatureQualityStats]] = None, cat_features_stats: Optional[Dict[str, FeatureQualityStats]] = None, datetime_features_stats: Optional[Dict[str, FeatureQualityStats]] = None, target_stats: Optional[Dict[str, FeatureQualityStats]] = None, prediction_stats: Optional[Dict[str, FeatureQualityStats]] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; cat_features_stats _: Optional[Dict[str, FeatureQualityStats]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; datetime_features_stats _: Optional[Dict[str, FeatureQualityStats]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; num_features_stats _: Optional[Dict[str, FeatureQualityStats]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; prediction_stats _: Optional[Dict[str, FeatureQualityStats]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; rows_count _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target_stats _: Optional[Dict[str, FeatureQualityStats]]_ _ = None_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; get_all_features()

### _class _ FeatureQualityStats(feature_type: str, number_of_rows: int = 0, count: int = 0, infinite_count: Optional[int] = None, infinite_percentage: Optional[float] = None, missing_count: Optional[int] = None, missing_percentage: Optional[float] = None, unique_count: Optional[int] = None, unique_percentage: Optional[float] = None, percentile_25: Optional[float] = None, percentile_50: Optional[float] = None, percentile_75: Optional[float] = None, max: Optional[Union[int, float, bool, str]] = None, min: Optional[Union[int, float, bool, str]] = None, mean: Optional[float] = None, most_common_value: Optional[Union[int, float, bool, str]] = None, most_common_value_percentage: Optional[float] = None, std: Optional[float] = None, most_common_not_null_value: Optional[Union[int, float, bool, str]] = None, most_common_not_null_value_percentage: Optional[float] = None, new_in_current_values_count: Optional[int] = None, unused_in_current_values_count: Optional[int] = None)
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


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; count _: int_ _ = 0_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; feature_type _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; infinite_count _: Optional[int]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; infinite_percentage _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; max _: Optional[Union[int, float, bool, str]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; mean _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; min _: Optional[Union[int, float, bool, str]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing_count _: Optional[int]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing_percentage _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common_not_null_value _: Optional[Union[int, float, bool, str]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common_not_null_value_percentage _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common_value _: Optional[Union[int, float, bool, str]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common_value_percentage _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; new_in_current_values_count _: Optional[int]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ _ = 0_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; percentile_25 _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; percentile_50 _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; percentile_75 _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; std _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unique_count _: Optional[int]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unique_percentage _: Optional[float]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unused_in_current_values_count _: Optional[int]_ _ = None_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; as_dict()

#####&nbsp;&nbsp;&nbsp;&nbsp; is_category()
Checks that the object store stats for a category feature

#####&nbsp;&nbsp;&nbsp;&nbsp; is_datetime()
Checks that the object store stats for a datetime feature

#####&nbsp;&nbsp;&nbsp;&nbsp; is_numeric()
Checks that the object store stats for a numeric feature

### calculate_category_column_correlations(column_name: str, dataset: DataFrame, columns: List[str])
For category columns calculate cramer_v correlation


### calculate_column_distribution(column: Series, column_type: str)

### calculate_correlations(dataset: DataFrame, columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### calculate_cramer_v_correlation(column_name: str, dataset: DataFrame, columns: List[str])

### calculate_data_quality_stats(dataset: DataFrame, columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), task: Optional[str])

### calculate_numerical_column_correlations(column_name: str, dataset: DataFrame, columns: List[str])

### get_features_stats(feature: Series, feature_type: str)

### get_pairwise_correlation(df, func: Callable[[Series, Series], float])
Compute pairwise correlation of columns
:param df: initial data frame.
:param func: function for computing pairwise correlation.


* **Returns**

    Correlation matrix.



### get_rows_count(data: Union[DataFrame, Series])
Count quantity of rows in  a dataset


### _class _ ErrorWithQuantiles(error, quantile_top, quantile_other)
Bases: `object`


#### Attributes: 

#### Methods: 

### _class _ FeatureBias(feature_type: str, majority: float, under: float, over: float, range: float)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; feature_type _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; majority _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; over _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; range _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; under _: float_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; as_dict(prefix)

### _class _ RegressionPerformanceMetrics(mean_error: float, mean_abs_error: float, mean_abs_perc_error: float, error_std: float, abs_error_max: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, error_bias: dict)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; abs_error_max _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; abs_error_std _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; abs_perc_error_std _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; error_bias _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; error_normality _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; error_std _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; mean_error _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; underperformance _: dict_ 

#### Methods: 

### calculate_regression_performance(dataset: DataFrame, columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), error_bias_prefix: str)

### error_bias_table(dataset, err_quantiles, num_feature_names, cat_feature_names)

### error_with_quantiles(dataset, prediction_column, target_column, quantile: float)
## Module contents
