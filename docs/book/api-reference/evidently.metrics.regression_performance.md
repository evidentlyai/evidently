# evidently.metrics.regression_performance package

## Submodules

## evidently.metrics.regression_performance.abs_perc_error_in_time module


### _class_ evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlot()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionAbsPercentageErrorPlotResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionAbsPercentageErrorPlot)

#### render_json(obj: RegressionAbsPercentageErrorPlot)

### _class_ evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`


#### current_scatter(_: Dict[str, Series_ )

#### reference_scatter(_: Optional[Dict[str, Series]_ )

#### x_name(_: st_ )
## evidently.metrics.regression_performance.error_bias_table module


### _class_ evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable(columns: Optional[List[str]] = None, top_error: Optional[float] = None)
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorBiasTableResults`]


#### TOP_ERROR_DEFAULT(_ = 0.0_ )

#### TOP_ERROR_MAX(_ = 0._ )

#### TOP_ERROR_MIN(_ = _ )

#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### columns(_: Optional[List[str]_ )

#### top_error(_: floa_ )

### _class_ evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionErrorBiasTable)

#### render_json(obj: RegressionErrorBiasTable)

### _class_ evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults(top_error: float, current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, prediction_name: str, num_feature_names: List[str], cat_feature_names: List[str], error_bias: Optional[dict] = None, columns: Optional[List[str]] = None)
Bases: `object`


#### cat_feature_names(_: List[str_ )

#### columns(_: Optional[List[str]_ _ = Non_ )

#### current_plot_data(_: DataFram_ )

#### error_bias(_: Optional[dict_ _ = Non_ )

#### num_feature_names(_: List[str_ )

#### prediction_name(_: st_ )

#### reference_plot_data(_: Optional[DataFrame_ )

#### target_name(_: st_ )

#### top_error(_: floa_ )
## evidently.metrics.regression_performance.error_distribution module


### _class_ evidently.metrics.regression_performance.error_distribution.RegressionErrorDistribution()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorDistributionResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionErrorDistribution)

#### render_json(obj: RegressionErrorDistribution)

### _class_ evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionResults(current_bins: pandas.core.frame.DataFrame, reference_bins: Optional[pandas.core.frame.DataFrame])
Bases: `object`


#### current_bins(_: DataFram_ )

#### reference_bins(_: Optional[DataFrame_ )
## evidently.metrics.regression_performance.error_in_time module


### _class_ evidently.metrics.regression_performance.error_in_time.RegressionErrorPlot()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorPlotResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionErrorPlot)

#### render_json(obj: RegressionErrorPlot)

### _class_ evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`


#### current_scatter(_: Dict[str, Series_ )

#### reference_scatter(_: Optional[Dict[str, Series]_ )

#### x_name(_: st_ )
## evidently.metrics.regression_performance.error_normality module


### _class_ evidently.metrics.regression_performance.error_normality.RegressionErrorNormality()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorNormalityResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionErrorNormality)

#### render_json(obj: RegressionErrorNormality)

### _class_ evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityResults(current_error: pandas.core.series.Series, reference_error: Optional[pandas.core.series.Series])
Bases: `object`


#### current_error(_: Serie_ )

#### reference_error(_: Optional[Series_ )
## evidently.metrics.regression_performance.predicted_and_actual_in_time module


### _class_ evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlot()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPredictedVsActualPlotResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionPredictedVsActualPlot)

#### render_json(obj: RegressionPredictedVsActualPlot)

### _class_ evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`


#### current_scatter(_: Dict[str, Series_ )

#### reference_scatter(_: Optional[Dict[str, Series]_ )

#### x_name(_: st_ )
## evidently.metrics.regression_performance.predicted_vs_actual module


### _class_ evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatter()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPredictedVsActualScatterResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionPredictedVsActualScatter)

#### render_json(obj: RegressionPredictedVsActualScatter)

### _class_ evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]])
Bases: `object`


#### current_scatter(_: Dict[str, Series_ )

#### reference_scatter(_: Optional[Dict[str, Series]_ )
## evidently.metrics.regression_performance.regression_performance_metrics module


### _class_ evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetrics()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPerformanceMetricsResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### get_parameters()

### _class_ evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionPerformanceMetrics)

#### render_json(obj: RegressionPerformanceMetrics)

### _class_ evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults(columns: [evidently.utils.data_operations.DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns), r2_score: float, rmse: float, rmse_default: float, mean_error: float, me_default_sigma: float, me_hist_for_plot: Dict[str, Union[pandas.core.series.Series, pandas.core.frame.DataFrame]], mean_abs_error: float, mean_abs_error_default: float, mean_abs_perc_error: float, mean_abs_perc_error_default: float, abs_error_max: float, abs_error_max_default: float, error_std: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, hist_for_plot: Dict[str, pandas.core.series.Series], vals_for_plots: Dict[str, Dict[str, pandas.core.series.Series]], error_bias: Optional[dict] = None, mean_error_ref: Optional[float] = None, mean_abs_error_ref: Optional[float] = None, mean_abs_perc_error_ref: Optional[float] = None, rmse_ref: Optional[float] = None, r2_score_ref: Optional[float] = None, abs_error_max_ref: Optional[float] = None, underperformance_ref: Optional[dict] = None)
Bases: `object`


#### abs_error_max(_: floa_ )

#### abs_error_max_default(_: floa_ )

