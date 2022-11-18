# evidently.model_monitoring package

## Subpackages

- [evidently.model_monitoring.monitors package](evidently.model_monitoring.monitors.md)

    - [Submodules](api-reference/evidently.model_monitoring.monitors.md#submodules)

    - [evidently.model_monitoring.monitors.cat_target_drift module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.cat_target_drift)

        - [`CatTargetDriftMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitor)

            - [`CatTargetDriftMonitor.analyzers()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitor.analyzers)

            - [`CatTargetDriftMonitor.metrics()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitor.metrics)

            - [`CatTargetDriftMonitor.monitor_id()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitor.monitor_id)

            - [`CatTargetDriftMonitor.options_provider`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitor.options_provider)

        - [`CatTargetDriftMonitorMetrics`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitorMetrics)

            - [`CatTargetDriftMonitorMetrics.count`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitorMetrics.count)

            - [`CatTargetDriftMonitorMetrics.drift`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.cat_target_drift.CatTargetDriftMonitorMetrics.drift)

    - [evidently.model_monitoring.monitors.classification_performance module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.classification_performance)

        - [`ClassificationPerformanceMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitor)

            - [`ClassificationPerformanceMonitor.analyzers()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitor.analyzers)

            - [`ClassificationPerformanceMonitor.metrics()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitor.metrics)

            - [`ClassificationPerformanceMonitor.monitor_id()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitor.monitor_id)

            - [`ClassificationPerformanceMonitor.options_provider`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitor.options_provider)

        - [`ClassificationPerformanceMonitorMetricsMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitorMetricsMonitor)

            - [`ClassificationPerformanceMonitorMetricsMonitor.class_confusion`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitorMetricsMonitor.class_confusion)

            - [`ClassificationPerformanceMonitorMetricsMonitor.class_quality`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitorMetricsMonitor.class_quality)

            - [`ClassificationPerformanceMonitorMetricsMonitor.class_representation`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitorMetricsMonitor.class_representation)

            - [`ClassificationPerformanceMonitorMetricsMonitor.confusion`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitorMetricsMonitor.confusion)

            - [`ClassificationPerformanceMonitorMetricsMonitor.quality`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.classification_performance.ClassificationPerformanceMonitorMetricsMonitor.quality)

    - [evidently.model_monitoring.monitors.data_drift module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.data_drift)

        - [`DataDriftMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitor)

            - [`DataDriftMonitor.analyzers()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitor.analyzers)

            - [`DataDriftMonitor.metrics()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitor.metrics)

            - [`DataDriftMonitor.monitor_id()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitor.monitor_id)

            - [`DataDriftMonitor.options_provider`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitor.options_provider)

        - [`DataDriftMonitorMetrics`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitorMetrics)

            - [`DataDriftMonitorMetrics.dataset_drift`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitorMetrics.dataset_drift)

            - [`DataDriftMonitorMetrics.n_drifted_features`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitorMetrics.n_drifted_features)

            - [`DataDriftMonitorMetrics.share_drifted_features`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitorMetrics.share_drifted_features)

            - [`DataDriftMonitorMetrics.value`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_drift.DataDriftMonitorMetrics.value)

    - [evidently.model_monitoring.monitors.data_quality module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.data_quality)

        - [`DataQualityMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_quality.DataQualityMonitor)

            - [`DataQualityMonitor.analyzers()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_quality.DataQualityMonitor.analyzers)

            - [`DataQualityMonitor.metrics()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_quality.DataQualityMonitor.metrics)

            - [`DataQualityMonitor.monitor_id()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_quality.DataQualityMonitor.monitor_id)

            - [`DataQualityMonitor.options_provider`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_quality.DataQualityMonitor.options_provider)

        - [`DataQualityMonitorMetrics`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_quality.DataQualityMonitorMetrics)

            - [`DataQualityMonitorMetrics.quality_stat`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.data_quality.DataQualityMonitorMetrics.quality_stat)

    - [evidently.model_monitoring.monitors.num_target_drift module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.num_target_drift)

        - [`NumTargetDriftMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitor)

            - [`NumTargetDriftMonitor.analyzers()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitor.analyzers)

            - [`NumTargetDriftMonitor.metrics()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitor.metrics)

            - [`NumTargetDriftMonitor.monitor_id()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitor.monitor_id)

            - [`NumTargetDriftMonitor.options_provider`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitor.options_provider)

        - [`NumTargetDriftMonitorMetrics`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitorMetrics)

            - [`NumTargetDriftMonitorMetrics.count`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitorMetrics.count)

            - [`NumTargetDriftMonitorMetrics.current_correlations`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitorMetrics.current_correlations)

            - [`NumTargetDriftMonitorMetrics.drift`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitorMetrics.drift)

            - [`NumTargetDriftMonitorMetrics.reference_correlations`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.num_target_drift.NumTargetDriftMonitorMetrics.reference_correlations)

    - [evidently.model_monitoring.monitors.prob_classification_performance module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.prob_classification_performance)

        - [`ProbClassificationPerformanceMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitor)

            - [`ProbClassificationPerformanceMonitor.analyzers()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitor.analyzers)

            - [`ProbClassificationPerformanceMonitor.metrics()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitor.metrics)

            - [`ProbClassificationPerformanceMonitor.monitor_id()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitor.monitor_id)

            - [`ProbClassificationPerformanceMonitor.options_provider`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitor.options_provider)

        - [`ProbClassificationPerformanceMonitorMetricsMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitorMetricsMonitor)

            - [`ProbClassificationPerformanceMonitorMetricsMonitor.class_confusion`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitorMetricsMonitor.class_confusion)

            - [`ProbClassificationPerformanceMonitorMetricsMonitor.class_quality`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitorMetricsMonitor.class_quality)

            - [`ProbClassificationPerformanceMonitorMetricsMonitor.class_representation`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitorMetricsMonitor.class_representation)

            - [`ProbClassificationPerformanceMonitorMetricsMonitor.confusion`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitorMetricsMonitor.confusion)

            - [`ProbClassificationPerformanceMonitorMetricsMonitor.quality`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.prob_classification_performance.ProbClassificationPerformanceMonitorMetricsMonitor.quality)

    - [evidently.model_monitoring.monitors.regression_performance module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.regression_performance)

        - [`RegressionPerformanceMonitor`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitor)

            - [`RegressionPerformanceMonitor.analyzers()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitor.analyzers)

            - [`RegressionPerformanceMonitor.metrics()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitor.metrics)

            - [`RegressionPerformanceMonitor.monitor_id()`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitor.monitor_id)

            - [`RegressionPerformanceMonitor.options_provider`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitor.options_provider)

        - [`RegressionPerformanceMonitorMetrics`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitorMetrics)

            - [`RegressionPerformanceMonitorMetrics.feature_error_bias`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitorMetrics.feature_error_bias)

            - [`RegressionPerformanceMonitorMetrics.normality`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitorMetrics.normality)

            - [`RegressionPerformanceMonitorMetrics.quality`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitorMetrics.quality)

            - [`RegressionPerformanceMonitorMetrics.underperformance`](api-reference/evidently.model_monitoring.monitors.md#evidently.model_monitoring.monitors.regression_performance.RegressionPerformanceMonitorMetrics.underperformance)

    - [Module contents](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors)


## Submodules

## evidently.model_monitoring.monitoring module


### _class_ evidently.model_monitoring.monitoring.ModelMonitor()
Bases: [`PipelineStage`](api-reference/evidently.pipeline.md#evidently.pipeline.stage.PipelineStage)


#### _abstract_ analyzers()

#### calculate(reference_data: DataFrame, current_data: DataFrame, column_mapping: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), analyzers_results: Dict[Type[Analyzer], Any])

#### _abstract_ metrics(analyzer_results)

#### _abstract_ monitor_id()

#### options_provider(_: [OptionsProvider](api-reference/evidently.options.md#evidently.options.OptionsProvider_ )

### _class_ evidently.model_monitoring.monitoring.ModelMonitoring(monitors: Sequence[ModelMonitor], options: Optional[list] = None)
Bases: [`Pipeline`](api-reference/evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline)


#### analyzers_results(_: Dict[Type[Analyzer], object_ )

#### get_analyzers()

#### metrics()

#### options_provider(_: [OptionsProvider](api-reference/evidently.options.md#evidently.options.OptionsProvider_ )

#### stages(_: Sequence[[PipelineStage](api-reference/evidently.pipeline.md#evidently.pipeline.stage.PipelineStage)_ )

### _class_ evidently.model_monitoring.monitoring.ModelMonitoringMetric(name: str, labels: Optional[List[str]] = None)
Bases: `object`


#### create(value: float, labels: Optional[Dict[str, str]] = None)
## Module contents
