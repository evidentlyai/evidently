# evidently.metrics.regression_performance package

## Submodules

## abs_perc_error_in_time module


### class RegressionAbsPercentageErrorPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionAbsPercentageErrorPlotResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionAbsPercentageErrorPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionAbsPercentageErrorPlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionAbsPercentageErrorPlot)

### class RegressionAbsPercentageErrorPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter : Dict[str, Series] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter : Optional[Dict[str, Series]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; x_name : str 
## error_bias_table module


### class RegressionErrorBiasTable(columns: Optional[List[str]] = None, top_error: Optional[float] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorBiasTableResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; TOP_ERROR_DEFAULT  = 0.05 

##### &nbsp;&nbsp;&nbsp;&nbsp; TOP_ERROR_MAX  = 0.5 

##### &nbsp;&nbsp;&nbsp;&nbsp; TOP_ERROR_MIN  = 0 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; top_error : float 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionErrorBiasTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionErrorBiasTable)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionErrorBiasTable)

### class RegressionErrorBiasTableResults(top_error: float, current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, prediction_name: str, num_feature_names: List[str], cat_feature_names: List[str], error_bias: Optional[dict] = None, columns: Optional[List[str]] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_feature_names : List[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_plot_data : DataFrame 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_bias : Optional[dict]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_feature_names : List[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; prediction_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_plot_data : Optional[DataFrame] 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; top_error : float 
## error_distribution module


### class RegressionErrorDistribution()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorDistributionResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionErrorDistributionRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionErrorDistribution)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionErrorDistribution)

### class RegressionErrorDistributionResults(current_bins: pandas.core.frame.DataFrame, reference_bins: Optional[pandas.core.frame.DataFrame])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_bins : DataFrame 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_bins : Optional[DataFrame] 
## error_in_time module


### class RegressionErrorPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorPlotResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionErrorPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionErrorPlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionErrorPlot)

### class RegressionErrorPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter : Dict[str, Series] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter : Optional[Dict[str, Series]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; x_name : str 
## error_normality module


### class RegressionErrorNormality()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorNormalityResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionErrorNormalityRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionErrorNormality)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionErrorNormality)

### class RegressionErrorNormalityResults(current_error: pandas.core.series.Series, reference_error: Optional[pandas.core.series.Series])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_error : Series 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_error : Optional[Series] 
## predicted_and_actual_in_time module


### class RegressionPredictedVsActualPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPredictedVsActualPlotResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionPredictedVsActualPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionPredictedVsActualPlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionPredictedVsActualPlot)

### class RegressionPredictedVsActualPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter : Dict[str, Series] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter : Optional[Dict[str, Series]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; x_name : str 
## predicted_vs_actual module


### class RegressionPredictedVsActualScatter()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPredictedVsActualScatterResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionPredictedVsActualScatterRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionPredictedVsActualScatter)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionPredictedVsActualScatter)

### class RegressionPredictedVsActualScatterResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter : Dict[str, Series] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter : Optional[Dict[str, Series]] 
## regression_dummy_metric module


### class RegressionDummyMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionDummyMetricResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; quality_metric : RegressionQualityMetric 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionDummyMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionDummyMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionDummyMetric)

### class RegressionDummyMetricResults(rmse_default: float, mean_abs_error_default: float, mean_abs_perc_error_default: float, abs_error_max_default: float, mean_abs_error_by_ref: Optional[float] = None, mean_abs_error: Optional[float] = None, mean_abs_perc_error_by_ref: Optional[float] = None, mean_abs_perc_error: Optional[float] = None, rmse_by_ref: Optional[float] = None, rmse: Optional[float] = None, abs_error_max_by_ref: Optional[float] = None, abs_error_max: Optional[float] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_by_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_by_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_by_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_by_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_default : float 
## regression_performance_metrics module


### class RegressionPerformanceMetrics()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPerformanceMetricsResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; get_parameters()

