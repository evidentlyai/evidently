# evidently.test_preset package

## Submodules

## <a name="module-evidently.test_preset.classification_binary"></a>classification_binary module


### class BinaryClassificationTestPreset(prediction_type: str, threshold: float = 0.5)
Bases: `TestPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.classification_binary_topk"></a>classification_binary_topk module


### class BinaryClassificationTopKTestPreset(k: Union[float, int])
Bases: `TestPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.classification_multiclass"></a>classification_multiclass module


### class MulticlassClassificationTestPreset(prediction_type: str)
Bases: `TestPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_drift"></a>data_drift module


### class DataDriftTestPreset()
Bases: `TestPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_quality"></a>data_quality module


### class DataQualityTestPreset()
Bases: `TestPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_stability"></a>data_stability module


### class DataStabilityTestPreset()
Bases: `TestPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.no_target_performance"></a>no_target_performance module


### class NoTargetPerformanceTestPreset(columns: Optional[List[str]] = None)
Bases: `TestPreset`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : List[str] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.regression"></a>regression module


### class RegressionTestPreset()
Bases: `TestPreset`


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.test_preset"></a>test_preset module


### class TestPreset()
Bases: `object`

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
