# evidently.test_preset package

Predefined Test Presets for Test Suite


### class BinaryClassificationTestPreset(prediction_type: str, threshold: float = 0.5)
Bases: `TestPreset`

Binary Classification Tests.
:param threshold: probabilities threshold for prediction with probas
:param prediction_type: type of prediction (‘probas’ or ‘labels’)

Contains:
- TestColumnValueDrift for target
- TestPrecisionScore - use threshold if prediction_type is ‘probas’
- TestRecallScore - use threshold if prediction_type is ‘probas’
- TestF1Score - use threshold if prediction_type is ‘probas’
- TestAccuracyScore - use threshold if prediction_type is ‘probas’


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class BinaryClassificationTopKTestPreset(k: Union[float, int])
Bases: `TestPreset`

Binary Classification tests with Top K threshold.


* **Parameters**

    `k` – number of rows or share of dataset


Contains tests:
- TestAccuracyScore
- TestPrecisionScore
- TestRecallScore
- TestF1Score
- TestColumnValueDrift
- TestRocAuc
- TestLogLoss


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataDriftTestPreset()
Bases: `TestPreset`

Data Drift tests.

Contains tests:
- TestShareOfDriftedColumns
- TestColumnValueDrift
- TestAllFeaturesValueDrift


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataQualityTestPreset()
Bases: `TestPreset`

Data Quality tests.

Contains tests:
- TestAllColumnsShareOfMissingValues
- TestAllColumnsMostCommonValueShare
- TestNumberOfConstantColumns
- TestNumberOfDuplicatedColumns
- TestNumberOfDuplicatedRows
- TestHighlyCorrelatedColumns


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataStabilityTestPreset()
Bases: `TestPreset`

Data Stability tests.

Contains tests:
- TestNumberOfRows
- TestNumberOfColumns
- TestColumnsType
- TestAllColumnsShareOfMissingValues
- TestNumColumnsOutOfRangeValues
- TestCatColumnsOutOfListValues
- TestNumColumnsMeanInNSigmas


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class MulticlassClassificationTestPreset(prediction_type: str)
Bases: `TestPreset`

Multiclass Classification tests.


* **Parameters**

    `prediction_type` – type of prediction data (‘probas’ or ‘labels’)


Contains tests:
- TestAccuracyScore
- TestF1Score
- TestPrecisionByClass for each class in data
- TestRecallByClass for each class in data
- TestNumberOfRows
- TestColumnValueDrift
- TestRocAuc
- TestLogLoss


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class NoTargetPerformanceTestPreset(columns: Optional[List[str]] = None)
Bases: `TestPreset`

No Target Performance tests.


* **Parameters**

    `columns` – list of columns include to tests


Contains tests:
- TestColumnValueDrift
- TestShareOfDriftedColumns
- TestColumnsType
- TestAllColumnsShareOfMissingValues
- TestNumColumnsOutOfRangeValues
- TestCatColumnsOutOfListValues
- TestNumColumnsMeanInNSigmas
- TestCustomFeaturesValueDrift

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : List[str] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class RegressionTestPreset()
Bases: `TestPreset`

Regression performance tests.

Contains tests:
- TestValueMeanError
- TestValueMAE
- TestValueRMSE
- TestValueMAPE


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Submodules

## <a name="module-evidently.test_preset.classification_binary"></a>classification_binary module


### class BinaryClassificationTestPreset(prediction_type: str, threshold: float = 0.5)
Bases: `TestPreset`

Binary Classification Tests.
:param threshold: probabilities threshold for prediction with probas
:param prediction_type: type of prediction (‘probas’ or ‘labels’)

Contains:
- TestColumnValueDrift for target
- TestPrecisionScore - use threshold if prediction_type is ‘probas’
- TestRecallScore - use threshold if prediction_type is ‘probas’
- TestF1Score - use threshold if prediction_type is ‘probas’
- TestAccuracyScore - use threshold if prediction_type is ‘probas’


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.classification_binary_topk"></a>classification_binary_topk module


### class BinaryClassificationTopKTestPreset(k: Union[float, int])
Bases: `TestPreset`

Binary Classification tests with Top K threshold.


* **Parameters**

    `k` – number of rows or share of dataset


Contains tests:
- TestAccuracyScore
- TestPrecisionScore
- TestRecallScore
- TestF1Score
- TestColumnValueDrift
- TestRocAuc
- TestLogLoss


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.classification_multiclass"></a>classification_multiclass module


### class MulticlassClassificationTestPreset(prediction_type: str)
Bases: `TestPreset`

Multiclass Classification tests.


* **Parameters**

    `prediction_type` – type of prediction data (‘probas’ or ‘labels’)


Contains tests:
- TestAccuracyScore
- TestF1Score
- TestPrecisionByClass for each class in data
- TestRecallByClass for each class in data
- TestNumberOfRows
- TestColumnValueDrift
- TestRocAuc
- TestLogLoss


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_drift"></a>data_drift module


### class DataDriftTestPreset()
Bases: `TestPreset`

Data Drift tests.

Contains tests:
- TestShareOfDriftedColumns
- TestColumnValueDrift
- TestAllFeaturesValueDrift


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_quality"></a>data_quality module


### class DataQualityTestPreset()
Bases: `TestPreset`

Data Quality tests.

Contains tests:
- TestAllColumnsShareOfMissingValues
- TestAllColumnsMostCommonValueShare
- TestNumberOfConstantColumns
- TestNumberOfDuplicatedColumns
- TestNumberOfDuplicatedRows
- TestHighlyCorrelatedColumns


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_stability"></a>data_stability module


### class DataStabilityTestPreset()
Bases: `TestPreset`

Data Stability tests.

Contains tests:
- TestNumberOfRows
- TestNumberOfColumns
- TestColumnsType
- TestAllColumnsShareOfMissingValues
- TestNumColumnsOutOfRangeValues
- TestCatColumnsOutOfListValues
- TestNumColumnsMeanInNSigmas


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.no_target_performance"></a>no_target_performance module


### class NoTargetPerformanceTestPreset(columns: Optional[List[str]] = None)
Bases: `TestPreset`

No Target Performance tests.


* **Parameters**

    `columns` – list of columns include to tests


Contains tests:
- TestColumnValueDrift
- TestShareOfDriftedColumns
- TestColumnsType
- TestAllColumnsShareOfMissingValues
- TestNumColumnsOutOfRangeValues
- TestCatColumnsOutOfListValues
- TestNumColumnsMeanInNSigmas
- TestCustomFeaturesValueDrift

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : List[str] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.regression"></a>regression module


### class RegressionTestPreset()
Bases: `TestPreset`

Regression performance tests.

Contains tests:
- TestValueMeanError
- TestValueMAE
- TestValueRMSE
- TestValueMAPE


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.test_preset"></a>test_preset module


### class TestPreset()
Bases: `object`

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
