# evidently.metrics.data_quality package

## Submodules


### _class_ ColumnCorrelationsMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnCorrelationsMetricResult`]

Calculates correlations between the selected column and all the other columns.
In the current and reference (if presented) datasets

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ColumnCorrelationsMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnCorrelationsMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnCorrelationsMetric)

### _class_ ColumnCorrelationsMetricResult(column_name: str, current: Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)], reference: Optional[Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current _: Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]]_ _ = None_ 

#### Methods: 

### _class_ ColumnDistributionMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnDistributionMetricResult`]

Calculates distribution for the column

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ColumnDistributionMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnDistributionMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnDistributionMetric)

### _class_ ColumnDistributionMetricResult(column_name: str, current: Dict[Any, Union[float, int]], reference: Optional[Dict[Any, Union[float, int]]] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current _: Dict[Any, Union[float, int]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[Dict[Any, Union[float, int]]]_ _ = None_ 

#### Methods: 

### _class_ ColumnQuantileMetric(column_name: str, quantile: float)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnQuantileMetricResult`]

Calculates quantile with specified range

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; quantile _: float_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ColumnQuantileMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnQuantileMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnQuantileMetric)

### _class_ ColumnQuantileMetricResult(column_name: str, quantile: float, current: float, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference: Optional[float] = None, reference_distribution: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_distribution _: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; quantile _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_distribution _: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)]_ _ = None_ 

#### Methods: 

### _class_ ColumnValueListMetric(column_name: str, values: Optional[list] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValueListMetricResult`]

Calculates count and shares of values in the predefined values list

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: Optional[list]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ColumnValueListMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnValueListMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnValueListMetric)

### _class_ ColumnValueListMetricResult(column_name: str, values: List[Any], current: ValueListStat, reference: Optional[ValueListStat] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current _: ValueListStat_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[ValueListStat]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: List[Any]_ 

#### Methods: 

### _class_ ValueListStat(number_in_list: int, number_not_in_list: int, share_in_list: float, share_not_in_list: float, values_in_list: Dict[Any, int], values_not_in_list: Dict[Any, int], rows_count: int)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_in_list _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_not_in_list _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rows_count _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_in_list _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_not_in_list _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values_in_list _: Dict[Any, int]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values_not_in_list _: Dict[Any, int]_ 

#### Methods: 

### _class_ ColumnValueRangeMetric(column_name: str, left: Optional[Union[float, int]] = None, right: Optional[Union[float, int]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValueRangeMetricResult`]

Calculates count and shares of values in the predefined values range

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; left _: Optional[Union[float, int]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; right _: Optional[Union[float, int]]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ColumnValueRangeMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnValueRangeMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnValueRangeMetric)

### _class_ ColumnValueRangeMetricResult(column_name: str, left: Union[float, int], right: Union[float, int], current: ValuesInRangeStat, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference: Optional[ValuesInRangeStat] = None, reference_distribution: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current _: ValuesInRangeStat_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_distribution _: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; left _: Union[float, int]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[ValuesInRangeStat]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_distribution _: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; right _: Union[float, int]_ 

#### Methods: 

### _class_ ValuesInRangeStat(number_in_range: int, number_not_in_range: int, share_in_range: float, share_not_in_range: float, number_of_values: int)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_in_range _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_not_in_range _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_values _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_in_range _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_not_in_range _: float_ 

#### Methods: 

### _class_ CorrelationStats(target_prediction_correlation: Optional[float] = None, abs_max_target_features_correlation: Optional[float] = None, abs_max_prediction_features_correlation: Optional[float] = None, abs_max_correlation: Optional[float] = None, abs_max_features_correlation: Optional[float] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_max_correlation _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_max_features_correlation _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_max_prediction_features_correlation _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_max_target_features_correlation _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_prediction_correlation _: Optional[float]_ _ = None_ 

#### Methods: 

### _class_ DataQualityCorrelationMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DatasetCorrelationsMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DatasetCorrelationsMetric)

### _class_ DatasetCorrelation(correlation: Dict[str, pandas.core.frame.DataFrame], stats: Dict[str, CorrelationStats])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; correlation _: Dict[str, DataFrame]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; stats _: Dict[str, CorrelationStats]_ 

#### Methods: 

### _class_ DatasetCorrelationsMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetCorrelationsMetricResult`]

Calculate different correlations with target, predictions and features


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ DatasetCorrelationsMetricResult(current: DatasetCorrelation, reference: Optional[DatasetCorrelation])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current _: DatasetCorrelation_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[DatasetCorrelation]_ 

#### Methods: 

### _class_ DataQualityStabilityMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataQualityStabilityMetricResult`]

Calculates stability by target and prediction


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ DataQualityStabilityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DataQualityStabilityMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DataQualityStabilityMetric)

### _class_ DataQualityStabilityMetricResult(number_not_stable_target: Optional[int] = None, number_not_stable_prediction: Optional[int] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_not_stable_prediction _: Optional[int]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_not_stable_target _: Optional[int]_ _ = None_ 

#### Methods: 
## Module contents
