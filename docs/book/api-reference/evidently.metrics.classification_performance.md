# evidently.metrics.classification_performance package

## Submodules


### _class _ ThresholdClassificationMetric(threshold: Optional[float], k: Optional[Union[float, int]])
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`TResult`], `ABC`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; labels _: Sequence[Union[str, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; values _: list_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; exception _: BaseException_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

#####&nbsp;&nbsp;&nbsp;&nbsp; get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### _class _ ClassificationClassBalance()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassBalanceResult`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ClassificationClassBalanceRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationClassBalance)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationClassBalance)

### _class _ ClassificationClassBalanceResult(plot_data: Dict[str, int])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; plot_data _: Dict[str, int]_ 

#### Methods: 

### _class _ ClassificationClassSeparationPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassSeparationPlotResults`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ClassificationClassSeparationPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationClassSeparationPlot)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationClassSeparationPlot)

### _class _ ClassificationClassSeparationPlotResults(target_name: str, current_plot: Optional[pandas.core.frame.DataFrame] = None, reference_plot: Optional[pandas.core.frame.DataFrame] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_plot _: Optional[DataFrame]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_plot _: Optional[DataFrame]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target_name _: str_ 

#### Methods: 

### _class _ ClassificationDummyMetric(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationDummyMetricResults`]


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; quality_metric _: ClassificationQualityMetric_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; correction_for_threshold(dummy_results: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), threshold: float, target: Series, labels: list, probas_shape: tuple)

### _class _ ClassificationDummyMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationDummyMetric)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationDummyMetric)

### _class _ ClassificationDummyMetricResults(dummy: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), by_reference_dummy: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], model_quality: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], metrics_matrix: dict)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; by_reference_dummy _: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; dummy _: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; metrics_matrix _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; model_quality _: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)]_ 

#### Methods: 

### _class _ ClassificationQualityMetric(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityMetricResult`]


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; confusion_matrix_metric _: ClassificationConfusionMatrix_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ClassificationQualityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityMetric)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityMetric)

### _class _ ClassificationQualityMetricResult(current: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), reference: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], target_name: str)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; current _: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target_name _: str_ 

#### Methods: 

### _class _ ClassificationConfusionMatrix(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationConfusionMatrixResult`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ClassificationConfusionMatrixRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationConfusionMatrix)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationConfusionMatrix)

### _class _ ClassificationConfusionMatrixResult(current_matrix: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix), reference_matrix: Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_matrix _: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_matrix _: Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)]_ 

#### Methods: 

### _class _ ClassificationPRCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRCurveResults`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class _ ClassificationPRCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationPRCurve)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationPRCurve)

### _class _ ClassificationPRCurveResults(current_pr_curve: Optional[dict] = None, reference_pr_curve: Optional[dict] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_pr_curve _: Optional[dict]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_pr_curve _: Optional[dict]_ _ = None_ 

#### Methods: 

### _class _ ClassificationPRTable()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRTableResults`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class _ ClassificationPRTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationPRTable)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationPRTable)

### _class _ ClassificationPRTableResults(current_pr_table: Optional[dict] = None, reference_pr_table: Optional[dict] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_pr_table _: Optional[dict]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_pr_table _: Optional[dict]_ _ = None_ 

#### Methods: 

### _class _ ClassificationProbDistribution()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationProbDistributionResults`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; _static _ get_distribution(dataset: DataFrame, target_name: str, prediction_labels: Iterable)

### _class _ ClassificationProbDistributionRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationProbDistribution)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationProbDistribution)

### _class _ ClassificationProbDistributionResults(current_distribution: Optional[Dict[str, list]], reference_distribution: Optional[Dict[str, list]])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_distribution _: Optional[Dict[str, list]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_distribution _: Optional[Dict[str, list]]_ 

#### Methods: 

### _class _ ClassificationQualityByClass(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityByClassResult`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ClassificationQualityByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityByClass)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityByClass)

### _class _ ClassificationQualityByClassResult(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), current_metrics: dict, current_roc_aucs: Optional[list], reference_metrics: Optional[dict], reference_roc_aucs: Optional[dict])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; columns _: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_metrics _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_roc_aucs _: Optional[list]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_metrics _: Optional[dict]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_roc_aucs _: Optional[dict]_ 

#### Methods: 

### _class _ ClassificationQualityByFeatureTable(columns: Optional[List[str]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationQualityByFeatureTableResults`]


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; columns _: Optional[List[str]]_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class _ ClassificationQualityByFeatureTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityByFeatureTable)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityByFeatureTable)

### _class _ ClassificationQualityByFeatureTableResults(current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, curr_predictions: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData), ref_predictions: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], columns: List[str])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; columns _: List[str]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; curr_predictions _: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_plot_data _: DataFrame_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; ref_predictions _: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_plot_data _: Optional[DataFrame]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target_name _: str_ 

#### Methods: 

### _class _ ClassificationRocCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationRocCurveResults`]


#### Attributes: 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class _ ClassificationRocCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationRocCurve)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationRocCurve)

### _class _ ClassificationRocCurveResults(current_roc_curve: Optional[dict] = None, reference_roc_curve: Optional[dict] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_roc_curve _: Optional[dict]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_roc_curve _: Optional[dict]_ _ = None_ 

#### Methods: 
## Module contents
