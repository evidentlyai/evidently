# evidently.metrics.data_integrity package

## Submodules

## evidently.metrics.data_integrity.column_missing_values_metric module


### _class_ evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues(number_of_rows: int, different_missing_values: Dict[Any, int], number_of_different_missing_values: int, number_of_missing_values: int, share_of_missing_values: float)
Bases: `object`

Statistics about missing values in a column


#### different_missing_values(_: Dict[Any, int_ )

#### number_of_different_missing_values(_: in_ )

#### number_of_missing_values(_: in_ )

#### number_of_rows(_: in_ )

#### share_of_missing_values(_: floa_ )

### _class_ evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric(column_name: str, missing_values: Optional[list] = None, replace: bool = True)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnMissingValuesMetricResult`]

Count missing values in a column.

Missing value is a null or NaN value.

Calculate an amount of missing values kinds and count for such values.
NA-types like numpy.NaN, pandas.NaT are counted as one type.

You can set you own missing values list with missing_values parameter.
Value None in the list means that Pandas null values will be included in the calculation.

If replace parameter is False - add defaults to user’s list.
If replace parameter is True - use values from missing_values list only.


#### DEFAULT_MISSING_VALUES(_ = ['', inf, -inf, None_ )

#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### missing_values(_: frozense_ )

### _class_ evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnMissingValuesMetric)

#### render_json(obj: ColumnMissingValuesMetric)

### _class_ evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult(column_name: str, current: evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues, reference: Optional[evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: ColumnMissingValue_ )

#### reference(_: Optional[ColumnMissingValues_ _ = Non_ )
## evidently.metrics.data_integrity.column_regexp_metric module


### _class_ evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric(column_name: str, reg_exp: str, top: int = 10)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataIntegrityValueByRegexpMetricResult`]

Count number of values in a column matched or not by a regular expression (regexp)


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### reg_exp(_: st_ )

#### top(_: in_ )

### _class_ evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnRegExpMetric)

#### render_json(obj: ColumnRegExpMetric)

### _class_ evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult(column_name: str, reg_exp: str, top: int, current: evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat, reference: Optional[evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: DataIntegrityValueByRegexpSta_ )

#### reference(_: Optional[DataIntegrityValueByRegexpStat_ _ = Non_ )

#### reg_exp(_: st_ )

#### top(_: in_ )

### _class_ evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat(number_of_matched: int, number_of_not_matched: int, number_of_rows: int, table_of_matched: Dict[str, int], table_of_not_matched: Dict[str, int])
Bases: `object`

Statistics about matched by a regular expression values in a column for one dataset


#### number_of_matched(_: in_ )

#### number_of_not_matched(_: in_ )

#### number_of_rows(_: in_ )

#### table_of_matched(_: Dict[str, int_ )

#### table_of_not_matched(_: Dict[str, int_ )
## evidently.metrics.data_integrity.column_summary_metric module


### _class_ evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics(number_of_rows: int, count: int, unique: Optional[int], unique_percentage: Optional[float], most_common: Optional[object], most_common_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], new_in_current_values_count: Optional[int] = None, unused_in_current_values_count: Optional[int] = None)
Bases: `object`


#### count(_: in_ )

#### missing(_: Optional[int_ )

#### missing_percentage(_: Optional[float_ )

#### most_common(_: Optional[object_ )

#### most_common_percentage(_: Optional[float_ )

#### new_in_current_values_count(_: Optional[int_ _ = Non_ )

#### number_of_rows(_: in_ )

#### unique(_: Optional[int_ )

#### unique_percentage(_: Optional[float_ )

#### unused_in_current_values_count(_: Optional[int_ _ = Non_ )

### _class_ evidently.metrics.data_integrity.column_summary_metric.ColumnSummary(column_name: str, column_type: str, reference_characteristics: Union[evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics, evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics, evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics, NoneType], current_characteristics: Union[evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics, evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics, evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics], plot_data: evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot)
Bases: `object`


#### column_name(_: st_ )

#### column_type(_: st_ )

#### current_characteristics(_: Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics_ )

#### plot_data(_: DataQualityPlo_ )

#### reference_characteristics(_: Optional[Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics]_ )

### _class_ evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnSummary`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### _static_ map_data(stats: [FeatureQualityStats](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats))

