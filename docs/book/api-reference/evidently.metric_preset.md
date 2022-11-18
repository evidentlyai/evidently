# evidently.metric_preset package

## Submodules


### _class_ ClassificationPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ DataDriftPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ DataQualityPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: Optional[List[str]]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ MetricPreset()
Bases: `object`

Base class for metric presets

#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ RegressionPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TargetDriftPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Module contents
