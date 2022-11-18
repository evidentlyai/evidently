# evidently.metrics package

## Subpackages

- [evidently.metrics.classification_performance package](evidently.metrics.classification_performance.md)

    - [Submodules](api-reference/evidently.metrics.classification_performance.md#submodules)

    - [evidently.metrics.classification_performance.base_classification_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.base_classification_metric)

        - [`ThresholdClassificationMetric`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.base_classification_metric.ThresholdClassificationMetric)

            - [`ThresholdClassificationMetric.get_target_prediction_data()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.base_classification_metric.ThresholdClassificationMetric.get_target_prediction_data)

    - [evidently.metrics.classification_performance.class_balance_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.class_balance_metric)

        - [`ClassificationClassBalance`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalance)

            - [`ClassificationClassBalance.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalance.calculate)

        - [`ClassificationClassBalanceRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer)

            - [`ClassificationClassBalanceRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer.color_options)

            - [`ClassificationClassBalanceRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer.render_html)

            - [`ClassificationClassBalanceRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceRenderer.render_json)

        - [`ClassificationClassBalanceResult`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceResult)

            - [`ClassificationClassBalanceResult.plot_data`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_balance_metric.ClassificationClassBalanceResult.plot_data)

    - [evidently.metrics.classification_performance.class_separation_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.class_separation_metric)

        - [`ClassificationClassSeparationPlot`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlot)

            - [`ClassificationClassSeparationPlot.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlot.calculate)

        - [`ClassificationClassSeparationPlotRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer)

            - [`ClassificationClassSeparationPlotRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer.color_options)

            - [`ClassificationClassSeparationPlotRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer.render_html)

            - [`ClassificationClassSeparationPlotRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotRenderer.render_json)

        - [`ClassificationClassSeparationPlotResults`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults)

            - [`ClassificationClassSeparationPlotResults.current_plot`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults.current_plot)

            - [`ClassificationClassSeparationPlotResults.reference_plot`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults.reference_plot)

            - [`ClassificationClassSeparationPlotResults.target_name`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.class_separation_metric.ClassificationClassSeparationPlotResults.target_name)

    - [evidently.metrics.classification_performance.classification_quality_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.classification_quality_metric)

        - [`ClassificationQualityMetric`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)

            - [`ClassificationQualityMetric.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric.calculate)

            - [`ClassificationQualityMetric.calculate_metrics()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric.calculate_metrics)

            - [`ClassificationQualityMetric.confusion_matrix_metric`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric.confusion_matrix_metric)

        - [`ClassificationQualityMetricRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer)

            - [`ClassificationQualityMetricRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer.color_options)

            - [`ClassificationQualityMetricRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer.render_html)

            - [`ClassificationQualityMetricRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricRenderer.render_json)

        - [`ClassificationQualityMetricResult`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult)

            - [`ClassificationQualityMetricResult.current`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult.current)

            - [`ClassificationQualityMetricResult.reference`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult.reference)

            - [`ClassificationQualityMetricResult.target_name`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetricResult.target_name)

        - [`DatasetClassificationQuality`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality)

            - [`DatasetClassificationQuality.accuracy`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.accuracy)

            - [`DatasetClassificationQuality.f1`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.f1)

            - [`DatasetClassificationQuality.fnr`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.fnr)

            - [`DatasetClassificationQuality.fpr`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.fpr)

            - [`DatasetClassificationQuality.log_loss`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.log_loss)

            - [`DatasetClassificationQuality.precision`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.precision)

            - [`DatasetClassificationQuality.recall`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.recall)

            - [`DatasetClassificationQuality.roc_auc`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.roc_auc)

            - [`DatasetClassificationQuality.tnr`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.tnr)

            - [`DatasetClassificationQuality.tpr`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.DatasetClassificationQuality.tpr)

    - [evidently.metrics.classification_performance.confusion_matrix_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.confusion_matrix_metric)

        - [`ClassificationConfusionMatrix`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)

            - [`ClassificationConfusionMatrix.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix.calculate)

        - [`ClassificationConfusionMatrixRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer)

            - [`ClassificationConfusionMatrixRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer.color_options)

            - [`ClassificationConfusionMatrixRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer.render_html)

            - [`ClassificationConfusionMatrixRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixRenderer.render_json)

        - [`ClassificationConfusionMatrixResult`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixResult)

            - [`ClassificationConfusionMatrixResult.current_matrix`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixResult.current_matrix)

            - [`ClassificationConfusionMatrixResult.reference_matrix`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrixResult.reference_matrix)

    - [evidently.metrics.classification_performance.pr_curve_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.pr_curve_metric)

        - [`ClassificationPRCurve`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurve)

            - [`ClassificationPRCurve.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurve.calculate)

            - [`ClassificationPRCurve.calculate_metrics()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurve.calculate_metrics)

        - [`ClassificationPRCurveRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer)

            - [`ClassificationPRCurveRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer.color_options)

            - [`ClassificationPRCurveRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer.render_html)

            - [`ClassificationPRCurveRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveRenderer.render_json)

        - [`ClassificationPRCurveResults`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveResults)

            - [`ClassificationPRCurveResults.current_pr_curve`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveResults.current_pr_curve)

            - [`ClassificationPRCurveResults.reference_pr_curve`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_curve_metric.ClassificationPRCurveResults.reference_pr_curve)

    - [evidently.metrics.classification_performance.pr_table_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.pr_table_metric)

        - [`ClassificationPRTable`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTable)

            - [`ClassificationPRTable.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTable.calculate)

            - [`ClassificationPRTable.calculate_metrics()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTable.calculate_metrics)

        - [`ClassificationPRTableRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer)

            - [`ClassificationPRTableRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer.color_options)

            - [`ClassificationPRTableRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer.render_html)

            - [`ClassificationPRTableRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableRenderer.render_json)

        - [`ClassificationPRTableResults`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableResults)

            - [`ClassificationPRTableResults.current_pr_table`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableResults.current_pr_table)

            - [`ClassificationPRTableResults.reference_pr_table`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.pr_table_metric.ClassificationPRTableResults.reference_pr_table)

    - [evidently.metrics.classification_performance.probability_distribution_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.probability_distribution_metric)

        - [`ClassificationProbDistribution`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistribution)

            - [`ClassificationProbDistribution.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistribution.calculate)

            - [`ClassificationProbDistribution.get_distribution()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistribution.get_distribution)

        - [`ClassificationProbDistributionRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer)

            - [`ClassificationProbDistributionRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer.color_options)

            - [`ClassificationProbDistributionRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer.render_html)

            - [`ClassificationProbDistributionRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionRenderer.render_json)

        - [`ClassificationProbDistributionResults`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionResults)

            - [`ClassificationProbDistributionResults.current_distribution`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionResults.current_distribution)

            - [`ClassificationProbDistributionResults.reference_distribution`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.probability_distribution_metric.ClassificationProbDistributionResults.reference_distribution)

    - [evidently.metrics.classification_performance.quality_by_class_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.quality_by_class_metric)

        - [`ClassificationQualityByClass`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass)

            - [`ClassificationQualityByClass.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass.calculate)

        - [`ClassificationQualityByClassRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer)

            - [`ClassificationQualityByClassRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer.color_options)

            - [`ClassificationQualityByClassRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer.render_html)

            - [`ClassificationQualityByClassRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassRenderer.render_json)

        - [`ClassificationQualityByClassResult`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult)

            - [`ClassificationQualityByClassResult.columns`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.columns)

            - [`ClassificationQualityByClassResult.current_metrics`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.current_metrics)

            - [`ClassificationQualityByClassResult.current_roc_aucs`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.current_roc_aucs)

            - [`ClassificationQualityByClassResult.reference_metrics`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.reference_metrics)

            - [`ClassificationQualityByClassResult.reference_roc_aucs`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClassResult.reference_roc_aucs)

    - [evidently.metrics.classification_performance.quality_by_feature_table module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.quality_by_feature_table)

        - [`ClassificationQualityByFeatureTable`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTable)

            - [`ClassificationQualityByFeatureTable.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTable.calculate)

            - [`ClassificationQualityByFeatureTable.columns`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTable.columns)

        - [`ClassificationQualityByFeatureTableRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer)

            - [`ClassificationQualityByFeatureTableRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer.color_options)

            - [`ClassificationQualityByFeatureTableRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer.render_html)

            - [`ClassificationQualityByFeatureTableRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableRenderer.render_json)

        - [`ClassificationQualityByFeatureTableResults`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults)

            - [`ClassificationQualityByFeatureTableResults.columns`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.columns)

            - [`ClassificationQualityByFeatureTableResults.curr_predictions`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.curr_predictions)

            - [`ClassificationQualityByFeatureTableResults.current_plot_data`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.current_plot_data)

            - [`ClassificationQualityByFeatureTableResults.ref_predictions`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.ref_predictions)

            - [`ClassificationQualityByFeatureTableResults.reference_plot_data`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.reference_plot_data)

            - [`ClassificationQualityByFeatureTableResults.target_name`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_feature_table.ClassificationQualityByFeatureTableResults.target_name)

    - [evidently.metrics.classification_performance.roc_curve_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.roc_curve_metric)

        - [`ClassificationRocCurve`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve)

            - [`ClassificationRocCurve.calculate()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve.calculate)

            - [`ClassificationRocCurve.calculate_metrics()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve.calculate_metrics)

        - [`ClassificationRocCurveRenderer`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer)

            - [`ClassificationRocCurveRenderer.color_options`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer.color_options)

            - [`ClassificationRocCurveRenderer.render_html()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer.render_html)

            - [`ClassificationRocCurveRenderer.render_json()`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveRenderer.render_json)

        - [`ClassificationRocCurveResults`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveResults)

            - [`ClassificationRocCurveResults.current_roc_curve`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveResults.current_roc_curve)

            - [`ClassificationRocCurveResults.reference_roc_curve`](api-reference/evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurveResults.reference_roc_curve)

    - [Module contents](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance)

- [evidently.metrics.data_drift package](evidently.metrics.data_drift.md)

    - [Submodules](api-reference/evidently.metrics.data_drift.md#submodules)

    - [evidently.metrics.data_drift.column_drift_metric module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.column_drift_metric)

        - [`ColumnDriftMetric`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric)

            - [`ColumnDriftMetric.calculate()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric.calculate)

            - [`ColumnDriftMetric.column_name`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric.column_name)

            - [`ColumnDriftMetric.options`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric.options)

        - [`ColumnDriftMetricRenderer`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer)

            - [`ColumnDriftMetricRenderer.color_options`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer.color_options)

            - [`ColumnDriftMetricRenderer.render_html()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer.render_html)

            - [`ColumnDriftMetricRenderer.render_json()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricRenderer.render_json)

        - [`ColumnDriftMetricResults`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults)

            - [`ColumnDriftMetricResults.column_name`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.column_name)

            - [`ColumnDriftMetricResults.column_type`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.column_type)

            - [`ColumnDriftMetricResults.current_distribution`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.current_distribution)

            - [`ColumnDriftMetricResults.current_scatter`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.current_scatter)

            - [`ColumnDriftMetricResults.drift_detected`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.drift_detected)

            - [`ColumnDriftMetricResults.drift_score`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.drift_score)

            - [`ColumnDriftMetricResults.plot_shape`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.plot_shape)

            - [`ColumnDriftMetricResults.reference_distribution`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.reference_distribution)

            - [`ColumnDriftMetricResults.stattest_name`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.stattest_name)

            - [`ColumnDriftMetricResults.threshold`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.threshold)

            - [`ColumnDriftMetricResults.x_name`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetricResults.x_name)

    - [evidently.metrics.data_drift.column_value_plot module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.column_value_plot)

        - [`ColumnValuePlot`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlot)

            - [`ColumnValuePlot.calculate()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlot.calculate)

            - [`ColumnValuePlot.column_name`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlot.column_name)

        - [`ColumnValuePlotRenderer`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotRenderer)

            - [`ColumnValuePlotRenderer.color_options`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotRenderer.color_options)

            - [`ColumnValuePlotRenderer.render_html()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotRenderer.render_html)

        - [`ColumnValuePlotResults`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults)

            - [`ColumnValuePlotResults.column_name`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults.column_name)

            - [`ColumnValuePlotResults.current_scatter`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults.current_scatter)

            - [`ColumnValuePlotResults.datetime_column_name`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults.datetime_column_name)

            - [`ColumnValuePlotResults.reference_scatter`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_value_plot.ColumnValuePlotResults.reference_scatter)

    - [evidently.metrics.data_drift.data_drift_table module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.data_drift_table)

        - [`DataDriftTable`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)

            - [`DataDriftTable.calculate()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable.calculate)

            - [`DataDriftTable.columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable.columns)

            - [`DataDriftTable.get_parameters()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable.get_parameters)

            - [`DataDriftTable.options`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable.options)

        - [`DataDriftTableRenderer`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer)

            - [`DataDriftTableRenderer.color_options`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer.color_options)

            - [`DataDriftTableRenderer.render_html()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer.render_html)

            - [`DataDriftTableRenderer.render_json()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableRenderer.render_json)

        - [`DataDriftTableResults`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults)

            - [`DataDriftTableResults.dataset_columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.dataset_columns)

            - [`DataDriftTableResults.dataset_drift`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.dataset_drift)

            - [`DataDriftTableResults.drift_by_columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.drift_by_columns)

            - [`DataDriftTableResults.number_of_columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.number_of_columns)

            - [`DataDriftTableResults.number_of_drifted_columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.number_of_drifted_columns)

            - [`DataDriftTableResults.share_of_drifted_columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTableResults.share_of_drifted_columns)

    - [evidently.metrics.data_drift.dataset_drift_metric module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.dataset_drift_metric)

        - [`DataDriftMetricsRenderer`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer)

            - [`DataDriftMetricsRenderer.color_options`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer.color_options)

            - [`DataDriftMetricsRenderer.render_html()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer.render_html)

            - [`DataDriftMetricsRenderer.render_json()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DataDriftMetricsRenderer.render_json)

        - [`DatasetDriftMetric`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric)

            - [`DatasetDriftMetric.calculate()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.calculate)

            - [`DatasetDriftMetric.columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.columns)

            - [`DatasetDriftMetric.get_parameters()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.get_parameters)

            - [`DatasetDriftMetric.options`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.options)

            - [`DatasetDriftMetric.threshold`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetric.threshold)

        - [`DatasetDriftMetricResults`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults)

            - [`DatasetDriftMetricResults.dataset_drift`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.dataset_drift)

            - [`DatasetDriftMetricResults.number_of_columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.number_of_columns)

            - [`DatasetDriftMetricResults.number_of_drifted_columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.number_of_drifted_columns)

            - [`DatasetDriftMetricResults.share_of_drifted_columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.share_of_drifted_columns)

            - [`DatasetDriftMetricResults.threshold`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.dataset_drift_metric.DatasetDriftMetricResults.threshold)

    - [evidently.metrics.data_drift.target_by_features_table module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.target_by_features_table)

        - [`TargetByFeaturesTable`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTable)

            - [`TargetByFeaturesTable.calculate()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTable.calculate)

            - [`TargetByFeaturesTable.columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTable.columns)

        - [`TargetByFeaturesTableRenderer`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer)

            - [`TargetByFeaturesTableRenderer.color_options`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer.color_options)

            - [`TargetByFeaturesTableRenderer.render_html()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer.render_html)

            - [`TargetByFeaturesTableRenderer.render_json()`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableRenderer.render_json)

        - [`TargetByFeaturesTableResults`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults)

            - [`TargetByFeaturesTableResults.columns`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.columns)

            - [`TargetByFeaturesTableResults.curr_predictions`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.curr_predictions)

            - [`TargetByFeaturesTableResults.current_plot_data`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.current_plot_data)

            - [`TargetByFeaturesTableResults.ref_predictions`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.ref_predictions)

            - [`TargetByFeaturesTableResults.reference_plot_data`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.reference_plot_data)

            - [`TargetByFeaturesTableResults.target_name`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.target_name)

            - [`TargetByFeaturesTableResults.task`](api-reference/evidently.metrics.data_drift.md#evidently.metrics.data_drift.target_by_features_table.TargetByFeaturesTableResults.task)

    - [Module contents](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift)

- [evidently.metrics.data_integrity package](evidently.metrics.data_integrity.md)

    - [Submodules](api-reference/evidently.metrics.data_integrity.md#submodules)

    - [evidently.metrics.data_integrity.column_missing_values_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_missing_values_metric)

        - [`ColumnMissingValues`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues)

            - [`ColumnMissingValues.different_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.different_missing_values)

            - [`ColumnMissingValues.number_of_different_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.number_of_different_missing_values)

            - [`ColumnMissingValues.number_of_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.number_of_missing_values)

            - [`ColumnMissingValues.number_of_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.number_of_rows)

            - [`ColumnMissingValues.share_of_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValues.share_of_missing_values)

        - [`ColumnMissingValuesMetric`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric)

            - [`ColumnMissingValuesMetric.DEFAULT_MISSING_VALUES`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric.DEFAULT_MISSING_VALUES)

            - [`ColumnMissingValuesMetric.calculate()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric.calculate)

            - [`ColumnMissingValuesMetric.column_name`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric.column_name)

            - [`ColumnMissingValuesMetric.missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetric.missing_values)

        - [`ColumnMissingValuesMetricRenderer`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer)

            - [`ColumnMissingValuesMetricRenderer.color_options`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer.color_options)

            - [`ColumnMissingValuesMetricRenderer.render_html()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer.render_html)

            - [`ColumnMissingValuesMetricRenderer.render_json()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricRenderer.render_json)

        - [`ColumnMissingValuesMetricResult`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult)

            - [`ColumnMissingValuesMetricResult.column_name`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult.column_name)

            - [`ColumnMissingValuesMetricResult.current`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult.current)

            - [`ColumnMissingValuesMetricResult.reference`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_missing_values_metric.ColumnMissingValuesMetricResult.reference)

    - [evidently.metrics.data_integrity.column_regexp_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_regexp_metric)

        - [`ColumnRegExpMetric`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric)

            - [`ColumnRegExpMetric.calculate()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric.calculate)

            - [`ColumnRegExpMetric.column_name`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric.column_name)

            - [`ColumnRegExpMetric.reg_exp`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric.reg_exp)

            - [`ColumnRegExpMetric.top`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric.top)

        - [`ColumnRegExpMetricRenderer`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer)

            - [`ColumnRegExpMetricRenderer.color_options`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer.color_options)

            - [`ColumnRegExpMetricRenderer.render_html()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer.render_html)

            - [`ColumnRegExpMetricRenderer.render_json()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetricRenderer.render_json)

        - [`DataIntegrityValueByRegexpMetricResult`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult)

            - [`DataIntegrityValueByRegexpMetricResult.column_name`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.column_name)

            - [`DataIntegrityValueByRegexpMetricResult.current`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.current)

            - [`DataIntegrityValueByRegexpMetricResult.reference`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.reference)

            - [`DataIntegrityValueByRegexpMetricResult.reg_exp`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.reg_exp)

            - [`DataIntegrityValueByRegexpMetricResult.top`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpMetricResult.top)

        - [`DataIntegrityValueByRegexpStat`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat)

            - [`DataIntegrityValueByRegexpStat.number_of_matched`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.number_of_matched)

            - [`DataIntegrityValueByRegexpStat.number_of_not_matched`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.number_of_not_matched)

            - [`DataIntegrityValueByRegexpStat.number_of_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.number_of_rows)

            - [`DataIntegrityValueByRegexpStat.table_of_matched`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.table_of_matched)

            - [`DataIntegrityValueByRegexpStat.table_of_not_matched`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.DataIntegrityValueByRegexpStat.table_of_not_matched)

    - [evidently.metrics.data_integrity.column_summary_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_summary_metric)

        - [`CategoricalCharacteristics`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics)

            - [`CategoricalCharacteristics.count`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.count)

            - [`CategoricalCharacteristics.missing`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.missing)

            - [`CategoricalCharacteristics.missing_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.missing_percentage)

            - [`CategoricalCharacteristics.most_common`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.most_common)

            - [`CategoricalCharacteristics.most_common_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.most_common_percentage)

            - [`CategoricalCharacteristics.new_in_current_values_count`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.new_in_current_values_count)

            - [`CategoricalCharacteristics.number_of_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.number_of_rows)

            - [`CategoricalCharacteristics.unique`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.unique)

            - [`CategoricalCharacteristics.unique_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.unique_percentage)

            - [`CategoricalCharacteristics.unused_in_current_values_count`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.CategoricalCharacteristics.unused_in_current_values_count)

        - [`ColumnSummary`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary)

            - [`ColumnSummary.column_name`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.column_name)

            - [`ColumnSummary.column_type`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.column_type)

            - [`ColumnSummary.current_characteristics`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.current_characteristics)

            - [`ColumnSummary.plot_data`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.plot_data)

            - [`ColumnSummary.reference_characteristics`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummary.reference_characteristics)

        - [`ColumnSummaryMetric`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)

            - [`ColumnSummaryMetric.calculate()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric.calculate)

            - [`ColumnSummaryMetric.map_data()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric.map_data)

        - [`ColumnSummaryMetricRenderer`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer)

            - [`ColumnSummaryMetricRenderer.color_options`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer.color_options)

            - [`ColumnSummaryMetricRenderer.render_html()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer.render_html)

            - [`ColumnSummaryMetricRenderer.render_json()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetricRenderer.render_json)

        - [`DataByTarget`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataByTarget)

            - [`DataByTarget.data_for_plots`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataByTarget.data_for_plots)

            - [`DataByTarget.target_name`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataByTarget.target_name)

            - [`DataByTarget.target_type`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataByTarget.target_type)

        - [`DataInTime`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataInTime)

            - [`DataInTime.data_for_plots`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataInTime.data_for_plots)

            - [`DataInTime.datetime_name`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataInTime.datetime_name)

            - [`DataInTime.freq`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataInTime.freq)

        - [`DataQualityPlot`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot)

            - [`DataQualityPlot.bins_for_hist`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot.bins_for_hist)

            - [`DataQualityPlot.counts_of_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot.counts_of_values)

            - [`DataQualityPlot.data_by_target`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot.data_by_target)

            - [`DataQualityPlot.data_in_time`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DataQualityPlot.data_in_time)

        - [`DatetimeCharacteristics`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics)

            - [`DatetimeCharacteristics.count`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.count)

            - [`DatetimeCharacteristics.first`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.first)

            - [`DatetimeCharacteristics.last`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.last)

            - [`DatetimeCharacteristics.missing`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.missing)

            - [`DatetimeCharacteristics.missing_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.missing_percentage)

            - [`DatetimeCharacteristics.most_common`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.most_common)

            - [`DatetimeCharacteristics.most_common_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.most_common_percentage)

            - [`DatetimeCharacteristics.number_of_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.number_of_rows)

            - [`DatetimeCharacteristics.unique`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.unique)

            - [`DatetimeCharacteristics.unique_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.DatetimeCharacteristics.unique_percentage)

        - [`NumericCharacteristics`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics)

            - [`NumericCharacteristics.count`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.count)

            - [`NumericCharacteristics.infinite_count`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.infinite_count)

            - [`NumericCharacteristics.infinite_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.infinite_percentage)

            - [`NumericCharacteristics.max`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.max)

            - [`NumericCharacteristics.mean`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.mean)

            - [`NumericCharacteristics.min`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.min)

            - [`NumericCharacteristics.missing`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.missing)

            - [`NumericCharacteristics.missing_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.missing_percentage)

            - [`NumericCharacteristics.most_common`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.most_common)

            - [`NumericCharacteristics.most_common_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.most_common_percentage)

            - [`NumericCharacteristics.number_of_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.number_of_rows)

            - [`NumericCharacteristics.p25`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.p25)

            - [`NumericCharacteristics.p50`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.p50)

            - [`NumericCharacteristics.p75`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.p75)

            - [`NumericCharacteristics.std`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.std)

            - [`NumericCharacteristics.unique`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.unique)

            - [`NumericCharacteristics.unique_percentage`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.NumericCharacteristics.unique_percentage)

    - [evidently.metrics.data_integrity.dataset_missing_values_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.dataset_missing_values_metric)

        - [`DatasetMissingValues`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues)

            - [`DatasetMissingValues.columns_with_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.columns_with_missing_values)

            - [`DatasetMissingValues.different_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.different_missing_values)

            - [`DatasetMissingValues.different_missing_values_by_column`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.different_missing_values_by_column)

            - [`DatasetMissingValues.number_of_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_columns)

            - [`DatasetMissingValues.number_of_columns_with_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_columns_with_missing_values)

            - [`DatasetMissingValues.number_of_different_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_different_missing_values)

            - [`DatasetMissingValues.number_of_different_missing_values_by_column`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_different_missing_values_by_column)

            - [`DatasetMissingValues.number_of_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_missing_values)

            - [`DatasetMissingValues.number_of_missing_values_by_column`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_missing_values_by_column)

            - [`DatasetMissingValues.number_of_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_rows)

            - [`DatasetMissingValues.number_of_rows_with_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.number_of_rows_with_missing_values)

            - [`DatasetMissingValues.share_of_columns_with_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.share_of_columns_with_missing_values)

            - [`DatasetMissingValues.share_of_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.share_of_missing_values)

            - [`DatasetMissingValues.share_of_missing_values_by_column`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.share_of_missing_values_by_column)

            - [`DatasetMissingValues.share_of_rows_with_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValues.share_of_rows_with_missing_values)

        - [`DatasetMissingValuesMetric`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)

            - [`DatasetMissingValuesMetric.DEFAULT_MISSING_VALUES`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric.DEFAULT_MISSING_VALUES)

            - [`DatasetMissingValuesMetric.calculate()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric.calculate)

            - [`DatasetMissingValuesMetric.missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric.missing_values)

        - [`DatasetMissingValuesMetricRenderer`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer)

            - [`DatasetMissingValuesMetricRenderer.color_options`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer.color_options)

            - [`DatasetMissingValuesMetricRenderer.render_html()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer.render_html)

            - [`DatasetMissingValuesMetricRenderer.render_json()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricRenderer.render_json)

        - [`DatasetMissingValuesMetricResult`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult)

            - [`DatasetMissingValuesMetricResult.current`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult.current)

            - [`DatasetMissingValuesMetricResult.reference`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult.reference)

    - [evidently.metrics.data_integrity.dataset_summary_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.dataset_summary_metric)

        - [`DatasetSummary`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary)

            - [`DatasetSummary.columns_type`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.columns_type)

            - [`DatasetSummary.date_column`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.date_column)

            - [`DatasetSummary.id_column`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.id_column)

            - [`DatasetSummary.nans_by_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.nans_by_columns)

            - [`DatasetSummary.number_of_almost_constant_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_almost_constant_columns)

            - [`DatasetSummary.number_of_almost_duplicated_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_almost_duplicated_columns)

            - [`DatasetSummary.number_of_categorical_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_categorical_columns)

            - [`DatasetSummary.number_of_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_columns)

            - [`DatasetSummary.number_of_constant_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_constant_columns)

            - [`DatasetSummary.number_of_datetime_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_datetime_columns)

            - [`DatasetSummary.number_of_duplicated_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_duplicated_columns)

            - [`DatasetSummary.number_of_duplicated_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_duplicated_rows)

            - [`DatasetSummary.number_of_empty_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_empty_columns)

            - [`DatasetSummary.number_of_empty_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_empty_rows)

            - [`DatasetSummary.number_of_missing_values`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_missing_values)

            - [`DatasetSummary.number_of_numeric_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_numeric_columns)

            - [`DatasetSummary.number_of_rows`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_of_rows)

            - [`DatasetSummary.number_uniques_by_columns`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.number_uniques_by_columns)

            - [`DatasetSummary.prediction`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.prediction)

            - [`DatasetSummary.target`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummary.target)

        - [`DatasetSummaryMetric`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)

            - [`DatasetSummaryMetric.almost_constant_threshold`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric.almost_constant_threshold)

            - [`DatasetSummaryMetric.almost_duplicated_threshold`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric.almost_duplicated_threshold)

            - [`DatasetSummaryMetric.calculate()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric.calculate)

        - [`DatasetSummaryMetricRenderer`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer)

            - [`DatasetSummaryMetricRenderer.color_options`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer.color_options)

            - [`DatasetSummaryMetricRenderer.render_html()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer.render_html)

            - [`DatasetSummaryMetricRenderer.render_json()`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricRenderer.render_json)

        - [`DatasetSummaryMetricResult`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult)

            - [`DatasetSummaryMetricResult.almost_duplicated_threshold`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult.almost_duplicated_threshold)

            - [`DatasetSummaryMetricResult.current`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult.current)

            - [`DatasetSummaryMetricResult.reference`](api-reference/evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetricResult.reference)

    - [Module contents](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity)

- [evidently.metrics.data_quality package](evidently.metrics.data_quality.md)

    - [Submodules](api-reference/evidently.metrics.data_quality.md#submodules)

    - [evidently.metrics.data_quality.column_correlations_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_correlations_metric)

        - [`ColumnCorrelationsMetric`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetric)

            - [`ColumnCorrelationsMetric.calculate()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetric.calculate)

            - [`ColumnCorrelationsMetric.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetric.column_name)

        - [`ColumnCorrelationsMetricRenderer`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer)

            - [`ColumnCorrelationsMetricRenderer.color_options`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer.color_options)

            - [`ColumnCorrelationsMetricRenderer.render_html()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer.render_html)

            - [`ColumnCorrelationsMetricRenderer.render_json()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricRenderer.render_json)

        - [`ColumnCorrelationsMetricResult`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult)

            - [`ColumnCorrelationsMetricResult.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult.column_name)

            - [`ColumnCorrelationsMetricResult.current`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult.current)

            - [`ColumnCorrelationsMetricResult.reference`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_correlations_metric.ColumnCorrelationsMetricResult.reference)

    - [evidently.metrics.data_quality.column_distribution_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_distribution_metric)

        - [`ColumnDistributionMetric`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetric)

            - [`ColumnDistributionMetric.calculate()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetric.calculate)

            - [`ColumnDistributionMetric.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetric.column_name)

        - [`ColumnDistributionMetricRenderer`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer)

            - [`ColumnDistributionMetricRenderer.color_options`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer.color_options)

            - [`ColumnDistributionMetricRenderer.render_html()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer.render_html)

            - [`ColumnDistributionMetricRenderer.render_json()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricRenderer.render_json)

        - [`ColumnDistributionMetricResult`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult)

            - [`ColumnDistributionMetricResult.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult.column_name)

            - [`ColumnDistributionMetricResult.current`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult.current)

            - [`ColumnDistributionMetricResult.reference`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_distribution_metric.ColumnDistributionMetricResult.reference)

    - [evidently.metrics.data_quality.column_quantile_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_quantile_metric)

        - [`ColumnQuantileMetric`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric)

            - [`ColumnQuantileMetric.calculate()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric.calculate)

            - [`ColumnQuantileMetric.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric.column_name)

            - [`ColumnQuantileMetric.quantile`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric.quantile)

        - [`ColumnQuantileMetricRenderer`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer)

            - [`ColumnQuantileMetricRenderer.color_options`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer.color_options)

            - [`ColumnQuantileMetricRenderer.render_html()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer.render_html)

            - [`ColumnQuantileMetricRenderer.render_json()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricRenderer.render_json)

        - [`ColumnQuantileMetricResult`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult)

            - [`ColumnQuantileMetricResult.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.column_name)

            - [`ColumnQuantileMetricResult.current`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.current)

            - [`ColumnQuantileMetricResult.current_distribution`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.current_distribution)

            - [`ColumnQuantileMetricResult.quantile`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.quantile)

            - [`ColumnQuantileMetricResult.reference`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.reference)

            - [`ColumnQuantileMetricResult.reference_distribution`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetricResult.reference_distribution)

    - [evidently.metrics.data_quality.column_value_list_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_value_list_metric)

        - [`ColumnValueListMetric`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)

            - [`ColumnValueListMetric.calculate()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric.calculate)

            - [`ColumnValueListMetric.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric.column_name)

            - [`ColumnValueListMetric.values`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric.values)

        - [`ColumnValueListMetricRenderer`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer)

            - [`ColumnValueListMetricRenderer.color_options`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer.color_options)

            - [`ColumnValueListMetricRenderer.render_html()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer.render_html)

            - [`ColumnValueListMetricRenderer.render_json()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricRenderer.render_json)

        - [`ColumnValueListMetricResult`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult)

            - [`ColumnValueListMetricResult.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult.column_name)

            - [`ColumnValueListMetricResult.current`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult.current)

            - [`ColumnValueListMetricResult.reference`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult.reference)

            - [`ColumnValueListMetricResult.values`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetricResult.values)

        - [`ValueListStat`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat)

            - [`ValueListStat.number_in_list`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.number_in_list)

            - [`ValueListStat.number_not_in_list`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.number_not_in_list)

            - [`ValueListStat.rows_count`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.rows_count)

            - [`ValueListStat.share_in_list`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.share_in_list)

            - [`ValueListStat.share_not_in_list`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.share_not_in_list)

            - [`ValueListStat.values_in_list`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.values_in_list)

            - [`ValueListStat.values_not_in_list`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ValueListStat.values_not_in_list)

    - [evidently.metrics.data_quality.column_value_range_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_value_range_metric)

        - [`ColumnValueRangeMetric`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)

            - [`ColumnValueRangeMetric.calculate()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric.calculate)

            - [`ColumnValueRangeMetric.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric.column_name)

            - [`ColumnValueRangeMetric.left`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric.left)

            - [`ColumnValueRangeMetric.right`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric.right)

        - [`ColumnValueRangeMetricRenderer`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer)

            - [`ColumnValueRangeMetricRenderer.color_options`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer.color_options)

            - [`ColumnValueRangeMetricRenderer.render_html()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer.render_html)

            - [`ColumnValueRangeMetricRenderer.render_json()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricRenderer.render_json)

        - [`ColumnValueRangeMetricResult`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult)

            - [`ColumnValueRangeMetricResult.column_name`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.column_name)

            - [`ColumnValueRangeMetricResult.current`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.current)

            - [`ColumnValueRangeMetricResult.current_distribution`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.current_distribution)

            - [`ColumnValueRangeMetricResult.left`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.left)

            - [`ColumnValueRangeMetricResult.reference`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.reference)

            - [`ColumnValueRangeMetricResult.reference_distribution`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.reference_distribution)

            - [`ColumnValueRangeMetricResult.right`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetricResult.right)

        - [`ValuesInRangeStat`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat)

            - [`ValuesInRangeStat.number_in_range`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.number_in_range)

            - [`ValuesInRangeStat.number_not_in_range`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.number_not_in_range)

            - [`ValuesInRangeStat.number_of_values`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.number_of_values)

            - [`ValuesInRangeStat.share_in_range`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.share_in_range)

            - [`ValuesInRangeStat.share_not_in_range`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ValuesInRangeStat.share_not_in_range)

    - [evidently.metrics.data_quality.dataset_correlations_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.dataset_correlations_metric)

        - [`CorrelationStats`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats)

            - [`CorrelationStats.abs_max_correlation`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.abs_max_correlation)

            - [`CorrelationStats.abs_max_features_correlation`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.abs_max_features_correlation)

            - [`CorrelationStats.abs_max_prediction_features_correlation`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.abs_max_prediction_features_correlation)

            - [`CorrelationStats.abs_max_target_features_correlation`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.abs_max_target_features_correlation)

            - [`CorrelationStats.target_prediction_correlation`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.CorrelationStats.target_prediction_correlation)

        - [`DataQualityCorrelationMetricsRenderer`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer)

            - [`DataQualityCorrelationMetricsRenderer.color_options`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer.color_options)

            - [`DataQualityCorrelationMetricsRenderer.render_html()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer.render_html)

            - [`DataQualityCorrelationMetricsRenderer.render_json()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DataQualityCorrelationMetricsRenderer.render_json)

        - [`DatasetCorrelation`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation)

            - [`DatasetCorrelation.correlation`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation.correlation)

            - [`DatasetCorrelation.stats`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelation.stats)

        - [`DatasetCorrelationsMetric`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)

            - [`DatasetCorrelationsMetric.calculate()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric.calculate)

        - [`DatasetCorrelationsMetricResult`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetricResult)

            - [`DatasetCorrelationsMetricResult.current`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetricResult.current)

            - [`DatasetCorrelationsMetricResult.reference`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetricResult.reference)

    - [evidently.metrics.data_quality.stability_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.stability_metric)

        - [`DataQualityStabilityMetric`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric)

            - [`DataQualityStabilityMetric.calculate()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric.calculate)

        - [`DataQualityStabilityMetricRenderer`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer)

            - [`DataQualityStabilityMetricRenderer.color_options`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer.color_options)

            - [`DataQualityStabilityMetricRenderer.render_html()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer.render_html)

            - [`DataQualityStabilityMetricRenderer.render_json()`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricRenderer.render_json)

        - [`DataQualityStabilityMetricResult`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricResult)

            - [`DataQualityStabilityMetricResult.number_not_stable_prediction`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricResult.number_not_stable_prediction)

            - [`DataQualityStabilityMetricResult.number_not_stable_target`](api-reference/evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetricResult.number_not_stable_target)

    - [Module contents](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality)

- [evidently.metrics.regression_performance package](evidently.metrics.regression_performance.md)

    - [Submodules](api-reference/evidently.metrics.regression_performance.md#submodules)

    - [evidently.metrics.regression_performance.abs_perc_error_in_time module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.abs_perc_error_in_time)

        - [`RegressionAbsPercentageErrorPlot`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlot)

            - [`RegressionAbsPercentageErrorPlot.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlot.calculate)

        - [`RegressionAbsPercentageErrorPlotRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer)

            - [`RegressionAbsPercentageErrorPlotRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer.color_options)

            - [`RegressionAbsPercentageErrorPlotRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer.render_html)

            - [`RegressionAbsPercentageErrorPlotRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotRenderer.render_json)

        - [`RegressionAbsPercentageErrorPlotResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults)

            - [`RegressionAbsPercentageErrorPlotResults.current_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults.current_scatter)

            - [`RegressionAbsPercentageErrorPlotResults.reference_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults.reference_scatter)

            - [`RegressionAbsPercentageErrorPlotResults.x_name`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.abs_perc_error_in_time.RegressionAbsPercentageErrorPlotResults.x_name)

    - [evidently.metrics.regression_performance.error_bias_table module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_bias_table)

        - [`RegressionErrorBiasTable`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable)

            - [`RegressionErrorBiasTable.TOP_ERROR_DEFAULT`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.TOP_ERROR_DEFAULT)

            - [`RegressionErrorBiasTable.TOP_ERROR_MAX`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.TOP_ERROR_MAX)

            - [`RegressionErrorBiasTable.TOP_ERROR_MIN`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.TOP_ERROR_MIN)

            - [`RegressionErrorBiasTable.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.calculate)

            - [`RegressionErrorBiasTable.columns`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.columns)

            - [`RegressionErrorBiasTable.top_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTable.top_error)

        - [`RegressionErrorBiasTableRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer)

            - [`RegressionErrorBiasTableRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer.color_options)

            - [`RegressionErrorBiasTableRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer.render_html)

            - [`RegressionErrorBiasTableRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableRenderer.render_json)

        - [`RegressionErrorBiasTableResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults)

            - [`RegressionErrorBiasTableResults.cat_feature_names`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.cat_feature_names)

            - [`RegressionErrorBiasTableResults.columns`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.columns)

            - [`RegressionErrorBiasTableResults.current_plot_data`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.current_plot_data)

            - [`RegressionErrorBiasTableResults.error_bias`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.error_bias)

            - [`RegressionErrorBiasTableResults.num_feature_names`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.num_feature_names)

            - [`RegressionErrorBiasTableResults.prediction_name`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.prediction_name)

            - [`RegressionErrorBiasTableResults.reference_plot_data`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.reference_plot_data)

            - [`RegressionErrorBiasTableResults.target_name`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.target_name)

            - [`RegressionErrorBiasTableResults.top_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_bias_table.RegressionErrorBiasTableResults.top_error)

    - [evidently.metrics.regression_performance.error_distribution module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_distribution)

        - [`RegressionErrorDistribution`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistribution)

            - [`RegressionErrorDistribution.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistribution.calculate)

        - [`RegressionErrorDistributionRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer)

            - [`RegressionErrorDistributionRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer.color_options)

            - [`RegressionErrorDistributionRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer.render_html)

            - [`RegressionErrorDistributionRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionRenderer.render_json)

        - [`RegressionErrorDistributionResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionResults)

            - [`RegressionErrorDistributionResults.current_bins`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionResults.current_bins)

            - [`RegressionErrorDistributionResults.reference_bins`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_distribution.RegressionErrorDistributionResults.reference_bins)

    - [evidently.metrics.regression_performance.error_in_time module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_in_time)

        - [`RegressionErrorPlot`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlot)

            - [`RegressionErrorPlot.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlot.calculate)

        - [`RegressionErrorPlotRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer)

            - [`RegressionErrorPlotRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer.color_options)

            - [`RegressionErrorPlotRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer.render_html)

            - [`RegressionErrorPlotRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotRenderer.render_json)

        - [`RegressionErrorPlotResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults)

            - [`RegressionErrorPlotResults.current_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults.current_scatter)

            - [`RegressionErrorPlotResults.reference_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults.reference_scatter)

            - [`RegressionErrorPlotResults.x_name`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_in_time.RegressionErrorPlotResults.x_name)

    - [evidently.metrics.regression_performance.error_normality module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_normality)

        - [`RegressionErrorNormality`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormality)

            - [`RegressionErrorNormality.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormality.calculate)

        - [`RegressionErrorNormalityRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer)

            - [`RegressionErrorNormalityRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer.color_options)

            - [`RegressionErrorNormalityRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer.render_html)

            - [`RegressionErrorNormalityRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityRenderer.render_json)

        - [`RegressionErrorNormalityResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityResults)

            - [`RegressionErrorNormalityResults.current_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityResults.current_error)

            - [`RegressionErrorNormalityResults.reference_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.error_normality.RegressionErrorNormalityResults.reference_error)

    - [evidently.metrics.regression_performance.predicted_and_actual_in_time module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.predicted_and_actual_in_time)

        - [`RegressionPredictedVsActualPlot`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlot)

            - [`RegressionPredictedVsActualPlot.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlot.calculate)

        - [`RegressionPredictedVsActualPlotRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer)

            - [`RegressionPredictedVsActualPlotRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer.color_options)

            - [`RegressionPredictedVsActualPlotRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer.render_html)

            - [`RegressionPredictedVsActualPlotRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotRenderer.render_json)

        - [`RegressionPredictedVsActualPlotResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults)

            - [`RegressionPredictedVsActualPlotResults.current_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults.current_scatter)

            - [`RegressionPredictedVsActualPlotResults.reference_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults.reference_scatter)

            - [`RegressionPredictedVsActualPlotResults.x_name`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_and_actual_in_time.RegressionPredictedVsActualPlotResults.x_name)

    - [evidently.metrics.regression_performance.predicted_vs_actual module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.predicted_vs_actual)

        - [`RegressionPredictedVsActualScatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatter)

            - [`RegressionPredictedVsActualScatter.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatter.calculate)

        - [`RegressionPredictedVsActualScatterRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer)

            - [`RegressionPredictedVsActualScatterRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer.color_options)

            - [`RegressionPredictedVsActualScatterRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer.render_html)

            - [`RegressionPredictedVsActualScatterRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterRenderer.render_json)

        - [`RegressionPredictedVsActualScatterResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterResults)

            - [`RegressionPredictedVsActualScatterResults.current_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterResults.current_scatter)

            - [`RegressionPredictedVsActualScatterResults.reference_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.predicted_vs_actual.RegressionPredictedVsActualScatterResults.reference_scatter)

    - [evidently.metrics.regression_performance.regression_performance_metrics module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_performance_metrics)

        - [`RegressionPerformanceMetrics`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetrics)

            - [`RegressionPerformanceMetrics.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetrics.calculate)

            - [`RegressionPerformanceMetrics.get_parameters()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetrics.get_parameters)

        - [`RegressionPerformanceMetricsRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer)

            - [`RegressionPerformanceMetricsRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer.color_options)

            - [`RegressionPerformanceMetricsRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer.render_html)

            - [`RegressionPerformanceMetricsRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsRenderer.render_json)

        - [`RegressionPerformanceMetricsResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults)

            - [`RegressionPerformanceMetricsResults.abs_error_max`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_error_max)

            - [`RegressionPerformanceMetricsResults.abs_error_max_default`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_error_max_default)

            - [`RegressionPerformanceMetricsResults.abs_error_max_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_error_max_ref)

            - [`RegressionPerformanceMetricsResults.abs_error_std`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_error_std)

            - [`RegressionPerformanceMetricsResults.abs_perc_error_std`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.abs_perc_error_std)

            - [`RegressionPerformanceMetricsResults.columns`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.columns)

            - [`RegressionPerformanceMetricsResults.error_bias`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.error_bias)

            - [`RegressionPerformanceMetricsResults.error_normality`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.error_normality)

            - [`RegressionPerformanceMetricsResults.error_std`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.error_std)

            - [`RegressionPerformanceMetricsResults.hist_for_plot`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.hist_for_plot)

            - [`RegressionPerformanceMetricsResults.me_default_sigma`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.me_default_sigma)

            - [`RegressionPerformanceMetricsResults.me_hist_for_plot`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.me_hist_for_plot)

            - [`RegressionPerformanceMetricsResults.mean_abs_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_error)

            - [`RegressionPerformanceMetricsResults.mean_abs_error_default`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_error_default)

            - [`RegressionPerformanceMetricsResults.mean_abs_error_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_error_ref)

            - [`RegressionPerformanceMetricsResults.mean_abs_perc_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_perc_error)

            - [`RegressionPerformanceMetricsResults.mean_abs_perc_error_default`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_perc_error_default)

            - [`RegressionPerformanceMetricsResults.mean_abs_perc_error_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_abs_perc_error_ref)

            - [`RegressionPerformanceMetricsResults.mean_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_error)

            - [`RegressionPerformanceMetricsResults.mean_error_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.mean_error_ref)

            - [`RegressionPerformanceMetricsResults.r2_score`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.r2_score)

            - [`RegressionPerformanceMetricsResults.r2_score_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.r2_score_ref)

            - [`RegressionPerformanceMetricsResults.rmse`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.rmse)

            - [`RegressionPerformanceMetricsResults.rmse_default`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.rmse_default)

            - [`RegressionPerformanceMetricsResults.rmse_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.rmse_ref)

            - [`RegressionPerformanceMetricsResults.underperformance`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.underperformance)

            - [`RegressionPerformanceMetricsResults.underperformance_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.underperformance_ref)

            - [`RegressionPerformanceMetricsResults.vals_for_plots`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_performance_metrics.RegressionPerformanceMetricsResults.vals_for_plots)

    - [evidently.metrics.regression_performance.regression_quality module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_quality)

        - [`RegressionQualityMetric`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)

            - [`RegressionQualityMetric.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric.calculate)

        - [`RegressionQualityMetricRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer)

            - [`RegressionQualityMetricRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer.color_options)

            - [`RegressionQualityMetricRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer.render_html)

            - [`RegressionQualityMetricRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricRenderer.render_json)

        - [`RegressionQualityMetricResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults)

            - [`RegressionQualityMetricResults.abs_error_max`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_max)

            - [`RegressionQualityMetricResults.abs_error_max_default`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_max_default)

            - [`RegressionQualityMetricResults.abs_error_max_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_max_ref)

            - [`RegressionQualityMetricResults.abs_error_std`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_std)

            - [`RegressionQualityMetricResults.abs_error_std_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_error_std_ref)

            - [`RegressionQualityMetricResults.abs_perc_error_std`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_perc_error_std)

            - [`RegressionQualityMetricResults.abs_perc_error_std_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.abs_perc_error_std_ref)

            - [`RegressionQualityMetricResults.columns`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.columns)

            - [`RegressionQualityMetricResults.error_bias`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.error_bias)

            - [`RegressionQualityMetricResults.error_normality`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.error_normality)

            - [`RegressionQualityMetricResults.error_std`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.error_std)

            - [`RegressionQualityMetricResults.error_std_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.error_std_ref)

            - [`RegressionQualityMetricResults.hist_for_plot`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.hist_for_plot)

            - [`RegressionQualityMetricResults.me_default_sigma`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.me_default_sigma)

            - [`RegressionQualityMetricResults.me_hist_for_plot`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.me_hist_for_plot)

            - [`RegressionQualityMetricResults.mean_abs_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_error)

            - [`RegressionQualityMetricResults.mean_abs_error_default`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_error_default)

            - [`RegressionQualityMetricResults.mean_abs_error_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_error_ref)

            - [`RegressionQualityMetricResults.mean_abs_perc_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_perc_error)

            - [`RegressionQualityMetricResults.mean_abs_perc_error_default`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_perc_error_default)

            - [`RegressionQualityMetricResults.mean_abs_perc_error_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_abs_perc_error_ref)

            - [`RegressionQualityMetricResults.mean_error`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_error)

            - [`RegressionQualityMetricResults.mean_error_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.mean_error_ref)

            - [`RegressionQualityMetricResults.r2_score`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.r2_score)

            - [`RegressionQualityMetricResults.r2_score_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.r2_score_ref)

            - [`RegressionQualityMetricResults.rmse`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.rmse)

            - [`RegressionQualityMetricResults.rmse_default`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.rmse_default)

            - [`RegressionQualityMetricResults.rmse_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.rmse_ref)

            - [`RegressionQualityMetricResults.underperformance`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.underperformance)

            - [`RegressionQualityMetricResults.underperformance_ref`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.underperformance_ref)

            - [`RegressionQualityMetricResults.vals_for_plots`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetricResults.vals_for_plots)

    - [evidently.metrics.regression_performance.top_error module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.top_error)

        - [`RegressionTopErrorMetric`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetric)

            - [`RegressionTopErrorMetric.calculate()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetric.calculate)

        - [`RegressionTopErrorMetricRenderer`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer)

            - [`RegressionTopErrorMetricRenderer.color_options`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer.color_options)

            - [`RegressionTopErrorMetricRenderer.render_html()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer.render_html)

            - [`RegressionTopErrorMetricRenderer.render_json()`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricRenderer.render_json)

        - [`RegressionTopErrorMetricResults`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults)

            - [`RegressionTopErrorMetricResults.curr_mean_err_per_group`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults.curr_mean_err_per_group)

            - [`RegressionTopErrorMetricResults.curr_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults.curr_scatter)

            - [`RegressionTopErrorMetricResults.ref_mean_err_per_group`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults.ref_mean_err_per_group)

            - [`RegressionTopErrorMetricResults.ref_scatter`](api-reference/evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.top_error.RegressionTopErrorMetricResults.ref_scatter)

    - [Module contents](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance)


## Submodules

## evidently.metrics.base_metric module


### _class_ evidently.metrics.base_metric.ErrorResult(exception: BaseException)
Bases: `object`


#### exception(_: BaseExceptio_ )

### _class_ evidently.metrics.base_metric.InputData(reference_data: Optional[pandas.core.frame.DataFrame], current_data: pandas.core.frame.DataFrame, column_mapping: [evidently.pipeline.column_mapping.ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), data_definition: [evidently.utils.data_preprocessing.DataDefinition](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition))
Bases: `object`


#### column_mapping(_: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping_ )

#### current_data(_: DataFram_ )

#### data_definition(_: [DataDefinition](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition_ )

#### reference_data(_: Optional[DataFrame_ )

### _class_ evidently.metrics.base_metric.Metric()
Bases: `Generic`[`TResult`]


#### _abstract_ calculate(data: InputData)

#### context(_ = Non_ )

#### get_id()

#### get_parameters()

#### get_result()

#### set_context(context)

### evidently.metrics.base_metric.generate_column_metrics(metric_class: Type[Metric], columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None)
Function for generating metrics for columns

## evidently.metrics.classification_performance_metrics module


### _class_ evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetrics()
Bases: `Metric`[`ClassificationPerformanceResults`]


#### calculate(data: InputData)

### _class_ evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationPerformanceMetrics)

#### render_json(obj: ClassificationPerformanceMetrics)

### _class_ evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold(threshold: float)
Bases: `ClassificationPerformanceMetricsThresholdBase`


#### calculate_metric(dataset: DataFrame, mapping: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

#### get_parameters()

#### get_threshold(dataset: DataFrame, mapping: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### _class_ evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase()
Bases: `Metric`[`ClassificationPerformanceResults`]


#### calculate(data: InputData)

#### _abstract_ calculate_metric(dataset: DataFrame, mapping: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

#### _abstract_ get_threshold(dataset: DataFrame, mapping: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### _class_ evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationPerformanceMetricsThreshold)

#### render_json(obj: ClassificationPerformanceMetricsThreshold)

### _class_ evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK(k: Union[float, int])
Bases: `ClassificationPerformanceMetricsThresholdBase`


#### calculate_metric(dataset: DataFrame, mapping: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

#### get_parameters()

#### get_threshold(dataset: DataFrame, columns: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### _class_ evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer(color_options: Optional[[ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)


#### color_options(_: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: ClassificationPerformanceMetricsTopK)

#### render_json(obj: ClassificationPerformanceMetricsTopK)

### _class_ evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults(columns: [evidently.utils.data_operations.DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns), current: evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics, dummy: evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics, reference: Optional[evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics] = None)
Bases: `object`


#### columns(_: [DatasetColumns](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns_ )

#### current(_: DatasetClassificationPerformanceMetric_ )

#### dummy(_: DatasetClassificationPerformanceMetric_ )

#### reference(_: Optional[DatasetClassificationPerformanceMetrics_ _ = Non_ )

### _class_ evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics(accuracy: float, precision: float, recall: float, f1: float, metrics_matrix: dict, confusion_matrix: [ConfusionMatrix](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix), confusion_by_classes: Dict[Union[str, int], Dict[str, int]], roc_auc: Optional[float] = None, log_loss: Optional[float] = None, roc_aucs: Optional[list] = None, roc_curve: Optional[dict] = None, pr_curve: Optional[dict] = None, pr_table: Optional[Union[dict, list]] = None, tpr: Optional[float] = None, tnr: Optional[float] = None, fpr: Optional[float] = None, fnr: Optional[float] = None, rate_plots_data: Optional[dict] = None, plot_data: Optional[Dict[str, Dict[str, list]]] = None)
Bases: `object`

Class for performance metrics values


#### accuracy(_: floa_ )

#### confusion_by_classes(_: Dict[Union[str, int], Dict[str, int]_ )

#### confusion_matrix(_: [ConfusionMatrix](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix_ )

#### f1(_: floa_ )

#### fnr(_: Optional[float_ _ = Non_ )

#### fpr(_: Optional[float_ _ = Non_ )

#### log_loss(_: Optional[float_ _ = Non_ )

#### metrics_matrix(_: dic_ )

#### plot_data(_: Optional[Dict[str, Dict[str, list]]_ _ = Non_ )

#### pr_curve(_: Optional[dict_ _ = Non_ )

#### pr_table(_: Optional[Union[dict, list]_ _ = Non_ )

#### precision(_: floa_ )

#### rate_plots_data(_: Optional[dict_ _ = Non_ )

#### recall(_: floa_ )

#### roc_auc(_: Optional[float_ _ = Non_ )

#### roc_aucs(_: Optional[list_ _ = Non_ )

#### roc_curve(_: Optional[dict_ _ = Non_ )

#### tnr(_: Optional[float_ _ = Non_ )

#### tpr(_: Optional[float_ _ = Non_ )

### evidently.metrics.classification_performance_metrics.classification_performance_metrics(target: Series, prediction: Series, prediction_probas: Optional[DataFrame], pos_label: Optional[Union[str, int]])
## evidently.metrics.utils module


### evidently.metrics.utils.apply_func_to_binned_data(df_for_bins, func, target_column, preds_column, is_ref_data=False)

### evidently.metrics.utils.make_target_bins_for_reg_plots(curr: DataFrame, target_column, preds_column, ref: Optional[DataFrame] = None)
## Module contents
