# evidently package

## Subpackages

- [evidently.calculations package](evidently.calculations.md)

    - [Subpackages](evidently.calculations.md#subpackages)

        - [evidently.calculations.stattests package](evidently.calculations.stattests.md)

            - [Submodules](evidently.calculations.stattests.md#submodules)

            - [evidently.calculations.stattests.anderson_darling_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.anderson_darling_stattest)

            - [evidently.calculations.stattests.chisquare_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.chisquare_stattest)

            - [evidently.calculations.stattests.cramer_von_mises_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.cramer_von_mises_stattest)

            - [evidently.calculations.stattests.energy_distance module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.energy_distance)

            - [evidently.calculations.stattests.epps_singleton_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.epps_singleton_stattest)

            - [evidently.calculations.stattests.fisher_exact_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.fisher_exact_stattest)

            - [evidently.calculations.stattests.g_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.g_stattest)

            - [evidently.calculations.stattests.hellinger_distance module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.hellinger_distance)

            - [evidently.calculations.stattests.jensenshannon module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.jensenshannon)

            - [evidently.calculations.stattests.kl_div module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.kl_div)

            - [evidently.calculations.stattests.ks_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.ks_stattest)

            - [evidently.calculations.stattests.mann_whitney_urank_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.mann_whitney_urank_stattest)

            - [evidently.calculations.stattests.psi module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.psi)

            - [evidently.calculations.stattests.registry module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.registry)

            - [evidently.calculations.stattests.t_test module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.t_test)

            - [evidently.calculations.stattests.tvd_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.tvd_stattest)

            - [evidently.calculations.stattests.utils module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.utils)

            - [evidently.calculations.stattests.wasserstein_distance_norm module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.wasserstein_distance_norm)

            - [evidently.calculations.stattests.z_stattest module](evidently.calculations.stattests.md#module-evidently.calculations.stattests.z_stattest)

            - [Module contents](evidently.calculations.stattests.md#module-evidently.calculations.stattests)

    - [Submodules](evidently.calculations.md#submodules)

    - [evidently.calculations.classification_performance module](evidently.calculations.md#module-evidently.calculations.classification_performance)

        - [`ConfusionMatrix`](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)

            - [`ConfusionMatrix.labels`](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix.labels)

            - [`ConfusionMatrix.values`](evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix.values)

        - [`PredictionData`](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)

            - [`PredictionData.labels`](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData.labels)

            - [`PredictionData.prediction_probas`](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData.prediction_probas)

            - [`PredictionData.predictions`](evidently.calculations.md#evidently.calculations.classification_performance.PredictionData.predictions)

        - [`calculate_confusion_by_classes()`](evidently.calculations.md#evidently.calculations.classification_performance.calculate_confusion_by_classes)

        - [`calculate_pr_table()`](evidently.calculations.md#evidently.calculations.classification_performance.calculate_pr_table)

        - [`get_prediction_data()`](evidently.calculations.md#evidently.calculations.classification_performance.get_prediction_data)

        - [`k_probability_threshold()`](evidently.calculations.md#evidently.calculations.classification_performance.k_probability_threshold)

        - [`threshold_probability_labels()`](evidently.calculations.md#evidently.calculations.classification_performance.threshold_probability_labels)

    - [evidently.calculations.data_drift module](evidently.calculations.md#module-evidently.calculations.data_drift)

        - [`ColumnDataDriftMetrics`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics)

            - [`ColumnDataDriftMetrics.column_name`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.column_name)

            - [`ColumnDataDriftMetrics.column_type`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.column_type)

            - [`ColumnDataDriftMetrics.current_correlations`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.current_correlations)

            - [`ColumnDataDriftMetrics.current_distribution`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.current_distribution)

            - [`ColumnDataDriftMetrics.current_scatter`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.current_scatter)

            - [`ColumnDataDriftMetrics.current_small_distribution`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.current_small_distribution)

            - [`ColumnDataDriftMetrics.drift_detected`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.drift_detected)

            - [`ColumnDataDriftMetrics.drift_score`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.drift_score)

            - [`ColumnDataDriftMetrics.plot_shape`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.plot_shape)

            - [`ColumnDataDriftMetrics.reference_correlations`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.reference_correlations)

            - [`ColumnDataDriftMetrics.reference_distribution`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.reference_distribution)

            - [`ColumnDataDriftMetrics.reference_small_distribution`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.reference_small_distribution)

            - [`ColumnDataDriftMetrics.stattest_name`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.stattest_name)

            - [`ColumnDataDriftMetrics.threshold`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.threshold)

            - [`ColumnDataDriftMetrics.x_name`](evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.x_name)

        - [`DatasetDrift`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDrift)

            - [`DatasetDrift.dataset_drift`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDrift.dataset_drift)

            - [`DatasetDrift.dataset_drift_score`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDrift.dataset_drift_score)

            - [`DatasetDrift.number_of_drifted_columns`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDrift.number_of_drifted_columns)

        - [`DatasetDriftMetrics`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics)

            - [`DatasetDriftMetrics.dataset_columns`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.dataset_columns)

            - [`DatasetDriftMetrics.dataset_drift`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.dataset_drift)

            - [`DatasetDriftMetrics.drift_by_columns`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.drift_by_columns)

            - [`DatasetDriftMetrics.number_of_columns`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.number_of_columns)

            - [`DatasetDriftMetrics.number_of_drifted_columns`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.number_of_drifted_columns)

            - [`DatasetDriftMetrics.options`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.options)

            - [`DatasetDriftMetrics.share_of_drifted_columns`](evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.share_of_drifted_columns)

        - [`ensure_prediction_column_is_string()`](evidently.calculations.md#evidently.calculations.data_drift.ensure_prediction_column_is_string)

        - [`get_dataset_drift()`](evidently.calculations.md#evidently.calculations.data_drift.get_dataset_drift)

        - [`get_drift_for_columns()`](evidently.calculations.md#evidently.calculations.data_drift.get_drift_for_columns)

        - [`get_one_column_drift()`](evidently.calculations.md#evidently.calculations.data_drift.get_one_column_drift)

    - [evidently.calculations.data_integration module](evidently.calculations.md#module-evidently.calculations.data_integration)

        - [`get_number_of_all_pandas_missed_values()`](evidently.calculations.md#evidently.calculations.data_integration.get_number_of_all_pandas_missed_values)

        - [`get_number_of_almost_constant_columns()`](evidently.calculations.md#evidently.calculations.data_integration.get_number_of_almost_constant_columns)

        - [`get_number_of_almost_duplicated_columns()`](evidently.calculations.md#evidently.calculations.data_integration.get_number_of_almost_duplicated_columns)

        - [`get_number_of_constant_columns()`](evidently.calculations.md#evidently.calculations.data_integration.get_number_of_constant_columns)

        - [`get_number_of_duplicated_columns()`](evidently.calculations.md#evidently.calculations.data_integration.get_number_of_duplicated_columns)

        - [`get_number_of_empty_columns()`](evidently.calculations.md#evidently.calculations.data_integration.get_number_of_empty_columns)

    - [evidently.calculations.data_quality module](evidently.calculations.md#module-evidently.calculations.data_quality)

        - [`ColumnCorrelations`](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)

            - [`ColumnCorrelations.column_name`](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations.column_name)

            - [`ColumnCorrelations.kind`](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations.kind)

            - [`ColumnCorrelations.values`](evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations.values)

        - [`DataQualityGetPlotData`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityGetPlotData)

            - [`DataQualityGetPlotData.calculate_data_by_target()`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityGetPlotData.calculate_data_by_target)

            - [`DataQualityGetPlotData.calculate_data_in_time()`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityGetPlotData.calculate_data_in_time)

            - [`DataQualityGetPlotData.calculate_main_plot()`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityGetPlotData.calculate_main_plot)

        - [`DataQualityPlot`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityPlot)

            - [`DataQualityPlot.bins_for_hist`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityPlot.bins_for_hist)

        - [`DataQualityStats`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats)

            - [`DataQualityStats.cat_features_stats`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.cat_features_stats)

            - [`DataQualityStats.datetime_features_stats`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.datetime_features_stats)

            - [`DataQualityStats.get_all_features()`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.get_all_features)

            - [`DataQualityStats.num_features_stats`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.num_features_stats)

            - [`DataQualityStats.prediction_stats`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.prediction_stats)

            - [`DataQualityStats.rows_count`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.rows_count)

            - [`DataQualityStats.target_stats`](evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.target_stats)

        - [`FeatureQualityStats`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats)

            - [`FeatureQualityStats.as_dict()`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.as_dict)

            - [`FeatureQualityStats.count`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.count)

            - [`FeatureQualityStats.feature_type`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.feature_type)

            - [`FeatureQualityStats.infinite_count`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.infinite_count)

            - [`FeatureQualityStats.infinite_percentage`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.infinite_percentage)

            - [`FeatureQualityStats.is_category()`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.is_category)

            - [`FeatureQualityStats.is_datetime()`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.is_datetime)

            - [`FeatureQualityStats.is_numeric()`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.is_numeric)

            - [`FeatureQualityStats.max`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.max)

            - [`FeatureQualityStats.mean`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.mean)

            - [`FeatureQualityStats.min`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.min)

            - [`FeatureQualityStats.missing_count`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.missing_count)

            - [`FeatureQualityStats.missing_percentage`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.missing_percentage)

            - [`FeatureQualityStats.most_common_not_null_value`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.most_common_not_null_value)

            - [`FeatureQualityStats.most_common_not_null_value_percentage`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.most_common_not_null_value_percentage)

            - [`FeatureQualityStats.most_common_value`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.most_common_value)

            - [`FeatureQualityStats.most_common_value_percentage`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.most_common_value_percentage)

            - [`FeatureQualityStats.new_in_current_values_count`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.new_in_current_values_count)

            - [`FeatureQualityStats.number_of_rows`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.number_of_rows)

            - [`FeatureQualityStats.percentile_25`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.percentile_25)

            - [`FeatureQualityStats.percentile_50`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.percentile_50)

            - [`FeatureQualityStats.percentile_75`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.percentile_75)

            - [`FeatureQualityStats.std`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.std)

            - [`FeatureQualityStats.unique_count`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.unique_count)

            - [`FeatureQualityStats.unique_percentage`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.unique_percentage)

            - [`FeatureQualityStats.unused_in_current_values_count`](evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.unused_in_current_values_count)

        - [`calculate_category_column_correlations()`](evidently.calculations.md#evidently.calculations.data_quality.calculate_category_column_correlations)

        - [`calculate_column_distribution()`](evidently.calculations.md#evidently.calculations.data_quality.calculate_column_distribution)

        - [`calculate_correlations()`](evidently.calculations.md#evidently.calculations.data_quality.calculate_correlations)

        - [`calculate_cramer_v_correlation()`](evidently.calculations.md#evidently.calculations.data_quality.calculate_cramer_v_correlation)

        - [`calculate_data_quality_stats()`](evidently.calculations.md#evidently.calculations.data_quality.calculate_data_quality_stats)

        - [`calculate_numerical_column_correlations()`](evidently.calculations.md#evidently.calculations.data_quality.calculate_numerical_column_correlations)

        - [`get_features_stats()`](evidently.calculations.md#evidently.calculations.data_quality.get_features_stats)

        - [`get_pairwise_correlation()`](evidently.calculations.md#evidently.calculations.data_quality.get_pairwise_correlation)

        - [`get_rows_count()`](evidently.calculations.md#evidently.calculations.data_quality.get_rows_count)

    - [evidently.calculations.regression_performance module](evidently.calculations.md#module-evidently.calculations.regression_performance)

        - [`ErrorWithQuantiles`](evidently.calculations.md#evidently.calculations.regression_performance.ErrorWithQuantiles)

        - [`FeatureBias`](evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias)

            - [`FeatureBias.as_dict()`](evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.as_dict)

            - [`FeatureBias.feature_type`](evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.feature_type)

            - [`FeatureBias.majority`](evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.majority)

            - [`FeatureBias.over`](evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.over)

            - [`FeatureBias.range`](evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.range)

            - [`FeatureBias.under`](evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.under)

        - [`RegressionPerformanceMetrics`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics)

            - [`RegressionPerformanceMetrics.abs_error_max`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.abs_error_max)

            - [`RegressionPerformanceMetrics.abs_error_std`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.abs_error_std)

            - [`RegressionPerformanceMetrics.abs_perc_error_std`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.abs_perc_error_std)

            - [`RegressionPerformanceMetrics.error_bias`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.error_bias)

            - [`RegressionPerformanceMetrics.error_normality`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.error_normality)

            - [`RegressionPerformanceMetrics.error_std`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.error_std)

            - [`RegressionPerformanceMetrics.mean_abs_error`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.mean_abs_error)

            - [`RegressionPerformanceMetrics.mean_abs_perc_error`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.mean_abs_perc_error)

            - [`RegressionPerformanceMetrics.mean_error`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.mean_error)

            - [`RegressionPerformanceMetrics.underperformance`](evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.underperformance)

        - [`calculate_regression_performance()`](evidently.calculations.md#evidently.calculations.regression_performance.calculate_regression_performance)

        - [`error_bias_table()`](evidently.calculations.md#evidently.calculations.regression_performance.error_bias_table)

        - [`error_with_quantiles()`](evidently.calculations.md#evidently.calculations.regression_performance.error_with_quantiles)

    - [Module contents](evidently.calculations.md#module-evidently.calculations)

- [evidently.metric_preset package](evidently.metric_preset.md)

    - [Submodules](evidently.metric_preset.md#submodules)

    - [evidently.metric_preset.classification_performance module](evidently.metric_preset.md#module-evidently.metric_preset.classification_performance)

        - [`ClassificationPreset`](evidently.metric_preset.md#evidently.metric_preset.classification_performance.ClassificationPreset)

            - [`ClassificationPreset.generate_metrics()`](evidently.metric_preset.md#evidently.metric_preset.classification_performance.ClassificationPreset.generate_metrics)

    - [evidently.metric_preset.data_drift module](evidently.metric_preset.md#module-evidently.metric_preset.data_drift)

        - [`DataDriftPreset`](evidently.metric_preset.md#evidently.metric_preset.data_drift.DataDriftPreset)

            - [`DataDriftPreset.generate_metrics()`](evidently.metric_preset.md#evidently.metric_preset.data_drift.DataDriftPreset.generate_metrics)

    - [evidently.metric_preset.data_quality module](evidently.metric_preset.md#module-evidently.metric_preset.data_quality)

        - [`DataQualityPreset`](evidently.metric_preset.md#evidently.metric_preset.data_quality.DataQualityPreset)

            - [`DataQualityPreset.columns`](evidently.metric_preset.md#evidently.metric_preset.data_quality.DataQualityPreset.columns)

            - [`DataQualityPreset.generate_metrics()`](evidently.metric_preset.md#evidently.metric_preset.data_quality.DataQualityPreset.generate_metrics)

    - [evidently.metric_preset.metric_preset module](evidently.metric_preset.md#module-evidently.metric_preset.metric_preset)

        - [`MetricPreset`](evidently.metric_preset.md#evidently.metric_preset.metric_preset.MetricPreset)

            - [`MetricPreset.generate_metrics()`](evidently.metric_preset.md#evidently.metric_preset.metric_preset.MetricPreset.generate_metrics)

    - [evidently.metric_preset.regression_performance module](evidently.metric_preset.md#module-evidently.metric_preset.regression_performance)

        - [`RegressionPreset`](evidently.metric_preset.md#evidently.metric_preset.regression_performance.RegressionPreset)

            - [`RegressionPreset.generate_metrics()`](evidently.metric_preset.md#evidently.metric_preset.regression_performance.RegressionPreset.generate_metrics)

    - [evidently.metric_preset.target_drift module](evidently.metric_preset.md#module-evidently.metric_preset.target_drift)

        - [`TargetDriftPreset`](evidently.metric_preset.md#evidently.metric_preset.target_drift.TargetDriftPreset)

            - [`TargetDriftPreset.generate_metrics()`](evidently.metric_preset.md#evidently.metric_preset.target_drift.TargetDriftPreset.generate_metrics)

    - [Module contents](evidently.metric_preset.md#module-evidently.metric_preset)

- [evidently.metrics package](evidently.metrics.md)

    - [Subpackages](evidently.metrics.md#subpackages)

        - [evidently.metrics.classification_performance package](evidently.metrics.classification_performance.md)

            - [Submodules](evidently.metrics.classification_performance.md#submodules)

            - [evidently.metrics.classification_performance.base_classification_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.base_classification_metric)

            - [evidently.metrics.classification_performance.class_balance_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.class_balance_metric)

            - [evidently.metrics.classification_performance.class_separation_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.class_separation_metric)

            - [evidently.metrics.classification_performance.classification_quality_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.classification_quality_metric)

            - [evidently.metrics.classification_performance.confusion_matrix_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.confusion_matrix_metric)

            - [evidently.metrics.classification_performance.pr_curve_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.pr_curve_metric)

            - [evidently.metrics.classification_performance.pr_table_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.pr_table_metric)

            - [evidently.metrics.classification_performance.probability_distribution_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.probability_distribution_metric)

            - [evidently.metrics.classification_performance.quality_by_class_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.quality_by_class_metric)

            - [evidently.metrics.classification_performance.quality_by_feature_table module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.quality_by_feature_table)

            - [evidently.metrics.classification_performance.roc_curve_metric module](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.roc_curve_metric)

            - [Module contents](evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance)

        - [evidently.metrics.data_drift package](evidently.metrics.data_drift.md)

            - [Submodules](evidently.metrics.data_drift.md#submodules)

            - [evidently.metrics.data_drift.column_drift_metric module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.column_drift_metric)

            - [evidently.metrics.data_drift.column_value_plot module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.column_value_plot)

            - [evidently.metrics.data_drift.data_drift_table module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.data_drift_table)

            - [evidently.metrics.data_drift.dataset_drift_metric module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.dataset_drift_metric)

            - [evidently.metrics.data_drift.target_by_features_table module](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.target_by_features_table)

            - [Module contents](evidently.metrics.data_drift.md#module-evidently.metrics.data_drift)

        - [evidently.metrics.data_integrity package](evidently.metrics.data_integrity.md)

            - [Submodules](evidently.metrics.data_integrity.md#submodules)

            - [evidently.metrics.data_integrity.column_missing_values_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_missing_values_metric)

            - [evidently.metrics.data_integrity.column_regexp_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_regexp_metric)

            - [evidently.metrics.data_integrity.column_summary_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_summary_metric)

            - [evidently.metrics.data_integrity.dataset_missing_values_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.dataset_missing_values_metric)

            - [evidently.metrics.data_integrity.dataset_summary_metric module](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.dataset_summary_metric)

            - [Module contents](evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity)

        - [evidently.metrics.data_quality package](evidently.metrics.data_quality.md)

            - [Submodules](evidently.metrics.data_quality.md#submodules)

            - [evidently.metrics.data_quality.column_correlations_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_correlations_metric)

            - [evidently.metrics.data_quality.column_distribution_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_distribution_metric)

            - [evidently.metrics.data_quality.column_quantile_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_quantile_metric)

            - [evidently.metrics.data_quality.column_value_list_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_value_list_metric)

            - [evidently.metrics.data_quality.column_value_range_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_value_range_metric)

            - [evidently.metrics.data_quality.dataset_correlations_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.dataset_correlations_metric)

            - [evidently.metrics.data_quality.stability_metric module](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.stability_metric)

            - [Module contents](evidently.metrics.data_quality.md#module-evidently.metrics.data_quality)

        - [evidently.metrics.regression_performance package](evidently.metrics.regression_performance.md)

            - [Submodules](evidently.metrics.regression_performance.md#submodules)

            - [evidently.metrics.regression_performance.abs_perc_error_in_time module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.abs_perc_error_in_time)

            - [evidently.metrics.regression_performance.error_bias_table module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_bias_table)

            - [evidently.metrics.regression_performance.error_distribution module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_distribution)

            - [evidently.metrics.regression_performance.error_in_time module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_in_time)

            - [evidently.metrics.regression_performance.error_normality module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_normality)

            - [evidently.metrics.regression_performance.predicted_and_actual_in_time module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.predicted_and_actual_in_time)

            - [evidently.metrics.regression_performance.predicted_vs_actual module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.predicted_vs_actual)

            - [evidently.metrics.regression_performance.regression_performance_metrics module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_performance_metrics)

            - [evidently.metrics.regression_performance.regression_quality module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_quality)

            - [evidently.metrics.regression_performance.top_error module](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.top_error)

            - [Module contents](evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance)

    - [Submodules](evidently.metrics.md#submodules)

    - [evidently.metrics.base_metric module](evidently.metrics.md#module-evidently.metrics.base_metric)

        - [`ErrorResult`](evidently.metrics.md#evidently.metrics.base_metric.ErrorResult)

            - [`ErrorResult.exception`](evidently.metrics.md#evidently.metrics.base_metric.ErrorResult.exception)

        - [`InputData`](evidently.metrics.md#evidently.metrics.base_metric.InputData)

            - [`InputData.column_mapping`](evidently.metrics.md#evidently.metrics.base_metric.InputData.column_mapping)

            - [`InputData.current_data`](evidently.metrics.md#evidently.metrics.base_metric.InputData.current_data)

            - [`InputData.data_definition`](evidently.metrics.md#evidently.metrics.base_metric.InputData.data_definition)

            - [`InputData.reference_data`](evidently.metrics.md#evidently.metrics.base_metric.InputData.reference_data)

        - [`Metric`](evidently.metrics.md#evidently.metrics.base_metric.Metric)

            - [`Metric.calculate()`](evidently.metrics.md#evidently.metrics.base_metric.Metric.calculate)

            - [`Metric.context`](evidently.metrics.md#evidently.metrics.base_metric.Metric.context)

            - [`Metric.get_id()`](evidently.metrics.md#evidently.metrics.base_metric.Metric.get_id)

            - [`Metric.get_parameters()`](evidently.metrics.md#evidently.metrics.base_metric.Metric.get_parameters)

            - [`Metric.get_result()`](evidently.metrics.md#evidently.metrics.base_metric.Metric.get_result)

            - [`Metric.set_context()`](evidently.metrics.md#evidently.metrics.base_metric.Metric.set_context)

        - [`generate_column_metrics()`](evidently.metrics.md#evidently.metrics.base_metric.generate_column_metrics)

    - [evidently.metrics.classification_performance_metrics module](evidently.metrics.md#module-evidently.metrics.classification_performance_metrics)

        - [`ClassificationPerformanceMetrics`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetrics)

            - [`ClassificationPerformanceMetrics.calculate()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetrics.calculate)

        - [`ClassificationPerformanceMetricsRenderer`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer)

            - [`ClassificationPerformanceMetricsRenderer.color_options`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer.color_options)

            - [`ClassificationPerformanceMetricsRenderer.render_html()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer.render_html)

            - [`ClassificationPerformanceMetricsRenderer.render_json()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer.render_json)

        - [`ClassificationPerformanceMetricsThreshold`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold)

            - [`ClassificationPerformanceMetricsThreshold.calculate_metric()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold.calculate_metric)

            - [`ClassificationPerformanceMetricsThreshold.get_parameters()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold.get_parameters)

            - [`ClassificationPerformanceMetricsThreshold.get_threshold()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold.get_threshold)

        - [`ClassificationPerformanceMetricsThresholdBase`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase)

            - [`ClassificationPerformanceMetricsThresholdBase.calculate()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase.calculate)

            - [`ClassificationPerformanceMetricsThresholdBase.calculate_metric()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase.calculate_metric)

            - [`ClassificationPerformanceMetricsThresholdBase.get_threshold()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase.get_threshold)

        - [`ClassificationPerformanceMetricsThresholdRenderer`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer)

            - [`ClassificationPerformanceMetricsThresholdRenderer.color_options`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer.color_options)

            - [`ClassificationPerformanceMetricsThresholdRenderer.render_html()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer.render_html)

            - [`ClassificationPerformanceMetricsThresholdRenderer.render_json()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer.render_json)

        - [`ClassificationPerformanceMetricsTopK`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK)

            - [`ClassificationPerformanceMetricsTopK.calculate_metric()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK.calculate_metric)

            - [`ClassificationPerformanceMetricsTopK.get_parameters()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK.get_parameters)

            - [`ClassificationPerformanceMetricsTopK.get_threshold()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK.get_threshold)

        - [`ClassificationPerformanceMetricsTopKRenderer`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer)

            - [`ClassificationPerformanceMetricsTopKRenderer.color_options`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer.color_options)

            - [`ClassificationPerformanceMetricsTopKRenderer.render_html()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer.render_html)

            - [`ClassificationPerformanceMetricsTopKRenderer.render_json()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer.render_json)

        - [`ClassificationPerformanceResults`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)

            - [`ClassificationPerformanceResults.columns`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults.columns)

            - [`ClassificationPerformanceResults.current`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults.current)

            - [`ClassificationPerformanceResults.dummy`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults.dummy)

            - [`ClassificationPerformanceResults.reference`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults.reference)

        - [`DatasetClassificationPerformanceMetrics`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics)

            - [`DatasetClassificationPerformanceMetrics.accuracy`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.accuracy)

            - [`DatasetClassificationPerformanceMetrics.confusion_by_classes`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.confusion_by_classes)

            - [`DatasetClassificationPerformanceMetrics.confusion_matrix`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.confusion_matrix)

            - [`DatasetClassificationPerformanceMetrics.f1`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.f1)

            - [`DatasetClassificationPerformanceMetrics.fnr`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.fnr)

            - [`DatasetClassificationPerformanceMetrics.fpr`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.fpr)

            - [`DatasetClassificationPerformanceMetrics.log_loss`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.log_loss)

            - [`DatasetClassificationPerformanceMetrics.metrics_matrix`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.metrics_matrix)

            - [`DatasetClassificationPerformanceMetrics.plot_data`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.plot_data)

            - [`DatasetClassificationPerformanceMetrics.pr_curve`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.pr_curve)

            - [`DatasetClassificationPerformanceMetrics.pr_table`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.pr_table)

            - [`DatasetClassificationPerformanceMetrics.precision`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.precision)

            - [`DatasetClassificationPerformanceMetrics.rate_plots_data`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.rate_plots_data)

            - [`DatasetClassificationPerformanceMetrics.recall`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.recall)

            - [`DatasetClassificationPerformanceMetrics.roc_auc`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.roc_auc)

            - [`DatasetClassificationPerformanceMetrics.roc_aucs`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.roc_aucs)

            - [`DatasetClassificationPerformanceMetrics.roc_curve`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.roc_curve)

            - [`DatasetClassificationPerformanceMetrics.tnr`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.tnr)

            - [`DatasetClassificationPerformanceMetrics.tpr`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.tpr)

        - [`classification_performance_metrics()`](evidently.metrics.md#evidently.metrics.classification_performance_metrics.classification_performance_metrics)

    - [evidently.metrics.utils module](evidently.metrics.md#module-evidently.metrics.utils)

        - [`apply_func_to_binned_data()`](evidently.metrics.md#evidently.metrics.utils.apply_func_to_binned_data)

        - [`make_target_bins_for_reg_plots()`](evidently.metrics.md#evidently.metrics.utils.make_target_bins_for_reg_plots)

    - [Module contents](evidently.metrics.md#module-evidently.metrics)

- [evidently.model package](evidently.model.md)

    - [Submodules](evidently.model.md#submodules)

    - [evidently.model.dashboard module](evidently.model.md#module-evidently.model.dashboard)

        - [`DashboardInfo`](evidently.model.md#evidently.model.dashboard.DashboardInfo)

            - [`DashboardInfo.name`](evidently.model.md#evidently.model.dashboard.DashboardInfo.name)

            - [`DashboardInfo.widgets`](evidently.model.md#evidently.model.dashboard.DashboardInfo.widgets)

    - [evidently.model.widget module](evidently.model.md#module-evidently.model.widget)

        - [`AdditionalGraphInfo`](evidently.model.md#evidently.model.widget.AdditionalGraphInfo)

            - [`AdditionalGraphInfo.id`](evidently.model.md#evidently.model.widget.AdditionalGraphInfo.id)

            - [`AdditionalGraphInfo.params`](evidently.model.md#evidently.model.widget.AdditionalGraphInfo.params)

        - [`Alert`](evidently.model.md#evidently.model.widget.Alert)

            - [`Alert.longText`](evidently.model.md#evidently.model.widget.Alert.longText)

            - [`Alert.state`](evidently.model.md#evidently.model.widget.Alert.state)

            - [`Alert.text`](evidently.model.md#evidently.model.widget.Alert.text)

            - [`Alert.value`](evidently.model.md#evidently.model.widget.Alert.value)

        - [`AlertStats`](evidently.model.md#evidently.model.widget.AlertStats)

            - [`AlertStats.active`](evidently.model.md#evidently.model.widget.AlertStats.active)

            - [`AlertStats.eggs`](evidently.model.md#evidently.model.widget.AlertStats.eggs)

            - [`AlertStats.active`](evidently.model.md#id0)

            - [`AlertStats.triggered`](evidently.model.md#evidently.model.widget.AlertStats.triggered)

        - [`BaseWidgetInfo`](evidently.model.md#evidently.model.widget.BaseWidgetInfo)

            - [`BaseWidgetInfo.additionalGraphs`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.additionalGraphs)

            - [`BaseWidgetInfo.alertStats`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.alertStats)

            - [`BaseWidgetInfo.alerts`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.alerts)

            - [`BaseWidgetInfo.alertsPosition`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.alertsPosition)

            - [`BaseWidgetInfo.details`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.details)

            - [`BaseWidgetInfo.get_additional_graphs()`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.get_additional_graphs)

            - [`BaseWidgetInfo.id`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.id)

            - [`BaseWidgetInfo.insights`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.insights)

            - [`BaseWidgetInfo.pageSize`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.pageSize)

            - [`BaseWidgetInfo.params`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.params)

            - [`BaseWidgetInfo.size`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.size)

            - [`BaseWidgetInfo.tabs`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.tabs)

            - [`BaseWidgetInfo.title`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.title)

            - [`BaseWidgetInfo.type`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.type)

            - [`BaseWidgetInfo.widgets`](evidently.model.md#evidently.model.widget.BaseWidgetInfo.widgets)

        - [`Insight`](evidently.model.md#evidently.model.widget.Insight)

            - [`Insight.title`](evidently.model.md#evidently.model.widget.Insight.title)

            - [`Insight.severity`](evidently.model.md#evidently.model.widget.Insight.severity)

            - [`Insight.text`](evidently.model.md#evidently.model.widget.Insight.text)

            - [`Insight.severity`](evidently.model.md#id1)

            - [`Insight.text`](evidently.model.md#id2)

            - [`Insight.title`](evidently.model.md#id3)

        - [`PlotlyGraphInfo`](evidently.model.md#evidently.model.widget.PlotlyGraphInfo)

            - [`PlotlyGraphInfo.data`](evidently.model.md#evidently.model.widget.PlotlyGraphInfo.data)

            - [`PlotlyGraphInfo.id`](evidently.model.md#evidently.model.widget.PlotlyGraphInfo.id)

            - [`PlotlyGraphInfo.layout`](evidently.model.md#evidently.model.widget.PlotlyGraphInfo.layout)

        - [`TabInfo`](evidently.model.md#evidently.model.widget.TabInfo)

            - [`TabInfo.id`](evidently.model.md#evidently.model.widget.TabInfo.id)

            - [`TabInfo.title`](evidently.model.md#evidently.model.widget.TabInfo.title)

            - [`TabInfo.widget`](evidently.model.md#evidently.model.widget.TabInfo.widget)

        - [`TriggeredAlertStats`](evidently.model.md#evidently.model.widget.TriggeredAlertStats)

            - [`TriggeredAlertStats.last_24h`](evidently.model.md#evidently.model.widget.TriggeredAlertStats.last_24h)

            - [`TriggeredAlertStats.period`](evidently.model.md#evidently.model.widget.TriggeredAlertStats.period)

        - [`WidgetType`](evidently.model.md#evidently.model.widget.WidgetType)

            - [`WidgetType.BIG_GRAPH`](evidently.model.md#evidently.model.widget.WidgetType.BIG_GRAPH)

            - [`WidgetType.BIG_TABLE`](evidently.model.md#evidently.model.widget.WidgetType.BIG_TABLE)

            - [`WidgetType.COUNTER`](evidently.model.md#evidently.model.widget.WidgetType.COUNTER)

            - [`WidgetType.RICH_DATA`](evidently.model.md#evidently.model.widget.WidgetType.RICH_DATA)

            - [`WidgetType.TABBED_GRAPH`](evidently.model.md#evidently.model.widget.WidgetType.TABBED_GRAPH)

            - [`WidgetType.TABLE`](evidently.model.md#evidently.model.widget.WidgetType.TABLE)

            - [`WidgetType.TABS`](evidently.model.md#evidently.model.widget.WidgetType.TABS)

    - [Module contents](evidently.model.md#module-evidently.model)

- [evidently.model_monitoring package](evidently.model_monitoring.md)

    - [Subpackages](evidently.model_monitoring.md#subpackages)

        - [evidently.model_monitoring.monitors package](evidently.model_monitoring.monitors.md)

            - [Submodules](evidently.model_monitoring.monitors.md#submodules)

            - [evidently.model_monitoring.monitors.cat_target_drift module](evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.cat_target_drift)

            - [evidently.model_monitoring.monitors.classification_performance module](evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.classification_performance)

            - [evidently.model_monitoring.monitors.data_drift module](evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.data_drift)

            - [evidently.model_monitoring.monitors.data_quality module](evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.data_quality)

            - [evidently.model_monitoring.monitors.num_target_drift module](evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.num_target_drift)

            - [evidently.model_monitoring.monitors.prob_classification_performance module](evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.prob_classification_performance)

            - [evidently.model_monitoring.monitors.regression_performance module](evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.regression_performance)

            - [Module contents](evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors)

    - [Submodules](evidently.model_monitoring.md#submodules)

    - [evidently.model_monitoring.monitoring module](evidently.model_monitoring.md#module-evidently.model_monitoring.monitoring)

        - [`ModelMonitor`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)

            - [`ModelMonitor.analyzers()`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.analyzers)

            - [`ModelMonitor.calculate()`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.calculate)

            - [`ModelMonitor.metrics()`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.metrics)

            - [`ModelMonitor.monitor_id()`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.monitor_id)

            - [`ModelMonitor.options_provider`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.options_provider)

        - [`ModelMonitoring`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring)

            - [`ModelMonitoring.analyzers_results`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.analyzers_results)

            - [`ModelMonitoring.get_analyzers()`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.get_analyzers)

            - [`ModelMonitoring.metrics()`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.metrics)

            - [`ModelMonitoring.options_provider`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.options_provider)

            - [`ModelMonitoring.stages`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.stages)

        - [`ModelMonitoringMetric`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoringMetric)

            - [`ModelMonitoringMetric.create()`](evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoringMetric.create)

    - [Module contents](evidently.model_monitoring.md#module-evidently.model_monitoring)

- [evidently.model_profile package](evidently.model_profile.md)

    - [Subpackages](evidently.model_profile.md#subpackages)

        - [evidently.model_profile.sections package](evidently.model_profile.sections.md)

            - [Submodules](evidently.model_profile.sections.md#submodules)

            - [evidently.model_profile.sections.base_profile_section module](evidently.model_profile.sections.md#module-evidently.model_profile.sections.base_profile_section)

            - [evidently.model_profile.sections.cat_target_drift_profile_section module](evidently.model_profile.sections.md#module-evidently.model_profile.sections.cat_target_drift_profile_section)

            - [evidently.model_profile.sections.classification_performance_profile_section module](evidently.model_profile.sections.md#module-evidently.model_profile.sections.classification_performance_profile_section)

            - [evidently.model_profile.sections.data_drift_profile_section module](evidently.model_profile.sections.md#module-evidently.model_profile.sections.data_drift_profile_section)

            - [evidently.model_profile.sections.data_quality_profile_section module](evidently.model_profile.sections.md#module-evidently.model_profile.sections.data_quality_profile_section)

            - [evidently.model_profile.sections.num_target_drift_profile_section module](evidently.model_profile.sections.md#module-evidently.model_profile.sections.num_target_drift_profile_section)

            - [evidently.model_profile.sections.prob_classification_performance_profile_section module](evidently.model_profile.sections.md#module-evidently.model_profile.sections.prob_classification_performance_profile_section)

            - [evidently.model_profile.sections.regression_performance_profile_section module](evidently.model_profile.sections.md#module-evidently.model_profile.sections.regression_performance_profile_section)

            - [Module contents](evidently.model_profile.sections.md#module-evidently.model_profile.sections)

    - [Submodules](evidently.model_profile.md#submodules)

    - [evidently.model_profile.model_profile module](evidently.model_profile.md#module-evidently.model_profile.model_profile)

        - [`Profile`](evidently.model_profile.md#evidently.model_profile.model_profile.Profile)

            - [`Profile.calculate()`](evidently.model_profile.md#evidently.model_profile.model_profile.Profile.calculate)

            - [`Profile.get_analyzers()`](evidently.model_profile.md#evidently.model_profile.model_profile.Profile.get_analyzers)

            - [`Profile.json()`](evidently.model_profile.md#evidently.model_profile.model_profile.Profile.json)

            - [`Profile.object()`](evidently.model_profile.md#evidently.model_profile.model_profile.Profile.object)

            - [`Profile.result`](evidently.model_profile.md#evidently.model_profile.model_profile.Profile.result)

            - [`Profile.stages`](evidently.model_profile.md#evidently.model_profile.model_profile.Profile.stages)

    - [Module contents](evidently.model_profile.md#module-evidently.model_profile)

- [evidently.nbextension package](evidently.nbextension.md)

    - [Module contents](evidently.nbextension.md#module-evidently.nbextension)

- [evidently.options package](evidently.options.md)

    - [Submodules](evidently.options.md#submodules)

    - [evidently.options.color_scheme module](evidently.options.md#module-evidently.options.color_scheme)

        - [`ColorOptions`](evidently.options.md#evidently.options.color_scheme.ColorOptions)

            - [`ColorOptions.color_sequence`](evidently.options.md#evidently.options.color_scheme.ColorOptions.color_sequence)

            - [`ColorOptions.current_data_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.current_data_color)

            - [`ColorOptions.fill_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.fill_color)

            - [`ColorOptions.get_current_data_color()`](evidently.options.md#evidently.options.color_scheme.ColorOptions.get_current_data_color)

            - [`ColorOptions.get_reference_data_color()`](evidently.options.md#evidently.options.color_scheme.ColorOptions.get_reference_data_color)

            - [`ColorOptions.heatmap`](evidently.options.md#evidently.options.color_scheme.ColorOptions.heatmap)

            - [`ColorOptions.majority_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.majority_color)

            - [`ColorOptions.non_visible_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.non_visible_color)

            - [`ColorOptions.overestimation_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.overestimation_color)

            - [`ColorOptions.primary_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.primary_color)

            - [`ColorOptions.reference_data_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.reference_data_color)

            - [`ColorOptions.secondary_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.secondary_color)

            - [`ColorOptions.underestimation_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.underestimation_color)

            - [`ColorOptions.vertical_lines`](evidently.options.md#evidently.options.color_scheme.ColorOptions.vertical_lines)

            - [`ColorOptions.zero_line_color`](evidently.options.md#evidently.options.color_scheme.ColorOptions.zero_line_color)

    - [evidently.options.data_drift module](evidently.options.md#module-evidently.options.data_drift)

        - [`DataDriftOptions`](evidently.options.md#evidently.options.data_drift.DataDriftOptions)

            - [`DataDriftOptions.confidence`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.confidence)

            - [`DataDriftOptions.threshold`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.threshold)

            - [`DataDriftOptions.drift_share`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.drift_share)

            - [`DataDriftOptions.nbinsx`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.nbinsx)

            - [`DataDriftOptions.xbins`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.xbins)

            - [`DataDriftOptions.feature_stattest_func`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.feature_stattest_func)

            - [`DataDriftOptions.all_features_stattest`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.all_features_stattest)

            - [`DataDriftOptions.cat_features_stattest`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.cat_features_stattest)

            - [`DataDriftOptions.num_features_stattest`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.num_features_stattest)

            - [`DataDriftOptions.per_feature_stattest`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.per_feature_stattest)

            - [`DataDriftOptions.cat_target_stattest_func`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.cat_target_stattest_func)

            - [`DataDriftOptions.num_target_stattest_func`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.num_target_stattest_func)

            - [`DataDriftOptions.all_features_stattest`](evidently.options.md#id0)

            - [`DataDriftOptions.as_dict()`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.as_dict)

            - [`DataDriftOptions.cat_features_stattest`](evidently.options.md#id1)

            - [`DataDriftOptions.cat_target_stattest_func`](evidently.options.md#id2)

            - [`DataDriftOptions.cat_target_threshold`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.cat_target_threshold)

            - [`DataDriftOptions.confidence`](evidently.options.md#id3)

            - [`DataDriftOptions.drift_share`](evidently.options.md#id4)

            - [`DataDriftOptions.feature_stattest_func`](evidently.options.md#id5)

            - [`DataDriftOptions.get_feature_stattest_func()`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.get_feature_stattest_func)

            - [`DataDriftOptions.get_nbinsx()`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.get_nbinsx)

            - [`DataDriftOptions.get_threshold()`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.get_threshold)

            - [`DataDriftOptions.nbinsx`](evidently.options.md#id6)

            - [`DataDriftOptions.num_features_stattest`](evidently.options.md#id7)

            - [`DataDriftOptions.num_target_stattest_func`](evidently.options.md#id8)

            - [`DataDriftOptions.num_target_threshold`](evidently.options.md#evidently.options.data_drift.DataDriftOptions.num_target_threshold)

            - [`DataDriftOptions.per_feature_stattest`](evidently.options.md#id9)

            - [`DataDriftOptions.threshold`](evidently.options.md#id10)

            - [`DataDriftOptions.xbins`](evidently.options.md#id11)

    - [evidently.options.quality_metrics module](evidently.options.md#module-evidently.options.quality_metrics)

        - [`QualityMetricsOptions`](evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions)

            - [`QualityMetricsOptions.as_dict()`](evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.as_dict)

            - [`QualityMetricsOptions.classification_threshold`](evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.classification_threshold)

            - [`QualityMetricsOptions.conf_interval_n_sigmas`](evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.conf_interval_n_sigmas)

            - [`QualityMetricsOptions.cut_quantile`](evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.cut_quantile)

            - [`QualityMetricsOptions.get_cut_quantile()`](evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.get_cut_quantile)

    - [Module contents](evidently.options.md#module-evidently.options)

        - [`OptionsProvider`](evidently.options.md#evidently.options.OptionsProvider)

            - [`OptionsProvider.add()`](evidently.options.md#evidently.options.OptionsProvider.add)

            - [`OptionsProvider.get()`](evidently.options.md#evidently.options.OptionsProvider.get)

- [evidently.pipeline package](evidently.pipeline.md)

    - [Submodules](evidently.pipeline.md#submodules)

    - [evidently.pipeline.column_mapping module](evidently.pipeline.md#module-evidently.pipeline.column_mapping)

        - [`ColumnMapping`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping)

            - [`ColumnMapping.categorical_features`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.categorical_features)

            - [`ColumnMapping.datetime`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.datetime)

            - [`ColumnMapping.datetime_features`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.datetime_features)

            - [`ColumnMapping.id`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.id)

            - [`ColumnMapping.is_classification_task()`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.is_classification_task)

            - [`ColumnMapping.is_regression_task()`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.is_regression_task)

            - [`ColumnMapping.numerical_features`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.numerical_features)

            - [`ColumnMapping.pos_label`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.pos_label)

            - [`ColumnMapping.prediction`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.prediction)

            - [`ColumnMapping.target`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.target)

            - [`ColumnMapping.target_names`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.target_names)

            - [`ColumnMapping.task`](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.task)

        - [`TaskType`](evidently.pipeline.md#evidently.pipeline.column_mapping.TaskType)

            - [`TaskType.CLASSIFICATION_TASK`](evidently.pipeline.md#evidently.pipeline.column_mapping.TaskType.CLASSIFICATION_TASK)

            - [`TaskType.REGRESSION_TASK`](evidently.pipeline.md#evidently.pipeline.column_mapping.TaskType.REGRESSION_TASK)

    - [evidently.pipeline.pipeline module](evidently.pipeline.md#module-evidently.pipeline.pipeline)

        - [`Pipeline`](evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline)

            - [`Pipeline.analyzers_results`](evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.analyzers_results)

            - [`Pipeline.execute()`](evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.execute)

            - [`Pipeline.get_analyzers()`](evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.get_analyzers)

            - [`Pipeline.options_provider`](evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.options_provider)

            - [`Pipeline.stages`](evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.stages)

    - [evidently.pipeline.stage module](evidently.pipeline.md#module-evidently.pipeline.stage)

        - [`PipelineStage`](evidently.pipeline.md#evidently.pipeline.stage.PipelineStage)

            - [`PipelineStage.add_analyzer()`](evidently.pipeline.md#evidently.pipeline.stage.PipelineStage.add_analyzer)

            - [`PipelineStage.analyzers()`](evidently.pipeline.md#evidently.pipeline.stage.PipelineStage.analyzers)

            - [`PipelineStage.calculate()`](evidently.pipeline.md#evidently.pipeline.stage.PipelineStage.calculate)

            - [`PipelineStage.options_provider`](evidently.pipeline.md#evidently.pipeline.stage.PipelineStage.options_provider)

    - [Module contents](evidently.pipeline.md#module-evidently.pipeline)

- [evidently.profile_sections package](evidently.profile_sections.md)

    - [Module contents](evidently.profile_sections.md#module-evidently.profile_sections)

- [evidently.renderers package](evidently.renderers.md)

    - [Submodules](evidently.renderers.md#submodules)

    - [evidently.renderers.base_renderer module](evidently.renderers.md#module-evidently.renderers.base_renderer)

        - [`BaseRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.BaseRenderer)

            - [`BaseRenderer.color_options`](evidently.renderers.md#evidently.renderers.base_renderer.BaseRenderer.color_options)

        - [`DetailsInfo`](evidently.renderers.md#evidently.renderers.base_renderer.DetailsInfo)

            - [`DetailsInfo.id`](evidently.renderers.md#evidently.renderers.base_renderer.DetailsInfo.id)

            - [`DetailsInfo.info`](evidently.renderers.md#evidently.renderers.base_renderer.DetailsInfo.info)

            - [`DetailsInfo.title`](evidently.renderers.md#evidently.renderers.base_renderer.DetailsInfo.title)

        - [`MetricRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

            - [`MetricRenderer.color_options`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer.color_options)

            - [`MetricRenderer.render_html()`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer.render_html)

            - [`MetricRenderer.render_json()`](evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer.render_json)

        - [`RenderersDefinitions`](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions)

            - [`RenderersDefinitions.default_html_metric_renderer`](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions.default_html_metric_renderer)

            - [`RenderersDefinitions.default_html_test_renderer`](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions.default_html_test_renderer)

            - [`RenderersDefinitions.typed_renderers`](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions.typed_renderers)

        - [`TestHtmlInfo`](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo)

            - [`TestHtmlInfo.description`](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.description)

            - [`TestHtmlInfo.details`](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.details)

            - [`TestHtmlInfo.groups`](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.groups)

            - [`TestHtmlInfo.name`](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.name)

            - [`TestHtmlInfo.status`](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.status)

            - [`TestHtmlInfo.with_details()`](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.with_details)

        - [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

            - [`TestRenderer.color_options`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.color_options)

            - [`TestRenderer.html_description()`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.html_description)

            - [`TestRenderer.json_description()`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.json_description)

            - [`TestRenderer.render_html()`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.render_html)

            - [`TestRenderer.render_json()`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.render_json)

        - [`default_renderer()`](evidently.renderers.md#evidently.renderers.base_renderer.default_renderer)

    - [evidently.renderers.html_widgets module](evidently.renderers.md#module-evidently.renderers.html_widgets)

        - [`ColumnDefinition`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition)

            - [`ColumnDefinition.as_dict()`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.as_dict)

            - [`ColumnDefinition.field_name`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.field_name)

            - [`ColumnDefinition.options`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.options)

            - [`ColumnDefinition.sort`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.sort)

            - [`ColumnDefinition.title`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.title)

            - [`ColumnDefinition.type`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.type)

        - [`ColumnType`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnType)

            - [`ColumnType.HISTOGRAM`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnType.HISTOGRAM)

            - [`ColumnType.LINE`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnType.LINE)

            - [`ColumnType.SCATTER`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnType.SCATTER)

            - [`ColumnType.STRING`](evidently.renderers.md#evidently.renderers.html_widgets.ColumnType.STRING)

        - [`CounterData`](evidently.renderers.md#evidently.renderers.html_widgets.CounterData)

            - [`CounterData.float()`](evidently.renderers.md#evidently.renderers.html_widgets.CounterData.float)

            - [`CounterData.int()`](evidently.renderers.md#evidently.renderers.html_widgets.CounterData.int)

            - [`CounterData.label`](evidently.renderers.md#evidently.renderers.html_widgets.CounterData.label)

            - [`CounterData.string()`](evidently.renderers.md#evidently.renderers.html_widgets.CounterData.string)

            - [`CounterData.value`](evidently.renderers.md#evidently.renderers.html_widgets.CounterData.value)

        - [`DetailsPartInfo`](evidently.renderers.md#evidently.renderers.html_widgets.DetailsPartInfo)

            - [`DetailsPartInfo.info`](evidently.renderers.md#evidently.renderers.html_widgets.DetailsPartInfo.info)

            - [`DetailsPartInfo.title`](evidently.renderers.md#evidently.renderers.html_widgets.DetailsPartInfo.title)

        - [`GraphData`](evidently.renderers.md#evidently.renderers.html_widgets.GraphData)

            - [`GraphData.data`](evidently.renderers.md#evidently.renderers.html_widgets.GraphData.data)

            - [`GraphData.figure()`](evidently.renderers.md#evidently.renderers.html_widgets.GraphData.figure)

            - [`GraphData.layout`](evidently.renderers.md#evidently.renderers.html_widgets.GraphData.layout)

            - [`GraphData.title`](evidently.renderers.md#evidently.renderers.html_widgets.GraphData.title)

        - [`HeatmapData`](evidently.renderers.md#evidently.renderers.html_widgets.HeatmapData)

            - [`HeatmapData.matrix`](evidently.renderers.md#evidently.renderers.html_widgets.HeatmapData.matrix)

            - [`HeatmapData.name`](evidently.renderers.md#evidently.renderers.html_widgets.HeatmapData.name)

        - [`HistogramData`](evidently.renderers.md#evidently.renderers.html_widgets.HistogramData)

            - [`HistogramData.name`](evidently.renderers.md#evidently.renderers.html_widgets.HistogramData.name)

            - [`HistogramData.x`](evidently.renderers.md#evidently.renderers.html_widgets.HistogramData.x)

            - [`HistogramData.y`](evidently.renderers.md#evidently.renderers.html_widgets.HistogramData.y)

        - [`RichTableDataRow`](evidently.renderers.md#evidently.renderers.html_widgets.RichTableDataRow)

            - [`RichTableDataRow.details`](evidently.renderers.md#evidently.renderers.html_widgets.RichTableDataRow.details)

            - [`RichTableDataRow.fields`](evidently.renderers.md#evidently.renderers.html_widgets.RichTableDataRow.fields)

        - [`RowDetails`](evidently.renderers.md#evidently.renderers.html_widgets.RowDetails)

            - [`RowDetails.parts`](evidently.renderers.md#evidently.renderers.html_widgets.RowDetails.parts)

            - [`RowDetails.with_part()`](evidently.renderers.md#evidently.renderers.html_widgets.RowDetails.with_part)

        - [`SortDirection`](evidently.renderers.md#evidently.renderers.html_widgets.SortDirection)

            - [`SortDirection.ASC`](evidently.renderers.md#evidently.renderers.html_widgets.SortDirection.ASC)

            - [`SortDirection.DESC`](evidently.renderers.md#evidently.renderers.html_widgets.SortDirection.DESC)

        - [`TabData`](evidently.renderers.md#evidently.renderers.html_widgets.TabData)

            - [`TabData.title`](evidently.renderers.md#evidently.renderers.html_widgets.TabData.title)

            - [`TabData.widget`](evidently.renderers.md#evidently.renderers.html_widgets.TabData.widget)

        - [`WidgetSize`](evidently.renderers.md#evidently.renderers.html_widgets.WidgetSize)

            - [`WidgetSize.FULL`](evidently.renderers.md#evidently.renderers.html_widgets.WidgetSize.FULL)

            - [`WidgetSize.HALF`](evidently.renderers.md#evidently.renderers.html_widgets.WidgetSize.HALF)

        - [`counter()`](evidently.renderers.md#evidently.renderers.html_widgets.counter)

        - [`get_class_separation_plot_data()`](evidently.renderers.md#evidently.renderers.html_widgets.get_class_separation_plot_data)

        - [`get_heatmaps_widget()`](evidently.renderers.md#evidently.renderers.html_widgets.get_heatmaps_widget)

        - [`get_histogram_figure()`](evidently.renderers.md#evidently.renderers.html_widgets.get_histogram_figure)

        - [`get_histogram_figure_with_quantile()`](evidently.renderers.md#evidently.renderers.html_widgets.get_histogram_figure_with_quantile)

        - [`get_histogram_figure_with_range()`](evidently.renderers.md#evidently.renderers.html_widgets.get_histogram_figure_with_range)

        - [`get_histogram_for_distribution()`](evidently.renderers.md#evidently.renderers.html_widgets.get_histogram_for_distribution)

        - [`get_pr_rec_plot_data()`](evidently.renderers.md#evidently.renderers.html_widgets.get_pr_rec_plot_data)

        - [`get_roc_auc_tab_data()`](evidently.renderers.md#evidently.renderers.html_widgets.get_roc_auc_tab_data)

        - [`header_text()`](evidently.renderers.md#evidently.renderers.html_widgets.header_text)

        - [`histogram()`](evidently.renderers.md#evidently.renderers.html_widgets.histogram)

        - [`plotly_data()`](evidently.renderers.md#evidently.renderers.html_widgets.plotly_data)

        - [`plotly_figure()`](evidently.renderers.md#evidently.renderers.html_widgets.plotly_figure)

        - [`plotly_graph()`](evidently.renderers.md#evidently.renderers.html_widgets.plotly_graph)

        - [`plotly_graph_tabs()`](evidently.renderers.md#evidently.renderers.html_widgets.plotly_graph_tabs)

        - [`rich_table_data()`](evidently.renderers.md#evidently.renderers.html_widgets.rich_table_data)

        - [`table_data()`](evidently.renderers.md#evidently.renderers.html_widgets.table_data)

        - [`widget_tabs()`](evidently.renderers.md#evidently.renderers.html_widgets.widget_tabs)

        - [`widget_tabs_for_more_than_one()`](evidently.renderers.md#evidently.renderers.html_widgets.widget_tabs_for_more_than_one)

    - [evidently.renderers.notebook_utils module](evidently.renderers.md#module-evidently.renderers.notebook_utils)

        - [`determine_template()`](evidently.renderers.md#evidently.renderers.notebook_utils.determine_template)

    - [evidently.renderers.render_utils module](evidently.renderers.md#module-evidently.renderers.render_utils)

        - [`get_distribution_plot_figure()`](evidently.renderers.md#evidently.renderers.render_utils.get_distribution_plot_figure)

        - [`plot_distr()`](evidently.renderers.md#evidently.renderers.render_utils.plot_distr)

    - [Module contents](evidently.renderers.md#module-evidently.renderers)

- [evidently.report package](evidently.report.md)

    - [Submodules](evidently.report.md#submodules)

    - [evidently.report.report module](evidently.report.md#module-evidently.report.report)

        - [`Report`](evidently.report.md#evidently.report.report.Report)

            - [`Report.as_dict()`](evidently.report.md#evidently.report.report.Report.as_dict)

            - [`Report.metrics`](evidently.report.md#evidently.report.report.Report.metrics)

            - [`Report.run()`](evidently.report.md#evidently.report.report.Report.run)

    - [Module contents](evidently.report.md#module-evidently.report)

- [evidently.runner package](evidently.runner.md)

    - [Submodules](evidently.runner.md#submodules)

    - [evidently.runner.dashboard_runner module](evidently.runner.md#module-evidently.runner.dashboard_runner)

        - [`DashboardRunner`](evidently.runner.md#evidently.runner.dashboard_runner.DashboardRunner)

            - [`DashboardRunner.run()`](evidently.runner.md#evidently.runner.dashboard_runner.DashboardRunner.run)

        - [`DashboardRunnerOptions`](evidently.runner.md#evidently.runner.dashboard_runner.DashboardRunnerOptions)

            - [`DashboardRunnerOptions.dashboard_tabs`](evidently.runner.md#evidently.runner.dashboard_runner.DashboardRunnerOptions.dashboard_tabs)

    - [evidently.runner.loader module](evidently.runner.md#module-evidently.runner.loader)

        - [`DataLoader`](evidently.runner.md#evidently.runner.loader.DataLoader)

            - [`DataLoader.load()`](evidently.runner.md#evidently.runner.loader.DataLoader.load)

        - [`DataOptions`](evidently.runner.md#evidently.runner.loader.DataOptions)

            - [`DataOptions.column_names`](evidently.runner.md#evidently.runner.loader.DataOptions.column_names)

            - [`DataOptions.date_column`](evidently.runner.md#evidently.runner.loader.DataOptions.date_column)

            - [`DataOptions.header`](evidently.runner.md#evidently.runner.loader.DataOptions.header)

            - [`DataOptions.separator`](evidently.runner.md#evidently.runner.loader.DataOptions.separator)

        - [`RandomizedSkipRows`](evidently.runner.md#evidently.runner.loader.RandomizedSkipRows)

            - [`RandomizedSkipRows.skiprows()`](evidently.runner.md#evidently.runner.loader.RandomizedSkipRows.skiprows)

        - [`SamplingOptions`](evidently.runner.md#evidently.runner.loader.SamplingOptions)

            - [`SamplingOptions.n`](evidently.runner.md#evidently.runner.loader.SamplingOptions.n)

            - [`SamplingOptions.random_seed`](evidently.runner.md#evidently.runner.loader.SamplingOptions.random_seed)

            - [`SamplingOptions.ratio`](evidently.runner.md#evidently.runner.loader.SamplingOptions.ratio)

            - [`SamplingOptions.type`](evidently.runner.md#evidently.runner.loader.SamplingOptions.type)

    - [evidently.runner.profile_runner module](evidently.runner.md#module-evidently.runner.profile_runner)

        - [`ProfileRunner`](evidently.runner.md#evidently.runner.profile_runner.ProfileRunner)

            - [`ProfileRunner.run()`](evidently.runner.md#evidently.runner.profile_runner.ProfileRunner.run)

        - [`ProfileRunnerOptions`](evidently.runner.md#evidently.runner.profile_runner.ProfileRunnerOptions)

            - [`ProfileRunnerOptions.pretty_print`](evidently.runner.md#evidently.runner.profile_runner.ProfileRunnerOptions.pretty_print)

            - [`ProfileRunnerOptions.profile_parts`](evidently.runner.md#evidently.runner.profile_runner.ProfileRunnerOptions.profile_parts)

    - [evidently.runner.runner module](evidently.runner.md#module-evidently.runner.runner)

        - [`Runner`](evidently.runner.md#evidently.runner.runner.Runner)

        - [`RunnerOptions`](evidently.runner.md#evidently.runner.runner.RunnerOptions)

            - [`RunnerOptions.column_mapping`](evidently.runner.md#evidently.runner.runner.RunnerOptions.column_mapping)

            - [`RunnerOptions.current_data_options`](evidently.runner.md#evidently.runner.runner.RunnerOptions.current_data_options)

            - [`RunnerOptions.current_data_path`](evidently.runner.md#evidently.runner.runner.RunnerOptions.current_data_path)

            - [`RunnerOptions.current_data_sampling`](evidently.runner.md#evidently.runner.runner.RunnerOptions.current_data_sampling)

            - [`RunnerOptions.options`](evidently.runner.md#evidently.runner.runner.RunnerOptions.options)

            - [`RunnerOptions.output_path`](evidently.runner.md#evidently.runner.runner.RunnerOptions.output_path)

            - [`RunnerOptions.reference_data_options`](evidently.runner.md#evidently.runner.runner.RunnerOptions.reference_data_options)

            - [`RunnerOptions.reference_data_path`](evidently.runner.md#evidently.runner.runner.RunnerOptions.reference_data_path)

            - [`RunnerOptions.reference_data_sampling`](evidently.runner.md#evidently.runner.runner.RunnerOptions.reference_data_sampling)

        - [`parse_options()`](evidently.runner.md#evidently.runner.runner.parse_options)

    - [Module contents](evidently.runner.md#module-evidently.runner)

- [evidently.suite package](evidently.suite.md)

    - [Submodules](evidently.suite.md#submodules)

    - [evidently.suite.base_suite module](evidently.suite.md#module-evidently.suite.base_suite)

        - [`Context`](evidently.suite.md#evidently.suite.base_suite.Context)

            - [`Context.execution_graph`](evidently.suite.md#evidently.suite.base_suite.Context.execution_graph)

            - [`Context.metric_results`](evidently.suite.md#evidently.suite.base_suite.Context.metric_results)

            - [`Context.metrics`](evidently.suite.md#evidently.suite.base_suite.Context.metrics)

            - [`Context.renderers`](evidently.suite.md#evidently.suite.base_suite.Context.renderers)

            - [`Context.state`](evidently.suite.md#evidently.suite.base_suite.Context.state)

            - [`Context.test_results`](evidently.suite.md#evidently.suite.base_suite.Context.test_results)

            - [`Context.tests`](evidently.suite.md#evidently.suite.base_suite.Context.tests)

        - [`Display`](evidently.suite.md#evidently.suite.base_suite.Display)

            - [`Display.as_dict()`](evidently.suite.md#evidently.suite.base_suite.Display.as_dict)

            - [`Display.json()`](evidently.suite.md#evidently.suite.base_suite.Display.json)

            - [`Display.options_provider`](evidently.suite.md#evidently.suite.base_suite.Display.options_provider)

            - [`Display.save_html()`](evidently.suite.md#evidently.suite.base_suite.Display.save_html)

            - [`Display.save_json()`](evidently.suite.md#evidently.suite.base_suite.Display.save_json)

            - [`Display.show()`](evidently.suite.md#evidently.suite.base_suite.Display.show)

        - [`ExecutionError`](evidently.suite.md#evidently.suite.base_suite.ExecutionError)

        - [`State`](evidently.suite.md#evidently.suite.base_suite.State)

            - [`State.name`](evidently.suite.md#evidently.suite.base_suite.State.name)

        - [`States`](evidently.suite.md#evidently.suite.base_suite.States)

            - [`States.Calculated`](evidently.suite.md#evidently.suite.base_suite.States.Calculated)

            - [`States.Init`](evidently.suite.md#evidently.suite.base_suite.States.Init)

            - [`States.Tested`](evidently.suite.md#evidently.suite.base_suite.States.Tested)

            - [`States.Verified`](evidently.suite.md#evidently.suite.base_suite.States.Verified)

        - [`Suite`](evidently.suite.md#evidently.suite.base_suite.Suite)

            - [`Suite.add_metric()`](evidently.suite.md#evidently.suite.base_suite.Suite.add_metric)

            - [`Suite.add_test()`](evidently.suite.md#evidently.suite.base_suite.Suite.add_test)

            - [`Suite.context`](evidently.suite.md#evidently.suite.base_suite.Suite.context)

            - [`Suite.run_calculate()`](evidently.suite.md#evidently.suite.base_suite.Suite.run_calculate)

            - [`Suite.run_checks()`](evidently.suite.md#evidently.suite.base_suite.Suite.run_checks)

            - [`Suite.verify()`](evidently.suite.md#evidently.suite.base_suite.Suite.verify)

        - [`find_metric_renderer()`](evidently.suite.md#evidently.suite.base_suite.find_metric_renderer)

        - [`find_test_renderer()`](evidently.suite.md#evidently.suite.base_suite.find_test_renderer)

    - [evidently.suite.execution_graph module](evidently.suite.md#module-evidently.suite.execution_graph)

        - [`ExecutionGraph`](evidently.suite.md#evidently.suite.execution_graph.ExecutionGraph)

            - [`ExecutionGraph.get_metric_execution_iterator()`](evidently.suite.md#evidently.suite.execution_graph.ExecutionGraph.get_metric_execution_iterator)

            - [`ExecutionGraph.get_test_execution_iterator()`](evidently.suite.md#evidently.suite.execution_graph.ExecutionGraph.get_test_execution_iterator)

        - [`SimpleExecutionGraph`](evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph)

            - [`SimpleExecutionGraph.get_metric_execution_iterator()`](evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph.get_metric_execution_iterator)

            - [`SimpleExecutionGraph.get_test_execution_iterator()`](evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph.get_test_execution_iterator)

            - [`SimpleExecutionGraph.metrics`](evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph.metrics)

            - [`SimpleExecutionGraph.tests`](evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph.tests)

    - [Module contents](evidently.suite.md#module-evidently.suite)

- [evidently.tabs package](evidently.tabs.md)

    - [Module contents](evidently.tabs.md#module-evidently.tabs)

- [evidently.test_preset package](evidently.test_preset.md)

    - [Submodules](evidently.test_preset.md#submodules)

    - [evidently.test_preset.classification_binary module](evidently.test_preset.md#module-evidently.test_preset.classification_binary)

        - [`BinaryClassificationTestPreset`](evidently.test_preset.md#evidently.test_preset.classification_binary.BinaryClassificationTestPreset)

            - [`BinaryClassificationTestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.classification_binary.BinaryClassificationTestPreset.generate_tests)

    - [evidently.test_preset.classification_binary_topk module](evidently.test_preset.md#module-evidently.test_preset.classification_binary_topk)

        - [`BinaryClassificationTopKTestPreset`](evidently.test_preset.md#evidently.test_preset.classification_binary_topk.BinaryClassificationTopKTestPreset)

            - [`BinaryClassificationTopKTestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.classification_binary_topk.BinaryClassificationTopKTestPreset.generate_tests)

    - [evidently.test_preset.classification_multiclass module](evidently.test_preset.md#module-evidently.test_preset.classification_multiclass)

        - [`MulticlassClassificationTestPreset`](evidently.test_preset.md#evidently.test_preset.classification_multiclass.MulticlassClassificationTestPreset)

            - [`MulticlassClassificationTestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.classification_multiclass.MulticlassClassificationTestPreset.generate_tests)

    - [evidently.test_preset.data_drift module](evidently.test_preset.md#module-evidently.test_preset.data_drift)

        - [`DataDriftTestPreset`](evidently.test_preset.md#evidently.test_preset.data_drift.DataDriftTestPreset)

            - [`DataDriftTestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.data_drift.DataDriftTestPreset.generate_tests)

    - [evidently.test_preset.data_quality module](evidently.test_preset.md#module-evidently.test_preset.data_quality)

        - [`DataQualityTestPreset`](evidently.test_preset.md#evidently.test_preset.data_quality.DataQualityTestPreset)

            - [`DataQualityTestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.data_quality.DataQualityTestPreset.generate_tests)

    - [evidently.test_preset.data_stability module](evidently.test_preset.md#module-evidently.test_preset.data_stability)

        - [`DataStabilityTestPreset`](evidently.test_preset.md#evidently.test_preset.data_stability.DataStabilityTestPreset)

            - [`DataStabilityTestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.data_stability.DataStabilityTestPreset.generate_tests)

    - [evidently.test_preset.no_target_performance module](evidently.test_preset.md#module-evidently.test_preset.no_target_performance)

        - [`NoTargetPerformanceTestPreset`](evidently.test_preset.md#evidently.test_preset.no_target_performance.NoTargetPerformanceTestPreset)

            - [`NoTargetPerformanceTestPreset.columns`](evidently.test_preset.md#evidently.test_preset.no_target_performance.NoTargetPerformanceTestPreset.columns)

            - [`NoTargetPerformanceTestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.no_target_performance.NoTargetPerformanceTestPreset.generate_tests)

    - [evidently.test_preset.regression module](evidently.test_preset.md#module-evidently.test_preset.regression)

        - [`RegressionTestPreset`](evidently.test_preset.md#evidently.test_preset.regression.RegressionTestPreset)

            - [`RegressionTestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.regression.RegressionTestPreset.generate_tests)

    - [evidently.test_preset.test_preset module](evidently.test_preset.md#module-evidently.test_preset.test_preset)

        - [`TestPreset`](evidently.test_preset.md#evidently.test_preset.test_preset.TestPreset)

            - [`TestPreset.generate_tests()`](evidently.test_preset.md#evidently.test_preset.test_preset.TestPreset.generate_tests)

    - [Module contents](evidently.test_preset.md#module-evidently.test_preset)

- [evidently.test_suite package](evidently.test_suite.md)

    - [Submodules](evidently.test_suite.md#submodules)

    - [evidently.test_suite.test_suite module](evidently.test_suite.md#module-evidently.test_suite.test_suite)

        - [`TestSuite`](evidently.test_suite.md#evidently.test_suite.test_suite.TestSuite)

            - [`TestSuite.as_dict()`](evidently.test_suite.md#evidently.test_suite.test_suite.TestSuite.as_dict)

            - [`TestSuite.run()`](evidently.test_suite.md#evidently.test_suite.test_suite.TestSuite.run)

    - [Module contents](evidently.test_suite.md#module-evidently.test_suite)

- [evidently.tests package](evidently.tests.md)

    - [Submodules](evidently.tests.md#submodules)

    - [evidently.tests.base_test module](evidently.tests.md#module-evidently.tests.base_test)

        - [`BaseCheckValueTest`](evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest)

            - [`BaseCheckValueTest.calculate_value_for_test()`](evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.calculate_value_for_test)

            - [`BaseCheckValueTest.check()`](evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.check)

            - [`BaseCheckValueTest.get_condition()`](evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.get_condition)

            - [`BaseCheckValueTest.get_description()`](evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.get_description)

            - [`BaseCheckValueTest.groups()`](evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.groups)

            - [`BaseCheckValueTest.value`](evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.value)

        - [`BaseConditionsTest`](evidently.tests.md#evidently.tests.base_test.BaseConditionsTest)

            - [`BaseConditionsTest.condition`](evidently.tests.md#evidently.tests.base_test.BaseConditionsTest.condition)

        - [`GroupData`](evidently.tests.md#evidently.tests.base_test.GroupData)

            - [`GroupData.description`](evidently.tests.md#evidently.tests.base_test.GroupData.description)

            - [`GroupData.id`](evidently.tests.md#evidently.tests.base_test.GroupData.id)

            - [`GroupData.severity`](evidently.tests.md#evidently.tests.base_test.GroupData.severity)

            - [`GroupData.sort_index`](evidently.tests.md#evidently.tests.base_test.GroupData.sort_index)

            - [`GroupData.title`](evidently.tests.md#evidently.tests.base_test.GroupData.title)

        - [`GroupTypeData`](evidently.tests.md#evidently.tests.base_test.GroupTypeData)

            - [`GroupTypeData.add_value()`](evidently.tests.md#evidently.tests.base_test.GroupTypeData.add_value)

            - [`GroupTypeData.id`](evidently.tests.md#evidently.tests.base_test.GroupTypeData.id)

            - [`GroupTypeData.title`](evidently.tests.md#evidently.tests.base_test.GroupTypeData.title)

            - [`GroupTypeData.values`](evidently.tests.md#evidently.tests.base_test.GroupTypeData.values)

        - [`GroupingTypes`](evidently.tests.md#evidently.tests.base_test.GroupingTypes)

            - [`GroupingTypes.ByClass`](evidently.tests.md#evidently.tests.base_test.GroupingTypes.ByClass)

            - [`GroupingTypes.ByFeature`](evidently.tests.md#evidently.tests.base_test.GroupingTypes.ByFeature)

            - [`GroupingTypes.TestGroup`](evidently.tests.md#evidently.tests.base_test.GroupingTypes.TestGroup)

            - [`GroupingTypes.TestType`](evidently.tests.md#evidently.tests.base_test.GroupingTypes.TestType)

        - [`Test`](evidently.tests.md#evidently.tests.base_test.Test)

            - [`Test.check()`](evidently.tests.md#evidently.tests.base_test.Test.check)

            - [`Test.context`](evidently.tests.md#evidently.tests.base_test.Test.context)

            - [`Test.get_result()`](evidently.tests.md#evidently.tests.base_test.Test.get_result)

            - [`Test.group`](evidently.tests.md#evidently.tests.base_test.Test.group)

            - [`Test.name`](evidently.tests.md#evidently.tests.base_test.Test.name)

            - [`Test.set_context()`](evidently.tests.md#evidently.tests.base_test.Test.set_context)

        - [`TestResult`](evidently.tests.md#evidently.tests.base_test.TestResult)

            - [`TestResult.ERROR`](evidently.tests.md#evidently.tests.base_test.TestResult.ERROR)

            - [`TestResult.FAIL`](evidently.tests.md#evidently.tests.base_test.TestResult.FAIL)

            - [`TestResult.SKIPPED`](evidently.tests.md#evidently.tests.base_test.TestResult.SKIPPED)

            - [`TestResult.SUCCESS`](evidently.tests.md#evidently.tests.base_test.TestResult.SUCCESS)

            - [`TestResult.WARNING`](evidently.tests.md#evidently.tests.base_test.TestResult.WARNING)

            - [`TestResult.description`](evidently.tests.md#evidently.tests.base_test.TestResult.description)

            - [`TestResult.groups`](evidently.tests.md#evidently.tests.base_test.TestResult.groups)

            - [`TestResult.is_passed()`](evidently.tests.md#evidently.tests.base_test.TestResult.is_passed)

            - [`TestResult.mark_as_error()`](evidently.tests.md#evidently.tests.base_test.TestResult.mark_as_error)

            - [`TestResult.mark_as_fail()`](evidently.tests.md#evidently.tests.base_test.TestResult.mark_as_fail)

            - [`TestResult.mark_as_success()`](evidently.tests.md#evidently.tests.base_test.TestResult.mark_as_success)

            - [`TestResult.mark_as_warning()`](evidently.tests.md#evidently.tests.base_test.TestResult.mark_as_warning)

            - [`TestResult.name`](evidently.tests.md#evidently.tests.base_test.TestResult.name)

            - [`TestResult.set_status()`](evidently.tests.md#evidently.tests.base_test.TestResult.set_status)

            - [`TestResult.status`](evidently.tests.md#evidently.tests.base_test.TestResult.status)

        - [`TestValueCondition`](evidently.tests.md#evidently.tests.base_test.TestValueCondition)

            - [`TestValueCondition.as_dict()`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.as_dict)

            - [`TestValueCondition.check_value()`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.check_value)

            - [`TestValueCondition.eq`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.eq)

            - [`TestValueCondition.gt`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.gt)

            - [`TestValueCondition.gte`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.gte)

            - [`TestValueCondition.has_condition()`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.has_condition)

            - [`TestValueCondition.is_in`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.is_in)

            - [`TestValueCondition.lt`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.lt)

            - [`TestValueCondition.lte`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.lte)

            - [`TestValueCondition.not_eq`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.not_eq)

            - [`TestValueCondition.not_in`](evidently.tests.md#evidently.tests.base_test.TestValueCondition.not_in)

        - [`generate_column_tests()`](evidently.tests.md#evidently.tests.base_test.generate_column_tests)

    - [evidently.tests.classification_performance_tests module](evidently.tests.md#module-evidently.tests.classification_performance_tests)

        - [`ByClassClassificationTest`](evidently.tests.md#evidently.tests.classification_performance_tests.ByClassClassificationTest)

            - [`ByClassClassificationTest.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.ByClassClassificationTest.metric)

            - [`ByClassClassificationTest.name`](evidently.tests.md#evidently.tests.classification_performance_tests.ByClassClassificationTest.name)

        - [`SimpleClassificationTest`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest)

            - [`SimpleClassificationTest.calculate_value_for_test()`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.calculate_value_for_test)

            - [`SimpleClassificationTest.get_condition()`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.get_condition)

            - [`SimpleClassificationTest.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.get_value)

            - [`SimpleClassificationTest.group`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.group)

            - [`SimpleClassificationTest.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.metric)

            - [`SimpleClassificationTest.name`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.name)

        - [`SimpleClassificationTestTopK`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK)

            - [`SimpleClassificationTestTopK.calculate_value_for_test()`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.calculate_value_for_test)

            - [`SimpleClassificationTestTopK.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.condition)

            - [`SimpleClassificationTestTopK.get_condition()`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.get_condition)

            - [`SimpleClassificationTestTopK.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.metric)

            - [`SimpleClassificationTestTopK.name`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.name)

            - [`SimpleClassificationTestTopK.value`](evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.value)

        - [`TestAccuracyScore`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore)

            - [`TestAccuracyScore.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.condition)

            - [`TestAccuracyScore.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.get_description)

            - [`TestAccuracyScore.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.get_value)

            - [`TestAccuracyScore.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.metric)

            - [`TestAccuracyScore.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.name)

            - [`TestAccuracyScore.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.value)

        - [`TestAccuracyScoreRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer)

            - [`TestAccuracyScoreRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer.color_options)

            - [`TestAccuracyScoreRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer.render_html)

            - [`TestAccuracyScoreRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer.render_json)

        - [`TestF1ByClass`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClass)

            - [`TestF1ByClass.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClass.get_description)

            - [`TestF1ByClass.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClass.get_value)

            - [`TestF1ByClass.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClass.name)

        - [`TestF1ByClassRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClassRenderer)

            - [`TestF1ByClassRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClassRenderer.color_options)

            - [`TestF1ByClassRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClassRenderer.render_html)

            - [`TestF1ByClassRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClassRenderer.render_json)

        - [`TestF1Score`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score)

            - [`TestF1Score.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.condition)

            - [`TestF1Score.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.get_description)

            - [`TestF1Score.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.get_value)

            - [`TestF1Score.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.metric)

            - [`TestF1Score.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.name)

            - [`TestF1Score.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.value)

        - [`TestF1ScoreRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ScoreRenderer)

            - [`TestF1ScoreRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ScoreRenderer.color_options)

            - [`TestF1ScoreRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ScoreRenderer.render_html)

            - [`TestF1ScoreRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ScoreRenderer.render_json)

        - [`TestFNR`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR)

            - [`TestFNR.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.condition)

            - [`TestFNR.get_condition()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.get_condition)

            - [`TestFNR.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.get_description)

            - [`TestFNR.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.get_value)

            - [`TestFNR.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.metric)

            - [`TestFNR.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.name)

            - [`TestFNR.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.value)

        - [`TestFNRRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNRRenderer)

            - [`TestFNRRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNRRenderer.color_options)

            - [`TestFNRRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNRRenderer.render_html)

            - [`TestFNRRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFNRRenderer.render_json)

        - [`TestFPR`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR)

            - [`TestFPR.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.condition)

            - [`TestFPR.get_condition()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.get_condition)

            - [`TestFPR.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.get_description)

            - [`TestFPR.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.get_value)

            - [`TestFPR.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.metric)

            - [`TestFPR.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.name)

            - [`TestFPR.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.value)

        - [`TestFPRRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPRRenderer)

            - [`TestFPRRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPRRenderer.color_options)

            - [`TestFPRRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPRRenderer.render_html)

            - [`TestFPRRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestFPRRenderer.render_json)

        - [`TestLogLoss`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss)

            - [`TestLogLoss.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.condition)

            - [`TestLogLoss.get_condition()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.get_condition)

            - [`TestLogLoss.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.get_description)

            - [`TestLogLoss.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.get_value)

            - [`TestLogLoss.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.metric)

            - [`TestLogLoss.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.name)

            - [`TestLogLoss.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.value)

        - [`TestLogLossRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLossRenderer)

            - [`TestLogLossRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLossRenderer.color_options)

            - [`TestLogLossRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLossRenderer.render_html)

            - [`TestLogLossRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLossRenderer.render_json)

        - [`TestPrecisionByClass`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClass)

            - [`TestPrecisionByClass.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClass.get_description)

            - [`TestPrecisionByClass.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClass.get_value)

            - [`TestPrecisionByClass.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClass.name)

        - [`TestPrecisionByClassRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer)

            - [`TestPrecisionByClassRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer.color_options)

            - [`TestPrecisionByClassRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer.render_html)

            - [`TestPrecisionByClassRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer.render_json)

        - [`TestPrecisionScore`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore)

            - [`TestPrecisionScore.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.condition)

            - [`TestPrecisionScore.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.get_description)

            - [`TestPrecisionScore.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.get_value)

            - [`TestPrecisionScore.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.metric)

            - [`TestPrecisionScore.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.name)

            - [`TestPrecisionScore.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.value)

        - [`TestPrecisionScoreRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer)

            - [`TestPrecisionScoreRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer.color_options)

            - [`TestPrecisionScoreRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer.render_html)

            - [`TestPrecisionScoreRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer.render_json)

        - [`TestRecallByClass`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClass)

            - [`TestRecallByClass.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClass.get_description)

            - [`TestRecallByClass.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClass.get_value)

            - [`TestRecallByClass.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClass.name)

        - [`TestRecallByClassRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClassRenderer)

            - [`TestRecallByClassRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClassRenderer.color_options)

            - [`TestRecallByClassRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClassRenderer.render_html)

            - [`TestRecallByClassRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClassRenderer.render_json)

        - [`TestRecallScore`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore)

            - [`TestRecallScore.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.condition)

            - [`TestRecallScore.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.get_description)

            - [`TestRecallScore.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.get_value)

            - [`TestRecallScore.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.metric)

            - [`TestRecallScore.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.name)

            - [`TestRecallScore.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.value)

        - [`TestRecallScoreRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScoreRenderer)

            - [`TestRecallScoreRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScoreRenderer.color_options)

            - [`TestRecallScoreRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScoreRenderer.render_html)

            - [`TestRecallScoreRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScoreRenderer.render_json)

        - [`TestRocAuc`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc)

            - [`TestRocAuc.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.condition)

            - [`TestRocAuc.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.get_description)

            - [`TestRocAuc.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.get_value)

            - [`TestRocAuc.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.metric)

            - [`TestRocAuc.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.name)

            - [`TestRocAuc.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.value)

        - [`TestRocAucRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAucRenderer)

            - [`TestRocAucRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAucRenderer.color_options)

            - [`TestRocAucRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAucRenderer.render_html)

            - [`TestRocAucRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAucRenderer.render_json)

        - [`TestTNR`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR)

            - [`TestTNR.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.condition)

            - [`TestTNR.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.get_description)

            - [`TestTNR.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.get_value)

            - [`TestTNR.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.metric)

            - [`TestTNR.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.name)

            - [`TestTNR.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.value)

        - [`TestTNRRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNRRenderer)

            - [`TestTNRRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNRRenderer.color_options)

            - [`TestTNRRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNRRenderer.render_html)

            - [`TestTNRRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTNRRenderer.render_json)

        - [`TestTPR`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR)

            - [`TestTPR.condition`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.condition)

            - [`TestTPR.get_description()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.get_description)

            - [`TestTPR.get_value()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.get_value)

            - [`TestTPR.metric`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.metric)

            - [`TestTPR.name`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.name)

            - [`TestTPR.value`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.value)

        - [`TestTPRRenderer`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPRRenderer)

            - [`TestTPRRenderer.color_options`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPRRenderer.color_options)

            - [`TestTPRRenderer.render_html()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPRRenderer.render_html)

            - [`TestTPRRenderer.render_json()`](evidently.tests.md#evidently.tests.classification_performance_tests.TestTPRRenderer.render_json)

    - [evidently.tests.data_drift_tests module](evidently.tests.md#module-evidently.tests.data_drift_tests)

        - [`BaseDataDriftMetricsTest`](evidently.tests.md#evidently.tests.data_drift_tests.BaseDataDriftMetricsTest)

            - [`BaseDataDriftMetricsTest.check()`](evidently.tests.md#evidently.tests.data_drift_tests.BaseDataDriftMetricsTest.check)

            - [`BaseDataDriftMetricsTest.group`](evidently.tests.md#evidently.tests.data_drift_tests.BaseDataDriftMetricsTest.group)

            - [`BaseDataDriftMetricsTest.metric`](evidently.tests.md#evidently.tests.data_drift_tests.BaseDataDriftMetricsTest.metric)

        - [`TestAllFeaturesValueDrift`](evidently.tests.md#evidently.tests.data_drift_tests.TestAllFeaturesValueDrift)

            - [`TestAllFeaturesValueDrift.generate()`](evidently.tests.md#evidently.tests.data_drift_tests.TestAllFeaturesValueDrift.generate)

        - [`TestColumnValueDrift`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift)

            - [`TestColumnValueDrift.check()`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.check)

            - [`TestColumnValueDrift.column_name`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.column_name)

            - [`TestColumnValueDrift.group`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.group)

            - [`TestColumnValueDrift.metric`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.metric)

            - [`TestColumnValueDrift.name`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.name)

        - [`TestColumnValueDriftRenderer`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDriftRenderer)

            - [`TestColumnValueDriftRenderer.color_options`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDriftRenderer.color_options)

            - [`TestColumnValueDriftRenderer.render_html()`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDriftRenderer.render_html)

            - [`TestColumnValueDriftRenderer.render_json()`](evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDriftRenderer.render_json)

        - [`TestCustomFeaturesValueDrift`](evidently.tests.md#evidently.tests.data_drift_tests.TestCustomFeaturesValueDrift)

            - [`TestCustomFeaturesValueDrift.features`](evidently.tests.md#evidently.tests.data_drift_tests.TestCustomFeaturesValueDrift.features)

            - [`TestCustomFeaturesValueDrift.generate()`](evidently.tests.md#evidently.tests.data_drift_tests.TestCustomFeaturesValueDrift.generate)

        - [`TestDataDriftResult`](evidently.tests.md#evidently.tests.data_drift_tests.TestDataDriftResult)

            - [`TestDataDriftResult.features`](evidently.tests.md#evidently.tests.data_drift_tests.TestDataDriftResult.features)

        - [`TestNumberOfDriftedColumns`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns)

            - [`TestNumberOfDriftedColumns.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.calculate_value_for_test)

            - [`TestNumberOfDriftedColumns.condition`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.condition)

            - [`TestNumberOfDriftedColumns.get_condition()`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.get_condition)

            - [`TestNumberOfDriftedColumns.get_description()`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.get_description)

            - [`TestNumberOfDriftedColumns.metric`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.metric)

            - [`TestNumberOfDriftedColumns.name`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.name)

            - [`TestNumberOfDriftedColumns.value`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.value)

        - [`TestNumberOfDriftedColumnsRenderer`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer)

            - [`TestNumberOfDriftedColumnsRenderer.color_options`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer.color_options)

            - [`TestNumberOfDriftedColumnsRenderer.render_html()`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer.render_html)

            - [`TestNumberOfDriftedColumnsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer.render_json)

        - [`TestShareOfDriftedColumns`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns)

            - [`TestShareOfDriftedColumns.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.calculate_value_for_test)

            - [`TestShareOfDriftedColumns.condition`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.condition)

            - [`TestShareOfDriftedColumns.get_condition()`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.get_condition)

            - [`TestShareOfDriftedColumns.get_description()`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.get_description)

            - [`TestShareOfDriftedColumns.metric`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.metric)

            - [`TestShareOfDriftedColumns.name`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.name)

            - [`TestShareOfDriftedColumns.value`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.value)

        - [`TestShareOfDriftedColumnsRenderer`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer)

            - [`TestShareOfDriftedColumnsRenderer.color_options`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer.color_options)

            - [`TestShareOfDriftedColumnsRenderer.render_html()`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer.render_html)

            - [`TestShareOfDriftedColumnsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer.render_json)

    - [evidently.tests.data_integrity_tests module](evidently.tests.md#module-evidently.tests.data_integrity_tests)

        - [`BaseIntegrityByColumnsConditionTest`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest)

            - [`BaseIntegrityByColumnsConditionTest.column_name`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest.column_name)

            - [`BaseIntegrityByColumnsConditionTest.data_integrity_metric`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest.data_integrity_metric)

            - [`BaseIntegrityByColumnsConditionTest.group`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest.group)

            - [`BaseIntegrityByColumnsConditionTest.groups()`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest.groups)

        - [`BaseIntegrityColumnMissingValuesTest`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest)

            - [`BaseIntegrityColumnMissingValuesTest.column_name`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest.column_name)

            - [`BaseIntegrityColumnMissingValuesTest.group`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest.group)

            - [`BaseIntegrityColumnMissingValuesTest.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest.metric)

        - [`BaseIntegrityMissingValuesValuesTest`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityMissingValuesValuesTest)

            - [`BaseIntegrityMissingValuesValuesTest.group`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityMissingValuesValuesTest.group)

            - [`BaseIntegrityMissingValuesValuesTest.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityMissingValuesValuesTest.metric)

        - [`BaseIntegrityOneColumnTest`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest)

            - [`BaseIntegrityOneColumnTest.column_name`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest.column_name)

            - [`BaseIntegrityOneColumnTest.group`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest.group)

            - [`BaseIntegrityOneColumnTest.groups()`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest.groups)

            - [`BaseIntegrityOneColumnTest.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest.metric)

        - [`BaseIntegrityValueTest`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityValueTest)

            - [`BaseIntegrityValueTest.group`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityValueTest.group)

            - [`BaseIntegrityValueTest.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityValueTest.metric)

        - [`BaseTestMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer)

            - [`BaseTestMissingValuesRenderer.MISSING_VALUES_NAMING_MAPPING`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer.MISSING_VALUES_NAMING_MAPPING)

            - [`BaseTestMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer.color_options)

            - [`BaseTestMissingValuesRenderer.get_table_with_missing_values_and_percents_by_column()`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer.get_table_with_missing_values_and_percents_by_column)

            - [`BaseTestMissingValuesRenderer.get_table_with_number_of_missing_values_by_one_missing_value()`](evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer.get_table_with_number_of_missing_values_by_one_missing_value)

        - [`TestAllColumnsShareOfMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestAllColumnsShareOfMissingValues)

            - [`TestAllColumnsShareOfMissingValues.generate()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestAllColumnsShareOfMissingValues.generate)

        - [`TestColumnAllConstantValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValues)

            - [`TestColumnAllConstantValues.check()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValues.check)

            - [`TestColumnAllConstantValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValues.metric)

            - [`TestColumnAllConstantValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValues.name)

        - [`TestColumnAllConstantValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValuesRenderer)

            - [`TestColumnAllConstantValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValuesRenderer.color_options)

            - [`TestColumnAllConstantValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValuesRenderer.render_html)

        - [`TestColumnAllUniqueValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues)

            - [`TestColumnAllUniqueValues.check()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues.check)

            - [`TestColumnAllUniqueValues.column_name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues.column_name)

            - [`TestColumnAllUniqueValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues.metric)

            - [`TestColumnAllUniqueValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues.name)

        - [`TestColumnAllUniqueValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValuesRenderer)

            - [`TestColumnAllUniqueValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValuesRenderer.color_options)

            - [`TestColumnAllUniqueValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValuesRenderer.render_html)

        - [`TestColumnNumberOfDifferentMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues)

            - [`TestColumnNumberOfDifferentMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.calculate_value_for_test)

            - [`TestColumnNumberOfDifferentMissingValues.column_name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.column_name)

            - [`TestColumnNumberOfDifferentMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.condition)

            - [`TestColumnNumberOfDifferentMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.get_condition)

            - [`TestColumnNumberOfDifferentMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.get_description)

            - [`TestColumnNumberOfDifferentMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.metric)

            - [`TestColumnNumberOfDifferentMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.name)

            - [`TestColumnNumberOfDifferentMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.value)

        - [`TestColumnNumberOfDifferentMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer)

            - [`TestColumnNumberOfDifferentMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer.color_options)

            - [`TestColumnNumberOfDifferentMissingValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer.render_html)

            - [`TestColumnNumberOfDifferentMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer.render_json)

        - [`TestColumnNumberOfMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues)

            - [`TestColumnNumberOfMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.calculate_value_for_test)

            - [`TestColumnNumberOfMissingValues.column_name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.column_name)

            - [`TestColumnNumberOfMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.condition)

            - [`TestColumnNumberOfMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.get_condition)

            - [`TestColumnNumberOfMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.get_description)

            - [`TestColumnNumberOfMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.metric)

            - [`TestColumnNumberOfMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.name)

            - [`TestColumnNumberOfMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.value)

        - [`TestColumnNumberOfMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValuesRenderer)

            - [`TestColumnNumberOfMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValuesRenderer.color_options)

            - [`TestColumnNumberOfMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValuesRenderer.render_json)

        - [`TestColumnShareOfMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues)

            - [`TestColumnShareOfMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.calculate_value_for_test)

            - [`TestColumnShareOfMissingValues.column_name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.column_name)

            - [`TestColumnShareOfMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.condition)

            - [`TestColumnShareOfMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.get_condition)

            - [`TestColumnShareOfMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.get_description)

            - [`TestColumnShareOfMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.metric)

            - [`TestColumnShareOfMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.name)

            - [`TestColumnShareOfMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.value)

        - [`TestColumnShareOfMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValuesRenderer)

            - [`TestColumnShareOfMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValuesRenderer.color_options)

            - [`TestColumnShareOfMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValuesRenderer.render_json)

        - [`TestColumnValueRegExp`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp)

            - [`TestColumnValueRegExp.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.calculate_value_for_test)

            - [`TestColumnValueRegExp.column_name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.column_name)

            - [`TestColumnValueRegExp.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.get_condition)

            - [`TestColumnValueRegExp.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.get_description)

            - [`TestColumnValueRegExp.group`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.group)

            - [`TestColumnValueRegExp.groups()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.groups)

            - [`TestColumnValueRegExp.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.metric)

            - [`TestColumnValueRegExp.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.name)

        - [`TestColumnValueRegExpRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExpRenderer)

            - [`TestColumnValueRegExpRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExpRenderer.color_options)

            - [`TestColumnValueRegExpRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExpRenderer.render_html)

        - [`TestColumnsType`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType)

            - [`TestColumnsType.Result`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.Result)

            - [`TestColumnsType.check()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.check)

            - [`TestColumnsType.columns_type`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.columns_type)

            - [`TestColumnsType.group`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.group)

            - [`TestColumnsType.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.metric)

            - [`TestColumnsType.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.name)

        - [`TestColumnsTypeRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsTypeRenderer)

            - [`TestColumnsTypeRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsTypeRenderer.color_options)

            - [`TestColumnsTypeRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsTypeRenderer.render_html)

            - [`TestColumnsTypeRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsTypeRenderer.render_json)

        - [`TestNumberOfColumns`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns)

            - [`TestNumberOfColumns.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.calculate_value_for_test)

            - [`TestNumberOfColumns.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.condition)

            - [`TestNumberOfColumns.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.get_condition)

            - [`TestNumberOfColumns.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.get_description)

            - [`TestNumberOfColumns.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.metric)

            - [`TestNumberOfColumns.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.name)

            - [`TestNumberOfColumns.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.value)

        - [`TestNumberOfColumnsRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer)

            - [`TestNumberOfColumnsRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer.color_options)

            - [`TestNumberOfColumnsRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer.render_html)

            - [`TestNumberOfColumnsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer.render_json)

        - [`TestNumberOfColumnsWithMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues)

            - [`TestNumberOfColumnsWithMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.calculate_value_for_test)

            - [`TestNumberOfColumnsWithMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.condition)

            - [`TestNumberOfColumnsWithMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.get_condition)

            - [`TestNumberOfColumnsWithMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.get_description)

            - [`TestNumberOfColumnsWithMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.metric)

            - [`TestNumberOfColumnsWithMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.name)

            - [`TestNumberOfColumnsWithMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.value)

        - [`TestNumberOfColumnsWithMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer)

            - [`TestNumberOfColumnsWithMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer.color_options)

            - [`TestNumberOfColumnsWithMissingValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer.render_html)

            - [`TestNumberOfColumnsWithMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer.render_json)

        - [`TestNumberOfConstantColumns`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns)

            - [`TestNumberOfConstantColumns.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.calculate_value_for_test)

            - [`TestNumberOfConstantColumns.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.condition)

            - [`TestNumberOfConstantColumns.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.get_condition)

            - [`TestNumberOfConstantColumns.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.get_description)

            - [`TestNumberOfConstantColumns.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.metric)

            - [`TestNumberOfConstantColumns.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.name)

            - [`TestNumberOfConstantColumns.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.value)

        - [`TestNumberOfConstantColumnsRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer)

            - [`TestNumberOfConstantColumnsRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer.color_options)

            - [`TestNumberOfConstantColumnsRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer.render_html)

            - [`TestNumberOfConstantColumnsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer.render_json)

        - [`TestNumberOfDifferentMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues)

            - [`TestNumberOfDifferentMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.calculate_value_for_test)

            - [`TestNumberOfDifferentMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.condition)

            - [`TestNumberOfDifferentMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.get_condition)

            - [`TestNumberOfDifferentMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.get_description)

            - [`TestNumberOfDifferentMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.metric)

            - [`TestNumberOfDifferentMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.name)

            - [`TestNumberOfDifferentMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.value)

        - [`TestNumberOfDifferentMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer)

            - [`TestNumberOfDifferentMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer.color_options)

            - [`TestNumberOfDifferentMissingValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer.render_html)

            - [`TestNumberOfDifferentMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer.render_json)

        - [`TestNumberOfDuplicatedColumns`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns)

            - [`TestNumberOfDuplicatedColumns.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.calculate_value_for_test)

            - [`TestNumberOfDuplicatedColumns.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.condition)

            - [`TestNumberOfDuplicatedColumns.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.get_condition)

            - [`TestNumberOfDuplicatedColumns.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.get_description)

            - [`TestNumberOfDuplicatedColumns.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.metric)

            - [`TestNumberOfDuplicatedColumns.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.name)

            - [`TestNumberOfDuplicatedColumns.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.value)

        - [`TestNumberOfDuplicatedColumnsRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumnsRenderer)

            - [`TestNumberOfDuplicatedColumnsRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumnsRenderer.color_options)

            - [`TestNumberOfDuplicatedColumnsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumnsRenderer.render_json)

        - [`TestNumberOfDuplicatedRows`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows)

            - [`TestNumberOfDuplicatedRows.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.calculate_value_for_test)

            - [`TestNumberOfDuplicatedRows.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.condition)

            - [`TestNumberOfDuplicatedRows.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.get_condition)

            - [`TestNumberOfDuplicatedRows.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.get_description)

            - [`TestNumberOfDuplicatedRows.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.metric)

            - [`TestNumberOfDuplicatedRows.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.name)

            - [`TestNumberOfDuplicatedRows.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.value)

        - [`TestNumberOfDuplicatedRowsRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRowsRenderer)

            - [`TestNumberOfDuplicatedRowsRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRowsRenderer.color_options)

            - [`TestNumberOfDuplicatedRowsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRowsRenderer.render_json)

        - [`TestNumberOfEmptyColumns`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns)

            - [`TestNumberOfEmptyColumns.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.calculate_value_for_test)

            - [`TestNumberOfEmptyColumns.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.condition)

            - [`TestNumberOfEmptyColumns.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.get_condition)

            - [`TestNumberOfEmptyColumns.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.get_description)

            - [`TestNumberOfEmptyColumns.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.metric)

            - [`TestNumberOfEmptyColumns.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.name)

            - [`TestNumberOfEmptyColumns.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.value)

        - [`TestNumberOfEmptyColumnsRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumnsRenderer)

            - [`TestNumberOfEmptyColumnsRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumnsRenderer.color_options)

            - [`TestNumberOfEmptyColumnsRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumnsRenderer.render_html)

        - [`TestNumberOfEmptyRows`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows)

            - [`TestNumberOfEmptyRows.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.calculate_value_for_test)

            - [`TestNumberOfEmptyRows.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.condition)

            - [`TestNumberOfEmptyRows.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.get_condition)

            - [`TestNumberOfEmptyRows.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.get_description)

            - [`TestNumberOfEmptyRows.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.metric)

            - [`TestNumberOfEmptyRows.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.name)

            - [`TestNumberOfEmptyRows.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.value)

        - [`TestNumberOfMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues)

            - [`TestNumberOfMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.calculate_value_for_test)

            - [`TestNumberOfMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.condition)

            - [`TestNumberOfMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.get_condition)

            - [`TestNumberOfMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.get_description)

            - [`TestNumberOfMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.metric)

            - [`TestNumberOfMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.name)

            - [`TestNumberOfMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.value)

        - [`TestNumberOfMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer)

            - [`TestNumberOfMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer.color_options)

            - [`TestNumberOfMissingValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer.render_html)

            - [`TestNumberOfMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer.render_json)

        - [`TestNumberOfRows`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows)

            - [`TestNumberOfRows.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.calculate_value_for_test)

            - [`TestNumberOfRows.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.condition)

            - [`TestNumberOfRows.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.get_condition)

            - [`TestNumberOfRows.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.get_description)

            - [`TestNumberOfRows.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.metric)

            - [`TestNumberOfRows.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.name)

            - [`TestNumberOfRows.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.value)

        - [`TestNumberOfRowsRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsRenderer)

            - [`TestNumberOfRowsRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsRenderer.color_options)

            - [`TestNumberOfRowsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsRenderer.render_json)

        - [`TestNumberOfRowsWithMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues)

            - [`TestNumberOfRowsWithMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.calculate_value_for_test)

            - [`TestNumberOfRowsWithMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.condition)

            - [`TestNumberOfRowsWithMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.get_condition)

            - [`TestNumberOfRowsWithMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.get_description)

            - [`TestNumberOfRowsWithMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.metric)

            - [`TestNumberOfRowsWithMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.name)

            - [`TestNumberOfRowsWithMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.value)

        - [`TestNumberOfRowsWithMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValuesRenderer)

            - [`TestNumberOfRowsWithMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValuesRenderer.color_options)

            - [`TestNumberOfRowsWithMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValuesRenderer.render_json)

        - [`TestShareOfColumnsWithMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues)

            - [`TestShareOfColumnsWithMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.calculate_value_for_test)

            - [`TestShareOfColumnsWithMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.condition)

            - [`TestShareOfColumnsWithMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.get_condition)

            - [`TestShareOfColumnsWithMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.get_description)

            - [`TestShareOfColumnsWithMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.metric)

            - [`TestShareOfColumnsWithMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.name)

            - [`TestShareOfColumnsWithMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.value)

        - [`TestShareOfColumnsWithMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer)

            - [`TestShareOfColumnsWithMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer.color_options)

            - [`TestShareOfColumnsWithMissingValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer.render_html)

            - [`TestShareOfColumnsWithMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer.render_json)

        - [`TestShareOfMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues)

            - [`TestShareOfMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.calculate_value_for_test)

            - [`TestShareOfMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.condition)

            - [`TestShareOfMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.get_condition)

            - [`TestShareOfMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.get_description)

            - [`TestShareOfMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.metric)

            - [`TestShareOfMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.name)

            - [`TestShareOfMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.value)

        - [`TestShareOfMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer)

            - [`TestShareOfMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer.color_options)

            - [`TestShareOfMissingValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer.render_html)

            - [`TestShareOfMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer.render_json)

        - [`TestShareOfRowsWithMissingValues`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues)

            - [`TestShareOfRowsWithMissingValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.calculate_value_for_test)

            - [`TestShareOfRowsWithMissingValues.condition`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.condition)

            - [`TestShareOfRowsWithMissingValues.get_condition()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.get_condition)

            - [`TestShareOfRowsWithMissingValues.get_description()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.get_description)

            - [`TestShareOfRowsWithMissingValues.metric`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.metric)

            - [`TestShareOfRowsWithMissingValues.name`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.name)

            - [`TestShareOfRowsWithMissingValues.value`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.value)

        - [`TestShareOfRowsWithMissingValuesRenderer`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValuesRenderer)

            - [`TestShareOfRowsWithMissingValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValuesRenderer.color_options)

            - [`TestShareOfRowsWithMissingValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValuesRenderer.render_json)

    - [evidently.tests.data_quality_tests module](evidently.tests.md#module-evidently.tests.data_quality_tests)

        - [`BaseDataQualityCorrelationsMetricsValueTest`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest)

            - [`BaseDataQualityCorrelationsMetricsValueTest.group`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest.group)

            - [`BaseDataQualityCorrelationsMetricsValueTest.method`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest.method)

            - [`BaseDataQualityCorrelationsMetricsValueTest.metric`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest.metric)

        - [`BaseDataQualityMetricsValueTest`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityMetricsValueTest)

            - [`BaseDataQualityMetricsValueTest.group`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityMetricsValueTest.group)

            - [`BaseDataQualityMetricsValueTest.metric`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityMetricsValueTest.metric)

        - [`BaseDataQualityValueListMetricsTest`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest)

            - [`BaseDataQualityValueListMetricsTest.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.column_name)

            - [`BaseDataQualityValueListMetricsTest.group`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.group)

            - [`BaseDataQualityValueListMetricsTest.groups()`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.groups)

            - [`BaseDataQualityValueListMetricsTest.metric`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.metric)

            - [`BaseDataQualityValueListMetricsTest.values`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.values)

        - [`BaseDataQualityValueRangeMetricsTest`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest)

            - [`BaseDataQualityValueRangeMetricsTest.column`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.column)

            - [`BaseDataQualityValueRangeMetricsTest.group`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.group)

            - [`BaseDataQualityValueRangeMetricsTest.groups()`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.groups)

            - [`BaseDataQualityValueRangeMetricsTest.left`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.left)

            - [`BaseDataQualityValueRangeMetricsTest.metric`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.metric)

            - [`BaseDataQualityValueRangeMetricsTest.right`](evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.right)

        - [`BaseFeatureDataQualityMetricsTest`](evidently.tests.md#evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest)

            - [`BaseFeatureDataQualityMetricsTest.check()`](evidently.tests.md#evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest.check)

            - [`BaseFeatureDataQualityMetricsTest.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest.column_name)

            - [`BaseFeatureDataQualityMetricsTest.groups()`](evidently.tests.md#evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest.groups)

        - [`TestAllColumnsMostCommonValueShare`](evidently.tests.md#evidently.tests.data_quality_tests.TestAllColumnsMostCommonValueShare)

            - [`TestAllColumnsMostCommonValueShare.generate()`](evidently.tests.md#evidently.tests.data_quality_tests.TestAllColumnsMostCommonValueShare.generate)

        - [`TestCatColumnsOutOfListValues`](evidently.tests.md#evidently.tests.data_quality_tests.TestCatColumnsOutOfListValues)

            - [`TestCatColumnsOutOfListValues.generate()`](evidently.tests.md#evidently.tests.data_quality_tests.TestCatColumnsOutOfListValues.generate)

        - [`TestColumnValueMax`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax)

            - [`TestColumnValueMax.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.calculate_value_for_test)

            - [`TestColumnValueMax.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.column_name)

            - [`TestColumnValueMax.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.condition)

            - [`TestColumnValueMax.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.get_condition)

            - [`TestColumnValueMax.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.get_description)

            - [`TestColumnValueMax.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.metric)

            - [`TestColumnValueMax.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.name)

            - [`TestColumnValueMax.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.value)

        - [`TestColumnValueMaxRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMaxRenderer)

            - [`TestColumnValueMaxRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMaxRenderer.color_options)

            - [`TestColumnValueMaxRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMaxRenderer.render_html)

        - [`TestColumnValueMean`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean)

            - [`TestColumnValueMean.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.calculate_value_for_test)

            - [`TestColumnValueMean.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.column_name)

            - [`TestColumnValueMean.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.condition)

            - [`TestColumnValueMean.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.get_condition)

            - [`TestColumnValueMean.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.get_description)

            - [`TestColumnValueMean.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.metric)

            - [`TestColumnValueMean.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.name)

            - [`TestColumnValueMean.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.value)

        - [`TestColumnValueMeanRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMeanRenderer)

            - [`TestColumnValueMeanRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMeanRenderer.color_options)

            - [`TestColumnValueMeanRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMeanRenderer.render_html)

        - [`TestColumnValueMedian`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian)

            - [`TestColumnValueMedian.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.calculate_value_for_test)

            - [`TestColumnValueMedian.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.column_name)

            - [`TestColumnValueMedian.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.condition)

            - [`TestColumnValueMedian.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.get_condition)

            - [`TestColumnValueMedian.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.get_description)

            - [`TestColumnValueMedian.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.metric)

            - [`TestColumnValueMedian.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.name)

            - [`TestColumnValueMedian.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.value)

        - [`TestColumnValueMedianRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedianRenderer)

            - [`TestColumnValueMedianRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedianRenderer.color_options)

            - [`TestColumnValueMedianRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedianRenderer.render_html)

        - [`TestColumnValueMin`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin)

            - [`TestColumnValueMin.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.calculate_value_for_test)

            - [`TestColumnValueMin.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.column_name)

            - [`TestColumnValueMin.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.condition)

            - [`TestColumnValueMin.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.get_condition)

            - [`TestColumnValueMin.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.get_description)

            - [`TestColumnValueMin.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.metric)

            - [`TestColumnValueMin.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.name)

            - [`TestColumnValueMin.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.value)

        - [`TestColumnValueMinRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMinRenderer)

            - [`TestColumnValueMinRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMinRenderer.color_options)

            - [`TestColumnValueMinRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMinRenderer.render_html)

        - [`TestColumnValueStd`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd)

            - [`TestColumnValueStd.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.calculate_value_for_test)

            - [`TestColumnValueStd.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.column_name)

            - [`TestColumnValueStd.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.condition)

            - [`TestColumnValueStd.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.get_condition)

            - [`TestColumnValueStd.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.get_description)

            - [`TestColumnValueStd.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.metric)

            - [`TestColumnValueStd.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.name)

            - [`TestColumnValueStd.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.value)

        - [`TestColumnValueStdRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStdRenderer)

            - [`TestColumnValueStdRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStdRenderer.color_options)

            - [`TestColumnValueStdRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStdRenderer.render_html)

        - [`TestConflictPrediction`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction)

            - [`TestConflictPrediction.check()`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction.check)

            - [`TestConflictPrediction.group`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction.group)

            - [`TestConflictPrediction.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction.metric)

            - [`TestConflictPrediction.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction.name)

        - [`TestConflictTarget`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget)

            - [`TestConflictTarget.check()`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget.check)

            - [`TestConflictTarget.group`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget.group)

            - [`TestConflictTarget.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget.metric)

            - [`TestConflictTarget.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget.name)

        - [`TestCorrelationChanges`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges)

            - [`TestCorrelationChanges.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.calculate_value_for_test)

            - [`TestCorrelationChanges.corr_diff`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.corr_diff)

            - [`TestCorrelationChanges.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.get_condition)

            - [`TestCorrelationChanges.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.get_description)

            - [`TestCorrelationChanges.group`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.group)

            - [`TestCorrelationChanges.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.metric)

            - [`TestCorrelationChanges.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.name)

        - [`TestCorrelationChangesRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChangesRenderer)

            - [`TestCorrelationChangesRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChangesRenderer.color_options)

            - [`TestCorrelationChangesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChangesRenderer.render_html)

        - [`TestHighlyCorrelatedColumns`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns)

            - [`TestHighlyCorrelatedColumns.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.calculate_value_for_test)

            - [`TestHighlyCorrelatedColumns.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.condition)

            - [`TestHighlyCorrelatedColumns.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.get_condition)

            - [`TestHighlyCorrelatedColumns.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.get_description)

            - [`TestHighlyCorrelatedColumns.method`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.method)

            - [`TestHighlyCorrelatedColumns.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.metric)

            - [`TestHighlyCorrelatedColumns.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.name)

            - [`TestHighlyCorrelatedColumns.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.value)

        - [`TestHighlyCorrelatedColumnsRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer)

            - [`TestHighlyCorrelatedColumnsRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer.color_options)

            - [`TestHighlyCorrelatedColumnsRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer.render_html)

            - [`TestHighlyCorrelatedColumnsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer.render_json)

        - [`TestMeanInNSigmas`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas)

            - [`TestMeanInNSigmas.check()`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.check)

            - [`TestMeanInNSigmas.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.column_name)

            - [`TestMeanInNSigmas.group`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.group)

            - [`TestMeanInNSigmas.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.metric)

            - [`TestMeanInNSigmas.n_sigmas`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.n_sigmas)

            - [`TestMeanInNSigmas.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.name)

        - [`TestMeanInNSigmasRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer)

            - [`TestMeanInNSigmasRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer.color_options)

            - [`TestMeanInNSigmasRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer.render_html)

            - [`TestMeanInNSigmasRenderer.render_json()`](evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer.render_json)

        - [`TestMostCommonValueShare`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare)

            - [`TestMostCommonValueShare.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.calculate_value_for_test)

            - [`TestMostCommonValueShare.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.column_name)

            - [`TestMostCommonValueShare.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.condition)

            - [`TestMostCommonValueShare.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.get_condition)

            - [`TestMostCommonValueShare.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.get_description)

            - [`TestMostCommonValueShare.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.metric)

            - [`TestMostCommonValueShare.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.name)

            - [`TestMostCommonValueShare.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.value)

        - [`TestMostCommonValueShareRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer)

            - [`TestMostCommonValueShareRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer.color_options)

            - [`TestMostCommonValueShareRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer.render_html)

            - [`TestMostCommonValueShareRenderer.render_json()`](evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer.render_json)

        - [`TestNumColumnsMeanInNSigmas`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumColumnsMeanInNSigmas)

            - [`TestNumColumnsMeanInNSigmas.generate()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumColumnsMeanInNSigmas.generate)

        - [`TestNumColumnsOutOfRangeValues`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumColumnsOutOfRangeValues)

            - [`TestNumColumnsOutOfRangeValues.generate()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumColumnsOutOfRangeValues.generate)

        - [`TestNumberOfOutListValues`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues)

            - [`TestNumberOfOutListValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.calculate_value_for_test)

            - [`TestNumberOfOutListValues.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.column_name)

            - [`TestNumberOfOutListValues.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.condition)

            - [`TestNumberOfOutListValues.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.get_condition)

            - [`TestNumberOfOutListValues.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.get_description)

            - [`TestNumberOfOutListValues.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.metric)

            - [`TestNumberOfOutListValues.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.name)

            - [`TestNumberOfOutListValues.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.value)

            - [`TestNumberOfOutListValues.values`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.values)

        - [`TestNumberOfOutListValuesRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValuesRenderer)

            - [`TestNumberOfOutListValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValuesRenderer.color_options)

            - [`TestNumberOfOutListValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValuesRenderer.render_html)

        - [`TestNumberOfOutRangeValues`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues)

            - [`TestNumberOfOutRangeValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.calculate_value_for_test)

            - [`TestNumberOfOutRangeValues.column`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.column)

            - [`TestNumberOfOutRangeValues.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.condition)

            - [`TestNumberOfOutRangeValues.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.get_condition)

            - [`TestNumberOfOutRangeValues.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.get_description)

            - [`TestNumberOfOutRangeValues.left`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.left)

            - [`TestNumberOfOutRangeValues.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.metric)

            - [`TestNumberOfOutRangeValues.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.name)

            - [`TestNumberOfOutRangeValues.right`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.right)

            - [`TestNumberOfOutRangeValues.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.value)

        - [`TestNumberOfOutRangeValuesRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValuesRenderer)

            - [`TestNumberOfOutRangeValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValuesRenderer.color_options)

            - [`TestNumberOfOutRangeValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValuesRenderer.render_html)

        - [`TestNumberOfUniqueValues`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues)

            - [`TestNumberOfUniqueValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.calculate_value_for_test)

            - [`TestNumberOfUniqueValues.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.column_name)

            - [`TestNumberOfUniqueValues.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.condition)

            - [`TestNumberOfUniqueValues.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.get_condition)

            - [`TestNumberOfUniqueValues.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.get_description)

            - [`TestNumberOfUniqueValues.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.metric)

            - [`TestNumberOfUniqueValues.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.name)

            - [`TestNumberOfUniqueValues.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.value)

        - [`TestNumberOfUniqueValuesRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValuesRenderer)

            - [`TestNumberOfUniqueValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValuesRenderer.color_options)

            - [`TestNumberOfUniqueValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValuesRenderer.render_html)

        - [`TestPredictionFeaturesCorrelations`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations)

            - [`TestPredictionFeaturesCorrelations.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.calculate_value_for_test)

            - [`TestPredictionFeaturesCorrelations.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.condition)

            - [`TestPredictionFeaturesCorrelations.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.get_condition)

            - [`TestPredictionFeaturesCorrelations.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.get_description)

            - [`TestPredictionFeaturesCorrelations.method`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.method)

            - [`TestPredictionFeaturesCorrelations.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.metric)

            - [`TestPredictionFeaturesCorrelations.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.name)

            - [`TestPredictionFeaturesCorrelations.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.value)

        - [`TestPredictionFeaturesCorrelationsRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer)

            - [`TestPredictionFeaturesCorrelationsRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer.color_options)

            - [`TestPredictionFeaturesCorrelationsRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer.render_html)

            - [`TestPredictionFeaturesCorrelationsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer.render_json)

        - [`TestShareOfOutListValues`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues)

            - [`TestShareOfOutListValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.calculate_value_for_test)

            - [`TestShareOfOutListValues.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.column_name)

            - [`TestShareOfOutListValues.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.condition)

            - [`TestShareOfOutListValues.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.get_condition)

            - [`TestShareOfOutListValues.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.get_description)

            - [`TestShareOfOutListValues.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.metric)

            - [`TestShareOfOutListValues.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.name)

            - [`TestShareOfOutListValues.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.value)

            - [`TestShareOfOutListValues.values`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.values)

        - [`TestShareOfOutListValuesRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer)

            - [`TestShareOfOutListValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer.color_options)

            - [`TestShareOfOutListValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer.render_html)

            - [`TestShareOfOutListValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer.render_json)

        - [`TestShareOfOutRangeValues`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues)

            - [`TestShareOfOutRangeValues.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.calculate_value_for_test)

            - [`TestShareOfOutRangeValues.column`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.column)

            - [`TestShareOfOutRangeValues.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.condition)

            - [`TestShareOfOutRangeValues.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.get_condition)

            - [`TestShareOfOutRangeValues.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.get_description)

            - [`TestShareOfOutRangeValues.left`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.left)

            - [`TestShareOfOutRangeValues.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.metric)

            - [`TestShareOfOutRangeValues.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.name)

            - [`TestShareOfOutRangeValues.right`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.right)

            - [`TestShareOfOutRangeValues.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.value)

        - [`TestShareOfOutRangeValuesRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer)

            - [`TestShareOfOutRangeValuesRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer.color_options)

            - [`TestShareOfOutRangeValuesRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer.render_html)

            - [`TestShareOfOutRangeValuesRenderer.render_json()`](evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer.render_json)

        - [`TestTargetFeaturesCorrelations`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations)

            - [`TestTargetFeaturesCorrelations.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.calculate_value_for_test)

            - [`TestTargetFeaturesCorrelations.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.condition)

            - [`TestTargetFeaturesCorrelations.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.get_condition)

            - [`TestTargetFeaturesCorrelations.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.get_description)

            - [`TestTargetFeaturesCorrelations.method`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.method)

            - [`TestTargetFeaturesCorrelations.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.metric)

            - [`TestTargetFeaturesCorrelations.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.name)

            - [`TestTargetFeaturesCorrelations.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.value)

        - [`TestTargetFeaturesCorrelationsRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer)

            - [`TestTargetFeaturesCorrelationsRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer.color_options)

            - [`TestTargetFeaturesCorrelationsRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer.render_html)

            - [`TestTargetFeaturesCorrelationsRenderer.render_json()`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer.render_json)

        - [`TestTargetPredictionCorrelation`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation)

            - [`TestTargetPredictionCorrelation.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.calculate_value_for_test)

            - [`TestTargetPredictionCorrelation.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.condition)

            - [`TestTargetPredictionCorrelation.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.get_condition)

            - [`TestTargetPredictionCorrelation.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.get_description)

            - [`TestTargetPredictionCorrelation.method`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.method)

            - [`TestTargetPredictionCorrelation.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.metric)

            - [`TestTargetPredictionCorrelation.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.name)

            - [`TestTargetPredictionCorrelation.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.value)

        - [`TestUniqueValuesShare`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare)

            - [`TestUniqueValuesShare.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.calculate_value_for_test)

            - [`TestUniqueValuesShare.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.column_name)

            - [`TestUniqueValuesShare.condition`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.condition)

            - [`TestUniqueValuesShare.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.get_condition)

            - [`TestUniqueValuesShare.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.get_description)

            - [`TestUniqueValuesShare.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.metric)

            - [`TestUniqueValuesShare.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.name)

            - [`TestUniqueValuesShare.value`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.value)

        - [`TestUniqueValuesShareRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShareRenderer)

            - [`TestUniqueValuesShareRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShareRenderer.color_options)

            - [`TestUniqueValuesShareRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShareRenderer.render_html)

        - [`TestValueList`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueList)

            - [`TestValueList.check()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.check)

            - [`TestValueList.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.column_name)

            - [`TestValueList.group`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.group)

            - [`TestValueList.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.metric)

            - [`TestValueList.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.name)

            - [`TestValueList.values`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.values)

        - [`TestValueListRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueListRenderer)

            - [`TestValueListRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueListRenderer.color_options)

            - [`TestValueListRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueListRenderer.render_html)

            - [`TestValueListRenderer.render_json()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueListRenderer.render_json)

        - [`TestValueQuantile`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile)

            - [`TestValueQuantile.calculate_value_for_test()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.calculate_value_for_test)

            - [`TestValueQuantile.column_name`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.column_name)

            - [`TestValueQuantile.get_condition()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.get_condition)

            - [`TestValueQuantile.get_description()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.get_description)

            - [`TestValueQuantile.group`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.group)

            - [`TestValueQuantile.groups()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.groups)

            - [`TestValueQuantile.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.metric)

            - [`TestValueQuantile.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.name)

            - [`TestValueQuantile.quantile`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.quantile)

        - [`TestValueQuantileRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantileRenderer)

            - [`TestValueQuantileRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantileRenderer.color_options)

            - [`TestValueQuantileRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantileRenderer.render_html)

        - [`TestValueRange`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange)

            - [`TestValueRange.check()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.check)

            - [`TestValueRange.column`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.column)

            - [`TestValueRange.group`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.group)

            - [`TestValueRange.left`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.left)

            - [`TestValueRange.metric`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.metric)

            - [`TestValueRange.name`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.name)

            - [`TestValueRange.right`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.right)

        - [`TestValueRangeRenderer`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRangeRenderer)

            - [`TestValueRangeRenderer.color_options`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRangeRenderer.color_options)

            - [`TestValueRangeRenderer.render_html()`](evidently.tests.md#evidently.tests.data_quality_tests.TestValueRangeRenderer.render_html)

    - [evidently.tests.regression_performance_tests module](evidently.tests.md#module-evidently.tests.regression_performance_tests)

        - [`BaseRegressionPerformanceMetricsTest`](evidently.tests.md#evidently.tests.regression_performance_tests.BaseRegressionPerformanceMetricsTest)

            - [`BaseRegressionPerformanceMetricsTest.group`](evidently.tests.md#evidently.tests.regression_performance_tests.BaseRegressionPerformanceMetricsTest.group)

            - [`BaseRegressionPerformanceMetricsTest.metric`](evidently.tests.md#evidently.tests.regression_performance_tests.BaseRegressionPerformanceMetricsTest.metric)

        - [`TestValueAbsMaxError`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError)

            - [`TestValueAbsMaxError.calculate_value_for_test()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.calculate_value_for_test)

            - [`TestValueAbsMaxError.condition`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.condition)

            - [`TestValueAbsMaxError.get_condition()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.get_condition)

            - [`TestValueAbsMaxError.get_description()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.get_description)

            - [`TestValueAbsMaxError.metric`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.metric)

            - [`TestValueAbsMaxError.name`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.name)

            - [`TestValueAbsMaxError.value`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.value)

        - [`TestValueAbsMaxErrorRenderer`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer)

            - [`TestValueAbsMaxErrorRenderer.color_options`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer.color_options)

            - [`TestValueAbsMaxErrorRenderer.render_html()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer.render_html)

            - [`TestValueAbsMaxErrorRenderer.render_json()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer.render_json)

        - [`TestValueMAE`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE)

            - [`TestValueMAE.calculate_value_for_test()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.calculate_value_for_test)

            - [`TestValueMAE.condition`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.condition)

            - [`TestValueMAE.get_condition()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.get_condition)

            - [`TestValueMAE.get_description()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.get_description)

            - [`TestValueMAE.metric`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.metric)

            - [`TestValueMAE.name`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.name)

            - [`TestValueMAE.value`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.value)

        - [`TestValueMAERenderer`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAERenderer)

            - [`TestValueMAERenderer.color_options`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAERenderer.color_options)

            - [`TestValueMAERenderer.render_html()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAERenderer.render_html)

            - [`TestValueMAERenderer.render_json()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAERenderer.render_json)

        - [`TestValueMAPE`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE)

            - [`TestValueMAPE.calculate_value_for_test()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.calculate_value_for_test)

            - [`TestValueMAPE.condition`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.condition)

            - [`TestValueMAPE.get_condition()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.get_condition)

            - [`TestValueMAPE.get_description()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.get_description)

            - [`TestValueMAPE.metric`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.metric)

            - [`TestValueMAPE.name`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.name)

            - [`TestValueMAPE.value`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.value)

        - [`TestValueMAPERenderer`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPERenderer)

            - [`TestValueMAPERenderer.color_options`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPERenderer.color_options)

            - [`TestValueMAPERenderer.render_html()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPERenderer.render_html)

            - [`TestValueMAPERenderer.render_json()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPERenderer.render_json)

        - [`TestValueMeanError`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError)

            - [`TestValueMeanError.calculate_value_for_test()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.calculate_value_for_test)

            - [`TestValueMeanError.condition`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.condition)

            - [`TestValueMeanError.get_condition()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.get_condition)

            - [`TestValueMeanError.get_description()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.get_description)

            - [`TestValueMeanError.metric`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.metric)

            - [`TestValueMeanError.name`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.name)

            - [`TestValueMeanError.value`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.value)

        - [`TestValueMeanErrorRenderer`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer)

            - [`TestValueMeanErrorRenderer.color_options`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer.color_options)

            - [`TestValueMeanErrorRenderer.render_html()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer.render_html)

            - [`TestValueMeanErrorRenderer.render_json()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer.render_json)

        - [`TestValueR2Score`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score)

            - [`TestValueR2Score.calculate_value_for_test()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.calculate_value_for_test)

            - [`TestValueR2Score.condition`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.condition)

            - [`TestValueR2Score.get_condition()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.get_condition)

            - [`TestValueR2Score.get_description()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.get_description)

            - [`TestValueR2Score.metric`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.metric)

            - [`TestValueR2Score.name`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.name)

            - [`TestValueR2Score.value`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.value)

        - [`TestValueR2ScoreRenderer`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer)

            - [`TestValueR2ScoreRenderer.color_options`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer.color_options)

            - [`TestValueR2ScoreRenderer.render_html()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer.render_html)

            - [`TestValueR2ScoreRenderer.render_json()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer.render_json)

        - [`TestValueRMSE`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE)

            - [`TestValueRMSE.calculate_value_for_test()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.calculate_value_for_test)

            - [`TestValueRMSE.condition`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.condition)

            - [`TestValueRMSE.get_condition()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.get_condition)

            - [`TestValueRMSE.get_description()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.get_description)

            - [`TestValueRMSE.metric`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.metric)

            - [`TestValueRMSE.name`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.name)

            - [`TestValueRMSE.value`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.value)

        - [`TestValueRMSERenderer`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSERenderer)

            - [`TestValueRMSERenderer.color_options`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSERenderer.color_options)

            - [`TestValueRMSERenderer.render_html()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSERenderer.render_html)

            - [`TestValueRMSERenderer.render_json()`](evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSERenderer.render_json)

    - [evidently.tests.utils module](evidently.tests.md#module-evidently.tests.utils)

        - [`approx()`](evidently.tests.md#evidently.tests.utils.approx)

        - [`dataframes_to_table()`](evidently.tests.md#evidently.tests.utils.dataframes_to_table)

        - [`plot_boxes()`](evidently.tests.md#evidently.tests.utils.plot_boxes)

        - [`plot_check()`](evidently.tests.md#evidently.tests.utils.plot_check)

        - [`plot_conf_mtrx()`](evidently.tests.md#evidently.tests.utils.plot_conf_mtrx)

        - [`plot_correlations()`](evidently.tests.md#evidently.tests.utils.plot_correlations)

        - [`plot_dicts_to_table()`](evidently.tests.md#evidently.tests.utils.plot_dicts_to_table)

        - [`plot_metric_value()`](evidently.tests.md#evidently.tests.utils.plot_metric_value)

        - [`plot_rates()`](evidently.tests.md#evidently.tests.utils.plot_rates)

        - [`plot_roc_auc()`](evidently.tests.md#evidently.tests.utils.plot_roc_auc)

        - [`plot_value_counts_tables()`](evidently.tests.md#evidently.tests.utils.plot_value_counts_tables)

        - [`plot_value_counts_tables_ref_curr()`](evidently.tests.md#evidently.tests.utils.plot_value_counts_tables_ref_curr)

        - [`regression_perf_plot()`](evidently.tests.md#evidently.tests.utils.regression_perf_plot)

    - [Module contents](evidently.tests.md#module-evidently.tests)

- [evidently.utils package](evidently.utils.md)

    - [Submodules](evidently.utils.md#submodules)

    - [evidently.utils.data_operations module](evidently.utils.md#module-evidently.utils.data_operations)

        - [`DatasetColumns`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns)

            - [`DatasetColumns.as_dict()`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.as_dict)

            - [`DatasetColumns.cat_feature_names`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.cat_feature_names)

            - [`DatasetColumns.datetime_feature_names`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.datetime_feature_names)

            - [`DatasetColumns.get_all_columns_list()`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.get_all_columns_list)

            - [`DatasetColumns.get_all_features_list()`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.get_all_features_list)

            - [`DatasetColumns.get_features_len()`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.get_features_len)

            - [`DatasetColumns.num_feature_names`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.num_feature_names)

            - [`DatasetColumns.target_names`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.target_names)

            - [`DatasetColumns.target_type`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.target_type)

            - [`DatasetColumns.task`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.task)

            - [`DatasetColumns.utility_columns`](evidently.utils.md#evidently.utils.data_operations.DatasetColumns.utility_columns)

        - [`DatasetUtilityColumns`](evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns)

            - [`DatasetUtilityColumns.as_dict()`](evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.as_dict)

            - [`DatasetUtilityColumns.date`](evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.date)

            - [`DatasetUtilityColumns.id_column`](evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.id_column)

            - [`DatasetUtilityColumns.prediction`](evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.prediction)

            - [`DatasetUtilityColumns.target`](evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.target)

        - [`process_columns()`](evidently.utils.md#evidently.utils.data_operations.process_columns)

        - [`recognize_column_type()`](evidently.utils.md#evidently.utils.data_operations.recognize_column_type)

        - [`recognize_task()`](evidently.utils.md#evidently.utils.data_operations.recognize_task)

        - [`replace_infinity_values_to_nan()`](evidently.utils.md#evidently.utils.data_operations.replace_infinity_values_to_nan)

    - [evidently.utils.data_preprocessing module](evidently.utils.md#module-evidently.utils.data_preprocessing)

        - [`ColumnDefinition`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnDefinition)

            - [`ColumnDefinition.column_name`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnDefinition.column_name)

            - [`ColumnDefinition.column_type`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnDefinition.column_type)

        - [`ColumnPresenceState`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnPresenceState)

            - [`ColumnPresenceState.Missing`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnPresenceState.Missing)

            - [`ColumnPresenceState.Partially`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnPresenceState.Partially)

            - [`ColumnPresenceState.Present`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnPresenceState.Present)

        - [`ColumnType`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnType)

            - [`ColumnType.Categorical`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnType.Categorical)

            - [`ColumnType.Datetime`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnType.Datetime)

            - [`ColumnType.Numerical`](evidently.utils.md#evidently.utils.data_preprocessing.ColumnType.Numerical)

        - [`DataDefinition`](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition)

            - [`DataDefinition.classification_labels()`](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.classification_labels)

            - [`DataDefinition.get_columns()`](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_columns)

            - [`DataDefinition.get_datetime_column()`](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_datetime_column)

            - [`DataDefinition.get_id_column()`](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_id_column)

            - [`DataDefinition.get_prediction_columns()`](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_prediction_columns)

            - [`DataDefinition.get_target_column()`](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_target_column)

            - [`DataDefinition.task()`](evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.task)

        - [`PredictionColumns`](evidently.utils.md#evidently.utils.data_preprocessing.PredictionColumns)

            - [`PredictionColumns.get_columns_list()`](evidently.utils.md#evidently.utils.data_preprocessing.PredictionColumns.get_columns_list)

            - [`PredictionColumns.predicted_values`](evidently.utils.md#evidently.utils.data_preprocessing.PredictionColumns.predicted_values)

            - [`PredictionColumns.prediction_probas`](evidently.utils.md#evidently.utils.data_preprocessing.PredictionColumns.prediction_probas)

        - [`create_data_definition()`](evidently.utils.md#evidently.utils.data_preprocessing.create_data_definition)

    - [evidently.utils.generators module](evidently.utils.md#module-evidently.utils.generators)

        - [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

            - [`BaseGenerator.generate()`](evidently.utils.md#evidently.utils.generators.BaseGenerator.generate)

        - [`make_generator_by_columns()`](evidently.utils.md#evidently.utils.generators.make_generator_by_columns)

    - [evidently.utils.numpy_encoder module](evidently.utils.md#module-evidently.utils.numpy_encoder)

        - [`NumpyEncoder`](evidently.utils.md#evidently.utils.numpy_encoder.NumpyEncoder)

            - [`NumpyEncoder.default()`](evidently.utils.md#evidently.utils.numpy_encoder.NumpyEncoder.default)

    - [evidently.utils.types module](evidently.utils.md#module-evidently.utils.types)

        - [`ApproxValue`](evidently.utils.md#evidently.utils.types.ApproxValue)

            - [`ApproxValue.DEFAULT_ABSOLUTE`](evidently.utils.md#evidently.utils.types.ApproxValue.DEFAULT_ABSOLUTE)

            - [`ApproxValue.DEFAULT_RELATIVE`](evidently.utils.md#evidently.utils.types.ApproxValue.DEFAULT_RELATIVE)

            - [`ApproxValue.as_dict()`](evidently.utils.md#evidently.utils.types.ApproxValue.as_dict)

            - [`ApproxValue.tolerance`](evidently.utils.md#evidently.utils.types.ApproxValue.tolerance)

            - [`ApproxValue.value`](evidently.utils.md#evidently.utils.types.ApproxValue.value)

    - [evidently.utils.visualizations module](evidently.utils.md#module-evidently.utils.visualizations)

        - [`Distribution`](evidently.utils.md#evidently.utils.visualizations.Distribution)

            - [`Distribution.x`](evidently.utils.md#evidently.utils.visualizations.Distribution.x)

            - [`Distribution.y`](evidently.utils.md#evidently.utils.visualizations.Distribution.y)

        - [`get_distribution_for_category_column()`](evidently.utils.md#evidently.utils.visualizations.get_distribution_for_category_column)

        - [`get_distribution_for_column()`](evidently.utils.md#evidently.utils.visualizations.get_distribution_for_column)

        - [`get_distribution_for_numerical_column()`](evidently.utils.md#evidently.utils.visualizations.get_distribution_for_numerical_column)

        - [`make_hist_df()`](evidently.utils.md#evidently.utils.visualizations.make_hist_df)

        - [`make_hist_for_cat_plot()`](evidently.utils.md#evidently.utils.visualizations.make_hist_for_cat_plot)

        - [`make_hist_for_num_plot()`](evidently.utils.md#evidently.utils.visualizations.make_hist_for_num_plot)

        - [`plot_boxes()`](evidently.utils.md#evidently.utils.visualizations.plot_boxes)

        - [`plot_cat_cat_rel()`](evidently.utils.md#evidently.utils.visualizations.plot_cat_cat_rel)

        - [`plot_cat_feature_in_time()`](evidently.utils.md#evidently.utils.visualizations.plot_cat_feature_in_time)

        - [`plot_conf_mtrx()`](evidently.utils.md#evidently.utils.visualizations.plot_conf_mtrx)

        - [`plot_distr()`](evidently.utils.md#evidently.utils.visualizations.plot_distr)

        - [`plot_distr_subplots()`](evidently.utils.md#evidently.utils.visualizations.plot_distr_subplots)

        - [`plot_distr_with_log_button()`](evidently.utils.md#evidently.utils.visualizations.plot_distr_with_log_button)

        - [`plot_error_bias_colored_scatter()`](evidently.utils.md#evidently.utils.visualizations.plot_error_bias_colored_scatter)

        - [`plot_line_in_time()`](evidently.utils.md#evidently.utils.visualizations.plot_line_in_time)

        - [`plot_num_feature_in_time()`](evidently.utils.md#evidently.utils.visualizations.plot_num_feature_in_time)

        - [`plot_num_num_rel()`](evidently.utils.md#evidently.utils.visualizations.plot_num_num_rel)

        - [`plot_pred_actual_time()`](evidently.utils.md#evidently.utils.visualizations.plot_pred_actual_time)

        - [`plot_scatter()`](evidently.utils.md#evidently.utils.visualizations.plot_scatter)

        - [`plot_scatter_for_data_drift()`](evidently.utils.md#evidently.utils.visualizations.plot_scatter_for_data_drift)

        - [`plot_time_feature_distr()`](evidently.utils.md#evidently.utils.visualizations.plot_time_feature_distr)

    - [Module contents](evidently.utils.md#module-evidently.utils)

- [evidently.widgets package](evidently.widgets.md)

    - [Module contents](evidently.widgets.md#module-evidently.widgets)


## Module contents
