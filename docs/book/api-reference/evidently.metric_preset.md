# evidently.metric_preset package

## Submodules


### _class _ ClassificationPreset()
Bases: `MetricPreset`


#### Attributes: 

##### labels _: Sequence[Union[str, int]]_ 

##### values _: list_ 

#### Methods: 

##### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ DataDriftPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ DataQualityPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`


#### Attributes: 

##### columns _: Optional[List[str]]_ 

#### Methods: 

##### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ MetricPreset()
Bases: `object`

Base class for metric presets


#### Attributes: 

#### Methods: 

##### _abstract _ generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ RegressionPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TargetDriftPreset()
Bases: `MetricPreset`


#### Attributes: 

#### Methods: 

##### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Module contents
