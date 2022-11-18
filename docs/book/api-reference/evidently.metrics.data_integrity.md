# evidently.metrics.data_integrity package

## Submodules


### _class _ ColumnMissingValues(number_of_rows: int, different_missing_values: Dict[Any, int], number_of_different_missing_values: int, number_of_missing_values: int, share_of_missing_values: float)
Bases: `object`

Statistics about missing values in a column


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; labels _: Sequence[Union[str, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; values _: list_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; exception _: BaseException_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; different_missing_values _: Dict[Any, int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_different_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; share_of_missing_values _: float_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

#####&nbsp;&nbsp;&nbsp;&nbsp; get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ColumnMissingValuesMetric(column_name: str, missing_values: Optional[list] = None, replace: bool = True)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnMissingValuesMetricResult`]

Count missing values in a column.

Missing value is a null or NaN value.

Calculate an amount of missing values kinds and count for such values.
NA-types like numpy.NaN, pandas.NaT are counted as one type.

You can set you own missing values list with missing_values parameter.
Value None in the list means that Pandas null values will be included in the calculation.

If replace parameter is False - add defaults to user’s list.
If replace parameter is True - use values from missing_values list only.


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; DEFAULT_MISSING_VALUES _ = ['', inf, -inf, None]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing_values _: frozenset_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ColumnMissingValuesMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnMissingValuesMetric)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnMissingValuesMetric)

### _class _ ColumnMissingValuesMetricResult(column_name: str, current: ColumnMissingValues, reference: Optional[ColumnMissingValues] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current _: ColumnMissingValues_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[ColumnMissingValues]_ _ = None_ 

#### Methods: 

### _class _ ColumnRegExpMetric(column_name: str, reg_exp: str, top: int = 10)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataIntegrityValueByRegexpMetricResult`]

Count number of values in a column matched or not by a regular expression (regexp)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reg_exp _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; top _: int_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ColumnRegExpMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnRegExpMetric)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnRegExpMetric)

### _class _ DataIntegrityValueByRegexpMetricResult(column_name: str, reg_exp: str, top: int, current: DataIntegrityValueByRegexpStat, reference: Optional[DataIntegrityValueByRegexpStat] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current _: DataIntegrityValueByRegexpStat_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[DataIntegrityValueByRegexpStat]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reg_exp _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; top _: int_ 

#### Methods: 

### _class _ DataIntegrityValueByRegexpStat(number_of_matched: int, number_of_not_matched: int, number_of_rows: int, table_of_matched: Dict[str, int], table_of_not_matched: Dict[str, int])
Bases: `object`

