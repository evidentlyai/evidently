# evidently.metric_preset package

## Submodules


### _class _ ClassificationPreset()
Bases: `MetricPreset`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; labels _: Sequence[Union[str, int]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: list_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ DataDriftPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ DataQualityPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: Optional[List[str]]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ MetricPreset()
Bases: `object`

Base class for metric presets


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ RegressionPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TargetDriftPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Module contents
