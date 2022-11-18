# evidently.metrics.data_drift package

## Submodules

## evidently.metrics.data_drift.column_drift_metric module


### _class_ evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric(column_name: str, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnDriftMetricResults`]

Calculate drift metric for a column


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

#### options(_: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions_ )

### _class_ evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnDriftMetric)

#### render_json(obj: ColumnDriftMetric)

### _class_ evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults(column_name: str, column_type: str, stattest_name: str, threshold: Optional[float], drift_score: Union[float, int], drift_detected: bool, current_distribution: [evidently.utils.visualizations.Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference_distribution: [evidently.utils.visualizations.Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), current_scatter: Optional[Dict[str, list]], x_name: Optional[str], plot_shape: Optional[Dict[str, float]])
Bases: `object`


#### column_name(_: st_ )

#### column_type(_: st_ )

#### current_distribution(_: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution_ )

#### current_scatter(_: Optional[Dict[str, list]_ )

#### drift_detected(_: boo_ )

#### drift_score(_: Union[float, int_ )

#### plot_shape(_: Optional[Dict[str, float]_ )

#### reference_distribution(_: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution_ )

#### stattest_name(_: st_ )

#### threshold(_: Optional[float_ )

#### x_name(_: Optional[str_ )
## evidently.metrics.data_drift.column_value_plot module


### _class_ evidently.metrics.data_drift.column_value_plot.ColumnValuePlot(column_name: str)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ColumnValuePlotResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### column_name(_: st_ )

### _class_ evidently.metrics.data_drift.column_value_plot.ColumnValuePlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ColumnValuePlot)

### _class_ evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults(column_name: str, datetime_column_name: Optional[str], current_scatter: pandas.core.frame.DataFrame, reference_scatter: pandas.core.frame.DataFrame)
Bases: `object`


#### column_name(_: st_ )

#### current_scatter(_: DataFram_ )

#### datetime_column_name(_: Optional[str_ )

#### reference_scatter(_: DataFram_ )
## evidently.metrics.data_drift.data_drift_table module


### _class_ evidently.metrics.data_drift.data_drift_table.DataDriftTable(columns: Optional[List[str]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DataDriftTableResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### columns(_: Optional[List[str]_ )

#### get_parameters()

#### options(_: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions_ )

### _class_ evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: DataDriftTable)

#### render_json(obj: DataDriftTable)

### _class_ evidently.metrics.data_drift.data_drift_table.DataDriftTableResults(number_of_columns: int, number_of_drifted_columns: int, share_of_drifted_columns: float, dataset_drift: bool, drift_by_columns: Dict[str, [evidently.calculations.data_drift.ColumnDataDriftMetrics](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics)], dataset_columns: [evidently.utils.data_operations.DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
Bases: `object`


#### dataset_columns(_: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns_ )

#### dataset_drift(_: boo_ )

#### drift_by_columns(_: Dict[str, [ColumnDataDriftMetrics](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics)_ )

#### number_of_columns(_: in_ )

#### number_of_drifted_columns(_: in_ )

#### share_of_drifted_columns(_: floa_ )
## evidently.metrics.data_drift.dataset_drift_metric module


### _class_ evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: DatasetDriftMetric)

#### render_json(obj: DatasetDriftMetric)

### _class_ evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric(columns: Optional[List[str]] = None, threshold: float = 0.5, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`DatasetDriftMetricResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### columns(_: Optional[List[str]_ )

#### get_parameters()

#### options(_: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions_ )

#### threshold(_: floa_ )

### _class_ evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults(threshold: float, number_of_columns: int, number_of_drifted_columns: int, share_of_drifted_columns: float, dataset_drift: bool)
Bases: `object`


#### dataset_drift(_: boo_ )

#### number_of_columns(_: in_ )

#### number_of_drifted_columns(_: in_ )

#### share_of_drifted_columns(_: floa_ )

#### threshold(_: floa_ )
## evidently.metrics.data_drift.target_by_features_table module


### _class_ evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTable(columns: Optional[List[str]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`TargetByFeaturesTableResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### columns(_: Optional[List[str]_ )

### _class_ evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TargetByFeaturesTable)

#### render_json(obj: TargetByFeaturesTable)

### _class_ evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults(current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: pandas.core.frame.DataFrame, target_name: Optional[str], curr_predictions: Optional[[evidently.calculations.classification_performance.PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], ref_predictions: Optional[[evidently.calculations.classification_performance.PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], columns: List[str], task: str)
Bases: `object`


#### columns(_: List[str_ )

#### curr_predictions(_: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)_ )

#### current_plot_data(_: DataFram_ )

#### ref_predictions(_: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)_ )

#### reference_plot_data(_: DataFram_ )

#### target_name(_: Optional[str_ )

#### task(_: st_ )
## Module contents
