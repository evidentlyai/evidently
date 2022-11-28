# evidently.metric_preset package


### class ClassificationPreset(columns: Optional[List[str]] = None, probas_threshold: Optional[float] = None, k: Optional[int] = None)
Bases: `MetricPreset`

Metrics preset for classification performance.

Contains metrics:
- ClassificationQualityMetric
- ClassificationClassBalance
- ClassificationConfusionMatrix
- ClassificationQualityByClass

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataDriftPreset(columns: Optional[List[str]] = None, drift_share: float = 0.5, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `MetricPreset`

Metric Preset for Data Drift analysis.

Contains metrics:
- DatasetDriftMetric
- DataDriftTable

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_share : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataQualityPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`

Metric preset for Data Quality analysis.

Contains metrics:
- DatasetSummaryMetric
- ColumnSummaryMetric for each column
- DatasetMissingValuesMetric
- DatasetCorrelationsMetric


* **Parameters**

    `columns` – list of columns for analysis.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class RegressionPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`

Metric preset for Regression performance analysis.

Contains metrics:
- RegressionQualityMetric
- RegressionPredictedVsActualScatter
- RegressionPredictedVsActualPlot
- RegressionErrorPlot
- RegressionAbsPercentageErrorPlot
- RegressionErrorDistribution
- RegressionErrorNormality
- RegressionTopErrorMetric
- RegressionErrorBiasTable

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TargetDriftPreset(columns: Optional[List[str]] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `MetricPreset`

Metric preset for Target Drift analysis.

Contains metrics:
- ColumnDriftMetric - for target and prediction if present in datasets.
- ColumnValuePlot - if task is regression.
- ColumnCorrelationsMetric - for target and prediction if present in datasets.
- TargetByFeaturesTable

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Submodules

## <a name="module-evidently.metric_preset.classification_performance"></a>classification_performance module


### class ClassificationPreset(columns: Optional[List[str]] = None, probas_threshold: Optional[float] = None, k: Optional[int] = None)
Bases: `MetricPreset`

Metrics preset for classification performance.

Contains metrics:
- ClassificationQualityMetric
- ClassificationClassBalance
- ClassificationConfusionMatrix
- ClassificationQualityByClass

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.data_drift"></a>data_drift module


### class DataDriftPreset(columns: Optional[List[str]] = None, drift_share: float = 0.5, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `MetricPreset`

Metric Preset for Data Drift analysis.

Contains metrics:
- DatasetDriftMetric
- DataDriftTable

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_share : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.data_quality"></a>data_quality module


### class DataQualityPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`

Metric preset for Data Quality analysis.

Contains metrics:
- DatasetSummaryMetric
- ColumnSummaryMetric for each column
- DatasetMissingValuesMetric
- DatasetCorrelationsMetric


* **Parameters**

    `columns` – list of columns for analysis.


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


### class RegressionPreset(columns: Optional[List[str]] = None)
Bases: `MetricPreset`

Metric preset for Regression performance analysis.

Contains metrics:
- RegressionQualityMetric
- RegressionPredictedVsActualScatter
- RegressionPredictedVsActualPlot
- RegressionErrorPlot
- RegressionAbsPercentageErrorPlot
- RegressionErrorDistribution
- RegressionErrorNormality
- RegressionTopErrorMetric
- RegressionErrorBiasTable

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.target_drift"></a>target_drift module


### class TargetDriftPreset(columns: Optional[List[str]] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `MetricPreset`

Metric preset for Target Drift analysis.

Contains metrics:
- ColumnDriftMetric - for target and prediction if present in datasets.
- ColumnValuePlot - if task is regression.
- ColumnCorrelationsMetric - for target and prediction if present in datasets.
- TargetByFeaturesTable

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
