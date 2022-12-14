# evidently.metrics package

Available metrics for Reports and Tests.
All metrics is grouped into modules.
For specific group see module documentation.

## Subpackages

- [evidently.metrics.classification_performance package](evidently.metrics.classification_performance.md)

    - [Submodules](evidently.metrics.classification_performance.md#submodules)

    - [base_classification_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.base_classification_metric)

        - [`ThresholdClassificationMetric`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.base_classification_metric.ThresholdClassificationMetric)

            - [`ThresholdClassificationMetric.get_target_prediction_data()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.base_classification_metric.ThresholdClassificationMetric.get_target_prediction_data)

            - [`ThresholdClassificationMetric.k`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.base_classification_metric.ThresholdClassificationMetric.k)

            - [`ThresholdClassificationMetric.probas_threshold`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.base_classification_metric.ThresholdClassificationMetric.probas_threshold)

    - [class_balance_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.class_balance_metric)

        - [`ClassificationClassBalance`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalance)

            - [`ClassificationClassBalance.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalance.calculate)

        - [`ClassificationClassBalanceRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer)

            - [`ClassificationClassBalanceRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer.color_options)

            - [`ClassificationClassBalanceRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer.render_html)

            - [`ClassificationClassBalanceRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer.render_json)

        - [`ClassificationClassBalanceResult`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceResult)

            - [`ClassificationClassBalanceResult.plot_data`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceResult.plot_data)

    - [class_separation_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.class_separation_metric)

        - [`ClassificationClassSeparationPlot`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlot)

            - [`ClassificationClassSeparationPlot.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlot.calculate)

        - [`ClassificationClassSeparationPlotRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer)

            - [`ClassificationClassSeparationPlotRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer.color_options)

            - [`ClassificationClassSeparationPlotRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer.render_html)

            - [`ClassificationClassSeparationPlotRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer.render_json)

        - [`ClassificationClassSeparationPlotResults`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults)

            - [`ClassificationClassSeparationPlotResults.current_plot`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults.current_plot)

            - [`ClassificationClassSeparationPlotResults.reference_plot`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults.reference_plot)

            - [`ClassificationClassSeparationPlotResults.target_name`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults.target_name)

    - [classification_dummy_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.classification_dummy_metric)

        - [`ClassificationDummyMetric`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)

            - [`ClassificationDummyMetric.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric.calculate)

            - [`ClassificationDummyMetric.correction_for_threshold()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric.correction_for_threshold)

            - [`ClassificationDummyMetric.quality_metric`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric.quality_metric)

        - [`ClassificationDummyMetricRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricRenderer)

            - [`ClassificationDummyMetricRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricRenderer.color_options)

            - [`ClassificationDummyMetricRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricRenderer.render_html)

            - [`ClassificationDummyMetricRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricRenderer.render_json)

        - [`ClassificationDummyMetricResults`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricResults)

            - [`ClassificationDummyMetricResults.by_reference_dummy`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricResults.by_reference_dummy)

            - [`ClassificationDummyMetricResults.dummy`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricResults.dummy)

            - [`ClassificationDummyMetricResults.metrics_matrix`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricResults.metrics_matrix)

            - [`ClassificationDummyMetricResults.model_quality`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetricResults.model_quality)

    - [classification_quality_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.classification_quality_metric)

        - [`ClassificationQualityMetric`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)

            - [`ClassificationQualityMetric.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric.calculate)

            - [`ClassificationQualityMetric.confusion_matrix_metric`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric.confusion_matrix_metric)

        - [`ClassificationQualityMetricRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer)

            - [`ClassificationQualityMetricRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer.color_options)

            - [`ClassificationQualityMetricRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer.render_html)

            - [`ClassificationQualityMetricRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer.render_json)

        - [`ClassificationQualityMetricResult`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult)

            - [`ClassificationQualityMetricResult.current`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult.current)

            - [`ClassificationQualityMetricResult.reference`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult.reference)

            - [`ClassificationQualityMetricResult.target_name`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult.target_name)

    - [confusion_matrix_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.confusion_matrix_metric)

        - [`ClassificationConfusionMatrix`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)

            - [`ClassificationConfusionMatrix.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix.calculate)

            - [`ClassificationConfusionMatrix.k`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix.k)

            - [`ClassificationConfusionMatrix.probas_threshold`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix.probas_threshold)

        - [`ClassificationConfusionMatrixRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer)

            - [`ClassificationConfusionMatrixRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer.color_options)

            - [`ClassificationConfusionMatrixRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer.render_html)

            - [`ClassificationConfusionMatrixRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer.render_json)

        - [`ClassificationConfusionMatrixResult`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixResult)

            - [`ClassificationConfusionMatrixResult.current_matrix`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixResult.current_matrix)

            - [`ClassificationConfusionMatrixResult.reference_matrix`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixResult.reference_matrix)

    - [pr_curve_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.pr_curve_metric)

        - [`ClassificationPRCurve`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurve)

            - [`ClassificationPRCurve.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurve.calculate)

            - [`ClassificationPRCurve.calculate_metrics()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurve.calculate_metrics)

        - [`ClassificationPRCurveRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer)

            - [`ClassificationPRCurveRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer.color_options)

            - [`ClassificationPRCurveRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer.render_html)

            - [`ClassificationPRCurveRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer.render_json)

        - [`ClassificationPRCurveResults`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveResults)

            - [`ClassificationPRCurveResults.current_pr_curve`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveResults.current_pr_curve)

            - [`ClassificationPRCurveResults.reference_pr_curve`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveResults.reference_pr_curve)

    - [pr_table_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.pr_table_metric)

        - [`ClassificationPRTable`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTable)

            - [`ClassificationPRTable.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTable.calculate)

            - [`ClassificationPRTable.calculate_metrics()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTable.calculate_metrics)

        - [`ClassificationPRTableRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer)

            - [`ClassificationPRTableRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer.color_options)

            - [`ClassificationPRTableRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer.render_html)

            - [`ClassificationPRTableRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer.render_json)

        - [`ClassificationPRTableResults`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableResults)

            - [`ClassificationPRTableResults.current_pr_table`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableResults.current_pr_table)

            - [`ClassificationPRTableResults.reference_pr_table`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableResults.reference_pr_table)

    - [probability_distribution_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.probability_distribution_metric)

        - [`ClassificationProbDistribution`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistribution)

            - [`ClassificationProbDistribution.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistribution.calculate)

            - [`ClassificationProbDistribution.get_distribution()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistribution.get_distribution)

        - [`ClassificationProbDistributionRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer)

            - [`ClassificationProbDistributionRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer.color_options)

            - [`ClassificationProbDistributionRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer.render_html)

            - [`ClassificationProbDistributionRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer.render_json)

        - [`ClassificationProbDistributionResults`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionResults)

            - [`ClassificationProbDistributionResults.current_distribution`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionResults.current_distribution)

            - [`ClassificationProbDistributionResults.reference_distribution`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionResults.reference_distribution)

    - [quality_by_class_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.quality_by_class_metric)

        - [`ClassificationQualityByClass`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass)

            - [`ClassificationQualityByClass.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass.calculate)

            - [`ClassificationQualityByClass.k`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass.k)

            - [`ClassificationQualityByClass.probas_threshold`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass.probas_threshold)

        - [`ClassificationQualityByClassRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer)

            - [`ClassificationQualityByClassRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer.color_options)

            - [`ClassificationQualityByClassRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer.render_html)

            - [`ClassificationQualityByClassRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer.render_json)

        - [`ClassificationQualityByClassResult`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult)

            - [`ClassificationQualityByClassResult.columns`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.columns)

            - [`ClassificationQualityByClassResult.current_metrics`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.current_metrics)

            - [`ClassificationQualityByClassResult.current_roc_aucs`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.current_roc_aucs)

            - [`ClassificationQualityByClassResult.reference_metrics`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.reference_metrics)

            - [`ClassificationQualityByClassResult.reference_roc_aucs`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.reference_roc_aucs)

    - [quality_by_feature_table module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.quality_by_feature_table)

        - [`ClassificationQualityByFeatureTable`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTable)

            - [`ClassificationQualityByFeatureTable.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTable.calculate)

            - [`ClassificationQualityByFeatureTable.columns`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTable.columns)

        - [`ClassificationQualityByFeatureTableRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer)

            - [`ClassificationQualityByFeatureTableRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer.color_options)

            - [`ClassificationQualityByFeatureTableRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer.render_html)

            - [`ClassificationQualityByFeatureTableRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer.render_json)

        - [`ClassificationQualityByFeatureTableResults`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults)

            - [`ClassificationQualityByFeatureTableResults.columns`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.columns)

            - [`ClassificationQualityByFeatureTableResults.curr_predictions`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.curr_predictions)

            - [`ClassificationQualityByFeatureTableResults.current_plot_data`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.current_plot_data)

            - [`ClassificationQualityByFeatureTableResults.ref_predictions`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.ref_predictions)

            - [`ClassificationQualityByFeatureTableResults.reference_plot_data`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.reference_plot_data)

            - [`ClassificationQualityByFeatureTableResults.target_name`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.target_name)

    - [roc_curve_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.roc_curve_metric)

        - [`ClassificationRocCurve`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve)

            - [`ClassificationRocCurve.calculate()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve.calculate)

            - [`ClassificationRocCurve.calculate_metrics()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve.calculate_metrics)

        - [`ClassificationRocCurveRenderer`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer)

            - [`ClassificationRocCurveRenderer.color_options`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer.color_options)

            - [`ClassificationRocCurveRenderer.render_html()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer.render_html)

            - [`ClassificationRocCurveRenderer.render_json()`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer.render_json)

        - [`ClassificationRocCurveResults`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveResults)

            - [`ClassificationRocCurveResults.current_roc_curve`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveResults.current_roc_curve)

            - [`ClassificationRocCurveResults.reference_roc_curve`](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveResults.reference_roc_curve)

- [evidently.metrics.data_drift package](evidently.metrics.data_drift.md)

    - [Submodules](evidently.metrics.data_drift.md#submodules)

    - [column_drift_metric module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.column_drift_metric)

        - [`ColumnDriftMetric`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric)

            - [`ColumnDriftMetric.calculate()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric.calculate)

            - [`ColumnDriftMetric.column_name`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric.column_name)

            - [`ColumnDriftMetric.get_parameters()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric.get_parameters)

            - [`ColumnDriftMetric.stattest`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric.stattest)

            - [`ColumnDriftMetric.stattest_threshold`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric.stattest_threshold)

        - [`ColumnDriftMetricRenderer`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer)

            - [`ColumnDriftMetricRenderer.color_options`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer.color_options)

            - [`ColumnDriftMetricRenderer.render_html()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer.render_html)

            - [`ColumnDriftMetricRenderer.render_json()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer.render_json)

        - [`ColumnDriftMetricResults`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults)

            - [`ColumnDriftMetricResults.column_name`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.column_name)

            - [`ColumnDriftMetricResults.column_type`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.column_type)

            - [`ColumnDriftMetricResults.current_distribution`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.current_distribution)

            - [`ColumnDriftMetricResults.current_scatter`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.current_scatter)

            - [`ColumnDriftMetricResults.drift_detected`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.drift_detected)

            - [`ColumnDriftMetricResults.drift_score`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.drift_score)

            - [`ColumnDriftMetricResults.plot_shape`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.plot_shape)

            - [`ColumnDriftMetricResults.reference_distribution`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.reference_distribution)

            - [`ColumnDriftMetricResults.stattest_name`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.stattest_name)

            - [`ColumnDriftMetricResults.stattest_threshold`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.stattest_threshold)

            - [`ColumnDriftMetricResults.x_name`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.x_name)

    - [column_value_plot module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.column_value_plot)

        - [`ColumnValuePlot`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlot)

            - [`ColumnValuePlot.calculate()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlot.calculate)

            - [`ColumnValuePlot.column_name`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlot.column_name)

        - [`ColumnValuePlotRenderer`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotRenderer)

            - [`ColumnValuePlotRenderer.color_options`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotRenderer.color_options)

            - [`ColumnValuePlotRenderer.render_html()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotRenderer.render_html)

            - [`ColumnValuePlotRenderer.render_json()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotRenderer.render_json)

        - [`ColumnValuePlotResults`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults)

            - [`ColumnValuePlotResults.column_name`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults.column_name)

            - [`ColumnValuePlotResults.current_scatter`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults.current_scatter)

            - [`ColumnValuePlotResults.datetime_column_name`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults.datetime_column_name)

            - [`ColumnValuePlotResults.reference_scatter`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults.reference_scatter)

    - [data_drift_table module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.data_drift_table)

        - [`DataDriftTable`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)

            - [`DataDriftTable.calculate()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable.calculate)

            - [`DataDriftTable.columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable.columns)

            - [`DataDriftTable.get_parameters()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable.get_parameters)

            - [`DataDriftTable.options`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable.options)

        - [`DataDriftTableRenderer`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer)

            - [`DataDriftTableRenderer.color_options`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer.color_options)

            - [`DataDriftTableRenderer.render_html()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer.render_html)

            - [`DataDriftTableRenderer.render_json()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer.render_json)

        - [`DataDriftTableResults`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults)

            - [`DataDriftTableResults.dataset_columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.dataset_columns)

            - [`DataDriftTableResults.dataset_drift`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.dataset_drift)

            - [`DataDriftTableResults.drift_by_columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.drift_by_columns)

            - [`DataDriftTableResults.number_of_columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.number_of_columns)

            - [`DataDriftTableResults.number_of_drifted_columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.number_of_drifted_columns)

            - [`DataDriftTableResults.share_of_drifted_columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.share_of_drifted_columns)

    - [dataset_drift_metric module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.dataset_drift_metric)

        - [`DataDriftMetricsRenderer`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer)

            - [`DataDriftMetricsRenderer.color_options`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer.color_options)

            - [`DataDriftMetricsRenderer.render_html()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer.render_html)

            - [`DataDriftMetricsRenderer.render_json()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer.render_json)

        - [`DatasetDriftMetric`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric)

            - [`DatasetDriftMetric.calculate()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.calculate)

            - [`DatasetDriftMetric.columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.columns)

            - [`DatasetDriftMetric.drift_share`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.drift_share)

            - [`DatasetDriftMetric.get_parameters()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.get_parameters)

            - [`DatasetDriftMetric.options`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.options)

        - [`DatasetDriftMetricResults`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults)

            - [`DatasetDriftMetricResults.dataset_drift`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.dataset_drift)

            - [`DatasetDriftMetricResults.drift_share`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.drift_share)

            - [`DatasetDriftMetricResults.number_of_columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.number_of_columns)

            - [`DatasetDriftMetricResults.number_of_drifted_columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.number_of_drifted_columns)

            - [`DatasetDriftMetricResults.share_of_drifted_columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.share_of_drifted_columns)

    - [target_by_features_table module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.target_by_features_table)

        - [`TargetByFeaturesTable`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTable)

            - [`TargetByFeaturesTable.calculate()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTable.calculate)

            - [`TargetByFeaturesTable.columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTable.columns)

        - [`TargetByFeaturesTableRenderer`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer)

            - [`TargetByFeaturesTableRenderer.color_options`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer.color_options)

            - [`TargetByFeaturesTableRenderer.render_html()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer.render_html)

            - [`TargetByFeaturesTableRenderer.render_json()`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer.render_json)

        - [`TargetByFeaturesTableResults`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults)

            - [`TargetByFeaturesTableResults.columns`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.columns)

            - [`TargetByFeaturesTableResults.curr_predictions`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.curr_predictions)

            - [`TargetByFeaturesTableResults.current_plot_data`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.current_plot_data)

            - [`TargetByFeaturesTableResults.ref_predictions`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.ref_predictions)

            - [`TargetByFeaturesTableResults.reference_plot_data`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.reference_plot_data)

            - [`TargetByFeaturesTableResults.target_name`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.target_name)

            - [`TargetByFeaturesTableResults.task`](evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.task)

- [evidently.metrics.data_integrity package](evidently.metrics.data_integrity.md)

    - [Submodules](evidently.metrics.data_integrity.md#submodules)

    - [column_missing_values_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_missing_values_metric)

        - [`ColumnMissingValues`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues)

            - [`ColumnMissingValues.different_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.different_missing_values)

            - [`ColumnMissingValues.number_of_different_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.number_of_different_missing_values)

            - [`ColumnMissingValues.number_of_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.number_of_missing_values)

            - [`ColumnMissingValues.number_of_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.number_of_rows)

            - [`ColumnMissingValues.share_of_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.share_of_missing_values)

        - [`ColumnMissingValuesMetric`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric)

            - [`ColumnMissingValuesMetric.DEFAULT_MISSING_VALUES`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric.DEFAULT_MISSING_VALUES)

            - [`ColumnMissingValuesMetric.calculate()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric.calculate)

            - [`ColumnMissingValuesMetric.column_name`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric.column_name)

            - [`ColumnMissingValuesMetric.missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric.missing_values)

        - [`ColumnMissingValuesMetricRenderer`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer)

            - [`ColumnMissingValuesMetricRenderer.color_options`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer.color_options)

            - [`ColumnMissingValuesMetricRenderer.render_html()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer.render_html)

            - [`ColumnMissingValuesMetricRenderer.render_json()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer.render_json)

        - [`ColumnMissingValuesMetricResult`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult)

            - [`ColumnMissingValuesMetricResult.column_name`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult.column_name)

            - [`ColumnMissingValuesMetricResult.current`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult.current)

            - [`ColumnMissingValuesMetricResult.reference`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult.reference)

    - [column_regexp_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_regexp_metric)

        - [`ColumnRegExpMetric`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric)

            - [`ColumnRegExpMetric.calculate()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric.calculate)

            - [`ColumnRegExpMetric.column_name`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric.column_name)

            - [`ColumnRegExpMetric.reg_exp`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric.reg_exp)

            - [`ColumnRegExpMetric.top`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric.top)

        - [`ColumnRegExpMetricRenderer`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer)

            - [`ColumnRegExpMetricRenderer.color_options`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer.color_options)

            - [`ColumnRegExpMetricRenderer.render_html()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer.render_html)

            - [`ColumnRegExpMetricRenderer.render_json()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer.render_json)

        - [`DataIntegrityValueByRegexpMetricResult`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult)

            - [`DataIntegrityValueByRegexpMetricResult.column_name`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.column_name)

            - [`DataIntegrityValueByRegexpMetricResult.current`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.current)

            - [`DataIntegrityValueByRegexpMetricResult.reference`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.reference)

            - [`DataIntegrityValueByRegexpMetricResult.reg_exp`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.reg_exp)

            - [`DataIntegrityValueByRegexpMetricResult.top`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.top)

        - [`DataIntegrityValueByRegexpStat`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat)

            - [`DataIntegrityValueByRegexpStat.number_of_matched`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.number_of_matched)

            - [`DataIntegrityValueByRegexpStat.number_of_not_matched`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.number_of_not_matched)

            - [`DataIntegrityValueByRegexpStat.number_of_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.number_of_rows)

            - [`DataIntegrityValueByRegexpStat.table_of_matched`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.table_of_matched)

            - [`DataIntegrityValueByRegexpStat.table_of_not_matched`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.table_of_not_matched)

    - [column_summary_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_summary_metric)

        - [`CategoricalCharacteristics`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics)

            - [`CategoricalCharacteristics.count`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.count)

            - [`CategoricalCharacteristics.missing`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.missing)

            - [`CategoricalCharacteristics.missing_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.missing_percentage)

            - [`CategoricalCharacteristics.most_common`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.most_common)

            - [`CategoricalCharacteristics.most_common_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.most_common_percentage)

            - [`CategoricalCharacteristics.new_in_current_values_count`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.new_in_current_values_count)

            - [`CategoricalCharacteristics.number_of_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.number_of_rows)

            - [`CategoricalCharacteristics.unique`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.unique)

            - [`CategoricalCharacteristics.unique_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.unique_percentage)

            - [`CategoricalCharacteristics.unused_in_current_values_count`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.unused_in_current_values_count)

        - [`ColumnSummary`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary)

            - [`ColumnSummary.column_name`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.column_name)

            - [`ColumnSummary.column_type`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.column_type)

            - [`ColumnSummary.current_characteristics`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.current_characteristics)

            - [`ColumnSummary.plot_data`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.plot_data)

            - [`ColumnSummary.reference_characteristics`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.reference_characteristics)

        - [`ColumnSummaryMetric`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)

            - [`ColumnSummaryMetric.calculate()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric.calculate)

            - [`ColumnSummaryMetric.map_data()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric.map_data)

        - [`ColumnSummaryMetricRenderer`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer)

            - [`ColumnSummaryMetricRenderer.color_options`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer.color_options)

            - [`ColumnSummaryMetricRenderer.render_html()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer.render_html)

            - [`ColumnSummaryMetricRenderer.render_json()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer.render_json)

        - [`DataByTarget`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataByTarget)

            - [`DataByTarget.data_for_plots`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataByTarget.data_for_plots)

            - [`DataByTarget.target_name`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataByTarget.target_name)

            - [`DataByTarget.target_type`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataByTarget.target_type)

        - [`DataInTime`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataInTime)

            - [`DataInTime.data_for_plots`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataInTime.data_for_plots)

            - [`DataInTime.datetime_name`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataInTime.datetime_name)

            - [`DataInTime.freq`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataInTime.freq)

        - [`DataQualityPlot`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot)

            - [`DataQualityPlot.bins_for_hist`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot.bins_for_hist)

            - [`DataQualityPlot.counts_of_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot.counts_of_values)

            - [`DataQualityPlot.data_by_target`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot.data_by_target)

            - [`DataQualityPlot.data_in_time`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot.data_in_time)

        - [`DatetimeCharacteristics`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics)

            - [`DatetimeCharacteristics.count`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.count)

            - [`DatetimeCharacteristics.first`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.first)

            - [`DatetimeCharacteristics.last`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.last)

            - [`DatetimeCharacteristics.missing`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.missing)

            - [`DatetimeCharacteristics.missing_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.missing_percentage)

            - [`DatetimeCharacteristics.most_common`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.most_common)

            - [`DatetimeCharacteristics.most_common_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.most_common_percentage)

            - [`DatetimeCharacteristics.number_of_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.number_of_rows)

            - [`DatetimeCharacteristics.unique`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.unique)

            - [`DatetimeCharacteristics.unique_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.unique_percentage)

        - [`NumericCharacteristics`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics)

            - [`NumericCharacteristics.count`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.count)

            - [`NumericCharacteristics.infinite_count`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.infinite_count)

            - [`NumericCharacteristics.infinite_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.infinite_percentage)

            - [`NumericCharacteristics.max`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.max)

            - [`NumericCharacteristics.mean`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.mean)

            - [`NumericCharacteristics.min`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.min)

            - [`NumericCharacteristics.missing`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.missing)

            - [`NumericCharacteristics.missing_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.missing_percentage)

            - [`NumericCharacteristics.most_common`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.most_common)

            - [`NumericCharacteristics.most_common_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.most_common_percentage)

            - [`NumericCharacteristics.number_of_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.number_of_rows)

            - [`NumericCharacteristics.p25`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.p25)

            - [`NumericCharacteristics.p50`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.p50)

            - [`NumericCharacteristics.p75`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.p75)

            - [`NumericCharacteristics.std`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.std)

            - [`NumericCharacteristics.unique`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.unique)

            - [`NumericCharacteristics.unique_percentage`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.unique_percentage)

    - [dataset_missing_values_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.dataset_missing_values_metric)

        - [`DatasetMissingValues`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues)

            - [`DatasetMissingValues.columns_with_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.columns_with_missing_values)

            - [`DatasetMissingValues.different_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.different_missing_values)

            - [`DatasetMissingValues.different_missing_values_by_column`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.different_missing_values_by_column)

            - [`DatasetMissingValues.number_of_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_columns)

            - [`DatasetMissingValues.number_of_columns_with_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_columns_with_missing_values)

            - [`DatasetMissingValues.number_of_different_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_different_missing_values)

            - [`DatasetMissingValues.number_of_different_missing_values_by_column`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_different_missing_values_by_column)

            - [`DatasetMissingValues.number_of_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_missing_values)

            - [`DatasetMissingValues.number_of_missing_values_by_column`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_missing_values_by_column)

            - [`DatasetMissingValues.number_of_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_rows)

            - [`DatasetMissingValues.number_of_rows_with_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_rows_with_missing_values)

            - [`DatasetMissingValues.share_of_columns_with_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.share_of_columns_with_missing_values)

            - [`DatasetMissingValues.share_of_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.share_of_missing_values)

            - [`DatasetMissingValues.share_of_missing_values_by_column`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.share_of_missing_values_by_column)

            - [`DatasetMissingValues.share_of_rows_with_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.share_of_rows_with_missing_values)

        - [`DatasetMissingValuesMetric`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)

            - [`DatasetMissingValuesMetric.DEFAULT_MISSING_VALUES`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric.DEFAULT_MISSING_VALUES)

            - [`DatasetMissingValuesMetric.calculate()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric.calculate)

            - [`DatasetMissingValuesMetric.missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric.missing_values)

        - [`DatasetMissingValuesMetricRenderer`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer)

            - [`DatasetMissingValuesMetricRenderer.color_options`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer.color_options)

            - [`DatasetMissingValuesMetricRenderer.render_html()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer.render_html)

            - [`DatasetMissingValuesMetricRenderer.render_json()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer.render_json)

        - [`DatasetMissingValuesMetricResult`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult)

            - [`DatasetMissingValuesMetricResult.current`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult.current)

            - [`DatasetMissingValuesMetricResult.reference`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult.reference)

    - [dataset_summary_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.dataset_summary_metric)

        - [`DatasetSummary`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary)

            - [`DatasetSummary.columns_type`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.columns_type)

            - [`DatasetSummary.date_column`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.date_column)

            - [`DatasetSummary.id_column`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.id_column)

            - [`DatasetSummary.nans_by_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.nans_by_columns)

            - [`DatasetSummary.number_of_almost_constant_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_almost_constant_columns)

            - [`DatasetSummary.number_of_almost_duplicated_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_almost_duplicated_columns)

            - [`DatasetSummary.number_of_categorical_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_categorical_columns)

            - [`DatasetSummary.number_of_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_columns)

            - [`DatasetSummary.number_of_constant_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_constant_columns)

            - [`DatasetSummary.number_of_datetime_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_datetime_columns)

            - [`DatasetSummary.number_of_duplicated_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_duplicated_columns)

            - [`DatasetSummary.number_of_duplicated_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_duplicated_rows)

            - [`DatasetSummary.number_of_empty_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_empty_columns)

            - [`DatasetSummary.number_of_empty_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_empty_rows)

            - [`DatasetSummary.number_of_missing_values`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_missing_values)

            - [`DatasetSummary.number_of_numeric_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_numeric_columns)

            - [`DatasetSummary.number_of_rows`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_rows)

            - [`DatasetSummary.number_uniques_by_columns`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_uniques_by_columns)

            - [`DatasetSummary.prediction`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.prediction)

            - [`DatasetSummary.target`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.target)

        - [`DatasetSummaryMetric`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)

            - [`DatasetSummaryMetric.almost_constant_threshold`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric.almost_constant_threshold)

            - [`DatasetSummaryMetric.almost_duplicated_threshold`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric.almost_duplicated_threshold)

            - [`DatasetSummaryMetric.calculate()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric.calculate)

        - [`DatasetSummaryMetricRenderer`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer)

            - [`DatasetSummaryMetricRenderer.color_options`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer.color_options)

            - [`DatasetSummaryMetricRenderer.render_html()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer.render_html)

            - [`DatasetSummaryMetricRenderer.render_json()`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer.render_json)

        - [`DatasetSummaryMetricResult`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult)

            - [`DatasetSummaryMetricResult.almost_duplicated_threshold`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult.almost_duplicated_threshold)

            - [`DatasetSummaryMetricResult.current`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult.current)

            - [`DatasetSummaryMetricResult.reference`](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult.reference)

- [evidently.metrics.data_quality package](evidently.metrics.data_quality.md)

    - [Submodules](evidently.metrics.data_quality.md#submodules)

    - [column_correlations_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_correlations_metric)

        - [`ColumnCorrelationsMetric`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetric)

            - [`ColumnCorrelationsMetric.calculate()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetric.calculate)

            - [`ColumnCorrelationsMetric.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetric.column_name)

        - [`ColumnCorrelationsMetricRenderer`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer)

            - [`ColumnCorrelationsMetricRenderer.color_options`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer.color_options)

            - [`ColumnCorrelationsMetricRenderer.render_html()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer.render_html)

            - [`ColumnCorrelationsMetricRenderer.render_json()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer.render_json)

        - [`ColumnCorrelationsMetricResult`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult)

            - [`ColumnCorrelationsMetricResult.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult.column_name)

            - [`ColumnCorrelationsMetricResult.current`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult.current)

            - [`ColumnCorrelationsMetricResult.reference`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult.reference)

    - [column_distribution_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_distribution_metric)

        - [`ColumnDistributionMetric`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetric)

            - [`ColumnDistributionMetric.calculate()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetric.calculate)

            - [`ColumnDistributionMetric.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetric.column_name)

        - [`ColumnDistributionMetricRenderer`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer)

            - [`ColumnDistributionMetricRenderer.color_options`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer.color_options)

            - [`ColumnDistributionMetricRenderer.render_html()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer.render_html)

            - [`ColumnDistributionMetricRenderer.render_json()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer.render_json)

        - [`ColumnDistributionMetricResult`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult)

            - [`ColumnDistributionMetricResult.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult.column_name)

            - [`ColumnDistributionMetricResult.current`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult.current)

            - [`ColumnDistributionMetricResult.reference`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult.reference)

    - [column_quantile_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_quantile_metric)

        - [`ColumnQuantileMetric`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric)

            - [`ColumnQuantileMetric.calculate()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric.calculate)

            - [`ColumnQuantileMetric.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric.column_name)

            - [`ColumnQuantileMetric.quantile`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric.quantile)

        - [`ColumnQuantileMetricRenderer`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer)

            - [`ColumnQuantileMetricRenderer.color_options`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer.color_options)

            - [`ColumnQuantileMetricRenderer.render_html()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer.render_html)

            - [`ColumnQuantileMetricRenderer.render_json()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer.render_json)

        - [`ColumnQuantileMetricResult`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult)

            - [`ColumnQuantileMetricResult.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.column_name)

            - [`ColumnQuantileMetricResult.current`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.current)

            - [`ColumnQuantileMetricResult.current_distribution`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.current_distribution)

            - [`ColumnQuantileMetricResult.quantile`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.quantile)

            - [`ColumnQuantileMetricResult.reference`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.reference)

            - [`ColumnQuantileMetricResult.reference_distribution`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.reference_distribution)

    - [column_value_list_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_value_list_metric)

        - [`ColumnValueListMetric`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)

            - [`ColumnValueListMetric.calculate()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric.calculate)

            - [`ColumnValueListMetric.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric.column_name)

            - [`ColumnValueListMetric.values`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric.values)

        - [`ColumnValueListMetricRenderer`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer)

            - [`ColumnValueListMetricRenderer.color_options`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer.color_options)

            - [`ColumnValueListMetricRenderer.render_html()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer.render_html)

            - [`ColumnValueListMetricRenderer.render_json()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer.render_json)

        - [`ColumnValueListMetricResult`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult)

            - [`ColumnValueListMetricResult.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult.column_name)

            - [`ColumnValueListMetricResult.current`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult.current)

            - [`ColumnValueListMetricResult.reference`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult.reference)

            - [`ColumnValueListMetricResult.values`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult.values)

        - [`ValueListStat`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat)

            - [`ValueListStat.number_in_list`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.number_in_list)

            - [`ValueListStat.number_not_in_list`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.number_not_in_list)

            - [`ValueListStat.rows_count`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.rows_count)

            - [`ValueListStat.share_in_list`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.share_in_list)

            - [`ValueListStat.share_not_in_list`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.share_not_in_list)

            - [`ValueListStat.values_in_list`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.values_in_list)

            - [`ValueListStat.values_not_in_list`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.values_not_in_list)

    - [column_value_range_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_value_range_metric)

        - [`ColumnValueRangeMetric`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)

            - [`ColumnValueRangeMetric.calculate()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric.calculate)

            - [`ColumnValueRangeMetric.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric.column_name)

            - [`ColumnValueRangeMetric.left`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric.left)

            - [`ColumnValueRangeMetric.right`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric.right)

        - [`ColumnValueRangeMetricRenderer`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer)

            - [`ColumnValueRangeMetricRenderer.color_options`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer.color_options)

            - [`ColumnValueRangeMetricRenderer.render_html()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer.render_html)

            - [`ColumnValueRangeMetricRenderer.render_json()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer.render_json)

        - [`ColumnValueRangeMetricResult`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult)

            - [`ColumnValueRangeMetricResult.column_name`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.column_name)

            - [`ColumnValueRangeMetricResult.current`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.current)

            - [`ColumnValueRangeMetricResult.current_distribution`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.current_distribution)

            - [`ColumnValueRangeMetricResult.left`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.left)

            - [`ColumnValueRangeMetricResult.reference`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.reference)

            - [`ColumnValueRangeMetricResult.reference_distribution`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.reference_distribution)

            - [`ColumnValueRangeMetricResult.right`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.right)

        - [`ValuesInRangeStat`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat)

            - [`ValuesInRangeStat.number_in_range`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.number_in_range)

            - [`ValuesInRangeStat.number_not_in_range`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.number_not_in_range)

            - [`ValuesInRangeStat.number_of_values`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.number_of_values)

            - [`ValuesInRangeStat.share_in_range`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.share_in_range)

            - [`ValuesInRangeStat.share_not_in_range`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.share_not_in_range)

    - [dataset_correlations_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.dataset_correlations_metric)

        - [`CorrelationStats`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats)

            - [`CorrelationStats.abs_max_correlation`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.abs_max_correlation)

            - [`CorrelationStats.abs_max_features_correlation`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.abs_max_features_correlation)

            - [`CorrelationStats.abs_max_prediction_features_correlation`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.abs_max_prediction_features_correlation)

            - [`CorrelationStats.abs_max_target_features_correlation`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.abs_max_target_features_correlation)

            - [`CorrelationStats.target_prediction_correlation`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.target_prediction_correlation)

        - [`DataQualityCorrelationMetricsRenderer`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer)

            - [`DataQualityCorrelationMetricsRenderer.color_options`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer.color_options)

            - [`DataQualityCorrelationMetricsRenderer.render_html()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer.render_html)

            - [`DataQualityCorrelationMetricsRenderer.render_json()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer.render_json)

        - [`DatasetCorrelation`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation)

            - [`DatasetCorrelation.correlation`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation.correlation)

            - [`DatasetCorrelation.stats`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation.stats)

        - [`DatasetCorrelationsMetric`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)

            - [`DatasetCorrelationsMetric.calculate()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric.calculate)

        - [`DatasetCorrelationsMetricResult`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetricResult)

            - [`DatasetCorrelationsMetricResult.current`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetricResult.current)

            - [`DatasetCorrelationsMetricResult.reference`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetricResult.reference)

    - [stability_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.stability_metric)

        - [`DataQualityStabilityMetric`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric)

            - [`DataQualityStabilityMetric.calculate()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric.calculate)

        - [`DataQualityStabilityMetricRenderer`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer)

            - [`DataQualityStabilityMetricRenderer.color_options`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer.color_options)

            - [`DataQualityStabilityMetricRenderer.render_html()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer.render_html)

            - [`DataQualityStabilityMetricRenderer.render_json()`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer.render_json)

        - [`DataQualityStabilityMetricResult`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricResult)

            - [`DataQualityStabilityMetricResult.number_not_stable_prediction`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricResult.number_not_stable_prediction)

            - [`DataQualityStabilityMetricResult.number_not_stable_target`](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricResult.number_not_stable_target)

- [evidently.metrics.regression_performance package](evidently.metrics.regression_performance.md)

    - [Submodules](evidently.metrics.regression_performance.md#submodules)

    - [abs_perc_error_in_time module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.abs_perc_error_in_time)

        - [`RegressionAbsPercentageErrorPlot`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlot)

            - [`RegressionAbsPercentageErrorPlot.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlot.calculate)

        - [`RegressionAbsPercentageErrorPlotRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer)

            - [`RegressionAbsPercentageErrorPlotRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer.color_options)

            - [`RegressionAbsPercentageErrorPlotRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer.render_html)

            - [`RegressionAbsPercentageErrorPlotRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer.render_json)

        - [`RegressionAbsPercentageErrorPlotResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults)

            - [`RegressionAbsPercentageErrorPlotResults.current_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults.current_scatter)

            - [`RegressionAbsPercentageErrorPlotResults.reference_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults.reference_scatter)

            - [`RegressionAbsPercentageErrorPlotResults.x_name`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults.x_name)

    - [error_bias_table module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_bias_table)

        - [`RegressionErrorBiasTable`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable)

            - [`RegressionErrorBiasTable.TOP_ERROR_DEFAULT`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.TOP_ERROR_DEFAULT)

            - [`RegressionErrorBiasTable.TOP_ERROR_MAX`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.TOP_ERROR_MAX)

            - [`RegressionErrorBiasTable.TOP_ERROR_MIN`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.TOP_ERROR_MIN)

            - [`RegressionErrorBiasTable.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.calculate)

            - [`RegressionErrorBiasTable.columns`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.columns)

            - [`RegressionErrorBiasTable.top_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.top_error)

        - [`RegressionErrorBiasTableRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer)

            - [`RegressionErrorBiasTableRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer.color_options)

            - [`RegressionErrorBiasTableRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer.render_html)

            - [`RegressionErrorBiasTableRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer.render_json)

        - [`RegressionErrorBiasTableResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults)

            - [`RegressionErrorBiasTableResults.cat_feature_names`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.cat_feature_names)

            - [`RegressionErrorBiasTableResults.columns`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.columns)

            - [`RegressionErrorBiasTableResults.current_plot_data`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.current_plot_data)

            - [`RegressionErrorBiasTableResults.error_bias`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.error_bias)

            - [`RegressionErrorBiasTableResults.num_feature_names`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.num_feature_names)

            - [`RegressionErrorBiasTableResults.prediction_name`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.prediction_name)

            - [`RegressionErrorBiasTableResults.reference_plot_data`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.reference_plot_data)

            - [`RegressionErrorBiasTableResults.target_name`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.target_name)

            - [`RegressionErrorBiasTableResults.top_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.top_error)

    - [error_distribution module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_distribution)

        - [`RegressionErrorDistribution`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistribution)

            - [`RegressionErrorDistribution.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistribution.calculate)

        - [`RegressionErrorDistributionRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer)

            - [`RegressionErrorDistributionRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer.color_options)

            - [`RegressionErrorDistributionRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer.render_html)

            - [`RegressionErrorDistributionRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer.render_json)

        - [`RegressionErrorDistributionResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionResults)

            - [`RegressionErrorDistributionResults.current_bins`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionResults.current_bins)

            - [`RegressionErrorDistributionResults.reference_bins`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionResults.reference_bins)

    - [error_in_time module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_in_time)

        - [`RegressionErrorPlot`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlot)

            - [`RegressionErrorPlot.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlot.calculate)

        - [`RegressionErrorPlotRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer)

            - [`RegressionErrorPlotRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer.color_options)

            - [`RegressionErrorPlotRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer.render_html)

            - [`RegressionErrorPlotRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer.render_json)

        - [`RegressionErrorPlotResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults)

            - [`RegressionErrorPlotResults.current_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults.current_scatter)

            - [`RegressionErrorPlotResults.reference_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults.reference_scatter)

            - [`RegressionErrorPlotResults.x_name`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults.x_name)

    - [error_normality module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_normality)

        - [`RegressionErrorNormality`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormality)

            - [`RegressionErrorNormality.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormality.calculate)

        - [`RegressionErrorNormalityRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer)

            - [`RegressionErrorNormalityRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer.color_options)

            - [`RegressionErrorNormalityRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer.render_html)

            - [`RegressionErrorNormalityRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer.render_json)

        - [`RegressionErrorNormalityResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityResults)

            - [`RegressionErrorNormalityResults.current_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityResults.current_error)

            - [`RegressionErrorNormalityResults.reference_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityResults.reference_error)

    - [predicted_and_actual_in_time module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.predicted_and_actual_in_time)

        - [`RegressionPredictedVsActualPlot`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlot)

            - [`RegressionPredictedVsActualPlot.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlot.calculate)

        - [`RegressionPredictedVsActualPlotRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer)

            - [`RegressionPredictedVsActualPlotRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer.color_options)

            - [`RegressionPredictedVsActualPlotRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer.render_html)

            - [`RegressionPredictedVsActualPlotRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer.render_json)

        - [`RegressionPredictedVsActualPlotResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults)

            - [`RegressionPredictedVsActualPlotResults.current_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults.current_scatter)

            - [`RegressionPredictedVsActualPlotResults.reference_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults.reference_scatter)

            - [`RegressionPredictedVsActualPlotResults.x_name`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults.x_name)

    - [predicted_vs_actual module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.predicted_vs_actual)

        - [`RegressionPredictedVsActualScatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatter)

            - [`RegressionPredictedVsActualScatter.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatter.calculate)

        - [`RegressionPredictedVsActualScatterRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer)

            - [`RegressionPredictedVsActualScatterRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer.color_options)

            - [`RegressionPredictedVsActualScatterRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer.render_html)

            - [`RegressionPredictedVsActualScatterRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer.render_json)

        - [`RegressionPredictedVsActualScatterResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterResults)

            - [`RegressionPredictedVsActualScatterResults.current_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterResults.current_scatter)

            - [`RegressionPredictedVsActualScatterResults.reference_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterResults.reference_scatter)

    - [regression_dummy_metric module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_dummy_metric)

        - [`RegressionDummyMetric`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)

            - [`RegressionDummyMetric.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric.calculate)

            - [`RegressionDummyMetric.quality_metric`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric.quality_metric)

        - [`RegressionDummyMetricRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricRenderer)

            - [`RegressionDummyMetricRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricRenderer.color_options)

            - [`RegressionDummyMetricRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricRenderer.render_html)

            - [`RegressionDummyMetricRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricRenderer.render_json)

        - [`RegressionDummyMetricResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults)

            - [`RegressionDummyMetricResults.abs_error_max`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.abs_error_max)

            - [`RegressionDummyMetricResults.abs_error_max_by_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.abs_error_max_by_ref)

            - [`RegressionDummyMetricResults.abs_error_max_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.abs_error_max_default)

            - [`RegressionDummyMetricResults.mean_abs_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.mean_abs_error)

            - [`RegressionDummyMetricResults.mean_abs_error_by_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.mean_abs_error_by_ref)

            - [`RegressionDummyMetricResults.mean_abs_error_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.mean_abs_error_default)

            - [`RegressionDummyMetricResults.mean_abs_perc_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.mean_abs_perc_error)

            - [`RegressionDummyMetricResults.mean_abs_perc_error_by_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.mean_abs_perc_error_by_ref)

            - [`RegressionDummyMetricResults.mean_abs_perc_error_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.mean_abs_perc_error_default)

            - [`RegressionDummyMetricResults.rmse`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.rmse)

            - [`RegressionDummyMetricResults.rmse_by_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.rmse_by_ref)

            - [`RegressionDummyMetricResults.rmse_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetricResults.rmse_default)

    - [regression_performance_metrics module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_performance_metrics)

        - [`RegressionPerformanceMetrics`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetrics)

            - [`RegressionPerformanceMetrics.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetrics.calculate)

            - [`RegressionPerformanceMetrics.get_parameters()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetrics.get_parameters)

        - [`RegressionPerformanceMetricsRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer)

            - [`RegressionPerformanceMetricsRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer.color_options)

            - [`RegressionPerformanceMetricsRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer.render_html)

            - [`RegressionPerformanceMetricsRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer.render_json)

        - [`RegressionPerformanceMetricsResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults)

            - [`RegressionPerformanceMetricsResults.abs_error_max`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_error_max)

            - [`RegressionPerformanceMetricsResults.abs_error_max_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_error_max_default)

            - [`RegressionPerformanceMetricsResults.abs_error_max_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_error_max_ref)

            - [`RegressionPerformanceMetricsResults.abs_error_std`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_error_std)

            - [`RegressionPerformanceMetricsResults.abs_perc_error_std`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_perc_error_std)

            - [`RegressionPerformanceMetricsResults.columns`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.columns)

            - [`RegressionPerformanceMetricsResults.error_bias`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.error_bias)

            - [`RegressionPerformanceMetricsResults.error_normality`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.error_normality)

            - [`RegressionPerformanceMetricsResults.error_std`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.error_std)

            - [`RegressionPerformanceMetricsResults.hist_for_plot`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.hist_for_plot)

            - [`RegressionPerformanceMetricsResults.me_default_sigma`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.me_default_sigma)

            - [`RegressionPerformanceMetricsResults.me_hist_for_plot`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.me_hist_for_plot)

            - [`RegressionPerformanceMetricsResults.mean_abs_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_error)

            - [`RegressionPerformanceMetricsResults.mean_abs_error_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_error_default)

            - [`RegressionPerformanceMetricsResults.mean_abs_error_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_error_ref)

            - [`RegressionPerformanceMetricsResults.mean_abs_perc_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_perc_error)

            - [`RegressionPerformanceMetricsResults.mean_abs_perc_error_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_perc_error_default)

            - [`RegressionPerformanceMetricsResults.mean_abs_perc_error_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_perc_error_ref)

            - [`RegressionPerformanceMetricsResults.mean_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_error)

            - [`RegressionPerformanceMetricsResults.mean_error_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_error_ref)

            - [`RegressionPerformanceMetricsResults.r2_score`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.r2_score)

            - [`RegressionPerformanceMetricsResults.r2_score_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.r2_score_ref)

            - [`RegressionPerformanceMetricsResults.rmse`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.rmse)

            - [`RegressionPerformanceMetricsResults.rmse_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.rmse_default)

            - [`RegressionPerformanceMetricsResults.rmse_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.rmse_ref)

            - [`RegressionPerformanceMetricsResults.underperformance`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.underperformance)

            - [`RegressionPerformanceMetricsResults.underperformance_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.underperformance_ref)

            - [`RegressionPerformanceMetricsResults.vals_for_plots`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.vals_for_plots)

    - [regression_quality module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_quality)

        - [`RegressionQualityMetric`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)

            - [`RegressionQualityMetric.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric.calculate)

        - [`RegressionQualityMetricRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer)

            - [`RegressionQualityMetricRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer.color_options)

            - [`RegressionQualityMetricRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer.render_html)

            - [`RegressionQualityMetricRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer.render_json)

        - [`RegressionQualityMetricResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults)

            - [`RegressionQualityMetricResults.abs_error_max`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_max)

            - [`RegressionQualityMetricResults.abs_error_max_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_max_default)

            - [`RegressionQualityMetricResults.abs_error_max_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_max_ref)

            - [`RegressionQualityMetricResults.abs_error_std`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_std)

            - [`RegressionQualityMetricResults.abs_error_std_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_std_ref)

            - [`RegressionQualityMetricResults.abs_perc_error_std`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_perc_error_std)

            - [`RegressionQualityMetricResults.abs_perc_error_std_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_perc_error_std_ref)

            - [`RegressionQualityMetricResults.columns`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.columns)

            - [`RegressionQualityMetricResults.error_bias`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.error_bias)

            - [`RegressionQualityMetricResults.error_normality`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.error_normality)

            - [`RegressionQualityMetricResults.error_std`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.error_std)

            - [`RegressionQualityMetricResults.error_std_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.error_std_ref)

            - [`RegressionQualityMetricResults.hist_for_plot`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.hist_for_plot)

            - [`RegressionQualityMetricResults.me_default_sigma`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.me_default_sigma)

            - [`RegressionQualityMetricResults.me_hist_for_plot`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.me_hist_for_plot)

            - [`RegressionQualityMetricResults.mean_abs_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_error)

            - [`RegressionQualityMetricResults.mean_abs_error_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_error_default)

            - [`RegressionQualityMetricResults.mean_abs_error_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_error_ref)

            - [`RegressionQualityMetricResults.mean_abs_perc_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_perc_error)

            - [`RegressionQualityMetricResults.mean_abs_perc_error_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_perc_error_default)

            - [`RegressionQualityMetricResults.mean_abs_perc_error_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_perc_error_ref)

            - [`RegressionQualityMetricResults.mean_error`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_error)

            - [`RegressionQualityMetricResults.mean_error_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_error_ref)

            - [`RegressionQualityMetricResults.r2_score`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.r2_score)

            - [`RegressionQualityMetricResults.r2_score_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.r2_score_ref)

            - [`RegressionQualityMetricResults.rmse`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.rmse)

            - [`RegressionQualityMetricResults.rmse_default`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.rmse_default)

            - [`RegressionQualityMetricResults.rmse_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.rmse_ref)

            - [`RegressionQualityMetricResults.underperformance`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.underperformance)

            - [`RegressionQualityMetricResults.underperformance_ref`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.underperformance_ref)

            - [`RegressionQualityMetricResults.vals_for_plots`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.vals_for_plots)

    - [top_error module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.top_error)

        - [`RegressionTopErrorMetric`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetric)

            - [`RegressionTopErrorMetric.calculate()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetric.calculate)

        - [`RegressionTopErrorMetricRenderer`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer)

            - [`RegressionTopErrorMetricRenderer.color_options`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer.color_options)

            - [`RegressionTopErrorMetricRenderer.render_html()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer.render_html)

            - [`RegressionTopErrorMetricRenderer.render_json()`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer.render_json)

        - [`RegressionTopErrorMetricResults`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults)

            - [`RegressionTopErrorMetricResults.curr_mean_err_per_group`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults.curr_mean_err_per_group)

            - [`RegressionTopErrorMetricResults.curr_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults.curr_scatter)

            - [`RegressionTopErrorMetricResults.ref_mean_err_per_group`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults.ref_mean_err_per_group)

            - [`RegressionTopErrorMetricResults.ref_scatter`](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults.ref_scatter)


## Submodules

## <a name="module-evidently.metrics.base_metric"></a>base_metric module


### class ErrorResult(exception: BaseException)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; exception : BaseException 

### class InputData(reference_data: Optional[pandas.core.frame.DataFrame], current_data: pandas.core.frame.DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), data_definition: [DataDefinition](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition))
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_mapping : [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping) 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_data : DataFrame 

##### &nbsp;&nbsp;&nbsp;&nbsp; data_definition : [DataDefinition](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition) 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_data : Optional[DataFrame] 

### class Metric()
Bases: `Generic`[`TResult`]

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; context  = None 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  calculate(data: InputData)

##### &nbsp;&nbsp;&nbsp;&nbsp; get_id()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_parameters()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_result()

##### &nbsp;&nbsp;&nbsp;&nbsp; set_context(context)

### generate_column_metrics(metric_class: Type[Metric], columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None, skip_id_column: bool = False)
Function for generating metrics for columns

## <a name="module-evidently.metrics.utils"></a>utils module


### apply_func_to_binned_data(df_for_bins, func, target_column, preds_column, is_ref_data=False)

### make_target_bins_for_reg_plots(curr: DataFrame, target_column, preds_column, ref: Optional[DataFrame] = None)