#### abs_error_max_ref(_: Optional[float_ _ = Non_ )

#### abs_error_std(_: floa_ )

#### abs_perc_error_std(_: floa_ )

#### columns(_: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns_ )

#### error_bias(_: Optional[dict_ _ = Non_ )

#### error_normality(_: dic_ )

#### error_std(_: floa_ )

#### hist_for_plot(_: Dict[str, Series_ )

#### me_default_sigma(_: floa_ )

#### me_hist_for_plot(_: Dict[str, Union[Series, DataFrame]_ )

#### mean_abs_error(_: floa_ )

#### mean_abs_error_default(_: floa_ )

#### mean_abs_error_ref(_: Optional[float_ _ = Non_ )

#### mean_abs_perc_error(_: floa_ )

#### mean_abs_perc_error_default(_: floa_ )

#### mean_abs_perc_error_ref(_: Optional[float_ _ = Non_ )

#### mean_error(_: floa_ )

#### mean_error_ref(_: Optional[float_ _ = Non_ )

#### r2_score(_: floa_ )

#### r2_score_ref(_: Optional[float_ _ = Non_ )

#### rmse(_: floa_ )

#### rmse_default(_: floa_ )

#### rmse_ref(_: Optional[float_ _ = Non_ )

#### underperformance(_: dic_ )

#### underperformance_ref(_: Optional[dict_ _ = Non_ )

#### vals_for_plots(_: Dict[str, Dict[str, Series]_ )
## evidently.metrics.regression_performance.regression_quality module


### _class_ evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionQualityMetricResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionQualityMetric)

#### render_json(obj: RegressionQualityMetric)

### _class_ evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults(columns: [evidently.utils.data_operations.DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns), r2_score: float, rmse: float, rmse_default: float, mean_error: float, me_default_sigma: float, me_hist_for_plot: Dict[str, pandas.core.series.Series], mean_abs_error: float, mean_abs_error_default: float, mean_abs_perc_error: float, mean_abs_perc_error_default: float, abs_error_max: float, abs_error_max_default: float, error_std: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, hist_for_plot: Dict[str, pandas.core.series.Series], vals_for_plots: Dict[str, Dict[str, pandas.core.series.Series]], error_bias: Optional[dict] = None, mean_error_ref: Optional[float] = None, mean_abs_error_ref: Optional[float] = None, mean_abs_perc_error_ref: Optional[float] = None, rmse_ref: Optional[float] = None, r2_score_ref: Optional[float] = None, abs_error_max_ref: Optional[float] = None, underperformance_ref: Optional[dict] = None, error_std_ref: Optional[float] = None, abs_error_std_ref: Optional[float] = None, abs_perc_error_std_ref: Optional[float] = None)
Bases: `object`


#### abs_error_max(_: floa_ )

#### abs_error_max_default(_: floa_ )

#### abs_error_max_ref(_: Optional[float_ _ = Non_ )

#### abs_error_std(_: floa_ )

#### abs_error_std_ref(_: Optional[float_ _ = Non_ )

#### abs_perc_error_std(_: floa_ )

#### abs_perc_error_std_ref(_: Optional[float_ _ = Non_ )

#### columns(_: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns_ )

#### error_bias(_: Optional[dict_ _ = Non_ )

#### error_normality(_: dic_ )

#### error_std(_: floa_ )

#### error_std_ref(_: Optional[float_ _ = Non_ )

#### hist_for_plot(_: Dict[str, Series_ )

#### me_default_sigma(_: floa_ )

#### me_hist_for_plot(_: Dict[str, Series_ )

#### mean_abs_error(_: floa_ )

#### mean_abs_error_default(_: floa_ )

#### mean_abs_error_ref(_: Optional[float_ _ = Non_ )

#### mean_abs_perc_error(_: floa_ )

#### mean_abs_perc_error_default(_: floa_ )

#### mean_abs_perc_error_ref(_: Optional[float_ _ = Non_ )

#### mean_error(_: floa_ )

#### mean_error_ref(_: Optional[float_ _ = Non_ )

#### r2_score(_: floa_ )

#### r2_score_ref(_: Optional[float_ _ = Non_ )

#### rmse(_: floa_ )

#### rmse_default(_: floa_ )

#### rmse_ref(_: Optional[float_ _ = Non_ )

#### underperformance(_: dic_ )

#### underperformance_ref(_: Optional[dict_ _ = Non_ )

#### vals_for_plots(_: Dict[str, Dict[str, Series]_ )
## evidently.metrics.regression_performance.top_error module


### _class_ evidently.metrics.regression_performance.top_error.RegressionTopErrorMetric()
Bases: [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionTopErrorMetricResults`]


#### calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: RegressionTopErrorMetric)

#### render_json(obj: RegressionTopErrorMetric)

### _class_ evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults(curr_mean_err_per_group: Dict[str, Dict[str, float]], curr_scatter: Dict[str, Dict[str, pandas.core.series.Series]], ref_mean_err_per_group: Optional[Dict[str, Dict[str, float]]], ref_scatter: Optional[Dict[str, Dict[str, pandas.core.series.Series]]])
Bases: `object`


#### curr_mean_err_per_group(_: Dict[str, Dict[str, float]_ )

#### curr_scatter(_: Dict[str, Dict[str, Series]_ )

#### ref_mean_err_per_group(_: Optional[Dict[str, Dict[str, float]]_ )

#### ref_scatter(_: Optional[Dict[str, Dict[str, Series]]_ )
## Module contents
