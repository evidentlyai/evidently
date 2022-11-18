# evidently.metrics.classification_performance package

## Submodules


### _class_ ThresholdClassificationMetric(threshold: Optional[float], k: Optional[Union[float, int]])
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`TResult`], `ABC`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### _class_ ClassificationClassBalance()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassBalanceResult`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationClassBalanceRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationClassBalance)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationClassBalance)

### _class_ ClassificationClassBalanceResult(plot_data: Dict[str, int])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; plot_data _: Dict[str, int]_ 

#### Methods: 

### _class_ ClassificationClassSeparationPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassSeparationPlotResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationClassSeparationPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationClassSeparationPlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationClassSeparationPlot)

### _class_ ClassificationClassSeparationPlotResults(target_name: str, current_plot: Optional[pandas.core.frame.DataFrame] = None, reference_plot: Optional[pandas.core.frame.DataFrame] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_plot _: Optional[DataFrame]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_plot _: Optional[DataFrame]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name _: str_ 

#### Methods: 

### _class_ ClassificationDummyMetric(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationDummyMetricResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; quality_metric _: ClassificationQualityMetric_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; correction_for_threshold(dummy_results: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), threshold: float, target: Series, labels: list, probas_shape: tuple)

### _class_ ClassificationDummyMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationDummyMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationDummyMetric)

### _class_ ClassificationDummyMetricResults(dummy: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), by_reference_dummy: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], model_quality: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], metrics_matrix: dict)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; by_reference_dummy _: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy _: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metrics_matrix _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; model_quality _: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)]_ 

#### Methods: 

### _class_ ClassificationQualityMetric(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityMetricResult`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; confusion_matrix_metric _: ClassificationConfusionMatrix_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationQualityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityMetric)

### _class_ ClassificationQualityMetricResult(current: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), reference: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], target_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current _: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference _: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name _: str_ 

#### Methods: 

### _class_ ClassificationConfusionMatrix(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationConfusionMatrixResult`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationConfusionMatrixRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationConfusionMatrix)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationConfusionMatrix)

### _class_ ClassificationConfusionMatrixResult(current_matrix: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix), reference_matrix: Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_matrix _: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_matrix _: Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)]_ 

#### Methods: 

### _class_ ClassificationPRCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRCurveResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ ClassificationPRCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationPRCurve)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationPRCurve)

### _class_ ClassificationPRCurveResults(current_pr_curve: Optional[dict] = None, reference_pr_curve: Optional[dict] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_pr_curve _: Optional[dict]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_pr_curve _: Optional[dict]_ _ = None_ 

#### Methods: 

### _class_ ClassificationPRTable()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRTableResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ ClassificationPRTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationPRTable)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationPRTable)

### _class_ ClassificationPRTableResults(current_pr_table: Optional[dict] = None, reference_pr_table: Optional[dict] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_pr_table _: Optional[dict]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_pr_table _: Optional[dict]_ _ = None_ 

#### Methods: 

### _class_ ClassificationProbDistribution()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationProbDistributionResults`]

#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; _static _ get_distribution(dataset: DataFrame, target_name: str, prediction_labels: Iterable)

### _class_ ClassificationProbDistributionRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationProbDistribution)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationProbDistribution)

### _class_ ClassificationProbDistributionResults(current_distribution: Optional[Dict[str, list]], reference_distribution: Optional[Dict[str, list]])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_distribution _: Optional[Dict[str, list]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_distribution _: Optional[Dict[str, list]]_ 

#### Methods: 

### _class_ ClassificationQualityByClass(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityByClassResult`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationQualityByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityByClass)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityByClass)

### _class_ ClassificationQualityByClassResult(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), current_metrics: dict, current_roc_aucs: Optional[list], reference_metrics: Optional[dict], reference_roc_aucs: Optional[dict])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_metrics _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_roc_aucs _: Optional[list]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_metrics _: Optional[dict]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_roc_aucs _: Optional[dict]_ 

#### Methods: 

### _class_ ClassificationQualityByFeatureTable(columns: Optional[List[str]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationQualityByFeatureTableResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: Optional[List[str]]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ ClassificationQualityByFeatureTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityByFeatureTable)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityByFeatureTable)

### _class_ ClassificationQualityByFeatureTableResults(current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, curr_predictions: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData), ref_predictions: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], columns: List[str])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: List[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; curr_predictions _: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_plot_data _: DataFrame_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; ref_predictions _: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_plot_data _: Optional[DataFrame]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name _: str_ 

#### Methods: 

### _class_ ClassificationRocCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationRocCurveResults`]


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ ClassificationRocCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationRocCurve)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationRocCurve)

### _class_ ClassificationRocCurveResults(current_roc_curve: Optional[dict] = None, reference_roc_curve: Optional[dict] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_roc_curve _: Optional[dict]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_roc_curve _: Optional[dict]_ _ = None_ 

#### Methods: 
## Module contents
