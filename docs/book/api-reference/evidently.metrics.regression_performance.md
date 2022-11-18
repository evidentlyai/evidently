# evidently.metrics.regression_performance package

## Submodules


### _class _ RegressionAbsPercentageErrorPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionAbsPercentageErrorPlotResults`]


#### Attributes: 

##### labels _: Sequence[Union[str, int]]_ 

##### values _: list_ 

##### exception _: BaseException_ 

##### column_name _: str_ 

##### options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

##### different_missing_values _: Dict[Any, int]_ 

##### number_of_different_missing_values _: int_ 

##### number_of_missing_values _: int_ 

##### number_of_rows _: int_ 

##### share_of_missing_values _: float_ 

##### column_name _: str_ 

#### Methods: 

##### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

##### get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionAbsPercentageErrorPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionAbsPercentageErrorPlot)

##### render_json(obj: RegressionAbsPercentageErrorPlot)

### _class _ RegressionAbsPercentageErrorPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`


#### Attributes: 

##### current_scatter _: Dict[str, Series]_ 

##### reference_scatter _: Optional[Dict[str, Series]]_ 

##### x_name _: str_ 

#### Methods: 

### _class _ RegressionErrorBiasTable(columns: Optional[List[str]] = None, top_error: Optional[float] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorBiasTableResults`]


#### Attributes: 

##### TOP_ERROR_DEFAULT _ = 0.05_ 

##### TOP_ERROR_MAX _ = 0.5_ 

##### TOP_ERROR_MIN _ = 0_ 

##### columns _: Optional[List[str]]_ 

##### top_error _: float_ 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionErrorBiasTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionErrorBiasTable)

##### render_json(obj: RegressionErrorBiasTable)

### _class _ RegressionErrorBiasTableResults(top_error: float, current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, prediction_name: str, num_feature_names: List[str], cat_feature_names: List[str], error_bias: Optional[dict] = None, columns: Optional[List[str]] = None)
Bases: `object`


#### Attributes: 

##### cat_feature_names _: List[str]_ 

##### columns _: Optional[List[str]]_ _ = None_ 

##### current_plot_data _: DataFrame_ 

##### error_bias _: Optional[dict]_ _ = None_ 

##### num_feature_names _: List[str]_ 

##### prediction_name _: str_ 

##### reference_plot_data _: Optional[DataFrame]_ 

##### target_name _: str_ 

##### top_error _: float_ 

#### Methods: 

### _class _ RegressionErrorDistribution()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorDistributionResults`]


#### Attributes: 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionErrorDistributionRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionErrorDistribution)

##### render_json(obj: RegressionErrorDistribution)

### _class _ RegressionErrorDistributionResults(current_bins: pandas.core.frame.DataFrame, reference_bins: Optional[pandas.core.frame.DataFrame])
Bases: `object`


#### Attributes: 

##### current_bins _: DataFrame_ 

##### reference_bins _: Optional[DataFrame]_ 

#### Methods: 

### _class _ RegressionErrorPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorPlotResults`]


#### Attributes: 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionErrorPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionErrorPlot)

##### render_json(obj: RegressionErrorPlot)

### _class _ RegressionErrorPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`


#### Attributes: 

##### current_scatter _: Dict[str, Series]_ 

##### reference_scatter _: Optional[Dict[str, Series]]_ 

##### x_name _: str_ 

#### Methods: 

### _class _ RegressionErrorNormality()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorNormalityResults`]


#### Attributes: 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionErrorNormalityRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionErrorNormality)

##### render_json(obj: RegressionErrorNormality)

### _class _ RegressionErrorNormalityResults(current_error: pandas.core.series.Series, reference_error: Optional[pandas.core.series.Series])
Bases: `object`


#### Attributes: 

##### current_error _: Series_ 

##### reference_error _: Optional[Series]_ 

#### Methods: 

### _class _ RegressionPredictedVsActualPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPredictedVsActualPlotResults`]


#### Attributes: 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionPredictedVsActualPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionPredictedVsActualPlot)

##### render_json(obj: RegressionPredictedVsActualPlot)

### _class _ RegressionPredictedVsActualPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`


#### Attributes: 

##### current_scatter _: Dict[str, Series]_ 

##### reference_scatter _: Optional[Dict[str, Series]]_ 

##### x_name _: str_ 

#### Methods: 

### _class _ RegressionPredictedVsActualScatter()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPredictedVsActualScatterResults`]


#### Attributes: 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionPredictedVsActualScatterRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionPredictedVsActualScatter)

##### render_json(obj: RegressionPredictedVsActualScatter)

### _class _ RegressionPredictedVsActualScatterResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]])
Bases: `object`


#### Attributes: 

##### current_scatter _: Dict[str, Series]_ 

##### reference_scatter _: Optional[Dict[str, Series]]_ 

#### Methods: 

### _class _ RegressionDummyMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionDummyMetricResults`]


#### Attributes: 

##### quality_metric _: RegressionQualityMetric_ 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionDummyMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionDummyMetric)

##### render_json(obj: RegressionDummyMetric)

### _class _ RegressionDummyMetricResults(rmse_default: float, mean_abs_error_default: float, mean_abs_perc_error_default: float, abs_error_max_default: float, mean_abs_error_by_ref: Optional[float] = None, mean_abs_error: Optional[float] = None, mean_abs_perc_error_by_ref: Optional[float] = None, mean_abs_perc_error: Optional[float] = None, rmse_by_ref: Optional[float] = None, rmse: Optional[float] = None, abs_error_max_by_ref: Optional[float] = None, abs_error_max: Optional[float] = None)
Bases: `object`


#### Attributes: 

##### abs_error_max _: Optional[float]_ _ = None_ 

##### abs_error_max_by_ref _: Optional[float]_ _ = None_ 

##### abs_error_max_default _: float_ 

##### mean_abs_error _: Optional[float]_ _ = None_ 

##### mean_abs_error_by_ref _: Optional[float]_ _ = None_ 

##### mean_abs_error_default _: float_ 

##### mean_abs_perc_error _: Optional[float]_ _ = None_ 

##### mean_abs_perc_error_by_ref _: Optional[float]_ _ = None_ 

##### mean_abs_perc_error_default _: float_ 

##### rmse _: Optional[float]_ _ = None_ 

##### rmse_by_ref _: Optional[float]_ _ = None_ 

##### rmse_default _: float_ 

#### Methods: 

### _class _ RegressionPerformanceMetrics()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPerformanceMetricsResults`]


#### Attributes: 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### get_parameters()

### _class _ RegressionPerformanceMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionPerformanceMetrics)

##### render_json(obj: RegressionPerformanceMetrics)

### _class _ RegressionPerformanceMetricsResults(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), r2_score: float, rmse: float, rmse_default: float, mean_error: float, me_default_sigma: float, me_hist_for_plot: Dict[str, Union[pandas.core.series.Series, pandas.core.frame.DataFrame]], mean_abs_error: float, mean_abs_error_default: float, mean_abs_perc_error: float, mean_abs_perc_error_default: float, abs_error_max: float, abs_error_max_default: float, error_std: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, hist_for_plot: Dict[str, pandas.core.series.Series], vals_for_plots: Dict[str, Dict[str, pandas.core.series.Series]], error_bias: Optional[dict] = None, mean_error_ref: Optional[float] = None, mean_abs_error_ref: Optional[float] = None, mean_abs_perc_error_ref: Optional[float] = None, rmse_ref: Optional[float] = None, r2_score_ref: Optional[float] = None, abs_error_max_ref: Optional[float] = None, underperformance_ref: Optional[dict] = None)
Bases: `object`


#### Attributes: 

##### abs_error_max _: float_ 

##### abs_error_max_default _: float_ 

##### abs_error_max_ref _: Optional[float]_ _ = None_ 

##### abs_error_std _: float_ 

##### abs_perc_error_std _: float_ 

##### columns _: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)_ 

##### error_bias _: Optional[dict]_ _ = None_ 

##### error_normality _: dict_ 

##### error_std _: float_ 

##### hist_for_plot _: Dict[str, Series]_ 

##### me_default_sigma _: float_ 

##### me_hist_for_plot _: Dict[str, Union[Series, DataFrame]]_ 

##### mean_abs_error _: float_ 

##### mean_abs_error_default _: float_ 

##### mean_abs_error_ref _: Optional[float]_ _ = None_ 

##### mean_abs_perc_error _: float_ 

##### mean_abs_perc_error_default _: float_ 

##### mean_abs_perc_error_ref _: Optional[float]_ _ = None_ 

##### mean_error _: float_ 

##### mean_error_ref _: Optional[float]_ _ = None_ 

##### r2_score _: float_ 

