# evidently.metrics.classification_performance package

## Submodules

## evidently.metrics.classification_performance.base_classification_metric module


### _class_ evidently.metrics.classification_performance.base_classification_metric.ThresholdClassificationMetric(threshold: Optional[float], k: Optional[Union[float, int]])
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`TResult`], `ABC`


#### get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))
## evidently.metrics.classification_performance.class_balance_metric module


### _class_ evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalance()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassBalanceResult`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationClassBalance)

#### render_json(obj: ClassificationClassBalance)

### _class_ evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceResult(plot_data: Dict[str, int])
Bases: `object`


#### plot_data(_: Dict[str, int_ )
## evidently.metrics.classification_performance.class_separation_metric module


### _class_ evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassSeparationPlotResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationClassSeparationPlot)

#### render_json(obj: ClassificationClassSeparationPlot)

### _class_ evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults(target_name: str, current_plot: Optional[pandas.core.frame.DataFrame] = None, reference_plot: Optional[pandas.core.frame.DataFrame] = None)
Bases: `object`


#### current_plot(_: Optional[DataFrame_ _ = Non_ )

#### reference_plot(_: Optional[DataFrame_ _ = Non_ )

#### target_name(_: st_ )
## evidently.metrics.classification_performance.classification_quality_metric module


### _class_ evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityMetricResult`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### calculate_metrics(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), confusion_matrix: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix))

#### confusion_matrix_metric(_: ClassificationConfusionMatri_ )

### _class_ evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationQualityMetric)

#### render_json(obj: ClassificationQualityMetric)

### _class_ evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult(current: evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality, reference: Optional[evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality], target_name: str)
Bases: `object`


#### current(_: DatasetClassificationQualit_ )

#### reference(_: Optional[DatasetClassificationQuality_ )

#### target_name(_: st_ )

### _class_ evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality(accuracy: float, precision: float, recall: float, f1: float, roc_auc: Optional[float] = None, log_loss: Optional[float] = None, tpr: Optional[float] = None, tnr: Optional[float] = None, fpr: Optional[float] = None, fnr: Optional[float] = None)
Bases: `object`


#### accuracy(_: floa_ )

#### f1(_: floa_ )

#### fnr(_: Optional[float_ _ = Non_ )

#### fpr(_: Optional[float_ _ = Non_ )

#### log_loss(_: Optional[float_ _ = Non_ )

#### precision(_: floa_ )

#### recall(_: floa_ )

#### roc_auc(_: Optional[float_ _ = Non_ )

#### tnr(_: Optional[float_ _ = Non_ )

#### tpr(_: Optional[float_ _ = Non_ )
## evidently.metrics.classification_performance.confusion_matrix_metric module


### _class_ evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationConfusionMatrixResult`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationConfusionMatrix)

#### render_json(obj: ClassificationConfusionMatrix)

### _class_ evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixResult(current_matrix: [evidently.calculations.classification_performance.ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix), reference_matrix: Optional[[evidently.calculations.classification_performance.ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)])
Bases: `object`


#### current_matrix(_: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix_ )

#### reference_matrix(_: Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)_ )
## evidently.metrics.classification_performance.pr_curve_metric module


### _class_ evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRCurveResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationPRCurve)

#### render_json(obj: ClassificationPRCurve)

### _class_ evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveResults(current_pr_curve: Optional[dict] = None, reference_pr_curve: Optional[dict] = None)
Bases: `object`


#### current_pr_curve(_: Optional[dict_ _ = Non_ )

#### reference_pr_curve(_: Optional[dict_ _ = Non_ )
## evidently.metrics.classification_performance.pr_table_metric module


### _class_ evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTable()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRTableResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationPRTable)

#### render_json(obj: ClassificationPRTable)

### _class_ evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableResults(current_pr_table: Optional[dict] = None, reference_pr_table: Optional[dict] = None)
Bases: `object`


#### current_pr_table(_: Optional[dict_ _ = Non_ )

#### reference_pr_table(_: Optional[dict_ _ = Non_ )
## evidently.metrics.classification_performance.probability_distribution_metric module


### _class_ evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistribution()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationProbDistributionResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### _static_ get_distribution(dataset: DataFrame, target_name: str, prediction_labels: Iterable)

### _class_ evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationProbDistribution)

#### render_json(obj: ClassificationProbDistribution)

### _class_ evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionResults(current_distribution: Optional[Dict[str, list]], reference_distribution: Optional[Dict[str, list]])
Bases: `object`


#### current_distribution(_: Optional[Dict[str, list]_ )

#### reference_distribution(_: Optional[Dict[str, list]_ )
## evidently.metrics.classification_performance.quality_by_class_metric module


### _class_ evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityByClassResult`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### _class_ evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationQualityByClass)

#### render_json(obj: ClassificationQualityByClass)

### _class_ evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult(columns: [evidently.utils.data_operations.DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), current_metrics: dict, current_roc_aucs: Optional[list], reference_metrics: Optional[dict], reference_roc_aucs: Optional[dict])
Bases: `object`


#### columns(_: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns_ )

#### current_metrics(_: dic_ )

#### current_roc_aucs(_: Optional[list_ )

#### reference_metrics(_: Optional[dict_ )

#### reference_roc_aucs(_: Optional[dict_ )
## evidently.metrics.classification_performance.quality_by_feature_table module


### _class_ evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTable(columns: Optional[List[str]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationQualityByFeatureTableResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### columns(_: Optional[List[str]_ )

### _class_ evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationQualityByFeatureTable)

#### render_json(obj: ClassificationQualityByFeatureTable)

### _class_ evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults(current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, curr_predictions: [evidently.calculations.classification_performance.PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData), ref_predictions: Optional[[evidently.calculations.classification_performance.PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], columns: List[str])
Bases: `object`


#### columns(_: List[str_ )

#### curr_predictions(_: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData_ )

#### current_plot_data(_: DataFram_ )

#### ref_predictions(_: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)_ )

#### reference_plot_data(_: Optional[DataFrame_ )

#### target_name(_: st_ )
## evidently.metrics.classification_performance.roc_curve_metric module


### _class_ evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationRocCurveResults`]


#### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### _class_ evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationRocCurve)

#### render_json(obj: ClassificationRocCurve)

### _class_ evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveResults(current_roc_curve: Optional[dict] = None, reference_roc_curve: Optional[dict] = None)
Bases: `object`


#### current_roc_curve(_: Optional[dict_ _ = Non_ )

#### reference_roc_curve(_: Optional[dict_ _ = Non_ )
## Module contents
