# evidently.test_preset package

## Submodules

## evidently.test_preset.classification_binary module


### _class_ evidently.test_preset.classification_binary.BinaryClassificationTestPreset(prediction_type: str, threshold: float = 0.5)
Bases: `TestPreset`


#### generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.test_preset.classification_binary_topk module


### _class_ evidently.test_preset.classification_binary_topk.BinaryClassificationTopKTestPreset(k: Union[float, int])
Bases: `TestPreset`


#### generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.test_preset.classification_multiclass module


### _class_ evidently.test_preset.classification_multiclass.MulticlassClassificationTestPreset(prediction_type: str)
Bases: `TestPreset`


#### generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.test_preset.data_drift module


### _class_ evidently.test_preset.data_drift.DataDriftTestPreset()
Bases: `TestPreset`


#### generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.test_preset.data_quality module


### _class_ evidently.test_preset.data_quality.DataQualityTestPreset()
Bases: `TestPreset`


#### generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.test_preset.data_stability module


### _class_ evidently.test_preset.data_stability.DataStabilityTestPreset()
Bases: `TestPreset`


#### generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.test_preset.no_target_performance module


### _class_ evidently.test_preset.no_target_performance.NoTargetPerformanceTestPreset(columns: Optional[List[str]] = None)
Bases: `TestPreset`


#### columns(_: List[str_ )

#### generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.test_preset.regression module


### _class_ evidently.test_preset.regression.RegressionTestPreset()
Bases: `TestPreset`


#### generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## evidently.test_preset.test_preset module


### _class_ evidently.test_preset.test_preset.TestPreset()
Bases: `object`


#### _abstract_ generate_tests(data: [InputData](./evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Module contents
