# evidently.test_preset package

Predefined Test Presets for Test Suite


### class BinaryClassificationTestPreset(stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, stattest_threshold: Optional[float] = None, probas_threshold: Optional[float] = None)
Bases: `TestPreset`

Binary Classification Tests.
:param stattest: statistical test for target drift test.
:param stattest_threshold: threshold for statistical test for target drift test.
:param probas_threshold: threshold for label calculation for prediction.

Contains:
- TestColumnValueDrift for target
- TestPrecisionScore
- TestRecallScore
- TestF1Score
- TestAccuracyScore


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class BinaryClassificationTopKTestPreset(k: Union[float, int], stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, stattest_threshold: Optional[float] = None)
Bases: `TestPreset`

Binary Classification Tests for Top K threshold.
:param stattest: stattest for TestColumnDrift
:param stattest_threshold: threshold for stattest

Contains:
- TestColumnDrift for target
- TestPrecisionScore
- TestRecallScore
- TestF1Score
- TestAccuracyScore

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataDriftTestPreset(columns: Optional[List[str]] = None, drift_share: Optional[float] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `TestPreset`

Data Drift tests.

Contains tests:
- TestShareOfDriftedColumns
- TestColumnValueDrift
- TestAllFeaturesValueDrift

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_share : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataQualityTestPreset(columns: Optional[List[str]] = None)
Bases: `TestPreset`

Data Quality tests.

Contains tests:
- TestAllColumnsShareOfMissingValues
- TestAllColumnsMostCommonValueShare
- TestNumberOfConstantColumns
- TestNumberOfDuplicatedColumns
- TestNumberOfDuplicatedRows
- TestHighlyCorrelatedColumns

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataStabilityTestPreset(columns: Optional[List[str]] = None)
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

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class MulticlassClassificationTestPreset(stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, stattest_threshold: Optional[float] = None)
Bases: `TestPreset`

Multiclass Classification tests.


* **Parameters**

    - `stattest` – statistical test for target drift test.

    - `stattest_threshold` – threshold for statistical test for target drift test.


Contains tests:
- TestAccuracyScore
- TestF1Score
- TestPrecisionByClass for each class in data
- TestRecallByClass for each class in data
- TestNumberOfRows
- TestColumnValueDrift
- TestRocAuc
- TestLogLoss

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class NoTargetPerformanceTestPreset(columns: Optional[List[str]] = None, drift_share: Optional[float] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
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

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_share : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float]  = None 

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


### class BinaryClassificationTestPreset(stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, stattest_threshold: Optional[float] = None, probas_threshold: Optional[float] = None)
Bases: `TestPreset`

Binary Classification Tests.
:param stattest: statistical test for target drift test.
:param stattest_threshold: threshold for statistical test for target drift test.
:param probas_threshold: threshold for label calculation for prediction.

Contains:
- TestColumnValueDrift for target
- TestPrecisionScore
- TestRecallScore
- TestF1Score
- TestAccuracyScore


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.classification_binary_topk"></a>classification_binary_topk module


### class BinaryClassificationTopKTestPreset(k: Union[float, int], stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, stattest_threshold: Optional[float] = None)
Bases: `TestPreset`

Binary Classification Tests for Top K threshold.
:param stattest: stattest for TestColumnDrift
:param stattest_threshold: threshold for stattest

Contains:
- TestColumnDrift for target
- TestPrecisionScore
- TestRecallScore
- TestF1Score
- TestAccuracyScore

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.classification_multiclass"></a>classification_multiclass module


### class MulticlassClassificationTestPreset(stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, stattest_threshold: Optional[float] = None)
Bases: `TestPreset`

Multiclass Classification tests.


* **Parameters**

    - `stattest` – statistical test for target drift test.

    - `stattest_threshold` – threshold for statistical test for target drift test.


Contains tests:
- TestAccuracyScore
- TestF1Score
- TestPrecisionByClass for each class in data
- TestRecallByClass for each class in data
- TestNumberOfRows
- TestColumnValueDrift
- TestRocAuc
- TestLogLoss

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_drift"></a>data_drift module


### class DataDriftTestPreset(columns: Optional[List[str]] = None, drift_share: Optional[float] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `TestPreset`

Data Drift tests.

Contains tests:
- TestShareOfDriftedColumns
- TestColumnValueDrift
- TestAllFeaturesValueDrift

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_share : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_quality"></a>data_quality module


### class DataQualityTestPreset(columns: Optional[List[str]] = None)
Bases: `TestPreset`

Data Quality tests.

Contains tests:
- TestAllColumnsShareOfMissingValues
- TestAllColumnsMostCommonValueShare
- TestNumberOfConstantColumns
- TestNumberOfDuplicatedColumns
- TestNumberOfDuplicatedRows
- TestHighlyCorrelatedColumns

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.data_stability"></a>data_stability module


### class DataStabilityTestPreset(columns: Optional[List[str]] = None)
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

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.test_preset.no_target_performance"></a>no_target_performance module


### class NoTargetPerformanceTestPreset(columns: Optional[List[str]] = None, drift_share: Optional[float] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
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

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_share : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float]  = None 

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
