# evidently.metric_preset package

## Submodules


### _class_ ClassificationPreset()
Bases: `MetricPreset`


#### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ DataDriftPreset()
Bases: `MetricPreset`


#### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ DataQualityPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`


#### columns(_: Optional[List[str]_ )

#### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ MetricPreset()
Bases: `object`

Base class for metric presets


#### _abstract_ generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ RegressionPreset()
Bases: `MetricPreset`


#### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TargetDriftPreset()
Bases: `MetricPreset`


#### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Module contents
