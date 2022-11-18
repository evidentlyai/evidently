# evidently.metric_preset package

## Submodules

## evidently.metric_preset.classification_performance module


### _class_ evidently.metric_preset.classification_performance.ClassificationPreset()
Bases: `MetricPreset`


#### generate_metrics(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.metric_preset.data_drift module


### _class_ evidently.metric_preset.data_drift.DataDriftPreset()
Bases: `MetricPreset`


#### generate_metrics(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.metric_preset.data_quality module


### _class_ evidently.metric_preset.data_quality.DataQualityPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`


#### columns(_: Optional[List[str]_ )

#### generate_metrics(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.metric_preset.metric_preset module


### _class_ evidently.metric_preset.metric_preset.MetricPreset()
Bases: `object`

Base class for metric presets


#### _abstract_ generate_metrics(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.metric_preset.regression_performance module


### _class_ evidently.metric_preset.regression_performance.RegressionPreset()
Bases: `MetricPreset`


#### generate_metrics(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.metric_preset.target_drift module


### _class_ evidently.metric_preset.target_drift.TargetDriftPreset()
Bases: `MetricPreset`


#### generate_metrics(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Module contents
