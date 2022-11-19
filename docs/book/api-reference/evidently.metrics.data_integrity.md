# evidently.metrics.data_integrity package

## Submodules

## column_missing_values_metric module


### class ColumnMissingValues(number_of_rows: int, different_missing_values: Dict[Any, int], number_of_different_missing_values: int, number_of_missing_values: int, share_of_missing_values: float)
Bases: `object`

Statistics about missing values in a column

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; different_missing_values : Dict[Any, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_different_missing_values : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_of_missing_values : float 

### class ColumnMissingValuesMetric(column_name: str, missing_values: Optional[list] = None, replace: bool = True)
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

##### &nbsp;&nbsp;&nbsp;&nbsp; DEFAULT_MISSING_VALUES  = ['', inf, -inf, None] 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; missing_values : frozenset 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ColumnMissingValuesMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnMissingValuesMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnMissingValuesMetric)

### class ColumnMissingValuesMetricResult(column_name: str, current: ColumnMissingValues, reference: Optional[ColumnMissingValues] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : ColumnMissingValues 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[ColumnMissingValues]  = None 
## column_regexp_metric module


### class ColumnRegExpMetric(column_name: str, reg_exp: str, top: int = 10)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataIntegrityValueByRegexpMetricResult`]

Count number of values in a column matched or not by a regular expression (regexp)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; reg_exp : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; top : int 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ColumnRegExpMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnRegExpMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnRegExpMetric)

### class DataIntegrityValueByRegexpMetricResult(column_name: str, reg_exp: str, top: int, current: DataIntegrityValueByRegexpStat, reference: Optional[DataIntegrityValueByRegexpStat] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : DataIntegrityValueByRegexpStat 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[DataIntegrityValueByRegexpStat]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; reg_exp : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; top : int 

### class DataIntegrityValueByRegexpStat(number_of_matched: int, number_of_not_matched: int, number_of_rows: int, table_of_matched: Dict[str, int], table_of_not_matched: Dict[str, int])
Bases: `object`

