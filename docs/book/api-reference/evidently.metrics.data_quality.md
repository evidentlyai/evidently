# evidently.metrics.data_quality package

## Submodules


### _class_ ColumnCorrelationsMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnCorrelationsMetricResult`]

Calculates correlations between the selected column and all the other columns.
In the current and reference (if presented) datasets


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

### _class_ ColumnCorrelationsMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnCorrelationsMetric)

#### render_json(obj: ColumnCorrelationsMetric)

### _class_ ColumnCorrelationsMetricResult(column_name: str, current: Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)], reference: Optional[Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)_ )

#### reference(_: Optional[Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]_ _ = Non_ )

### _class_ ColumnDistributionMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnDistributionMetricResult`]

Calculates distribution for the column


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

### _class_ ColumnDistributionMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnDistributionMetric)

#### render_json(obj: ColumnDistributionMetric)

### _class_ ColumnDistributionMetricResult(column_name: str, current: Dict[Any, Union[float, int]], reference: Optional[Dict[Any, Union[float, int]]] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: Dict[Any, Union[float, int]_ )

#### reference(_: Optional[Dict[Any, Union[float, int]]_ _ = Non_ )

### _class_ ColumnQuantileMetric(column_name: str, quantile: float)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnQuantileMetricResult`]

Calculates quantile with specified range


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### quantile(_: floa_ )

### _class_ ColumnQuantileMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnQuantileMetric)

#### render_json(obj: ColumnQuantileMetric)

### _class_ ColumnQuantileMetricResult(column_name: str, quantile: float, current: float, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference: Optional[float] = None, reference_distribution: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: floa_ )

#### current_distribution(_: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution_ )

#### quantile(_: floa_ )

#### reference(_: Optional[float_ _ = Non_ )

#### reference_distribution(_: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ _ = Non_ )

### _class_ ColumnValueListMetric(column_name: str, values: Optional[list] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValueListMetricResult`]

Calculates count and shares of values in the predefined values list


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### values(_: Optional[list_ )

### _class_ ColumnValueListMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnValueListMetric)

#### render_json(obj: ColumnValueListMetric)

### _class_ ColumnValueListMetricResult(column_name: str, values: List[Any], current: ValueListStat, reference: Optional[ValueListStat] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: ValueListSta_ )

#### reference(_: Optional[ValueListStat_ _ = Non_ )

#### values(_: List[Any_ )

### _class_ ValueListStat(number_in_list: int, number_not_in_list: int, share_in_list: float, share_not_in_list: float, values_in_list: Dict[Any, int], values_not_in_list: Dict[Any, int], rows_count: int)
Bases: `object`


#### number_in_list(_: in_ )

#### number_not_in_list(_: in_ )

#### rows_count(_: in_ )

#### share_in_list(_: floa_ )

#### share_not_in_list(_: floa_ )

#### values_in_list(_: Dict[Any, int_ )

#### values_not_in_list(_: Dict[Any, int_ )

### _class_ ColumnValueRangeMetric(column_name: str, left: Optional[Union[float, int]] = None, right: Optional[Union[float, int]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValueRangeMetricResult`]

Calculates count and shares of values in the predefined values range


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### left(_: Optional[Union[float, int]_ )

#### right(_: Optional[Union[float, int]_ )

### _class_ ColumnValueRangeMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnValueRangeMetric)

#### render_json(obj: ColumnValueRangeMetric)

### _class_ ColumnValueRangeMetricResult(column_name: str, left: Union[float, int], right: Union[float, int], current: ValuesInRangeStat, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference: Optional[ValuesInRangeStat] = None, reference_distribution: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)] = None)
Bases: `object`


#### column_name(_: st_ )

#### current(_: ValuesInRangeSta_ )

#### current_distribution(_: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution_ )

#### left(_: Union[float, int_ )

#### reference(_: Optional[ValuesInRangeStat_ _ = Non_ )

#### reference_distribution(_: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ _ = Non_ )

#### right(_: Union[float, int_ )

### _class_ ValuesInRangeStat(number_in_range: int, number_not_in_range: int, share_in_range: float, share_not_in_range: float, number_of_values: int)
Bases: `object`


#### number_in_range(_: in_ )

#### number_not_in_range(_: in_ )

#### number_of_values(_: in_ )

#### share_in_range(_: floa_ )

#### share_not_in_range(_: floa_ )

### _class_ CorrelationStats(target_prediction_correlation: Optional[float] = None, abs_max_target_features_correlation: Optional[float] = None, abs_max_prediction_features_correlation: Optional[float] = None, abs_max_correlation: Optional[float] = None, abs_max_features_correlation: Optional[float] = None)
Bases: `object`


#### abs_max_correlation(_: Optional[float_ _ = Non_ )

#### abs_max_features_correlation(_: Optional[float_ _ = Non_ )

#### abs_max_prediction_features_correlation(_: Optional[float_ _ = Non_ )

#### abs_max_target_features_correlation(_: Optional[float_ _ = Non_ )

#### target_prediction_correlation(_: Optional[float_ _ = Non_ )

### _class_ DataQualityCorrelationMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: DatasetCorrelationsMetric)

#### render_json(obj: DatasetCorrelationsMetric)

### _class_ DatasetCorrelation(correlation: Dict[str, pandas.core.frame.DataFrame], stats: Dict[str, CorrelationStats])
Bases: `object`


#### correlation(_: Dict[str, DataFrame_ )

#### stats(_: Dict[str, CorrelationStats_ )

### _class_ DatasetCorrelationsMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetCorrelationsMetricResult`]

Calculate different correlations with target, predictions and features


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ DatasetCorrelationsMetricResult(current: DatasetCorrelation, reference: Optional[DatasetCorrelation])
Bases: `object`


#### current(_: DatasetCorrelatio_ )

#### reference(_: Optional[DatasetCorrelation_ )

### _class_ DataQualityStabilityMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataQualityStabilityMetricResult`]

Calculates stability by target and prediction


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ DataQualityStabilityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: DataQualityStabilityMetric)

#### render_json(obj: DataQualityStabilityMetric)

### _class_ DataQualityStabilityMetricResult(number_not_stable_target: Optional[int] = None, number_not_stable_prediction: Optional[int] = None)
Bases: `object`


#### number_not_stable_prediction(_: Optional[int_ _ = Non_ )

#### number_not_stable_target(_: Optional[int_ _ = Non_ )
## Module contents
