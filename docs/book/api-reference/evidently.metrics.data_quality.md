# evidently.metrics.data_quality package

## Submodules

## evidently.metrics.data_quality.column_correlations_metric module


### _class_ evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetric(column_name: str)
Bases: [`Metric`](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnCorrelationsMetricResult`]

Calculates correlations between the selected column and all the other columns.
In the current and reference (if presented) datasets


#### calculate(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

### _class_ evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnCorrelationsMetric)

#### render_json(obj: ColumnCorrelationsMetric)

### _class_ evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult(column_name: str, current: Dict[str, [evidently.calculations.data_quality.ColumnCorrelations](./evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)], reference: Optional[Dict[str, [evidently.calculations.data_quality.ColumnCorrelations](./evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: Dict[str, [ColumnCorrelations](./evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)_ )

#### reference(_: Optional[Dict[str, [ColumnCorrelations](./evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]_ _ = Non_ )
## evidently.metrics.data_quality.column_distribution_metric module


### _class_ evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetric(column_name: str)
Bases: [`Metric`](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnDistributionMetricResult`]

Calculates distribution for the column


#### calculate(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

### _class_ evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnDistributionMetric)

#### render_json(obj: ColumnDistributionMetric)

### _class_ evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult(column_name: str, current: Dict[Any, Union[float, int]], reference: Optional[Dict[Any, Union[float, int]]] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: Dict[Any, Union[float, int]_ )

#### reference(_: Optional[Dict[Any, Union[float, int]]_ _ = Non_ )
## evidently.metrics.data_quality.column_quantile_metric module


### _class_ evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric(column_name: str, quantile: float)
Bases: [`Metric`](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnQuantileMetricResult`]

Calculates quantile with specified range


#### calculate(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### quantile(_: floa_ )

### _class_ evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnQuantileMetric)

#### render_json(obj: ColumnQuantileMetric)

### _class_ evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult(column_name: str, quantile: float, current: float, current_distribution: [evidently.utils.visualizations.Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution), reference: Optional[float] = None, reference_distribution: Optional[[evidently.utils.visualizations.Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution)] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: floa_ )

#### current_distribution(_: [Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution_ )

#### quantile(_: floa_ )

#### reference(_: Optional[float_ _ = Non_ )

#### reference_distribution(_: Optional[[Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution)_ _ = Non_ )
## evidently.metrics.data_quality.column_value_list_metric module


### _class_ evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric(column_name: str, values: Optional[list] = None)
Bases: [`Metric`](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValueListMetricResult`]

Calculates count and shares of values in the predefined values list


#### calculate(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### values(_: Optional[list_ )

### _class_ evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnValueListMetric)

#### render_json(obj: ColumnValueListMetric)

### _class_ evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult(column_name: str, values: List[Any], current: evidently.metrics.data_quality.column_value_list_metric.ValueListStat, reference: Optional[evidently.metrics.data_quality.column_value_list_metric.ValueListStat] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: ValueListSta_ )

#### reference(_: Optional[ValueListStat_ _ = Non_ )

#### values(_: List[Any_ )

### _class_ evidently.metrics.data_quality.column_value_list_metric.ValueListStat(number_in_list: int, number_not_in_list: int, share_in_list: float, share_not_in_list: float, values_in_list: Dict[Any, int], values_not_in_list: Dict[Any, int], rows_count: int)
Bases: `object`


#### number_in_list(_: in_ )

#### number_not_in_list(_: in_ )

#### rows_count(_: in_ )

#### share_in_list(_: floa_ )

#### share_not_in_list(_: floa_ )

#### values_in_list(_: Dict[Any, int_ )

#### values_not_in_list(_: Dict[Any, int_ )
## evidently.metrics.data_quality.column_value_range_metric module


### _class_ evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric(column_name: str, left: Optional[Union[float, int]] = None, right: Optional[Union[float, int]] = None)
Bases: [`Metric`](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValueRangeMetricResult`]

Calculates count and shares of values in the predefined values range


#### calculate(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### left(_: Optional[Union[float, int]_ )

#### right(_: Optional[Union[float, int]_ )

### _class_ evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnValueRangeMetric)

#### render_json(obj: ColumnValueRangeMetric)

### _class_ evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult(column_name: str, left: Union[float, int], right: Union[float, int], current: evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat, current_distribution: [evidently.utils.visualizations.Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution), reference: Optional[evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat] = None, reference_distribution: Optional[[evidently.utils.visualizations.Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution)] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: ValuesInRangeSta_ )

#### current_distribution(_: [Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution_ )

#### left(_: Union[float, int_ )

#### reference(_: Optional[ValuesInRangeStat_ _ = Non_ )

#### reference_distribution(_: Optional[[Distribution](./evidently.utils.md#evidently.utils.visualizations.Distribution)_ _ = Non_ )

#### right(_: Union[float, int_ )

### _class_ evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat(number_in_range: int, number_not_in_range: int, share_in_range: float, share_not_in_range: float, number_of_values: int)
Bases: `object`


#### number_in_range(_: in_ )

#### number_not_in_range(_: in_ )

#### number_of_values(_: in_ )

#### share_in_range(_: floa_ )

#### share_not_in_range(_: floa_ )
## evidently.metrics.data_quality.dataset_correlations_metric module


### _class_ evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats(target_prediction_correlation: Optional[float] = None, abs_max_target_features_correlation: Optional[float] = None, abs_max_prediction_features_correlation: Optional[float] = None, abs_max_correlation: Optional[float] = None, abs_max_features_correlation: Optional[float] = None)
Bases: `object`


#### abs_max_correlation(_: Optional[float_ _ = Non_ )

#### abs_max_features_correlation(_: Optional[float_ _ = Non_ )

#### abs_max_prediction_features_correlation(_: Optional[float_ _ = Non_ )

#### abs_max_target_features_correlation(_: Optional[float_ _ = Non_ )

#### target_prediction_correlation(_: Optional[float_ _ = Non_ )

### _class_ evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: DatasetCorrelationsMetric)

#### render_json(obj: DatasetCorrelationsMetric)

### _class_ evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation(correlation: Dict[str, pandas.core.frame.DataFrame], stats: Dict[str, evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats])
Bases: `object`


#### correlation(_: Dict[str, DataFrame_ )

#### stats(_: Dict[str, CorrelationStats_ )

### _class_ evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric()
Bases: [`Metric`](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetCorrelationsMetricResult`]

Calculate different correlations with target, predictions and features


#### calculate(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetricResult(current: evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation, reference: Optional[evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation])
Bases: `object`


#### current(_: DatasetCorrelatio_ )

#### reference(_: Optional[DatasetCorrelation_ )
## evidently.metrics.data_quality.stability_metric module


### _class_ evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric()
Bases: [`Metric`](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataQualityStabilityMetricResult`]

Calculates stability by target and prediction


#### calculate(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: DataQualityStabilityMetric)

#### render_json(obj: DataQualityStabilityMetric)

### _class_ evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricResult(number_not_stable_target: Optional[int] = None, number_not_stable_prediction: Optional[int] = None)
Bases: `object`


#### number_not_stable_prediction(_: Optional[int_ _ = Non_ )

#### number_not_stable_target(_: Optional[int_ _ = Non_ )
## Module contents