### _class_ evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnSummaryMetric)

#### render_json(obj: ColumnSummaryMetric)

### _class_ evidently.metrics.data_integrity.column_summary_metric.DataByTarget(data_for_plots: Dict[str, Dict[str, Union[list, pandas.core.frame.DataFrame]]], target_name: str, target_type: str)
Bases: `object`


#### data_for_plots(_: Dict[str, Dict[str, Union[list, DataFrame]]_ )

#### target_name(_: st_ )

#### target_type(_: st_ )

### _class_ evidently.metrics.data_integrity.column_summary_metric.DataInTime(data_for_plots: Dict[str, pandas.core.frame.DataFrame], freq: str, datetime_name: str)
Bases: `object`


#### data_for_plots(_: Dict[str, DataFrame_ )

#### datetime_name(_: st_ )

#### freq(_: st_ )

### _class_ evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot(bins_for_hist: Dict[str, pandas.core.frame.DataFrame], data_in_time: Optional[evidently.metrics.data_integrity.column_summary_metric.DataInTime], data_by_target: Optional[evidently.metrics.data_integrity.column_summary_metric.DataByTarget], counts_of_values: Optional[Dict[str, pandas.core.frame.DataFrame]])
Bases: `object`


#### bins_for_hist(_: Dict[str, DataFrame_ )

#### counts_of_values(_: Optional[Dict[str, DataFrame]_ )

#### data_by_target(_: Optional[DataByTarget_ )

#### data_in_time(_: Optional[DataInTime_ )

### _class_ evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics(number_of_rows: int, count: int, unique: Optional[int], unique_percentage: Optional[float], most_common: Optional[object], most_common_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], first: Optional[str], last: Optional[str])
Bases: `object`


#### count(_: in_ )

#### first(_: Optional[str_ )

#### last(_: Optional[str_ )

#### missing(_: Optional[int_ )

#### missing_percentage(_: Optional[float_ )

#### most_common(_: Optional[object_ )

#### most_common_percentage(_: Optional[float_ )

#### number_of_rows(_: in_ )

#### unique(_: Optional[int_ )

#### unique_percentage(_: Optional[float_ )

### _class_ evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics(number_of_rows: int, count: int, mean: Union[float, int, NoneType], std: Union[float, int, NoneType], min: Union[float, int, NoneType], p25: Union[float, int, NoneType], p50: Union[float, int, NoneType], p75: Union[float, int, NoneType], max: Union[float, int, NoneType], unique: Optional[int], unique_percentage: Optional[float], missing: Optional[int], missing_percentage: Optional[float], infinite_count: Optional[int], infinite_percentage: Optional[float], most_common: Union[float, int, NoneType], most_common_percentage: Optional[float])
Bases: `object`


#### count(_: in_ )

#### infinite_count(_: Optional[int_ )

#### infinite_percentage(_: Optional[float_ )

#### max(_: Optional[Union[float, int]_ )

#### mean(_: Optional[Union[float, int]_ )

#### min(_: Optional[Union[float, int]_ )

#### missing(_: Optional[int_ )

#### missing_percentage(_: Optional[float_ )

#### most_common(_: Optional[Union[float, int]_ )

#### most_common_percentage(_: Optional[float_ )

#### number_of_rows(_: in_ )

#### p25(_: Optional[Union[float, int]_ )

#### p50(_: Optional[Union[float, int]_ )

#### p75(_: Optional[Union[float, int]_ )

#### std(_: Optional[Union[float, int]_ )

#### unique(_: Optional[int_ )

#### unique_percentage(_: Optional[float_ )
## evidently.metrics.data_integrity.dataset_missing_values_metric module


### _class_ evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues(different_missing_values: Dict[Any, int], number_of_different_missing_values: int, different_missing_values_by_column: Dict[str, Dict[Any, int]], number_of_different_missing_values_by_column: Dict[str, int], number_of_missing_values: int, share_of_missing_values: float, number_of_missing_values_by_column: Dict[str, int], share_of_missing_values_by_column: Dict[str, float], number_of_rows: int, number_of_rows_with_missing_values: int, share_of_rows_with_missing_values: float, number_of_columns: int, columns_with_missing_values: List[str], number_of_columns_with_missing_values: int, share_of_columns_with_missing_values: float)
Bases: `object`

Statistics about missed values in a dataset


