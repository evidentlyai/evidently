# evidently.metrics.regression_performance package

## Submodules


### _class_ RegressionAbsPercentageErrorPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionAbsPercentageErrorPlotResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionAbsPercentageErrorPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionAbsPercentageErrorPlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionAbsPercentageErrorPlot)

### _class_ RegressionAbsPercentageErrorPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter _: Dict[str, Series]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter _: Optional[Dict[str, Series]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; x_name _: str_ 

#### Methods: 

### _class_ RegressionErrorBiasTable(columns: Optional[List[str]] = None, top_error: Optional[float] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorBiasTableResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; TOP_ERROR_DEFAULT _ = 0.05_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; TOP_ERROR_MAX _ = 0.5_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; TOP_ERROR_MIN _ = 0_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: Optional[List[str]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; top_error _: float_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionErrorBiasTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionErrorBiasTable)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionErrorBiasTable)

### _class_ RegressionErrorBiasTableResults(top_error: float, current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, prediction_name: str, num_feature_names: List[str], cat_feature_names: List[str], error_bias: Optional[dict] = None, columns: Optional[List[str]] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_feature_names _: List[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: Optional[List[str]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_plot_data _: DataFrame_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_bias _: Optional[dict]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_feature_names _: List[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; prediction_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_plot_data _: Optional[DataFrame]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; top_error _: float_ 

#### Methods: 

### _class_ RegressionErrorDistribution()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorDistributionResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionErrorDistributionRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionErrorDistribution)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionErrorDistribution)

### _class_ RegressionErrorDistributionResults(current_bins: pandas.core.frame.DataFrame, reference_bins: Optional[pandas.core.frame.DataFrame])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_bins _: DataFrame_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_bins _: Optional[DataFrame]_ 

#### Methods: 

### _class_ RegressionErrorPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorPlotResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionErrorPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionErrorPlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionErrorPlot)

### _class_ RegressionErrorPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter _: Dict[str, Series]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter _: Optional[Dict[str, Series]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; x_name _: str_ 

#### Methods: 

### _class_ RegressionErrorNormality()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionErrorNormalityResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionErrorNormalityRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionErrorNormality)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionErrorNormality)

### _class_ RegressionErrorNormalityResults(current_error: pandas.core.series.Series, reference_error: Optional[pandas.core.series.Series])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_error _: Series_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_error _: Optional[Series]_ 

#### Methods: 

### _class_ RegressionPredictedVsActualPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPredictedVsActualPlotResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionPredictedVsActualPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionPredictedVsActualPlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionPredictedVsActualPlot)

### _class_ RegressionPredictedVsActualPlotResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]], x_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter _: Dict[str, Series]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter _: Optional[Dict[str, Series]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; x_name _: str_ 

#### Methods: 

### _class_ RegressionPredictedVsActualScatter()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPredictedVsActualScatterResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionPredictedVsActualScatterRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionPredictedVsActualScatter)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionPredictedVsActualScatter)

### _class_ RegressionPredictedVsActualScatterResults(current_scatter: Dict[str, pandas.core.series.Series], reference_scatter: Optional[Dict[str, pandas.core.series.Series]])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_scatter _: Dict[str, Series]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_scatter _: Optional[Dict[str, Series]]_ 

#### Methods: 

### _class_ RegressionDummyMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionDummyMetricResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; quality_metric _: RegressionQualityMetric_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionDummyMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionDummyMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionDummyMetric)

### _class_ RegressionDummyMetricResults(rmse_default: float, mean_abs_error_default: float, mean_abs_perc_error_default: float, abs_error_max_default: float, mean_abs_error_by_ref: Optional[float] = None, mean_abs_error: Optional[float] = None, mean_abs_perc_error_by_ref: Optional[float] = None, mean_abs_perc_error: Optional[float] = None, rmse_by_ref: Optional[float] = None, rmse: Optional[float] = None, abs_error_max_by_ref: Optional[float] = None, abs_error_max: Optional[float] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_by_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_by_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_by_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_by_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_default _: float_ 

#### Methods: 

### _class_ RegressionPerformanceMetrics()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionPerformanceMetricsResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; get_parameters()

### _class_ RegressionPerformanceMetricsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionPerformanceMetrics)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionPerformanceMetrics)

### _class_ RegressionPerformanceMetricsResults(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), r2_score: float, rmse: float, rmse_default: float, mean_error: float, me_default_sigma: float, me_hist_for_plot: Dict[str, Union[pandas.core.series.Series, pandas.core.frame.DataFrame]], mean_abs_error: float, mean_abs_error_default: float, mean_abs_perc_error: float, mean_abs_perc_error_default: float, abs_error_max: float, abs_error_max_default: float, error_std: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, hist_for_plot: Dict[str, pandas.core.series.Series], vals_for_plots: Dict[str, Dict[str, pandas.core.series.Series]], error_bias: Optional[dict] = None, mean_error_ref: Optional[float] = None, mean_abs_error_ref: Optional[float] = None, mean_abs_perc_error_ref: Optional[float] = None, rmse_ref: Optional[float] = None, r2_score_ref: Optional[float] = None, abs_error_max_ref: Optional[float] = None, underperformance_ref: Optional[dict] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_std _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_perc_error_std _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_bias _: Optional[dict]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_normality _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_std _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; hist_for_plot _: Dict[str, Series]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; me_default_sigma _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; me_hist_for_plot _: Dict[str, Union[Series, DataFrame]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_error _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_error_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; r2_score _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; r2_score_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; underperformance _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; underperformance_ref _: Optional[dict]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; vals_for_plots _: Dict[str, Dict[str, Series]]_ 

#### Methods: 

### _class_ RegressionQualityMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionQualityMetricResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionQualityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionQualityMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionQualityMetric)

### _class_ RegressionQualityMetricResults(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), r2_score: float, rmse: float, rmse_default: float, mean_error: float, me_default_sigma: float, me_hist_for_plot: Dict[str, pandas.core.series.Series], mean_abs_error: float, mean_abs_error_default: float, mean_abs_perc_error: float, mean_abs_perc_error_default: float, abs_error_max: float, abs_error_max_default: float, error_std: float, abs_error_std: float, abs_perc_error_std: float, error_normality: dict, underperformance: dict, hist_for_plot: Dict[str, pandas.core.series.Series], vals_for_plots: Dict[str, Dict[str, pandas.core.series.Series]], error_bias: Optional[dict] = None, mean_error_ref: Optional[float] = None, mean_abs_error_ref: Optional[float] = None, mean_abs_perc_error_ref: Optional[float] = None, rmse_ref: Optional[float] = None, r2_score_ref: Optional[float] = None, abs_error_max_ref: Optional[float] = None, underperformance_ref: Optional[dict] = None, error_std_ref: Optional[float] = None, abs_error_std_ref: Optional[float] = None, abs_perc_error_std_ref: Optional[float] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_max_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_std _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_error_std_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_perc_error_std _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; abs_perc_error_std_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_bias _: Optional[dict]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_normality _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_std _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; error_std_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; hist_for_plot _: Dict[str, Series]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; me_default_sigma _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; me_hist_for_plot _: Dict[str, Series]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_error_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_abs_perc_error_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_error _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; mean_error_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; r2_score _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; r2_score_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_default _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; rmse_ref _: Optional[float]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; underperformance _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; underperformance_ref _: Optional[dict]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; vals_for_plots _: Dict[str, Dict[str, Series]]_ 

#### Methods: 

### _class_ RegressionTopErrorMetric()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`RegressionTopErrorMetricResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ RegressionTopErrorMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: RegressionTopErrorMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: RegressionTopErrorMetric)

### _class_ RegressionTopErrorMetricResults(curr_mean_err_per_group: Dict[str, Dict[str, float]], curr_scatter: Dict[str, Dict[str, pandas.core.series.Series]], ref_mean_err_per_group: Optional[Dict[str, Dict[str, float]]], ref_scatter: Optional[Dict[str, Dict[str, pandas.core.series.Series]]])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; curr_mean_err_per_group _: Dict[str, Dict[str, float]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; curr_scatter _: Dict[str, Dict[str, Series]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; ref_mean_err_per_group _: Optional[Dict[str, Dict[str, float]]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; ref_scatter _: Optional[Dict[str, Dict[str, Series]]]_ 

#### Methods: 
## Module contents
