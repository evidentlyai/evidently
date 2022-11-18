# evidently.metrics.classification_performance package

## Submodules


### _class_ ThresholdClassificationMetric(threshold: Optional[float], k: Optional[Union[float, int]])
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`TResult`], `ABC`


#### get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### _class_ ClassificationClassBalance()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassBalanceResult`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationClassBalanceRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationClassBalance)

#### render_json(obj: ClassificationClassBalance)

### _class_ ClassificationClassBalanceResult(plot_data: Dict[str, int])
Bases: `object`


#### plot_data(_: Dict[str, int_ )

### _class_ ClassificationClassSeparationPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassSeparationPlotResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationClassSeparationPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationClassSeparationPlot)

#### render_json(obj: ClassificationClassSeparationPlot)

### _class_ ClassificationClassSeparationPlotResults(target_name: str, current_plot: Optional[pandas.core.frame.DataFrame] = None, reference_plot: Optional[pandas.core.frame.DataFrame] = None)
Bases: `object`


#### current_plot(_: Optional[DataFrame_ _ = Non_ )

#### reference_plot(_: Optional[DataFrame_ _ = Non_ )

#### target_name(_: st_ )

### _class_ ClassificationDummyMetric(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationDummyMetricResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### correction_for_threshold(dummy_results: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), threshold: float, target: Series, labels: list, probas_shape: tuple)

#### quality_metric(_: ClassificationQualityMetri_ )

### _class_ ClassificationDummyMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationDummyMetric)

#### render_json(obj: ClassificationDummyMetric)

### _class_ ClassificationDummyMetricResults(dummy: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), by_reference_dummy: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], model_quality: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], metrics_matrix: dict)
Bases: `object`


#### by_reference_dummy(_: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)_ )

#### dummy(_: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality_ )

#### metrics_matrix(_: dic_ )

#### model_quality(_: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)_ )

### _class_ ClassificationQualityMetric(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityMetricResult`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### confusion_matrix_metric(_: ClassificationConfusionMatri_ )

### _class_ ClassificationQualityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationQualityMetric)

#### render_json(obj: ClassificationQualityMetric)

### _class_ ClassificationQualityMetricResult(current: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), reference: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], target_name: str)
Bases: `object`


#### current(_: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality_ )

#### reference(_: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)_ )

#### target_name(_: st_ )

### _class_ ClassificationConfusionMatrix(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationConfusionMatrixResult`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationConfusionMatrixRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationConfusionMatrix)

#### render_json(obj: ClassificationConfusionMatrix)

### _class_ ClassificationConfusionMatrixResult(current_matrix: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix), reference_matrix: Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)])
Bases: `object`


#### current_matrix(_: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix_ )

#### reference_matrix(_: Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)_ )

### _class_ ClassificationPRCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRCurveResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ ClassificationPRCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationPRCurve)

#### render_json(obj: ClassificationPRCurve)

### _class_ ClassificationPRCurveResults(current_pr_curve: Optional[dict] = None, reference_pr_curve: Optional[dict] = None)
Bases: `object`


#### current_pr_curve(_: Optional[dict_ _ = Non_ )

#### reference_pr_curve(_: Optional[dict_ _ = Non_ )

### _class_ ClassificationPRTable()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRTableResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ ClassificationPRTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationPRTable)

#### render_json(obj: ClassificationPRTable)

### _class_ ClassificationPRTableResults(current_pr_table: Optional[dict] = None, reference_pr_table: Optional[dict] = None)
Bases: `object`


#### current_pr_table(_: Optional[dict_ _ = Non_ )

#### reference_pr_table(_: Optional[dict_ _ = Non_ )

### _class_ ClassificationProbDistribution()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationProbDistributionResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### _static_ get_distribution(dataset: DataFrame, target_name: str, prediction_labels: Iterable)

### _class_ ClassificationProbDistributionRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationProbDistribution)

#### render_json(obj: ClassificationProbDistribution)

### _class_ ClassificationProbDistributionResults(current_distribution: Optional[Dict[str, list]], reference_distribution: Optional[Dict[str, list]])
Bases: `object`


#### current_distribution(_: Optional[Dict[str, list]_ )

#### reference_distribution(_: Optional[Dict[str, list]_ )

### _class_ ClassificationQualityByClass(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityByClassResult`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationQualityByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationQualityByClass)

#### render_json(obj: ClassificationQualityByClass)

### _class_ ClassificationQualityByClassResult(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), current_metrics: dict, current_roc_aucs: Optional[list], reference_metrics: Optional[dict], reference_roc_aucs: Optional[dict])
Bases: `object`


#### columns(_: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns_ )

#### current_metrics(_: dic_ )

#### current_roc_aucs(_: Optional[list_ )

#### reference_metrics(_: Optional[dict_ )

#### reference_roc_aucs(_: Optional[dict_ )

### _class_ ClassificationQualityByFeatureTable(columns: Optional[List[str]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationQualityByFeatureTableResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### columns(_: Optional[List[str]_ )

### _class_ ClassificationQualityByFeatureTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationQualityByFeatureTable)

#### render_json(obj: ClassificationQualityByFeatureTable)

### _class_ ClassificationQualityByFeatureTableResults(current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, curr_predictions: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData), ref_predictions: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], columns: List[str])
Bases: `object`


#### columns(_: List[str_ )

#### curr_predictions(_: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData_ )

#### current_plot_data(_: DataFram_ )

#### ref_predictions(_: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)_ )

#### reference_plot_data(_: Optional[DataFrame_ )

#### target_name(_: st_ )

### _class_ ClassificationRocCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationRocCurveResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ ClassificationRocCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationRocCurve)

#### render_json(obj: ClassificationRocCurve)

### _class_ ClassificationRocCurveResults(current_roc_curve: Optional[dict] = None, reference_roc_curve: Optional[dict] = None)
Bases: `object`


#### current_roc_curve(_: Optional[dict_ _ = Non_ )

#### reference_roc_curve(_: Optional[dict_ _ = Non_ )
## Module contents
