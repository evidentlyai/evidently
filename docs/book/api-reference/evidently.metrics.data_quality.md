# evidently.metrics.data_quality package

## Submodules

## <a name="module-evidently.metrics.data_quality.column_correlations_metric"></a>column_correlations_metric module


### class ColumnCorrelationsMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnCorrelationsMetricResult`]

Calculates correlations between the selected column and all the other columns.
In the current and reference (if presented) datasets

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ColumnCorrelationsMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnCorrelationsMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnCorrelationsMetric)

### class ColumnCorrelationsMetricResult(column_name: str, current: Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)], reference: Optional[Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[Dict[str, [ColumnCorrelations](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)]]  = None 
## <a name="module-evidently.metrics.data_quality.column_distribution_metric"></a>column_distribution_metric module


### class ColumnDistributionMetric(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnDistributionMetricResult`]

Calculates distribution for the column

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ColumnDistributionMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnDistributionMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnDistributionMetric)

### class ColumnDistributionMetricResult(column_name: str, current: Dict[Any, Union[float, int]], reference: Optional[Dict[Any, Union[float, int]]] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : Dict[Any, Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[Dict[Any, Union[float, int]]]  = None 
## <a name="module-evidently.metrics.data_quality.column_quantile_metric"></a>column_quantile_metric module


### class ColumnQuantileMetric(column_name: str, quantile: float)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnQuantileMetricResult`]

Calculates quantile with specified range

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; quantile : float 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ColumnQuantileMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnQuantileMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnQuantileMetric)

### class ColumnQuantileMetricResult(column_name: str, quantile: float, current: float, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference: Optional[float] = None, reference_distribution: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_distribution : [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution) 

##### &nbsp;&nbsp;&nbsp;&nbsp; quantile : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_distribution : Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)]  = None 
## <a name="module-evidently.metrics.data_quality.column_value_list_metric"></a>column_value_list_metric module


### class ColumnValueListMetric(column_name: str, values: Optional[list] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValueListMetricResult`]

Calculates count and shares of values in the predefined values list

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; values : Optional[list] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ColumnValueListMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnValueListMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnValueListMetric)

### class ColumnValueListMetricResult(column_name: str, values: List[Any], current: ValueListStat, reference: Optional[ValueListStat] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : ValueListStat 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[ValueListStat]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; values : List[Any] 

### class ValueListStat(number_in_list: int, number_not_in_list: int, share_in_list: float, share_not_in_list: float, values_in_list: Dict[Any, int], values_not_in_list: Dict[Any, int], rows_count: int)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_in_list : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_not_in_list : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; rows_count : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_in_list : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_not_in_list : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; values_in_list : Dict[Any, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; values_not_in_list : Dict[Any, int] 
## <a name="module-evidently.metrics.data_quality.column_value_range_metric"></a>column_value_range_metric module


### class ColumnValueRangeMetric(column_name: str, left: Optional[Union[float, int]] = None, right: Optional[Union[float, int]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValueRangeMetricResult`]

Calculates count and shares of values in the predefined values range

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; left : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; right : Optional[Union[float, int]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ColumnValueRangeMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnValueRangeMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnValueRangeMetric)

### class ColumnValueRangeMetricResult(column_name: str, left: Union[float, int], right: Union[float, int], current: ValuesInRangeStat, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference: Optional[ValuesInRangeStat] = None, reference_distribution: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : ValuesInRangeStat 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_distribution : [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution) 

##### &nbsp;&nbsp;&nbsp;&nbsp; left : Union[float, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[ValuesInRangeStat]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_distribution : Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; right : Union[float, int] 

### class ValuesInRangeStat(number_in_range: int, number_not_in_range: int, share_in_range: float, share_not_in_range: float, number_of_values: int)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_in_range : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_not_in_range : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_values : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_in_range : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_not_in_range : float 
## <a name="module-evidently.metrics.data_quality.dataset_correlations_metric"></a>dataset_correlations_metric module


### class CorrelationStats(target_prediction_correlation: Optional[float] = None, abs_max_target_features_correlation: Optional[float] = None, abs_max_prediction_features_correlation: Optional[float] = None, abs_max_correlation: Optional[float] = None, abs_max_features_correlation: Optional[float] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_max_correlation : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_max_features_correlation : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_max_prediction_features_correlation : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_max_target_features_correlation : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_prediction_correlation : Optional[float]  = None 

### class DataQualityCorrelationMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DatasetCorrelationsMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DatasetCorrelationsMetric)

### class DatasetCorrelation(correlation: Dict[str, pandas.core.frame.DataFrame], stats: Dict[str, CorrelationStats])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; correlation : Dict[str, DataFrame] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stats : Dict[str, CorrelationStats] 

### class DatasetCorrelationsMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetCorrelationsMetricResult`]

Calculate different correlations with target, predictions and features


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class DatasetCorrelationsMetricResult(current: DatasetCorrelation, reference: Optional[DatasetCorrelation])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : DatasetCorrelation 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[DatasetCorrelation] 
## <a name="module-evidently.metrics.data_quality.stability_metric"></a>stability_metric module


### class DataQualityStabilityMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataQualityStabilityMetricResult`]

Calculates stability by target and prediction


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class DataQualityStabilityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DataQualityStabilityMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DataQualityStabilityMetric)

### class DataQualityStabilityMetricResult(number_not_stable_target: Optional[int] = None, number_not_stable_prediction: Optional[int] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_not_stable_prediction : Optional[int]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_not_stable_target : Optional[int]  = None 
## Module contents
