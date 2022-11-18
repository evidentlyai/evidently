# evidently.metrics.data_drift package

## Submodules


### _class _ ColumnDriftMetric(column_name: str, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnDriftMetricResults`]

Calculate drift metric for a column


#### Attributes: 

##### labels _: Sequence[Union[str, int]]_ 

##### values _: list_ 

##### exception _: BaseException_ 

##### column_name _: str_ 

##### options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

#### Methods: 

##### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

##### get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ColumnDriftMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: ColumnDriftMetric)

##### render_json(obj: ColumnDriftMetric)

### _class _ ColumnDriftMetricResults(column_name: str, column_type: str, stattest_name: str, threshold: Optional[float], drift_score: Union[float, int], drift_detected: bool, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), current_scatter: Optional[Dict[str, list]], x_name: Optional[str], plot_shape: Optional[Dict[str, float]])
Bases: `object`


#### Attributes: 

##### column_name _: str_ 

##### column_type _: str_ 

##### current_distribution _: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ 

##### current_scatter _: Optional[Dict[str, list]]_ 

##### drift_detected _: bool_ 

##### drift_score _: Union[float, int]_ 

##### plot_shape _: Optional[Dict[str, float]]_ 

##### reference_distribution _: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)_ 

##### stattest_name _: str_ 

##### threshold _: Optional[float]_ 

##### x_name _: Optional[str]_ 

#### Methods: 

### _class _ ColumnValuePlot(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValuePlotResults`]


#### Attributes: 

##### column_name _: str_ 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ColumnValuePlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: ColumnValuePlot)

### _class _ ColumnValuePlotResults(column_name: str, datetime_column_name: Optional[str], current_scatter: pandas.core.frame.DataFrame, reference_scatter: pandas.core.frame.DataFrame)
Bases: `object`


#### Attributes: 

##### column_name _: str_ 

##### current_scatter _: DataFrame_ 

##### datetime_column_name _: Optional[str]_ 

##### reference_scatter _: DataFrame_ 

#### Methods: 

### _class _ DataDriftTable(columns: Optional[List[str]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataDriftTableResults`]


#### Attributes: 

##### columns _: Optional[List[str]]_ 

##### options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### get_parameters()

### _class _ DataDriftTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: DataDriftTable)

##### render_json(obj: DataDriftTable)

### _class _ DataDriftTableResults(number_of_columns: int, number_of_drifted_columns: int, share_of_drifted_columns: float, dataset_drift: bool, drift_by_columns: Dict[str, [ColumnDataDriftMetrics](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics)], dataset_columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
Bases: `object`


#### Attributes: 

##### dataset_columns _: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)_ 

##### dataset_drift _: bool_ 

##### drift_by_columns _: Dict[str, [ColumnDataDriftMetrics](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics)]_ 

##### number_of_columns _: int_ 

##### number_of_drifted_columns _: int_ 

##### share_of_drifted_columns _: float_ 

#### Methods: 

### _class _ DataDriftMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: DatasetDriftMetric)

##### render_json(obj: DatasetDriftMetric)

### _class _ DatasetDriftMetric(columns: Optional[List[str]] = None, threshold: float = 0.5, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetDriftMetricResults`]


#### Attributes: 

##### columns _: Optional[List[str]]_ 

##### options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

##### threshold _: float_ 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### get_parameters()

### _class _ DatasetDriftMetricResults(threshold: float, number_of_columns: int, number_of_drifted_columns: int, share_of_drifted_columns: float, dataset_drift: bool)
Bases: `object`


#### Attributes: 

##### dataset_drift _: bool_ 

##### number_of_columns _: int_ 

##### number_of_drifted_columns _: int_ 

##### share_of_drifted_columns _: float_ 

##### threshold _: float_ 

#### Methods: 

### _class _ TargetByFeaturesTable(columns: Optional[List[str]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`TargetByFeaturesTableResults`]


#### Attributes: 

##### columns _: Optional[List[str]]_ 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ TargetByFeaturesTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TargetByFeaturesTable)

##### render_json(obj: TargetByFeaturesTable)

### _class _ TargetByFeaturesTableResults(current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: pandas.core.frame.DataFrame, target_name: Optional[str], curr_predictions: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], ref_predictions: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], columns: List[str], task: str)
Bases: `object`


#### Attributes: 

##### columns _: List[str]_ 

##### curr_predictions _: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)]_ 

##### current_plot_data _: DataFrame_ 

##### ref_predictions _: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)]_ 

##### reference_plot_data _: DataFrame_ 

##### target_name _: Optional[str]_ 

##### task _: str_ 

#### Methods: 
## Module contents
