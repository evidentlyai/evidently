# evidently.metrics.classification_performance package

## Submodules

## <a name="module-evidently.metrics.classification_performance.base_classification_metric"></a>base_classification_metric module


### class ThresholdClassificationMetric(probas_threshold: Optional[float], k: Optional[Union[float, int]])
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`TResult`], `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))
## <a name="module-evidently.metrics.classification_performance.class_balance_metric"></a>class_balance_metric module


### class ClassificationClassBalance()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassBalanceResult`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ClassificationClassBalanceRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationClassBalance)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationClassBalance)

### class ClassificationClassBalanceResult(plot_data: Dict[str, int])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; plot_data : Dict[str, int] 
## <a name="module-evidently.metrics.classification_performance.class_separation_metric"></a>class_separation_metric module


### class ClassificationClassSeparationPlot()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationClassSeparationPlotResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ClassificationClassSeparationPlotRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationClassSeparationPlot)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationClassSeparationPlot)

### class ClassificationClassSeparationPlotResults(target_name: str, current_plot: Optional[pandas.core.frame.DataFrame] = None, reference_plot: Optional[pandas.core.frame.DataFrame] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_plot : Optional[DataFrame]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_plot : Optional[DataFrame]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name : str 
## <a name="module-evidently.metrics.classification_performance.classification_dummy_metric"></a>classification_dummy_metric module


### class ClassificationDummyMetric(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationDummyMetricResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; quality_metric : ClassificationQualityMetric 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; correction_for_threshold(dummy_results: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), threshold: float, target: Series, labels: list, probas_shape: tuple)

### class ClassificationDummyMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationDummyMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationDummyMetric)

### class ClassificationDummyMetricResults(dummy: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), by_reference_dummy: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], model_quality: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], metrics_matrix: dict)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; by_reference_dummy : Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)] 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy : [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality) 

##### &nbsp;&nbsp;&nbsp;&nbsp; metrics_matrix : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; model_quality : Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)] 
## <a name="module-evidently.metrics.classification_performance.classification_quality_metric"></a>classification_quality_metric module


### class ClassificationQualityMetric(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityMetricResult`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; confusion_matrix_metric : ClassificationConfusionMatrix 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ClassificationQualityMetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityMetric)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityMetric)

### class ClassificationQualityMetricResult(current: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality), reference: Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)], target_name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current : [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality) 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference : Optional[[DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality)] 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name : str 
## <a name="module-evidently.metrics.classification_performance.confusion_matrix_metric"></a>confusion_matrix_metric module


### class ClassificationConfusionMatrix(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationConfusionMatrixResult`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ClassificationConfusionMatrixRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationConfusionMatrix)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationConfusionMatrix)

### class ClassificationConfusionMatrixResult(current_matrix: [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix), reference_matrix: Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_matrix : [ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_matrix : Optional[[ConfusionMatrix](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)] 
## <a name="module-evidently.metrics.classification_performance.pr_curve_metric"></a>pr_curve_metric module


### class ClassificationPRCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRCurveResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### class ClassificationPRCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationPRCurve)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationPRCurve)

### class ClassificationPRCurveResults(current_pr_curve: Optional[dict] = None, reference_pr_curve: Optional[dict] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_pr_curve : Optional[dict]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_pr_curve : Optional[dict]  = None 
## <a name="module-evidently.metrics.classification_performance.pr_table_metric"></a>pr_table_metric module


### class ClassificationPRTable()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationPRTableResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### class ClassificationPRTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationPRTable)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationPRTable)

### class ClassificationPRTableResults(current_pr_table: Optional[dict] = None, reference_pr_table: Optional[dict] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_pr_table : Optional[dict]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_pr_table : Optional[dict]  = None 
## <a name="module-evidently.metrics.classification_performance.probability_distribution_metric"></a>probability_distribution_metric module


### class ClassificationProbDistribution()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationProbDistributionResults`]

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; static  get_distribution(dataset: DataFrame, target_name: str, prediction_labels: Iterable)

### class ClassificationProbDistributionRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationProbDistribution)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationProbDistribution)

### class ClassificationProbDistributionResults(current_distribution: Optional[Dict[str, list]], reference_distribution: Optional[Dict[str, list]])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_distribution : Optional[Dict[str, list]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_distribution : Optional[Dict[str, list]] 
## <a name="module-evidently.metrics.classification_performance.quality_by_class_metric"></a>quality_by_class_metric module


### class ClassificationQualityByClass(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None)
Bases: `ThresholdClassificationMetric`[`ClassificationQualityByClassResult`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ClassificationQualityByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityByClass)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityByClass)

### class ClassificationQualityByClassResult(columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns), current_metrics: dict, current_roc_aucs: Optional[list], reference_metrics: Optional[dict], reference_roc_aucs: Optional[dict])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns) 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_metrics : dict 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_roc_aucs : Optional[list] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_metrics : Optional[dict] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_roc_aucs : Optional[dict] 
## <a name="module-evidently.metrics.classification_performance.quality_by_feature_table"></a>quality_by_feature_table module


### class ClassificationQualityByFeatureTable(columns: Optional[List[str]] = None)
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationQualityByFeatureTableResults`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

### class ClassificationQualityByFeatureTableRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationQualityByFeatureTable)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationQualityByFeatureTable)

### class ClassificationQualityByFeatureTableResults(current_plot_data: pandas.core.frame.DataFrame, reference_plot_data: Optional[pandas.core.frame.DataFrame], target_name: str, curr_predictions: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData), ref_predictions: Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)], columns: List[str])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : List[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; curr_predictions : [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData) 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_plot_data : DataFrame 

##### &nbsp;&nbsp;&nbsp;&nbsp; ref_predictions : Optional[[PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)] 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_plot_data : Optional[DataFrame] 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_name : str 
## <a name="module-evidently.metrics.classification_performance.roc_curve_metric"></a>roc_curve_metric module


### class ClassificationRocCurve()
Bases: [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)[`ClassificationRocCurveResults`]


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_metrics(target_data: Series, prediction: [PredictionData](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData))

### class ClassificationRocCurveRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: ClassificationRocCurve)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: ClassificationRocCurve)

### class ClassificationRocCurveResults(current_roc_curve: Optional[dict] = None, reference_roc_curve: Optional[dict] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_roc_curve : Optional[dict]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_roc_curve : Optional[dict]  = None
