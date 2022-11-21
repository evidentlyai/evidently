# evidently.metric_preset package


### class ClassificationPreset()
Bases: `MetricPreset`

Metrics preset for classification performance.

Contains metrics:
- ClassificationQualityMetric
- ClassificationClassBalance
- ClassificationConfusionMatrix
- ClassificationQualityByClass


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class DataDriftPreset()
Bases: `MetricPreset`

Metric Preset for Data Drift analysis.

Contains metrics:
- DatasetDriftMetric
- DataDriftTable


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

### class RegressionPreset()
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


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TargetDriftPreset()
Bases: `MetricPreset`

Metric preset for Target Drift analysis.

Contains metrics:
- ColumnDriftMetric - for target and prediction if present in datasets.
- ColumnValuePlot - if task is regression.
- ColumnCorrelationsMetric - for target and prediction if present in datasets.
- TargetByFeaturesTable


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Submodules

## <a name="module-evidently.metric_preset.classification_performance"></a>classification_performance module


### class ClassificationPreset()
Bases: `MetricPreset`

Metrics preset for classification performance.

Contains metrics:
- ClassificationQualityMetric
- ClassificationClassBalance
- ClassificationConfusionMatrix
- ClassificationQualityByClass


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.data_drift"></a>data_drift module


### class DataDriftPreset()
Bases: `MetricPreset`

Metric Preset for Data Drift analysis.

Contains metrics:
- DatasetDriftMetric
- DataDriftTable


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


### class RegressionPreset()
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


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## <a name="module-evidently.metric_preset.target_drift"></a>target_drift module


### class TargetDriftPreset()
Bases: `MetricPreset`

Metric preset for Target Drift analysis.

Contains metrics:
- ColumnDriftMetric - for target and prediction if present in datasets.
- ColumnValuePlot - if task is regression.
- ColumnCorrelationsMetric - for target and prediction if present in datasets.
- TargetByFeaturesTable


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
