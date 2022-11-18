# evidently.test_preset package

## Submodules


### _class_ BinaryClassificationTestPreset(prediction_type: str, threshold: float = 0.5)
Bases: `TestPreset`


#### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ BinaryClassificationTopKTestPreset(k: Union[float, int])
Bases: `TestPreset`


#### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ MulticlassClassificationTestPreset(prediction_type: str)
Bases: `TestPreset`


#### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ DataDriftTestPreset()
Bases: `TestPreset`


#### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ DataQualityTestPreset()
Bases: `TestPreset`


#### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ DataStabilityTestPreset()
Bases: `TestPreset`


#### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ NoTargetPerformanceTestPreset(columns: Optional[List[str]] = None)
Bases: `TestPreset`


#### columns(_: List[str_ )

#### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ RegressionTestPreset()
Bases: `TestPreset`


#### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TestPreset()
Bases: `object`


#### _abstract_ generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Module contents
