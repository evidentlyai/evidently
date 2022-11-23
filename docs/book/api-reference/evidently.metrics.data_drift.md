# evidently.metrics.data_drift package

## Submodules

## <a name="module-evidently.metrics.data_drift.column_drift_metric"></a>column_drift_metric module


### class ColumnDriftMetric(column_name: str, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, stattest_threshold: Optional[float] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnDriftMetricResults`]

Calculate drift metric for a column

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; get_parameters()

### class ColumnDriftMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnDriftMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnDriftMetric)

### class ColumnDriftMetricResults(column_name: str, column_type: str, stattest_name: str, stattest_threshold: float, drift_score: Union[float, int], drift_detected: bool, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), current_scatter: Optional[Dict[str, list]], x_name: Optional[str], plot_shape: Optional[Dict[str, float]])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_type : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_distribution : [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution) 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter : Optional[Dict[str, list]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_detected : bool 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_score : Union[float, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; plot_shape : Optional[Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_distribution : [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution) 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; x_name : Optional[str] 
## <a name="module-evidently.metrics.data_drift.column_value_plot"></a>column_value_plot module


### class ColumnValuePlot(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValuePlotResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ColumnValuePlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ColumnValuePlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ColumnValuePlot)

### class ColumnValuePlotResults(column_name: str, datetime_column_name: Optional[str], current_scatter: pandas.core.frame.DataFrame, reference_scatter: pandas.core.frame.DataFrame)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter : DataFrame 

##### &nbsp;&nbsp;&nbsp;&nbsp; datetime_column_name : Optional[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter : DataFrame 
## <a name="module-evidently.metrics.data_drift.data_drift_table"></a>data_drift_table module


### class DataDriftTable(columns: Optional[List[str]] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataDriftTableResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; options : [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; get_parameters()

### class DataDriftTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DataDriftTable)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DataDriftTable)

### class DataDriftTableResults(number_of_columns: int, number_of_drifted_columns: int, share_of_drifted_columns: float, dataset_drift: bool, drift_by_columns: Dict[str, [ColumnDataDriftMetrics](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics)], dataset_columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; dataset_columns : [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dataset_drift : bool 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_by_columns : Dict[str, [ColumnDataDriftMetrics](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics)] 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_drifted_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_of_drifted_columns : float 
## <a name="module-evidently.metrics.data_drift.dataset_drift_metric"></a>dataset_drift_metric module


### class DataDriftMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: DatasetDriftMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: DatasetDriftMetric)

### class DatasetDriftMetric(columns: Optional[List[str]] = None, drift_share: float = 0.5, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetDriftMetricResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_share : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; options : [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; get_parameters()

### class DatasetDriftMetricResults(drift_share: float, number_of_columns: int, number_of_drifted_columns: int, share_of_drifted_columns: float, dataset_drift: bool)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; dataset_drift : bool 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_share : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_drifted_columns : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_of_drifted_columns : float 
## <a name="module-evidently.metrics.data_drift.target_by_features_table"></a>target_by_features_table module


### class TargetByFeaturesTable(columns: Optional[List[str]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`TargetByFeaturesTableResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class TargetByFeaturesTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TargetByFeaturesTable)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TargetByFeaturesTable)

### class TargetByFeaturesTableResults(current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: pandas.core.frame.DataFrame, target_name: Optional[str], curr_predictions: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], ref_predictions: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], columns: List[str], task: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : List[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; curr_predictions : Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)] 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_plot_data : DataFrame 

##### &nbsp;&nbsp;&nbsp;&nbsp; ref_predictions : Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_plot_data : DataFrame 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name : Optional[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; task : str
