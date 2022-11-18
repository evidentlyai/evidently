# evidently.model_monitoring.monitors package

## Submodules

## evidently.model_monitoring.monitors.cat_target_drift module


### _class_ evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitor()
Bases: [`ModelMonitor`](./evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)


#### analyzers()

#### metrics(analyzer_results)

#### monitor_id()

#### options_provider(_: [OptionsProvider](./evidently.options.md#evidently.options.OptionsProvider_ )

### _class_ evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitorMetrics()
Bases: `object`

Class for category target grift metrics.

Metrics list:

    - count: quantity of rows in reference and current datasets

    - drift: p_value for the data drift


#### count(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### drift(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )
## evidently.model_monitoring.monitors.classification_performance module


### _class_ evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitor()
Bases: [`ModelMonitor`](./evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)


#### analyzers()

#### metrics(analyzer_results)

#### monitor_id()

#### options_provider(_: [OptionsProvider](./evidently.options.md#evidently.options.OptionsProvider_ )

### _class_ evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitorMetricsMonitor()
Bases: `object`

Class for classification performance metrics in monitor.

Metrics list:

    > - quality: model quality with macro-average metrics in reference and current datasets

    > Each metric name is marked as a metric label
    > - class_representation: quantity of items in each class
    > A class name is marked as a class_name label
    > target and prediction columns are marked as type

    - class_quality: quality metrics for each class

    - confusion: aggregated confusion metrics

    - class_confusion: confusion (TP, TN, FP, FN) by class


#### class_confusion(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### class_quality(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### class_representation(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### confusion(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### quality(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )
## evidently.model_monitoring.monitors.data_drift module


### _class_ evidently.model_monitoring.monitors.data_drift.DataDriftMonitor()
Bases: [`ModelMonitor`](./evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)


#### analyzers()

#### metrics(analyzer_results)

#### monitor_id()

#### options_provider(_: [OptionsProvider](./evidently.options.md#evidently.options.OptionsProvider_ )

### _class_ evidently.model_monitoring.monitors.data_drift.DataDriftMonitorMetrics()
Bases: `object`


#### dataset_drift(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### n_drifted_features(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### share_drifted_features(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### value(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )
## evidently.model_monitoring.monitors.data_quality module


### _class_ evidently.model_monitoring.monitors.data_quality.DataQualityMonitor()
Bases: [`ModelMonitor`](./evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)


#### analyzers()

#### metrics(analyzer_results)

#### monitor_id()

#### options_provider(_: [OptionsProvider](./evidently.options.md#evidently.options.OptionsProvider_ )

### _class_ evidently.model_monitoring.monitors.data_quality.DataQualityMonitorMetrics()
Bases: `object`


#### quality_stat(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )
## evidently.model_monitoring.monitors.num_target_drift module


### _class_ evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitor()
Bases: [`ModelMonitor`](./evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)


#### analyzers()

#### metrics(analyzer_results)

#### monitor_id()

#### options_provider(_: [OptionsProvider](./evidently.options.md#evidently.options.OptionsProvider_ )

### _class_ evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitorMetrics()
Bases: `object`

Class for numeric target grift metrics.

Metrics list:

    - count: quantity of rows in reference and current datasets

    - drift: p_value for the data drift

    - current_correlations: correlation with target and prediction columns

        for numeric features in current dataset

    - reference_correlations: correlation with target and prediction columns

        for numeric features in reference dataset


#### count(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### current_correlations(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### drift(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### reference_correlations(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )
## evidently.model_monitoring.monitors.prob_classification_performance module


### _class_ evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitor()
Bases: [`ModelMonitor`](./evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)


#### analyzers()

#### metrics(analyzer_results)

#### monitor_id()

#### options_provider(_: [OptionsProvider](./evidently.options.md#evidently.options.OptionsProvider_ )

### _class_ evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitorMetricsMonitor()
Bases: `object`

Class for probabilistic classification performance metrics in monitor.

Metrics list:

    > - quality: model quality with macro-average metrics in reference and current datasets

    > Each metric name is marked as a metric label
    > - class_representation: quantity of items in each class
    > A class name is marked as a class_name label
    > target and prediction columns are marked as type

    - class_quality: quality metrics for each class

    - confusion: aggregated confusion metrics

    - class_confusion: confusion (TP, TN, FP, FN) by class


#### class_confusion(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### class_quality(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### class_representation(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### confusion(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### quality(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )
## evidently.model_monitoring.monitors.regression_performance module


### _class_ evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitor()
Bases: [`ModelMonitor`](./evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)


#### analyzers()

#### metrics(analyzer_results)

#### monitor_id()

#### options_provider(_: [OptionsProvider](./evidently.options.md#evidently.options.OptionsProvider_ )

### _class_ evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitorMetrics()
Bases: `object`


#### feature_error_bias(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### normality(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### quality(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )

#### underperformance(_ = <evidently.model_monitoring.monitoring.ModelMonitoringMetric object_ )
## Module contents