### class RegressionPerformanceMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionPerformanceMetrics)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionPerformanceMetrics)

### class RegressionPerformanceMetricsResults(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), r2_score: float, rmse: float, rmse_default: float, mean_error: float, me_default_sigma: float, me_hist_for_plot: Dict[str, Union[pandas.core.series.Series, pandas.core.frame.DataFrame]], mean_abs_error: float, mean_abs_error_default: float, mean_abs_perc_error: float, mean_abs_perc_error_default: float, abs_error_max: float, abs_error_max_default: float, error_std: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, hist_for_plot: Dict[str, pandas.core.series.Series], vals_for_plots: Dict[str, Dict[str, pandas.core.series.Series]], error_bias: Optional[dict] = None, mean_error_ref: Optional[float] = None, mean_abs_error_ref: Optional[float] = None, mean_abs_perc_error_ref: Optional[float] = None, rmse_ref: Optional[float] = None, r2_score_ref: Optional[float] = None, abs_error_max_ref: Optional[float] = None, underperformance_ref: Optional[dict] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_std : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_perc_error_std : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns) 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_bias : Optional[dict]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_normality : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_std : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; hist_for_plot : Dict[str, Series] 

##### &nbsp;&nbsp;&nbsp;&nbsp; me_default_sigma : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; me_hist_for_plot : Dict[str, Union[Series, DataFrame]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_error : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_error_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; r2_score : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; r2_score_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; underperformance : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; underperformance_ref : Optional[dict]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; vals_for_plots : Dict[str, Dict[str, Series]] 
## regression_quality module


### class RegressionQualityMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionQualityMetricResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionQualityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionQualityMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionQualityMetric)

### class RegressionQualityMetricResults(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), r2_score: float, rmse: float, rmse_default: float, mean_error: float, me_default_sigma: float, me_hist_for_plot: Dict[str, pandas.core.series.Series], mean_abs_error: float, mean_abs_error_default: float, mean_abs_perc_error: float, mean_abs_perc_error_default: float, abs_error_max: float, abs_error_max_default: float, error_std: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, hist_for_plot: Dict[str, pandas.core.series.Series], vals_for_plots: Dict[str, Dict[str, pandas.core.series.Series]], error_bias: Optional[dict] = None, mean_error_ref: Optional[float] = None, mean_abs_error_ref: Optional[float] = None, mean_abs_perc_error_ref: Optional[float] = None, rmse_ref: Optional[float] = None, r2_score_ref: Optional[float] = None, abs_error_max_ref: Optional[float] = None, underperformance_ref: Optional[dict] = None, error_std_ref: Optional[float] = None, abs_error_std_ref: Optional[float] = None, abs_perc_error_std_ref: Optional[float] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_std : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_std_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_perc_error_std : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_perc_error_std_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns) 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_bias : Optional[dict]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_normality : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_std : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_std_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; hist_for_plot : Dict[str, Series] 

##### &nbsp;&nbsp;&nbsp;&nbsp; me_default_sigma : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; me_hist_for_plot : Dict[str, Series] 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_error : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_error_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; r2_score : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; r2_score_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_default : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_ref : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; underperformance : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; underperformance_ref : Optional[dict]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; vals_for_plots : Dict[str, Dict[str, Series]] 
## top_error module


### class RegressionTopErrorMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionTopErrorMetricResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class RegressionTopErrorMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionTopErrorMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionTopErrorMetric)

### class RegressionTopErrorMetricResults(curr_mean_err_per_group: Dict[str, Dict[str, float]], curr_scatter: Dict[str, Dict[str, pandas.core.series.Series]], ref_mean_err_per_group: Optional[Dict[str, Dict[str, float]]], ref_scatter: Optional[Dict[str, Dict[str, pandas.core.series.Series]]])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; curr_mean_err_per_group : Dict[str, Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; curr_scatter : Dict[str, Dict[str, Series]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; ref_mean_err_per_group : Optional[Dict[str, Dict[str, float]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; ref_scatter : Optional[Dict[str, Dict[str, Series]]] 
## Module contents