Statistics about matched by a regular expression values in a column for one dataset

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_matched : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_not_matched : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; table_of_matched : Dict[str, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; table_of_not_matched : Dict[str, int] 
## column_summary_metric module


### class CategoricalCharacteristics(number_of_rows: int, count: int, unique: Optional[int], unique_percentage: Optional[float], most_common: Optional[object], most_common_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], new_in_current_values_count: Optional[int] = None, unused_in_current_values_count: Optional[int] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; count : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; missing : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; missing_percentage : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; most_common : Optional[object] 

##### &nbsp;&nbsp;&nbsp;&nbsp; most_common_percentage : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; new_in_current_values_count : Optional[int]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; unique : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; unique_percentage : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; unused_in_current_values_count : Optional[int]  = None 

### class ColumnSummary(column_name: str, column_type: str, reference_characteristics: Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics, NoneType], current_characteristics: Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics], plot_data: DataQualityPlot)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_type : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_characteristics : Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics] 

##### &nbsp;&nbsp;&nbsp;&nbsp; plot_data : DataQualityPlot 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_characteristics : Optional[Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics]] 

### class ColumnSummaryMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnSummary`]

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; static  map_data(stats: [FeatureQualityStats](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats))

### class ColumnSummaryMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnSummaryMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnSummaryMetric)

### class DataByTarget(data_for_plots: Dict[str, Dict[str, Union[list, pandas.core.frame.DataFrame]]], target_name: str, target_type: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; data_for_plots : Dict[str, Dict[str, Union[list, DataFrame]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_type : str 

### class DataInTime(data_for_plots: Dict[str, pandas.core.frame.DataFrame], freq: str, datetime_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; data_for_plots : Dict[str, DataFrame] 

##### &nbsp;&nbsp;&nbsp;&nbsp; datetime_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; freq : str 

### class DataQualityPlot(bins_for_hist: Dict[str, pandas.core.frame.DataFrame], data_in_time: Optional[DataInTime], data_by_target: Optional[DataByTarget], counts_of_values: Optional[Dict[str, pandas.core.frame.DataFrame]])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; bins_for_hist : Dict[str, DataFrame] 

##### &nbsp;&nbsp;&nbsp;&nbsp; counts_of_values : Optional[Dict[str, DataFrame]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; data_by_target : Optional[DataByTarget] 

##### &nbsp;&nbsp;&nbsp;&nbsp; data_in_time : Optional[DataInTime] 

### class DatetimeCharacteristics(number_of_rows: int, count: int, unique: Optional[int], unique_percentage: Optional[float], most_common: Optional[object], most_common_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], first: Optional[str], last: Optional[str])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; count : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; first : Optional[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; last : Optional[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; missing : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; missing_percentage : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; most_common : Optional[object] 

##### &nbsp;&nbsp;&nbsp;&nbsp; most_common_percentage : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; unique : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; unique_percentage : Optional[float] 

### class NumericCharacteristics(number_of_rows: int, count: int, mean: Union[float, int, NoneType], std: Union[float, int, NoneType], min: Union[float, int, NoneType], p25: Union[float, int, NoneType], p50: Union[float, int, NoneType], p75: Union[float, int, NoneType], max: Union[float, int, NoneType], unique: Optional[int], unique_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], infinite_count: Optional[int], infinite_percentage: Optional[float], most_common: Union[float, int, NoneType], most_common_percentage: Optional[float])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; count : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; infinite_count : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; infinite_percentage : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; max : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; min : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; missing : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; missing_percentage : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; most_common : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; most_common_percentage : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; p25 : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; p50 : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; p75 : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; std : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; unique : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; unique_percentage : Optional[float] 
## dataset_missing_values_metric module


### class DatasetMissingValues(different_missing_values: Dict[Any, int], number_of_different_missing_values: int, different_missing_values_by_column: Dict[str, Dict[Any, int]], number_of_different_missing_values_by_column: Dict[str, int], number_of_missing_values: int, share_of_missing_values: float, number_of_missing_values_by_column: Dict[str, int], share_of_missing_values_by_column: Dict[str, float], number_of_rows: int, number_of_rows_with_missing_values: int, share_of_rows_with_missing_values: float, number_of_columns: int, columns_with_missing_values: List[str], number_of_columns_with_missing_values: int, share_of_columns_with_missing_values: float)
Bases: `object`

Statistics about missed values in a dataset

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns_with_missing_values : List[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; different_missing_values : Dict[Any, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; different_missing_values_by_column : Dict[str, Dict[Any, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_columns_with_missing_values : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_different_missing_values : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_different_missing_values_by_column : Dict[str, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values_by_column : Dict[str, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows_with_missing_values : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_of_columns_with_missing_values : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_of_missing_values : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_of_missing_values_by_column : Dict[str, float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_of_rows_with_missing_values : float 

### class DatasetMissingValuesMetric(missing_values: Optional[list] = None, replace: bool = True)
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

##### &nbsp;&nbsp;&nbsp;&nbsp; DEFAULT_MISSING_VALUES  = ['', inf, -inf, None] 

##### &nbsp;&nbsp;&nbsp;&nbsp; missing_values : frozenset 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class DatasetMissingValuesMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DatasetMissingValuesMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DatasetMissingValuesMetric)

### class DatasetMissingValuesMetricResult(current: DatasetMissingValues, reference: Optional[DatasetMissingValues] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : DatasetMissingValues 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[DatasetMissingValues]  = None 
## dataset_summary_metric module


### class DatasetSummary(target: Optional[str], prediction: Optional[Union[str, Sequence[str]]], date_column: Optional[str], id_column: Optional[str], number_of_columns: int, number_of_rows: int, number_of_missing_values: int, number_of_categorical_columns: int, number_of_numeric_columns: int, number_of_datetime_columns: int, number_of_constant_columns: int, number_of_almost_constant_columns: int, number_of_duplicated_columns: int, number_of_almost_duplicated_columns: int, number_of_empty_rows: int, number_of_empty_columns: int, number_of_duplicated_rows: int, columns_type: dict, nans_by_columns: dict, number_uniques_by_columns: dict)
Bases: `object`

Columns information in a dataset

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns_type : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; date_column : Optional[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; id_column : Optional[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; nans_by_columns : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_almost_constant_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_almost_duplicated_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_categorical_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_constant_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_datetime_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_duplicated_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_duplicated_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_empty_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_empty_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_numeric_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_uniques_by_columns : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; prediction : Optional[Union[str, Sequence[str]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; target : Optional[str] 

### class DatasetSummaryMetric(almost_duplicated_threshold: float = 0.95, almost_constant_threshold: float = 0.95)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetSummaryMetricResult`]

Common dataset(s) columns/features characteristics

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; almost_constant_threshold : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; almost_duplicated_threshold : float 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class DatasetSummaryMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DatasetSummaryMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DatasetSummaryMetric)

### class DatasetSummaryMetricResult(almost_duplicated_threshold: float, current: DatasetSummary, reference: Optional[DatasetSummary] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; almost_duplicated_threshold : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : DatasetSummary 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[DatasetSummary]  = None 
## Module contents