#### columns_with_missing_values(_: List[str_ )

#### different_missing_values(_: Dict[Any, int_ )

#### different_missing_values_by_column(_: Dict[str, Dict[Any, int]_ )

#### number_of_columns(_: in_ )

#### number_of_columns_with_missing_values(_: in_ )

#### number_of_different_missing_values(_: in_ )

#### number_of_different_missing_values_by_column(_: Dict[str, int_ )

#### number_of_missing_values(_: in_ )

#### number_of_missing_values_by_column(_: Dict[str, int_ )

#### number_of_rows(_: in_ )

#### number_of_rows_with_missing_values(_: in_ )

#### share_of_columns_with_missing_values(_: floa_ )

#### share_of_missing_values(_: floa_ )

#### share_of_missing_values_by_column(_: Dict[str, float_ )

#### share_of_rows_with_missing_values(_: floa_ )

### _class_ evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric(missing_values: Optional[list] = None, replace: bool = True)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetMissingValuesMetricResult`]

Count missing values in a dataset.

Missing value is a null or NaN value.

Calculate an amount of missing values kinds and count for such values.
NA-types like numpy.NaN, pandas.NaT are counted as one type.

You can set you own missing values list with missing_values parameter.
Value None in the list means that Pandas null values will be included in the calculation.

If replace parameter is False - add defaults to user’s list.
If replace parameter is True - use values from missing_values list only.


#### DEFAULT_MISSING_VALUES(_ = ['', inf, -inf, None_ )

#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### missing_values(_: frozense_ )

### _class_ evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: DatasetMissingValuesMetric)

#### render_json(obj: DatasetMissingValuesMetric)

### _class_ evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult(current: evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues, reference: Optional[evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues] = None)
Bases: `object`


#### current(_: DatasetMissingValue_ )

#### reference(_: Optional[DatasetMissingValues_ _ = Non_ )
## evidently.metrics.data_integrity.dataset_summary_metric module


### _class_ evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary(target: Optional[str], prediction: Optional[Union[str, Sequence[str]]], date_column: Optional[str], id_column: Optional[str], number_of_columns: int, number_of_rows: int, number_of_missing_values: int, number_of_categorical_columns: int, number_of_numeric_columns: int, number_of_datetime_columns: int, number_of_constant_columns: int, number_of_almost_constant_columns: int, number_of_duplicated_columns: int, number_of_almost_duplicated_columns: int, number_of_empty_rows: int, number_of_empty_columns: int, number_of_duplicated_rows: int, columns_type: dict, nans_by_columns: dict, number_uniques_by_columns: dict)
Bases: `object`

Columns information in a dataset


#### columns_type(_: dic_ )

#### date_column(_: Optional[str_ )

#### id_column(_: Optional[str_ )

#### nans_by_columns(_: dic_ )

#### number_of_almost_constant_columns(_: in_ )

#### number_of_almost_duplicated_columns(_: in_ )

#### number_of_categorical_columns(_: in_ )

#### number_of_columns(_: in_ )

#### number_of_constant_columns(_: in_ )

#### number_of_datetime_columns(_: in_ )

#### number_of_duplicated_columns(_: in_ )

#### number_of_duplicated_rows(_: in_ )

#### number_of_empty_columns(_: in_ )

#### number_of_empty_rows(_: in_ )

#### number_of_missing_values(_: in_ )

#### number_of_numeric_columns(_: in_ )

#### number_of_rows(_: in_ )

#### number_uniques_by_columns(_: dic_ )

#### prediction(_: Optional[Union[str, Sequence[str]]_ )

#### target(_: Optional[str_ )

### _class_ evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric(almost_duplicated_threshold: float = 0.95, almost_constant_threshold: float = 0.95)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetSummaryMetricResult`]

Common dataset(s) columns/features characteristics


#### almost_constant_threshold(_: floa_ )

#### almost_duplicated_threshold(_: floa_ )

#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: DatasetSummaryMetric)

#### render_json(obj: DatasetSummaryMetric)

### _class_ evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult(almost_duplicated_threshold: float, current: evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary, reference: Optional[evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary] = None)
Bases: `object`


#### almost_duplicated_threshold(_: floa_ )

#### current(_: DatasetSummar_ )

#### reference(_: Optional[DatasetSummary_ _ = Non_ )
## Module contents
