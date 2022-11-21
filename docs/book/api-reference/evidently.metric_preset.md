# evidently.metric_preset package

## Submodules

## <a name="module-evidently.metric_preset.classification_performance"></a>classification_performance module


### class ClassificationPreset()
Bases: `MetricPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.data_drift"></a>data_drift module


### class DataDriftPreset()
Bases: `MetricPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.data_quality"></a>data_quality module


### class DataQualityPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.metric_preset"></a>metric_preset module


### class MetricPreset()
Bases: `object`

Base class for metric presets

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.regression_performance"></a>regression_performance module


### class RegressionPreset()
Bases: `MetricPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.target_drift"></a>target_drift module


### class TargetDriftPreset()
Bases: `MetricPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
