# evidently.report package

## Submodules

## <a name="module-evidently.report.report"></a>report module


### class Report(metrics: List[Union[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric), [MetricPreset](evidently.metric_preset.md#evidently.metric_preset.metric_preset.MetricPreset), [BaseGenerator](evidently.utils.md#evidently.utils.generators.BaseGenerator)]], options: Optional[List] = None)
Bases: [`Display`](evidently.suite.md#evidently.suite.base_suite.Display)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; metrics : List[Union[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric), [MetricPreset](evidently.metric_preset.md#evidently.metric_preset.metric_preset.MetricPreset), [BaseGenerator](evidently.utils.md#evidently.utils.generators.BaseGenerator)]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; run(\*, reference_data: Optional[DataFrame], current_data: DataFrame, column_mapping: Optional[[ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping)] = None)
## Module contents