##### r2_score_ref _: Optional[float]_ _ = None_ 

##### rmse _: float_ 

##### rmse_default _: float_ 

##### rmse_ref _: Optional[float]_ _ = None_ 

##### underperformance _: dict_ 

##### underperformance_ref _: Optional[dict]_ _ = None_ 

##### vals_for_plots _: Dict[str, Dict[str, Series]]_ 

#### Methods: 

### _class _ RegressionQualityMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionQualityMetricResults`]


#### Attributes: 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionQualityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionQualityMetric)

##### render_json(obj: RegressionQualityMetric)

### _class _ RegressionQualityMetricResults(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), r2_score: float, rmse: float, rmse_default: float, mean_error: float, me_default_sigma: float, me_hist_for_plot: Dict[str, pandas.core.series.Series], mean_abs_error: float, mean_abs_error_default: float, mean_abs_perc_error: float, mean_abs_perc_error_default: float, abs_error_max: float, abs_error_max_default: float, error_std: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, hist_for_plot: Dict[str, pandas.core.series.Series], vals_for_plots: Dict[str, Dict[str, pandas.core.series.Series]], error_bias: Optional[dict] = None, mean_error_ref: Optional[float] = None, mean_abs_error_ref: Optional[float] = None, mean_abs_perc_error_ref: Optional[float] = None, rmse_ref: Optional[float] = None, r2_score_ref: Optional[float] = None, abs_error_max_ref: Optional[float] = None, underperformance_ref: Optional[dict] = None, error_std_ref: Optional[float] = None, abs_error_std_ref: Optional[float] = None, abs_perc_error_std_ref: Optional[float] = None)
Bases: `object`


#### Attributes: 

##### abs_error_max _: float_ 

##### abs_error_max_default _: float_ 

##### abs_error_max_ref _: Optional[float]_ _ = None_ 

##### abs_error_std _: float_ 

##### abs_error_std_ref _: Optional[float]_ _ = None_ 

##### abs_perc_error_std _: float_ 

##### abs_perc_error_std_ref _: Optional[float]_ _ = None_ 

##### columns _: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)_ 

##### error_bias _: Optional[dict]_ _ = None_ 

##### error_normality _: dict_ 

##### error_std _: float_ 

##### error_std_ref _: Optional[float]_ _ = None_ 

##### hist_for_plot _: Dict[str, Series]_ 

##### me_default_sigma _: float_ 

##### me_hist_for_plot _: Dict[str, Series]_ 

##### mean_abs_error _: float_ 

##### mean_abs_error_default _: float_ 

##### mean_abs_error_ref _: Optional[float]_ _ = None_ 

##### mean_abs_perc_error _: float_ 

##### mean_abs_perc_error_default _: float_ 

##### mean_abs_perc_error_ref _: Optional[float]_ _ = None_ 

##### mean_error _: float_ 

##### mean_error_ref _: Optional[float]_ _ = None_ 

##### r2_score _: float_ 

##### r2_score_ref _: Optional[float]_ _ = None_ 

##### rmse _: float_ 

##### rmse_default _: float_ 

##### rmse_ref _: Optional[float]_ _ = None_ 

##### underperformance _: dict_ 

##### underperformance_ref _: Optional[dict]_ _ = None_ 

##### vals_for_plots _: Dict[str, Dict[str, Series]]_ 

#### Methods: 

### _class _ RegressionTopErrorMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionTopErrorMetricResults`]


#### Attributes: 

#### Methods: 

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ RegressionTopErrorMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: RegressionTopErrorMetric)

##### render_json(obj: RegressionTopErrorMetric)

### _class _ RegressionTopErrorMetricResults(curr_mean_err_per_group: Dict[str, Dict[str, float]], curr_scatter: Dict[str, Dict[str, pandas.core.series.Series]], ref_mean_err_per_group: Optional[Dict[str, Dict[str, float]]], ref_scatter: Optional[Dict[str, Dict[str, pandas.core.series.Series]]])
Bases: `object`


#### Attributes: 

##### curr_mean_err_per_group _: Dict[str, Dict[str, float]]_ 

##### curr_scatter _: Dict[str, Dict[str, Series]]_ 

##### ref_mean_err_per_group _: Optional[Dict[str, Dict[str, float]]]_ 

##### ref_scatter _: Optional[Dict[str, Dict[str, Series]]]_ 

#### Methods: 
## Module contents