Statistics about matched by a regular expression values in a column for one dataset


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_matched _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_not_matched _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; table_of_matched _: Dict[str, int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; table_of_not_matched _: Dict[str, int]_ 

#### Methods: 

### _class _ CategoricalCharacteristics(number_of_rows: int, count: int, unique: Optional[int], unique_percentage: Optional[float], most_common: Optional[object], most_common_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], new_in_current_values_count: Optional[int] = None, unused_in_current_values_count: Optional[int] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; count _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing _: Optional[int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing_percentage _: Optional[float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common _: Optional[object]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common_percentage _: Optional[float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; new_in_current_values_count _: Optional[int]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unique _: Optional[int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unique_percentage _: Optional[float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unused_in_current_values_count _: Optional[int]_ _ = None_ 

#### Methods: 

### _class _ ColumnSummary(column_name: str, column_type: str, reference_characteristics: Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics, NoneType], current_characteristics: Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics], plot_data: DataQualityPlot)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_type _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_characteristics _: Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; plot_data _: DataQualityPlot_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_characteristics _: Optional[Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics]]_ 

#### Methods: 

### _class _ ColumnSummaryMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnSummary`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; _static _ map_data(stats: [FeatureQualityStats](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats))

### _class _ ColumnSummaryMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnSummaryMetric)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnSummaryMetric)

### _class _ DataByTarget(data_for_plots: Dict[str, Dict[str, Union[list, pandas.core.frame.DataFrame]]], target_name: str, target_type: str)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; data_for_plots _: Dict[str, Dict[str, Union[list, DataFrame]]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target_type _: str_ 

#### Methods: 

### _class _ DataInTime(data_for_plots: Dict[str, pandas.core.frame.DataFrame], freq: str, datetime_name: str)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; data_for_plots _: Dict[str, DataFrame]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; datetime_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; freq _: str_ 

#### Methods: 

### _class _ DataQualityPlot(bins_for_hist: Dict[str, pandas.core.frame.DataFrame], data_in_time: Optional[DataInTime], data_by_target: Optional[DataByTarget], counts_of_values: Optional[Dict[str, pandas.core.frame.DataFrame]])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; bins_for_hist _: Dict[str, DataFrame]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; counts_of_values _: Optional[Dict[str, DataFrame]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; data_by_target _: Optional[DataByTarget]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; data_in_time _: Optional[DataInTime]_ 

#### Methods: 

### _class _ DatetimeCharacteristics(number_of_rows: int, count: int, unique: Optional[int], unique_percentage: Optional[float], most_common: Optional[object], most_common_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], first: Optional[str], last: Optional[str])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; count _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; first _: Optional[str]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; last _: Optional[str]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing _: Optional[int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing_percentage _: Optional[float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common _: Optional[object]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common_percentage _: Optional[float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unique _: Optional[int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unique_percentage _: Optional[float]_ 

#### Methods: 

### _class _ NumericCharacteristics(number_of_rows: int, count: int, mean: Union[float, int, NoneType], std: Union[float, int, NoneType], min: Union[float, int, NoneType], p25: Union[float, int, NoneType], p50: Union[float, int, NoneType], p75: Union[float, int, NoneType], max: Union[float, int, NoneType], unique: Optional[int], unique_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], infinite_count: Optional[int], infinite_percentage: Optional[float], most_common: Union[float, int, NoneType], most_common_percentage: Optional[float])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; count _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; infinite_count _: Optional[int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; infinite_percentage _: Optional[float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; max _: Optional[Union[float, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; mean _: Optional[Union[float, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; min _: Optional[Union[float, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing _: Optional[int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing_percentage _: Optional[float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common _: Optional[Union[float, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; most_common_percentage _: Optional[float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; p25 _: Optional[Union[float, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; p50 _: Optional[Union[float, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; p75 _: Optional[Union[float, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; std _: Optional[Union[float, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unique _: Optional[int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; unique_percentage _: Optional[float]_ 

#### Methods: 

### _class _ DatasetMissingValues(different_missing_values: Dict[Any, int], number_of_different_missing_values: int, different_missing_values_by_column: Dict[str, Dict[Any, int]], number_of_different_missing_values_by_column: Dict[str, int], number_of_missing_values: int, share_of_missing_values: float, number_of_missing_values_by_column: Dict[str, int], share_of_missing_values_by_column: Dict[str, float], number_of_rows: int, number_of_rows_with_missing_values: int, share_of_rows_with_missing_values: float, number_of_columns: int, columns_with_missing_values: List[str], number_of_columns_with_missing_values: int, share_of_columns_with_missing_values: float)
Bases: `object`

Statistics about missed values in a dataset


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; columns_with_missing_values _: List[str]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; different_missing_values _: Dict[Any, int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; different_missing_values_by_column _: Dict[str, Dict[Any, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_columns_with_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_different_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_different_missing_values_by_column _: Dict[str, int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values_by_column _: Dict[str, int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows_with_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; share_of_columns_with_missing_values _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; share_of_missing_values _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; share_of_missing_values_by_column _: Dict[str, float]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; share_of_rows_with_missing_values _: float_ 

#### Methods: 

### _class _ DatasetMissingValuesMetric(missing_values: Optional[list] = None, replace: bool = True)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetMissingValuesMetricResult`]

Count missing values in a dataset.

Missing value is a null or NaN value.

Calculate an amount of missing values kinds and count for such values.
NA-types like numpy.NaN, pandas.NaT are counted as one type.

You can set you own missing values list with missing_values parameter.
Value None in the list means that Pandas null values will be included in the calculation.

If replace parameter is False - add defaults to user’s list.
If replace parameter is True - use values from missing_values list only.


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; DEFAULT_MISSING_VALUES _ = ['', inf, -inf, None]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; missing_values _: frozenset_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ DatasetMissingValuesMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DatasetMissingValuesMetric)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DatasetMissingValuesMetric)

### _class _ DatasetMissingValuesMetricResult(current: DatasetMissingValues, reference: Optional[DatasetMissingValues] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; current _: DatasetMissingValues_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[DatasetMissingValues]_ _ = None_ 

#### Methods: 

### _class _ DatasetSummary(target: Optional[str], prediction: Optional[Union[str, Sequence[str]]], date_column: Optional[str], id_column: Optional[str], number_of_columns: int, number_of_rows: int, number_of_missing_values: int, number_of_categorical_columns: int, number_of_numeric_columns: int, number_of_datetime_columns: int, number_of_constant_columns: int, number_of_almost_constant_columns: int, number_of_duplicated_columns: int, number_of_almost_duplicated_columns: int, number_of_empty_rows: int, number_of_empty_columns: int, number_of_duplicated_rows: int, columns_type: dict, nans_by_columns: dict, number_uniques_by_columns: dict)
Bases: `object`

Columns information in a dataset


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; columns_type _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; date_column _: Optional[str]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; id_column _: Optional[str]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; nans_by_columns _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_almost_constant_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_almost_duplicated_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_categorical_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_constant_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_datetime_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_duplicated_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_duplicated_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_empty_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_empty_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_numeric_columns _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_uniques_by_columns _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; prediction _: Optional[Union[str, Sequence[str]]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target _: Optional[str]_ 

#### Methods: 

### _class _ DatasetSummaryMetric(almost_duplicated_threshold: float = 0.95, almost_constant_threshold: float = 0.95)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetSummaryMetricResult`]

Common dataset(s) columns/features characteristics


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; almost_constant_threshold _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; almost_duplicated_threshold _: float_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ DatasetSummaryMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DatasetSummaryMetric)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DatasetSummaryMetric)

### _class _ DatasetSummaryMetricResult(almost_duplicated_threshold: float, current: DatasetSummary, reference: Optional[DatasetSummary] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; almost_duplicated_threshold _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current _: DatasetSummary_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[DatasetSummary]_ _ = None_ 

#### Methods: 
## Module contents
