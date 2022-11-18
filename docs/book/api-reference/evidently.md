# evidently package

## Subpackages

- [evidently.calculations package](evidently.calculations.md)

    - [Subpackages](api-reference/evidently.calculations.md#subpackages)

        - [evidently.calculations.stattests package](evidently.calculations.stattests.md)

            - [Submodules](api-reference/evidently.calculations.stattests.md#submodules)

            - [evidently.calculations.stattests.anderson_darling_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.anderson_darling_stattest)

            - [evidently.calculations.stattests.chisquare_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.chisquare_stattest)

            - [evidently.calculations.stattests.cramer_von_mises_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.cramer_von_mises_stattest)

            - [evidently.calculations.stattests.energy_distance module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.energy_distance)

            - [evidently.calculations.stattests.epps_singleton_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.epps_singleton_stattest)

            - [evidently.calculations.stattests.fisher_exact_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.fisher_exact_stattest)

            - [evidently.calculations.stattests.g_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.g_stattest)

            - [evidently.calculations.stattests.hellinger_distance module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.hellinger_distance)

            - [evidently.calculations.stattests.jensenshannon module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.jensenshannon)

            - [evidently.calculations.stattests.kl_div module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.kl_div)

            - [evidently.calculations.stattests.ks_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.ks_stattest)

            - [evidently.calculations.stattests.mann_whitney_urank_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.mann_whitney_urank_stattest)

            - [evidently.calculations.stattests.psi module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.psi)

            - [evidently.calculations.stattests.registry module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.registry)

            - [evidently.calculations.stattests.t_test module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.t_test)

            - [evidently.calculations.stattests.tvd_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.tvd_stattest)

            - [evidently.calculations.stattests.utils module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.utils)

            - [evidently.calculations.stattests.wasserstein_distance_norm module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.wasserstein_distance_norm)

            - [evidently.calculations.stattests.z_stattest module](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests.z_stattest)

            - [Module contents](api-reference/evidently.calculations.stattests.md#module-evidently.calculations.stattests)

    - [Submodules](api-reference/evidently.calculations.md#submodules)

    - [evidently.calculations.classification_performance module](api-reference/evidently.calculations.md#module-evidently.calculations.classification_performance)

        - [`ConfusionMatrix`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix)

            - [`ConfusionMatrix.labels`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix.labels)

            - [`ConfusionMatrix.values`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.ConfusionMatrix.values)

        - [`PredictionData`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.PredictionData)

            - [`PredictionData.labels`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.PredictionData.labels)

            - [`PredictionData.prediction_probas`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.PredictionData.prediction_probas)

            - [`PredictionData.predictions`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.PredictionData.predictions)

        - [`calculate_confusion_by_classes()`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.calculate_confusion_by_classes)

        - [`calculate_pr_table()`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.calculate_pr_table)

        - [`get_prediction_data()`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.get_prediction_data)

        - [`k_probability_threshold()`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.k_probability_threshold)

        - [`threshold_probability_labels()`](api-reference/evidently.calculations.md#evidently.calculations.classification_performance.threshold_probability_labels)

    - [evidently.calculations.data_drift module](api-reference/evidently.calculations.md#module-evidently.calculations.data_drift)

        - [`ColumnDataDriftMetrics`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics)

            - [`ColumnDataDriftMetrics.column_name`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.column_name)

            - [`ColumnDataDriftMetrics.column_type`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.column_type)

            - [`ColumnDataDriftMetrics.current_correlations`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.current_correlations)

            - [`ColumnDataDriftMetrics.current_distribution`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.current_distribution)

            - [`ColumnDataDriftMetrics.current_scatter`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.current_scatter)

            - [`ColumnDataDriftMetrics.current_small_distribution`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.current_small_distribution)

            - [`ColumnDataDriftMetrics.drift_detected`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.drift_detected)

            - [`ColumnDataDriftMetrics.drift_score`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.drift_score)

            - [`ColumnDataDriftMetrics.plot_shape`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.plot_shape)

            - [`ColumnDataDriftMetrics.reference_correlations`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.reference_correlations)

            - [`ColumnDataDriftMetrics.reference_distribution`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.reference_distribution)

            - [`ColumnDataDriftMetrics.reference_small_distribution`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.reference_small_distribution)

            - [`ColumnDataDriftMetrics.stattest_name`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.stattest_name)

            - [`ColumnDataDriftMetrics.threshold`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.threshold)

            - [`ColumnDataDriftMetrics.x_name`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ColumnDataDriftMetrics.x_name)

        - [`DatasetDrift`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDrift)

            - [`DatasetDrift.dataset_drift`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDrift.dataset_drift)

            - [`DatasetDrift.dataset_drift_score`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDrift.dataset_drift_score)

            - [`DatasetDrift.number_of_drifted_columns`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDrift.number_of_drifted_columns)

        - [`DatasetDriftMetrics`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics)

            - [`DatasetDriftMetrics.dataset_columns`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.dataset_columns)

            - [`DatasetDriftMetrics.dataset_drift`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.dataset_drift)

            - [`DatasetDriftMetrics.drift_by_columns`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.drift_by_columns)

            - [`DatasetDriftMetrics.number_of_columns`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.number_of_columns)

            - [`DatasetDriftMetrics.number_of_drifted_columns`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.number_of_drifted_columns)

            - [`DatasetDriftMetrics.options`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.options)

            - [`DatasetDriftMetrics.share_of_drifted_columns`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.DatasetDriftMetrics.share_of_drifted_columns)

        - [`ensure_prediction_column_is_string()`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.ensure_prediction_column_is_string)

        - [`get_dataset_drift()`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.get_dataset_drift)

        - [`get_drift_for_columns()`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.get_drift_for_columns)

        - [`get_one_column_drift()`](api-reference/evidently.calculations.md#evidently.calculations.data_drift.get_one_column_drift)

    - [evidently.calculations.data_integration module](api-reference/evidently.calculations.md#module-evidently.calculations.data_integration)

        - [`get_number_of_all_pandas_missed_values()`](api-reference/evidently.calculations.md#evidently.calculations.data_integration.get_number_of_all_pandas_missed_values)

        - [`get_number_of_almost_constant_columns()`](api-reference/evidently.calculations.md#evidently.calculations.data_integration.get_number_of_almost_constant_columns)

        - [`get_number_of_almost_duplicated_columns()`](api-reference/evidently.calculations.md#evidently.calculations.data_integration.get_number_of_almost_duplicated_columns)

        - [`get_number_of_constant_columns()`](api-reference/evidently.calculations.md#evidently.calculations.data_integration.get_number_of_constant_columns)

        - [`get_number_of_duplicated_columns()`](api-reference/evidently.calculations.md#evidently.calculations.data_integration.get_number_of_duplicated_columns)

        - [`get_number_of_empty_columns()`](api-reference/evidently.calculations.md#evidently.calculations.data_integration.get_number_of_empty_columns)

    - [evidently.calculations.data_quality module](api-reference/evidently.calculations.md#module-evidently.calculations.data_quality)

        - [`ColumnCorrelations`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations)

            - [`ColumnCorrelations.column_name`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations.column_name)

            - [`ColumnCorrelations.kind`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations.kind)

            - [`ColumnCorrelations.values`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.ColumnCorrelations.values)

        - [`DataQualityGetPlotData`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityGetPlotData)

            - [`DataQualityGetPlotData.calculate_data_by_target()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityGetPlotData.calculate_data_by_target)

            - [`DataQualityGetPlotData.calculate_data_in_time()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityGetPlotData.calculate_data_in_time)

            - [`DataQualityGetPlotData.calculate_main_plot()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityGetPlotData.calculate_main_plot)

        - [`DataQualityPlot`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityPlot)

            - [`DataQualityPlot.bins_for_hist`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityPlot.bins_for_hist)

        - [`DataQualityStats`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats)

            - [`DataQualityStats.cat_features_stats`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.cat_features_stats)

            - [`DataQualityStats.datetime_features_stats`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.datetime_features_stats)

            - [`DataQualityStats.get_all_features()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.get_all_features)

            - [`DataQualityStats.num_features_stats`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.num_features_stats)

            - [`DataQualityStats.prediction_stats`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.prediction_stats)

            - [`DataQualityStats.rows_count`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.rows_count)

            - [`DataQualityStats.target_stats`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.DataQualityStats.target_stats)

        - [`FeatureQualityStats`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats)

            - [`FeatureQualityStats.as_dict()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.as_dict)

            - [`FeatureQualityStats.count`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.count)

            - [`FeatureQualityStats.feature_type`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.feature_type)

            - [`FeatureQualityStats.infinite_count`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.infinite_count)

            - [`FeatureQualityStats.infinite_percentage`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.infinite_percentage)

            - [`FeatureQualityStats.is_category()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.is_category)

            - [`FeatureQualityStats.is_datetime()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.is_datetime)

            - [`FeatureQualityStats.is_numeric()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.is_numeric)

            - [`FeatureQualityStats.max`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.max)

            - [`FeatureQualityStats.mean`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.mean)

            - [`FeatureQualityStats.min`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.min)

            - [`FeatureQualityStats.missing_count`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.missing_count)

            - [`FeatureQualityStats.missing_percentage`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.missing_percentage)

            - [`FeatureQualityStats.most_common_not_null_value`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.most_common_not_null_value)

            - [`FeatureQualityStats.most_common_not_null_value_percentage`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.most_common_not_null_value_percentage)

            - [`FeatureQualityStats.most_common_value`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.most_common_value)

            - [`FeatureQualityStats.most_common_value_percentage`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.most_common_value_percentage)

            - [`FeatureQualityStats.new_in_current_values_count`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.new_in_current_values_count)

            - [`FeatureQualityStats.number_of_rows`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.number_of_rows)

            - [`FeatureQualityStats.percentile_25`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.percentile_25)

            - [`FeatureQualityStats.percentile_50`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.percentile_50)

            - [`FeatureQualityStats.percentile_75`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.percentile_75)

            - [`FeatureQualityStats.std`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.std)

            - [`FeatureQualityStats.unique_count`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.unique_count)

            - [`FeatureQualityStats.unique_percentage`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.unique_percentage)

            - [`FeatureQualityStats.unused_in_current_values_count`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.FeatureQualityStats.unused_in_current_values_count)

        - [`calculate_category_column_correlations()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.calculate_category_column_correlations)

        - [`calculate_column_distribution()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.calculate_column_distribution)

        - [`calculate_correlations()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.calculate_correlations)

        - [`calculate_cramer_v_correlation()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.calculate_cramer_v_correlation)

        - [`calculate_data_quality_stats()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.calculate_data_quality_stats)

        - [`calculate_numerical_column_correlations()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.calculate_numerical_column_correlations)

        - [`get_features_stats()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.get_features_stats)

        - [`get_pairwise_correlation()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.get_pairwise_correlation)

        - [`get_rows_count()`](api-reference/evidently.calculations.md#evidently.calculations.data_quality.get_rows_count)

    - [evidently.calculations.regression_performance module](api-reference/evidently.calculations.md#module-evidently.calculations.regression_performance)

        - [`ErrorWithQuantiles`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.ErrorWithQuantiles)

        - [`FeatureBias`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias)

            - [`FeatureBias.as_dict()`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.as_dict)

            - [`FeatureBias.feature_type`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.feature_type)

            - [`FeatureBias.majority`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.majority)

            - [`FeatureBias.over`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.over)

            - [`FeatureBias.range`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.range)

            - [`FeatureBias.under`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.FeatureBias.under)

        - [`RegressionPerformanceMetrics`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics)

            - [`RegressionPerformanceMetrics.abs_error_max`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.abs_error_max)

            - [`RegressionPerformanceMetrics.abs_error_std`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.abs_error_std)

            - [`RegressionPerformanceMetrics.abs_perc_error_std`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.abs_perc_error_std)

            - [`RegressionPerformanceMetrics.error_bias`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.error_bias)

            - [`RegressionPerformanceMetrics.error_normality`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.error_normality)

            - [`RegressionPerformanceMetrics.error_std`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.error_std)

            - [`RegressionPerformanceMetrics.mean_abs_error`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.mean_abs_error)

            - [`RegressionPerformanceMetrics.mean_abs_perc_error`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.mean_abs_perc_error)

            - [`RegressionPerformanceMetrics.mean_error`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.mean_error)

            - [`RegressionPerformanceMetrics.underperformance`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.RegressionPerformanceMetrics.underperformance)

        - [`calculate_regression_performance()`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.calculate_regression_performance)

        - [`error_bias_table()`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.error_bias_table)

        - [`error_with_quantiles()`](api-reference/evidently.calculations.md#evidently.calculations.regression_performance.error_with_quantiles)

    - [Module contents](api-reference/evidently.calculations.md#module-evidently.calculations)

- [evidently.metric_preset package](evidently.metric_preset.md)

    - [Submodules](api-reference/evidently.metric_preset.md#submodules)

    - [evidently.metric_preset.classification_performance module](api-reference/evidently.metric_preset.md#module-evidently.metric_preset.classification_performance)

        - [`ClassificationPreset`](api-reference/evidently.metric_preset.md#evidently.metric_preset.classification_performance.ClassificationPreset)

            - [`ClassificationPreset.generate_metrics()`](api-reference/evidently.metric_preset.md#evidently.metric_preset.classification_performance.ClassificationPreset.generate_metrics)

    - [evidently.metric_preset.data_drift module](api-reference/evidently.metric_preset.md#module-evidently.metric_preset.data_drift)

        - [`DataDriftPreset`](api-reference/evidently.metric_preset.md#evidently.metric_preset.data_drift.DataDriftPreset)

            - [`DataDriftPreset.generate_metrics()`](api-reference/evidently.metric_preset.md#evidently.metric_preset.data_drift.DataDriftPreset.generate_metrics)

    - [evidently.metric_preset.data_quality module](api-reference/evidently.metric_preset.md#module-evidently.metric_preset.data_quality)

        - [`DataQualityPreset`](api-reference/evidently.metric_preset.md#evidently.metric_preset.data_quality.DataQualityPreset)

            - [`DataQualityPreset.columns`](api-reference/evidently.metric_preset.md#evidently.metric_preset.data_quality.DataQualityPreset.columns)

            - [`DataQualityPreset.generate_metrics()`](api-reference/evidently.metric_preset.md#evidently.metric_preset.data_quality.DataQualityPreset.generate_metrics)

    - [evidently.metric_preset.metric_preset module](api-reference/evidently.metric_preset.md#module-evidently.metric_preset.metric_preset)

        - [`MetricPreset`](api-reference/evidently.metric_preset.md#evidently.metric_preset.metric_preset.MetricPreset)

            - [`MetricPreset.generate_metrics()`](api-reference/evidently.metric_preset.md#evidently.metric_preset.metric_preset.MetricPreset.generate_metrics)

    - [evidently.metric_preset.regression_performance module](api-reference/evidently.metric_preset.md#module-evidently.metric_preset.regression_performance)

        - [`RegressionPreset`](api-reference/evidently.metric_preset.md#evidently.metric_preset.regression_performance.RegressionPreset)

            - [`RegressionPreset.generate_metrics()`](api-reference/evidently.metric_preset.md#evidently.metric_preset.regression_performance.RegressionPreset.generate_metrics)

    - [evidently.metric_preset.target_drift module](api-reference/evidently.metric_preset.md#module-evidently.metric_preset.target_drift)

        - [`TargetDriftPreset`](api-reference/evidently.metric_preset.md#evidently.metric_preset.target_drift.TargetDriftPreset)

            - [`TargetDriftPreset.generate_metrics()`](api-reference/evidently.metric_preset.md#evidently.metric_preset.target_drift.TargetDriftPreset.generate_metrics)

    - [Module contents](api-reference/evidently.metric_preset.md#module-evidently.metric_preset)

- [evidently.metrics package](evidently.metrics.md)

    - [Subpackages](api-reference/evidently.metrics.md#subpackages)

        - [evidently.metrics.classification_performance package](evidently.metrics.classification_performance.md)

            - [Submodules](api-reference/evidently.metrics.classification_performance.md#submodules)

            - [evidently.metrics.classification_performance.base_classification_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.base_classification_metric)

            - [evidently.metrics.classification_performance.class_balance_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.class_balance_metric)

            - [evidently.metrics.classification_performance.class_separation_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.class_separation_metric)

            - [evidently.metrics.classification_performance.classification_quality_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.classification_quality_metric)

            - [evidently.metrics.classification_performance.confusion_matrix_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.confusion_matrix_metric)

            - [evidently.metrics.classification_performance.pr_curve_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.pr_curve_metric)

            - [evidently.metrics.classification_performance.pr_table_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.pr_table_metric)

            - [evidently.metrics.classification_performance.probability_distribution_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.probability_distribution_metric)

            - [evidently.metrics.classification_performance.quality_by_class_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.quality_by_class_metric)

            - [evidently.metrics.classification_performance.quality_by_feature_table module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.quality_by_feature_table)

            - [evidently.metrics.classification_performance.roc_curve_metric module](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance.roc_curve_metric)

            - [Module contents](api-reference/evidently.metrics.classification_performance.md#module-evidently.metrics.classification_performance)

        - [evidently.metrics.data_drift package](evidently.metrics.data_drift.md)

            - [Submodules](api-reference/evidently.metrics.data_drift.md#submodules)

            - [evidently.metrics.data_drift.column_drift_metric module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.column_drift_metric)

            - [evidently.metrics.data_drift.column_value_plot module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.column_value_plot)

            - [evidently.metrics.data_drift.data_drift_table module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.data_drift_table)

            - [evidently.metrics.data_drift.dataset_drift_metric module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.dataset_drift_metric)

            - [evidently.metrics.data_drift.target_by_features_table module](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift.target_by_features_table)

            - [Module contents](api-reference/evidently.metrics.data_drift.md#module-evidently.metrics.data_drift)

        - [evidently.metrics.data_integrity package](evidently.metrics.data_integrity.md)

            - [Submodules](api-reference/evidently.metrics.data_integrity.md#submodules)

            - [evidently.metrics.data_integrity.column_missing_values_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_missing_values_metric)

            - [evidently.metrics.data_integrity.column_regexp_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_regexp_metric)

            - [evidently.metrics.data_integrity.column_summary_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.column_summary_metric)

            - [evidently.metrics.data_integrity.dataset_missing_values_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.dataset_missing_values_metric)

            - [evidently.metrics.data_integrity.dataset_summary_metric module](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity.dataset_summary_metric)

            - [Module contents](api-reference/evidently.metrics.data_integrity.md#module-evidently.metrics.data_integrity)

        - [evidently.metrics.data_quality package](evidently.metrics.data_quality.md)

            - [Submodules](api-reference/evidently.metrics.data_quality.md#submodules)

            - [evidently.metrics.data_quality.column_correlations_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_correlations_metric)

            - [evidently.metrics.data_quality.column_distribution_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_distribution_metric)

            - [evidently.metrics.data_quality.column_quantile_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_quantile_metric)

            - [evidently.metrics.data_quality.column_value_list_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_value_list_metric)

            - [evidently.metrics.data_quality.column_value_range_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.column_value_range_metric)

            - [evidently.metrics.data_quality.dataset_correlations_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.dataset_correlations_metric)

            - [evidently.metrics.data_quality.stability_metric module](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality.stability_metric)

            - [Module contents](api-reference/evidently.metrics.data_quality.md#module-evidently.metrics.data_quality)

        - [evidently.metrics.regression_performance package](evidently.metrics.regression_performance.md)

            - [Submodules](api-reference/evidently.metrics.regression_performance.md#submodules)

            - [evidently.metrics.regression_performance.abs_perc_error_in_time module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.abs_perc_error_in_time)

            - [evidently.metrics.regression_performance.error_bias_table module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_bias_table)

            - [evidently.metrics.regression_performance.error_distribution module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_distribution)

            - [evidently.metrics.regression_performance.error_in_time module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_in_time)

            - [evidently.metrics.regression_performance.error_normality module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.error_normality)

            - [evidently.metrics.regression_performance.predicted_and_actual_in_time module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.predicted_and_actual_in_time)

            - [evidently.metrics.regression_performance.predicted_vs_actual module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.predicted_vs_actual)

            - [evidently.metrics.regression_performance.regression_performance_metrics module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_performance_metrics)

            - [evidently.metrics.regression_performance.regression_quality module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.regression_quality)

            - [evidently.metrics.regression_performance.top_error module](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance.top_error)

            - [Module contents](api-reference/evidently.metrics.regression_performance.md#module-evidently.metrics.regression_performance)

    - [Submodules](api-reference/evidently.metrics.md#submodules)

    - [evidently.metrics.base_metric module](api-reference/evidently.metrics.md#module-evidently.metrics.base_metric)

        - [`ErrorResult`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.ErrorResult)

            - [`ErrorResult.exception`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.ErrorResult.exception)

        - [`InputData`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData)

            - [`InputData.column_mapping`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData.column_mapping)

            - [`InputData.current_data`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData.current_data)

            - [`InputData.data_definition`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData.data_definition)

            - [`InputData.reference_data`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData.reference_data)

        - [`Metric`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)

            - [`Metric.calculate()`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric.calculate)

            - [`Metric.context`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric.context)

            - [`Metric.get_id()`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric.get_id)

            - [`Metric.get_parameters()`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric.get_parameters)

            - [`Metric.get_result()`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric.get_result)

            - [`Metric.set_context()`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric.set_context)

        - [`generate_column_metrics()`](api-reference/evidently.metrics.md#evidently.metrics.base_metric.generate_column_metrics)

    - [evidently.metrics.classification_performance_metrics module](api-reference/evidently.metrics.md#module-evidently.metrics.classification_performance_metrics)

        - [`ClassificationPerformanceMetrics`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetrics)

            - [`ClassificationPerformanceMetrics.calculate()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetrics.calculate)

        - [`ClassificationPerformanceMetricsRenderer`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer)

            - [`ClassificationPerformanceMetricsRenderer.color_options`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer.color_options)

            - [`ClassificationPerformanceMetricsRenderer.render_html()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer.render_html)

            - [`ClassificationPerformanceMetricsRenderer.render_json()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsRenderer.render_json)

        - [`ClassificationPerformanceMetricsThreshold`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold)

            - [`ClassificationPerformanceMetricsThreshold.calculate_metric()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold.calculate_metric)

            - [`ClassificationPerformanceMetricsThreshold.get_parameters()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold.get_parameters)

            - [`ClassificationPerformanceMetricsThreshold.get_threshold()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThreshold.get_threshold)

        - [`ClassificationPerformanceMetricsThresholdBase`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase)

            - [`ClassificationPerformanceMetricsThresholdBase.calculate()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase.calculate)

            - [`ClassificationPerformanceMetricsThresholdBase.calculate_metric()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase.calculate_metric)

            - [`ClassificationPerformanceMetricsThresholdBase.get_threshold()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdBase.get_threshold)

        - [`ClassificationPerformanceMetricsThresholdRenderer`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer)

            - [`ClassificationPerformanceMetricsThresholdRenderer.color_options`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer.color_options)

            - [`ClassificationPerformanceMetricsThresholdRenderer.render_html()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer.render_html)

            - [`ClassificationPerformanceMetricsThresholdRenderer.render_json()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsThresholdRenderer.render_json)

        - [`ClassificationPerformanceMetricsTopK`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK)

            - [`ClassificationPerformanceMetricsTopK.calculate_metric()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK.calculate_metric)

            - [`ClassificationPerformanceMetricsTopK.get_parameters()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK.get_parameters)

            - [`ClassificationPerformanceMetricsTopK.get_threshold()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopK.get_threshold)

        - [`ClassificationPerformanceMetricsTopKRenderer`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer)

            - [`ClassificationPerformanceMetricsTopKRenderer.color_options`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer.color_options)

            - [`ClassificationPerformanceMetricsTopKRenderer.render_html()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer.render_html)

            - [`ClassificationPerformanceMetricsTopKRenderer.render_json()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceMetricsTopKRenderer.render_json)

        - [`ClassificationPerformanceResults`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)

            - [`ClassificationPerformanceResults.columns`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults.columns)

            - [`ClassificationPerformanceResults.current`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults.current)

            - [`ClassificationPerformanceResults.dummy`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults.dummy)

            - [`ClassificationPerformanceResults.reference`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults.reference)

        - [`DatasetClassificationPerformanceMetrics`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics)

            - [`DatasetClassificationPerformanceMetrics.accuracy`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.accuracy)

            - [`DatasetClassificationPerformanceMetrics.confusion_by_classes`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.confusion_by_classes)

            - [`DatasetClassificationPerformanceMetrics.confusion_matrix`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.confusion_matrix)

            - [`DatasetClassificationPerformanceMetrics.f1`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.f1)

            - [`DatasetClassificationPerformanceMetrics.fnr`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.fnr)

            - [`DatasetClassificationPerformanceMetrics.fpr`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.fpr)

            - [`DatasetClassificationPerformanceMetrics.log_loss`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.log_loss)

            - [`DatasetClassificationPerformanceMetrics.metrics_matrix`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.metrics_matrix)

            - [`DatasetClassificationPerformanceMetrics.plot_data`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.plot_data)

            - [`DatasetClassificationPerformanceMetrics.pr_curve`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.pr_curve)

            - [`DatasetClassificationPerformanceMetrics.pr_table`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.pr_table)

            - [`DatasetClassificationPerformanceMetrics.precision`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.precision)

            - [`DatasetClassificationPerformanceMetrics.rate_plots_data`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.rate_plots_data)

            - [`DatasetClassificationPerformanceMetrics.recall`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.recall)

            - [`DatasetClassificationPerformanceMetrics.roc_auc`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.roc_auc)

            - [`DatasetClassificationPerformanceMetrics.roc_aucs`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.roc_aucs)

            - [`DatasetClassificationPerformanceMetrics.roc_curve`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.roc_curve)

            - [`DatasetClassificationPerformanceMetrics.tnr`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.tnr)

            - [`DatasetClassificationPerformanceMetrics.tpr`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics.tpr)

        - [`classification_performance_metrics()`](api-reference/evidently.metrics.md#evidently.metrics.classification_performance_metrics.classification_performance_metrics)

    - [evidently.metrics.utils module](api-reference/evidently.metrics.md#module-evidently.metrics.utils)

        - [`apply_func_to_binned_data()`](api-reference/evidently.metrics.md#evidently.metrics.utils.apply_func_to_binned_data)

        - [`make_target_bins_for_reg_plots()`](api-reference/evidently.metrics.md#evidently.metrics.utils.make_target_bins_for_reg_plots)

    - [Module contents](api-reference/evidently.metrics.md#module-evidently.metrics)

- [evidently.model package](evidently.model.md)

    - [Submodules](api-reference/evidently.model.md#submodules)

    - [evidently.model.dashboard module](api-reference/evidently.model.md#module-evidently.model.dashboard)

        - [`DashboardInfo`](api-reference/evidently.model.md#evidently.model.dashboard.DashboardInfo)

            - [`DashboardInfo.name`](api-reference/evidently.model.md#evidently.model.dashboard.DashboardInfo.name)

            - [`DashboardInfo.widgets`](api-reference/evidently.model.md#evidently.model.dashboard.DashboardInfo.widgets)

    - [evidently.model.widget module](api-reference/evidently.model.md#module-evidently.model.widget)

        - [`AdditionalGraphInfo`](api-reference/evidently.model.md#evidently.model.widget.AdditionalGraphInfo)

            - [`AdditionalGraphInfo.id`](api-reference/evidently.model.md#evidently.model.widget.AdditionalGraphInfo.id)

            - [`AdditionalGraphInfo.params`](api-reference/evidently.model.md#evidently.model.widget.AdditionalGraphInfo.params)

        - [`Alert`](api-reference/evidently.model.md#evidently.model.widget.Alert)

            - [`Alert.longText`](api-reference/evidently.model.md#evidently.model.widget.Alert.longText)

            - [`Alert.state`](api-reference/evidently.model.md#evidently.model.widget.Alert.state)

            - [`Alert.text`](api-reference/evidently.model.md#evidently.model.widget.Alert.text)

            - [`Alert.value`](api-reference/evidently.model.md#evidently.model.widget.Alert.value)

        - [`AlertStats`](api-reference/evidently.model.md#evidently.model.widget.AlertStats)

            - [`AlertStats.active`](api-reference/evidently.model.md#evidently.model.widget.AlertStats.active)

            - [`AlertStats.eggs`](api-reference/evidently.model.md#evidently.model.widget.AlertStats.eggs)

            - [`AlertStats.active`](api-reference/evidently.model.md#id0)

            - [`AlertStats.triggered`](api-reference/evidently.model.md#evidently.model.widget.AlertStats.triggered)

        - [`BaseWidgetInfo`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo)

            - [`BaseWidgetInfo.additionalGraphs`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.additionalGraphs)

            - [`BaseWidgetInfo.alertStats`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.alertStats)

            - [`BaseWidgetInfo.alerts`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.alerts)

            - [`BaseWidgetInfo.alertsPosition`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.alertsPosition)

            - [`BaseWidgetInfo.details`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.details)

            - [`BaseWidgetInfo.get_additional_graphs()`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.get_additional_graphs)

            - [`BaseWidgetInfo.id`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.id)

            - [`BaseWidgetInfo.insights`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.insights)

            - [`BaseWidgetInfo.pageSize`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.pageSize)

            - [`BaseWidgetInfo.params`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.params)

            - [`BaseWidgetInfo.size`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.size)

            - [`BaseWidgetInfo.tabs`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.tabs)

            - [`BaseWidgetInfo.title`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.title)

            - [`BaseWidgetInfo.type`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.type)

            - [`BaseWidgetInfo.widgets`](api-reference/evidently.model.md#evidently.model.widget.BaseWidgetInfo.widgets)

        - [`Insight`](api-reference/evidently.model.md#evidently.model.widget.Insight)

            - [`Insight.title`](api-reference/evidently.model.md#evidently.model.widget.Insight.title)

            - [`Insight.severity`](api-reference/evidently.model.md#evidently.model.widget.Insight.severity)

            - [`Insight.text`](api-reference/evidently.model.md#evidently.model.widget.Insight.text)

            - [`Insight.severity`](api-reference/evidently.model.md#id1)

            - [`Insight.text`](api-reference/evidently.model.md#id2)

            - [`Insight.title`](api-reference/evidently.model.md#id3)

        - [`PlotlyGraphInfo`](api-reference/evidently.model.md#evidently.model.widget.PlotlyGraphInfo)

            - [`PlotlyGraphInfo.data`](api-reference/evidently.model.md#evidently.model.widget.PlotlyGraphInfo.data)

            - [`PlotlyGraphInfo.id`](api-reference/evidently.model.md#evidently.model.widget.PlotlyGraphInfo.id)

            - [`PlotlyGraphInfo.layout`](api-reference/evidently.model.md#evidently.model.widget.PlotlyGraphInfo.layout)

        - [`TabInfo`](api-reference/evidently.model.md#evidently.model.widget.TabInfo)

            - [`TabInfo.id`](api-reference/evidently.model.md#evidently.model.widget.TabInfo.id)

            - [`TabInfo.title`](api-reference/evidently.model.md#evidently.model.widget.TabInfo.title)

            - [`TabInfo.widget`](api-reference/evidently.model.md#evidently.model.widget.TabInfo.widget)

        - [`TriggeredAlertStats`](api-reference/evidently.model.md#evidently.model.widget.TriggeredAlertStats)

            - [`TriggeredAlertStats.last_24h`](api-reference/evidently.model.md#evidently.model.widget.TriggeredAlertStats.last_24h)

            - [`TriggeredAlertStats.period`](api-reference/evidently.model.md#evidently.model.widget.TriggeredAlertStats.period)

        - [`WidgetType`](api-reference/evidently.model.md#evidently.model.widget.WidgetType)

            - [`WidgetType.BIG_GRAPH`](api-reference/evidently.model.md#evidently.model.widget.WidgetType.BIG_GRAPH)

            - [`WidgetType.BIG_TABLE`](api-reference/evidently.model.md#evidently.model.widget.WidgetType.BIG_TABLE)

            - [`WidgetType.COUNTER`](api-reference/evidently.model.md#evidently.model.widget.WidgetType.COUNTER)

            - [`WidgetType.RICH_DATA`](api-reference/evidently.model.md#evidently.model.widget.WidgetType.RICH_DATA)

            - [`WidgetType.TABBED_GRAPH`](api-reference/evidently.model.md#evidently.model.widget.WidgetType.TABBED_GRAPH)

            - [`WidgetType.TABLE`](api-reference/evidently.model.md#evidently.model.widget.WidgetType.TABLE)

            - [`WidgetType.TABS`](api-reference/evidently.model.md#evidently.model.widget.WidgetType.TABS)

    - [Module contents](api-reference/evidently.model.md#module-evidently.model)

- [evidently.model_monitoring package](evidently.model_monitoring.md)

    - [Subpackages](api-reference/evidently.model_monitoring.md#subpackages)

        - [evidently.model_monitoring.monitors package](evidently.model_monitoring.monitors.md)

            - [Submodules](api-reference/evidently.model_monitoring.monitors.md#submodules)

            - [evidently.model_monitoring.monitors.cat_target_drift module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.cat_target_drift)

            - [evidently.model_monitoring.monitors.classification_performance module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.classification_performance)

            - [evidently.model_monitoring.monitors.data_drift module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.data_drift)

            - [evidently.model_monitoring.monitors.data_quality module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.data_quality)

            - [evidently.model_monitoring.monitors.num_target_drift module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.num_target_drift)

            - [evidently.model_monitoring.monitors.prob_classification_performance module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.prob_classification_performance)

            - [evidently.model_monitoring.monitors.regression_performance module](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors.regression_performance)

            - [Module contents](api-reference/evidently.model_monitoring.monitors.md#module-evidently.model_monitoring.monitors)

    - [Submodules](api-reference/evidently.model_monitoring.md#submodules)

    - [evidently.model_monitoring.monitoring module](api-reference/evidently.model_monitoring.md#module-evidently.model_monitoring.monitoring)

        - [`ModelMonitor`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor)

            - [`ModelMonitor.analyzers()`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.analyzers)

            - [`ModelMonitor.calculate()`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.calculate)

            - [`ModelMonitor.metrics()`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.metrics)

            - [`ModelMonitor.monitor_id()`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.monitor_id)

            - [`ModelMonitor.options_provider`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitor.options_provider)

        - [`ModelMonitoring`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring)

            - [`ModelMonitoring.analyzers_results`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.analyzers_results)

            - [`ModelMonitoring.get_analyzers()`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.get_analyzers)

            - [`ModelMonitoring.metrics()`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.metrics)

            - [`ModelMonitoring.options_provider`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.options_provider)

            - [`ModelMonitoring.stages`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoring.stages)

        - [`ModelMonitoringMetric`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoringMetric)

            - [`ModelMonitoringMetric.create()`](api-reference/evidently.model_monitoring.md#evidently.model_monitoring.monitoring.ModelMonitoringMetric.create)

    - [Module contents](api-reference/evidently.model_monitoring.md#module-evidently.model_monitoring)

- [evidently.model_profile package](evidently.model_profile.md)

    - [Subpackages](api-reference/evidently.model_profile.md#subpackages)

        - [evidently.model_profile.sections package](evidently.model_profile.sections.md)

            - [Submodules](api-reference/evidently.model_profile.sections.md#submodules)

            - [evidently.model_profile.sections.base_profile_section module](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections.base_profile_section)

            - [evidently.model_profile.sections.cat_target_drift_profile_section module](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections.cat_target_drift_profile_section)

            - [evidently.model_profile.sections.classification_performance_profile_section module](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections.classification_performance_profile_section)

            - [evidently.model_profile.sections.data_drift_profile_section module](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections.data_drift_profile_section)

            - [evidently.model_profile.sections.data_quality_profile_section module](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections.data_quality_profile_section)

            - [evidently.model_profile.sections.num_target_drift_profile_section module](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections.num_target_drift_profile_section)

            - [evidently.model_profile.sections.prob_classification_performance_profile_section module](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections.prob_classification_performance_profile_section)

            - [evidently.model_profile.sections.regression_performance_profile_section module](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections.regression_performance_profile_section)

            - [Module contents](api-reference/evidently.model_profile.sections.md#module-evidently.model_profile.sections)

    - [Submodules](api-reference/evidently.model_profile.md#submodules)

    - [evidently.model_profile.model_profile module](api-reference/evidently.model_profile.md#module-evidently.model_profile.model_profile)

        - [`Profile`](api-reference/evidently.model_profile.md#evidently.model_profile.model_profile.Profile)

            - [`Profile.calculate()`](api-reference/evidently.model_profile.md#evidently.model_profile.model_profile.Profile.calculate)

            - [`Profile.get_analyzers()`](api-reference/evidently.model_profile.md#evidently.model_profile.model_profile.Profile.get_analyzers)

            - [`Profile.json()`](api-reference/evidently.model_profile.md#evidently.model_profile.model_profile.Profile.json)

            - [`Profile.object()`](api-reference/evidently.model_profile.md#evidently.model_profile.model_profile.Profile.object)

            - [`Profile.result`](api-reference/evidently.model_profile.md#evidently.model_profile.model_profile.Profile.result)

            - [`Profile.stages`](api-reference/evidently.model_profile.md#evidently.model_profile.model_profile.Profile.stages)

    - [Module contents](api-reference/evidently.model_profile.md#module-evidently.model_profile)

- [evidently.nbextension package](evidently.nbextension.md)

    - [Module contents](api-reference/evidently.nbextension.md#module-evidently.nbextension)

- [evidently.options package](evidently.options.md)

    - [Submodules](api-reference/evidently.options.md#submodules)

    - [evidently.options.color_scheme module](api-reference/evidently.options.md#module-evidently.options.color_scheme)

        - [`ColorOptions`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions)

            - [`ColorOptions.color_sequence`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.color_sequence)

            - [`ColorOptions.current_data_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.current_data_color)

            - [`ColorOptions.fill_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.fill_color)

            - [`ColorOptions.get_current_data_color()`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.get_current_data_color)

            - [`ColorOptions.get_reference_data_color()`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.get_reference_data_color)

            - [`ColorOptions.heatmap`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.heatmap)

            - [`ColorOptions.majority_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.majority_color)

            - [`ColorOptions.non_visible_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.non_visible_color)

            - [`ColorOptions.overestimation_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.overestimation_color)

            - [`ColorOptions.primary_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.primary_color)

            - [`ColorOptions.reference_data_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.reference_data_color)

            - [`ColorOptions.secondary_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.secondary_color)

            - [`ColorOptions.underestimation_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.underestimation_color)

            - [`ColorOptions.vertical_lines`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.vertical_lines)

            - [`ColorOptions.zero_line_color`](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions.zero_line_color)

    - [evidently.options.data_drift module](api-reference/evidently.options.md#module-evidently.options.data_drift)

        - [`DataDriftOptions`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions)

            - [`DataDriftOptions.confidence`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.confidence)

            - [`DataDriftOptions.threshold`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.threshold)

            - [`DataDriftOptions.drift_share`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.drift_share)

            - [`DataDriftOptions.nbinsx`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.nbinsx)

            - [`DataDriftOptions.xbins`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.xbins)

            - [`DataDriftOptions.feature_stattest_func`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.feature_stattest_func)

            - [`DataDriftOptions.all_features_stattest`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.all_features_stattest)

            - [`DataDriftOptions.cat_features_stattest`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.cat_features_stattest)

            - [`DataDriftOptions.num_features_stattest`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.num_features_stattest)

            - [`DataDriftOptions.per_feature_stattest`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.per_feature_stattest)

            - [`DataDriftOptions.cat_target_stattest_func`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.cat_target_stattest_func)

            - [`DataDriftOptions.num_target_stattest_func`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.num_target_stattest_func)

            - [`DataDriftOptions.all_features_stattest`](api-reference/evidently.options.md#id0)

            - [`DataDriftOptions.as_dict()`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.as_dict)

            - [`DataDriftOptions.cat_features_stattest`](api-reference/evidently.options.md#id1)

            - [`DataDriftOptions.cat_target_stattest_func`](api-reference/evidently.options.md#id2)

            - [`DataDriftOptions.cat_target_threshold`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.cat_target_threshold)

            - [`DataDriftOptions.confidence`](api-reference/evidently.options.md#id3)

            - [`DataDriftOptions.drift_share`](api-reference/evidently.options.md#id4)

            - [`DataDriftOptions.feature_stattest_func`](api-reference/evidently.options.md#id5)

            - [`DataDriftOptions.get_feature_stattest_func()`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.get_feature_stattest_func)

            - [`DataDriftOptions.get_nbinsx()`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.get_nbinsx)

            - [`DataDriftOptions.get_threshold()`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.get_threshold)

            - [`DataDriftOptions.nbinsx`](api-reference/evidently.options.md#id6)

            - [`DataDriftOptions.num_features_stattest`](api-reference/evidently.options.md#id7)

            - [`DataDriftOptions.num_target_stattest_func`](api-reference/evidently.options.md#id8)

            - [`DataDriftOptions.num_target_threshold`](api-reference/evidently.options.md#evidently.options.data_drift.DataDriftOptions.num_target_threshold)

            - [`DataDriftOptions.per_feature_stattest`](api-reference/evidently.options.md#id9)

            - [`DataDriftOptions.threshold`](api-reference/evidently.options.md#id10)

            - [`DataDriftOptions.xbins`](api-reference/evidently.options.md#id11)

    - [evidently.options.quality_metrics module](api-reference/evidently.options.md#module-evidently.options.quality_metrics)

        - [`QualityMetricsOptions`](api-reference/evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions)

            - [`QualityMetricsOptions.as_dict()`](api-reference/evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.as_dict)

            - [`QualityMetricsOptions.classification_threshold`](api-reference/evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.classification_threshold)

            - [`QualityMetricsOptions.conf_interval_n_sigmas`](api-reference/evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.conf_interval_n_sigmas)

            - [`QualityMetricsOptions.cut_quantile`](api-reference/evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.cut_quantile)

            - [`QualityMetricsOptions.get_cut_quantile()`](api-reference/evidently.options.md#evidently.options.quality_metrics.QualityMetricsOptions.get_cut_quantile)

    - [Module contents](api-reference/evidently.options.md#module-evidently.options)

        - [`OptionsProvider`](api-reference/evidently.options.md#evidently.options.OptionsProvider)

            - [`OptionsProvider.add()`](api-reference/evidently.options.md#evidently.options.OptionsProvider.add)

            - [`OptionsProvider.get()`](api-reference/evidently.options.md#evidently.options.OptionsProvider.get)

- [evidently.pipeline package](evidently.pipeline.md)

    - [Submodules](api-reference/evidently.pipeline.md#submodules)

    - [evidently.pipeline.column_mapping module](api-reference/evidently.pipeline.md#module-evidently.pipeline.column_mapping)

        - [`ColumnMapping`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping)

            - [`ColumnMapping.categorical_features`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.categorical_features)

            - [`ColumnMapping.datetime`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.datetime)

            - [`ColumnMapping.datetime_features`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.datetime_features)

            - [`ColumnMapping.id`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.id)

            - [`ColumnMapping.is_classification_task()`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.is_classification_task)

            - [`ColumnMapping.is_regression_task()`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.is_regression_task)

            - [`ColumnMapping.numerical_features`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.numerical_features)

            - [`ColumnMapping.pos_label`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.pos_label)

            - [`ColumnMapping.prediction`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.prediction)

            - [`ColumnMapping.target`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.target)

            - [`ColumnMapping.target_names`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.target_names)

            - [`ColumnMapping.task`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping.task)

        - [`TaskType`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.TaskType)

            - [`TaskType.CLASSIFICATION_TASK`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.TaskType.CLASSIFICATION_TASK)

            - [`TaskType.REGRESSION_TASK`](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.TaskType.REGRESSION_TASK)

    - [evidently.pipeline.pipeline module](api-reference/evidently.pipeline.md#module-evidently.pipeline.pipeline)

        - [`Pipeline`](api-reference/evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline)

            - [`Pipeline.analyzers_results`](api-reference/evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.analyzers_results)

            - [`Pipeline.execute()`](api-reference/evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.execute)

            - [`Pipeline.get_analyzers()`](api-reference/evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.get_analyzers)

            - [`Pipeline.options_provider`](api-reference/evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.options_provider)

            - [`Pipeline.stages`](api-reference/evidently.pipeline.md#evidently.pipeline.pipeline.Pipeline.stages)

    - [evidently.pipeline.stage module](api-reference/evidently.pipeline.md#module-evidently.pipeline.stage)

        - [`PipelineStage`](api-reference/evidently.pipeline.md#evidently.pipeline.stage.PipelineStage)

            - [`PipelineStage.add_analyzer()`](api-reference/evidently.pipeline.md#evidently.pipeline.stage.PipelineStage.add_analyzer)

            - [`PipelineStage.analyzers()`](api-reference/evidently.pipeline.md#evidently.pipeline.stage.PipelineStage.analyzers)

            - [`PipelineStage.calculate()`](api-reference/evidently.pipeline.md#evidently.pipeline.stage.PipelineStage.calculate)

            - [`PipelineStage.options_provider`](api-reference/evidently.pipeline.md#evidently.pipeline.stage.PipelineStage.options_provider)

    - [Module contents](api-reference/evidently.pipeline.md#module-evidently.pipeline)

- [evidently.profile_sections package](evidently.profile_sections.md)

    - [Module contents](api-reference/evidently.profile_sections.md#module-evidently.profile_sections)

- [evidently.renderers package](evidently.renderers.md)

    - [Submodules](api-reference/evidently.renderers.md#submodules)

    - [evidently.renderers.base_renderer module](api-reference/evidently.renderers.md#module-evidently.renderers.base_renderer)

        - [`BaseRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.BaseRenderer)

            - [`BaseRenderer.color_options`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.BaseRenderer.color_options)

        - [`DetailsInfo`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.DetailsInfo)

            - [`DetailsInfo.id`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.DetailsInfo.id)

            - [`DetailsInfo.info`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.DetailsInfo.info)

            - [`DetailsInfo.title`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.DetailsInfo.title)

        - [`MetricRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer)

            - [`MetricRenderer.color_options`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer.color_options)

            - [`MetricRenderer.render_html()`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer.render_html)

            - [`MetricRenderer.render_json()`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.MetricRenderer.render_json)

        - [`RenderersDefinitions`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions)

            - [`RenderersDefinitions.default_html_metric_renderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions.default_html_metric_renderer)

            - [`RenderersDefinitions.default_html_test_renderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions.default_html_test_renderer)

            - [`RenderersDefinitions.typed_renderers`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions.typed_renderers)

        - [`TestHtmlInfo`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo)

            - [`TestHtmlInfo.description`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.description)

            - [`TestHtmlInfo.details`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.details)

            - [`TestHtmlInfo.groups`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.groups)

            - [`TestHtmlInfo.name`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.name)

            - [`TestHtmlInfo.status`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.status)

            - [`TestHtmlInfo.with_details()`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo.with_details)

        - [`TestRenderer`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

            - [`TestRenderer.color_options`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.color_options)

            - [`TestRenderer.html_description()`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.html_description)

            - [`TestRenderer.json_description()`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.json_description)

            - [`TestRenderer.render_html()`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.render_html)

            - [`TestRenderer.render_json()`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer.render_json)

        - [`default_renderer()`](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.default_renderer)

    - [evidently.renderers.html_widgets module](api-reference/evidently.renderers.md#module-evidently.renderers.html_widgets)

        - [`ColumnDefinition`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition)

            - [`ColumnDefinition.as_dict()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.as_dict)

            - [`ColumnDefinition.field_name`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.field_name)

            - [`ColumnDefinition.options`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.options)

            - [`ColumnDefinition.sort`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.sort)

            - [`ColumnDefinition.title`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.title)

            - [`ColumnDefinition.type`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnDefinition.type)

        - [`ColumnType`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnType)

            - [`ColumnType.HISTOGRAM`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnType.HISTOGRAM)

            - [`ColumnType.LINE`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnType.LINE)

            - [`ColumnType.SCATTER`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnType.SCATTER)

            - [`ColumnType.STRING`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.ColumnType.STRING)

        - [`CounterData`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.CounterData)

            - [`CounterData.float()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.CounterData.float)

            - [`CounterData.int()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.CounterData.int)

            - [`CounterData.label`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.CounterData.label)

            - [`CounterData.string()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.CounterData.string)

            - [`CounterData.value`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.CounterData.value)

        - [`DetailsPartInfo`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.DetailsPartInfo)

            - [`DetailsPartInfo.info`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.DetailsPartInfo.info)

            - [`DetailsPartInfo.title`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.DetailsPartInfo.title)

        - [`GraphData`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.GraphData)

            - [`GraphData.data`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.GraphData.data)

            - [`GraphData.figure()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.GraphData.figure)

            - [`GraphData.layout`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.GraphData.layout)

            - [`GraphData.title`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.GraphData.title)

        - [`HeatmapData`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.HeatmapData)

            - [`HeatmapData.matrix`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.HeatmapData.matrix)

            - [`HeatmapData.name`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.HeatmapData.name)

        - [`HistogramData`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.HistogramData)

            - [`HistogramData.name`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.HistogramData.name)

            - [`HistogramData.x`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.HistogramData.x)

            - [`HistogramData.y`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.HistogramData.y)

        - [`RichTableDataRow`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.RichTableDataRow)

            - [`RichTableDataRow.details`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.RichTableDataRow.details)

            - [`RichTableDataRow.fields`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.RichTableDataRow.fields)

        - [`RowDetails`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.RowDetails)

            - [`RowDetails.parts`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.RowDetails.parts)

            - [`RowDetails.with_part()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.RowDetails.with_part)

        - [`SortDirection`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.SortDirection)

            - [`SortDirection.ASC`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.SortDirection.ASC)

            - [`SortDirection.DESC`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.SortDirection.DESC)

        - [`TabData`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.TabData)

            - [`TabData.title`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.TabData.title)

            - [`TabData.widget`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.TabData.widget)

        - [`WidgetSize`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.WidgetSize)

            - [`WidgetSize.FULL`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.WidgetSize.FULL)

            - [`WidgetSize.HALF`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.WidgetSize.HALF)

        - [`counter()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.counter)

        - [`get_class_separation_plot_data()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.get_class_separation_plot_data)

        - [`get_heatmaps_widget()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.get_heatmaps_widget)

        - [`get_histogram_figure()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.get_histogram_figure)

        - [`get_histogram_figure_with_quantile()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.get_histogram_figure_with_quantile)

        - [`get_histogram_figure_with_range()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.get_histogram_figure_with_range)

        - [`get_histogram_for_distribution()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.get_histogram_for_distribution)

        - [`get_pr_rec_plot_data()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.get_pr_rec_plot_data)

        - [`get_roc_auc_tab_data()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.get_roc_auc_tab_data)

        - [`header_text()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.header_text)

        - [`histogram()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.histogram)

        - [`plotly_data()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.plotly_data)

        - [`plotly_figure()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.plotly_figure)

        - [`plotly_graph()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.plotly_graph)

        - [`plotly_graph_tabs()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.plotly_graph_tabs)

        - [`rich_table_data()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.rich_table_data)

        - [`table_data()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.table_data)

        - [`widget_tabs()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.widget_tabs)

        - [`widget_tabs_for_more_than_one()`](api-reference/evidently.renderers.md#evidently.renderers.html_widgets.widget_tabs_for_more_than_one)

    - [evidently.renderers.notebook_utils module](api-reference/evidently.renderers.md#module-evidently.renderers.notebook_utils)

        - [`determine_template()`](api-reference/evidently.renderers.md#evidently.renderers.notebook_utils.determine_template)

    - [evidently.renderers.render_utils module](api-reference/evidently.renderers.md#module-evidently.renderers.render_utils)

        - [`get_distribution_plot_figure()`](api-reference/evidently.renderers.md#evidently.renderers.render_utils.get_distribution_plot_figure)

        - [`plot_distr()`](api-reference/evidently.renderers.md#evidently.renderers.render_utils.plot_distr)

    - [Module contents](api-reference/evidently.renderers.md#module-evidently.renderers)

- [evidently.report package](evidently.report.md)

    - [Submodules](api-reference/evidently.report.md#submodules)

    - [evidently.report.report module](api-reference/evidently.report.md#module-evidently.report.report)

        - [`Report`](api-reference/evidently.report.md#evidently.report.report.Report)

            - [`Report.as_dict()`](api-reference/evidently.report.md#evidently.report.report.Report.as_dict)

            - [`Report.metrics`](api-reference/evidently.report.md#evidently.report.report.Report.metrics)

            - [`Report.run()`](api-reference/evidently.report.md#evidently.report.report.Report.run)

    - [Module contents](api-reference/evidently.report.md#module-evidently.report)

- [evidently.runner package](evidently.runner.md)

    - [Submodules](api-reference/evidently.runner.md#submodules)

    - [evidently.runner.dashboard_runner module](api-reference/evidently.runner.md#module-evidently.runner.dashboard_runner)

        - [`DashboardRunner`](api-reference/evidently.runner.md#evidently.runner.dashboard_runner.DashboardRunner)

            - [`DashboardRunner.run()`](api-reference/evidently.runner.md#evidently.runner.dashboard_runner.DashboardRunner.run)

        - [`DashboardRunnerOptions`](api-reference/evidently.runner.md#evidently.runner.dashboard_runner.DashboardRunnerOptions)

            - [`DashboardRunnerOptions.dashboard_tabs`](api-reference/evidently.runner.md#evidently.runner.dashboard_runner.DashboardRunnerOptions.dashboard_tabs)

    - [evidently.runner.loader module](api-reference/evidently.runner.md#module-evidently.runner.loader)

        - [`DataLoader`](api-reference/evidently.runner.md#evidently.runner.loader.DataLoader)

            - [`DataLoader.load()`](api-reference/evidently.runner.md#evidently.runner.loader.DataLoader.load)

        - [`DataOptions`](api-reference/evidently.runner.md#evidently.runner.loader.DataOptions)

            - [`DataOptions.column_names`](api-reference/evidently.runner.md#evidently.runner.loader.DataOptions.column_names)

            - [`DataOptions.date_column`](api-reference/evidently.runner.md#evidently.runner.loader.DataOptions.date_column)

            - [`DataOptions.header`](api-reference/evidently.runner.md#evidently.runner.loader.DataOptions.header)

            - [`DataOptions.separator`](api-reference/evidently.runner.md#evidently.runner.loader.DataOptions.separator)

        - [`RandomizedSkipRows`](api-reference/evidently.runner.md#evidently.runner.loader.RandomizedSkipRows)

            - [`RandomizedSkipRows.skiprows()`](api-reference/evidently.runner.md#evidently.runner.loader.RandomizedSkipRows.skiprows)

        - [`SamplingOptions`](api-reference/evidently.runner.md#evidently.runner.loader.SamplingOptions)

            - [`SamplingOptions.n`](api-reference/evidently.runner.md#evidently.runner.loader.SamplingOptions.n)

            - [`SamplingOptions.random_seed`](api-reference/evidently.runner.md#evidently.runner.loader.SamplingOptions.random_seed)

            - [`SamplingOptions.ratio`](api-reference/evidently.runner.md#evidently.runner.loader.SamplingOptions.ratio)

            - [`SamplingOptions.type`](api-reference/evidently.runner.md#evidently.runner.loader.SamplingOptions.type)

    - [evidently.runner.profile_runner module](api-reference/evidently.runner.md#module-evidently.runner.profile_runner)

        - [`ProfileRunner`](api-reference/evidently.runner.md#evidently.runner.profile_runner.ProfileRunner)

            - [`ProfileRunner.run()`](api-reference/evidently.runner.md#evidently.runner.profile_runner.ProfileRunner.run)

        - [`ProfileRunnerOptions`](api-reference/evidently.runner.md#evidently.runner.profile_runner.ProfileRunnerOptions)

            - [`ProfileRunnerOptions.pretty_print`](api-reference/evidently.runner.md#evidently.runner.profile_runner.ProfileRunnerOptions.pretty_print)

            - [`ProfileRunnerOptions.profile_parts`](api-reference/evidently.runner.md#evidently.runner.profile_runner.ProfileRunnerOptions.profile_parts)

    - [evidently.runner.runner module](api-reference/evidently.runner.md#module-evidently.runner.runner)

        - [`Runner`](api-reference/evidently.runner.md#evidently.runner.runner.Runner)

        - [`RunnerOptions`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions)

            - [`RunnerOptions.column_mapping`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.column_mapping)

            - [`RunnerOptions.current_data_options`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.current_data_options)

            - [`RunnerOptions.current_data_path`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.current_data_path)

            - [`RunnerOptions.current_data_sampling`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.current_data_sampling)

            - [`RunnerOptions.options`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.options)

            - [`RunnerOptions.output_path`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.output_path)

            - [`RunnerOptions.reference_data_options`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.reference_data_options)

            - [`RunnerOptions.reference_data_path`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.reference_data_path)

            - [`RunnerOptions.reference_data_sampling`](api-reference/evidently.runner.md#evidently.runner.runner.RunnerOptions.reference_data_sampling)

        - [`parse_options()`](api-reference/evidently.runner.md#evidently.runner.runner.parse_options)

    - [Module contents](api-reference/evidently.runner.md#module-evidently.runner)

- [evidently.suite package](evidently.suite.md)

    - [Submodules](api-reference/evidently.suite.md#submodules)

    - [evidently.suite.base_suite module](api-reference/evidently.suite.md#module-evidently.suite.base_suite)

        - [`Context`](api-reference/evidently.suite.md#evidently.suite.base_suite.Context)

            - [`Context.execution_graph`](api-reference/evidently.suite.md#evidently.suite.base_suite.Context.execution_graph)

            - [`Context.metric_results`](api-reference/evidently.suite.md#evidently.suite.base_suite.Context.metric_results)

            - [`Context.metrics`](api-reference/evidently.suite.md#evidently.suite.base_suite.Context.metrics)

            - [`Context.renderers`](api-reference/evidently.suite.md#evidently.suite.base_suite.Context.renderers)

            - [`Context.state`](api-reference/evidently.suite.md#evidently.suite.base_suite.Context.state)

            - [`Context.test_results`](api-reference/evidently.suite.md#evidently.suite.base_suite.Context.test_results)

            - [`Context.tests`](api-reference/evidently.suite.md#evidently.suite.base_suite.Context.tests)

        - [`Display`](api-reference/evidently.suite.md#evidently.suite.base_suite.Display)

            - [`Display.as_dict()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Display.as_dict)

            - [`Display.json()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Display.json)

            - [`Display.options_provider`](api-reference/evidently.suite.md#evidently.suite.base_suite.Display.options_provider)

            - [`Display.save_html()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Display.save_html)

            - [`Display.save_json()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Display.save_json)

            - [`Display.show()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Display.show)

        - [`ExecutionError`](api-reference/evidently.suite.md#evidently.suite.base_suite.ExecutionError)

        - [`State`](api-reference/evidently.suite.md#evidently.suite.base_suite.State)

            - [`State.name`](api-reference/evidently.suite.md#evidently.suite.base_suite.State.name)

        - [`States`](api-reference/evidently.suite.md#evidently.suite.base_suite.States)

            - [`States.Calculated`](api-reference/evidently.suite.md#evidently.suite.base_suite.States.Calculated)

            - [`States.Init`](api-reference/evidently.suite.md#evidently.suite.base_suite.States.Init)

            - [`States.Tested`](api-reference/evidently.suite.md#evidently.suite.base_suite.States.Tested)

            - [`States.Verified`](api-reference/evidently.suite.md#evidently.suite.base_suite.States.Verified)

        - [`Suite`](api-reference/evidently.suite.md#evidently.suite.base_suite.Suite)

            - [`Suite.add_metric()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Suite.add_metric)

            - [`Suite.add_test()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Suite.add_test)

            - [`Suite.context`](api-reference/evidently.suite.md#evidently.suite.base_suite.Suite.context)

            - [`Suite.run_calculate()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Suite.run_calculate)

            - [`Suite.run_checks()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Suite.run_checks)

            - [`Suite.verify()`](api-reference/evidently.suite.md#evidently.suite.base_suite.Suite.verify)

        - [`find_metric_renderer()`](api-reference/evidently.suite.md#evidently.suite.base_suite.find_metric_renderer)

        - [`find_test_renderer()`](api-reference/evidently.suite.md#evidently.suite.base_suite.find_test_renderer)

    - [evidently.suite.execution_graph module](api-reference/evidently.suite.md#module-evidently.suite.execution_graph)

        - [`ExecutionGraph`](api-reference/evidently.suite.md#evidently.suite.execution_graph.ExecutionGraph)

            - [`ExecutionGraph.get_metric_execution_iterator()`](api-reference/evidently.suite.md#evidently.suite.execution_graph.ExecutionGraph.get_metric_execution_iterator)

            - [`ExecutionGraph.get_test_execution_iterator()`](api-reference/evidently.suite.md#evidently.suite.execution_graph.ExecutionGraph.get_test_execution_iterator)

        - [`SimpleExecutionGraph`](api-reference/evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph)

            - [`SimpleExecutionGraph.get_metric_execution_iterator()`](api-reference/evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph.get_metric_execution_iterator)

            - [`SimpleExecutionGraph.get_test_execution_iterator()`](api-reference/evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph.get_test_execution_iterator)

            - [`SimpleExecutionGraph.metrics`](api-reference/evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph.metrics)

            - [`SimpleExecutionGraph.tests`](api-reference/evidently.suite.md#evidently.suite.execution_graph.SimpleExecutionGraph.tests)

    - [Module contents](api-reference/evidently.suite.md#module-evidently.suite)

- [evidently.tabs package](evidently.tabs.md)

    - [Module contents](api-reference/evidently.tabs.md#module-evidently.tabs)

- [evidently.test_preset package](evidently.test_preset.md)

    - [Submodules](api-reference/evidently.test_preset.md#submodules)

    - [evidently.test_preset.classification_binary module](api-reference/evidently.test_preset.md#module-evidently.test_preset.classification_binary)

        - [`BinaryClassificationTestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.classification_binary.BinaryClassificationTestPreset)

            - [`BinaryClassificationTestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.classification_binary.BinaryClassificationTestPreset.generate_tests)

    - [evidently.test_preset.classification_binary_topk module](api-reference/evidently.test_preset.md#module-evidently.test_preset.classification_binary_topk)

        - [`BinaryClassificationTopKTestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.classification_binary_topk.BinaryClassificationTopKTestPreset)

            - [`BinaryClassificationTopKTestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.classification_binary_topk.BinaryClassificationTopKTestPreset.generate_tests)

    - [evidently.test_preset.classification_multiclass module](api-reference/evidently.test_preset.md#module-evidently.test_preset.classification_multiclass)

        - [`MulticlassClassificationTestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.classification_multiclass.MulticlassClassificationTestPreset)

            - [`MulticlassClassificationTestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.classification_multiclass.MulticlassClassificationTestPreset.generate_tests)

    - [evidently.test_preset.data_drift module](api-reference/evidently.test_preset.md#module-evidently.test_preset.data_drift)

        - [`DataDriftTestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.data_drift.DataDriftTestPreset)

            - [`DataDriftTestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.data_drift.DataDriftTestPreset.generate_tests)

    - [evidently.test_preset.data_quality module](api-reference/evidently.test_preset.md#module-evidently.test_preset.data_quality)

        - [`DataQualityTestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.data_quality.DataQualityTestPreset)

            - [`DataQualityTestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.data_quality.DataQualityTestPreset.generate_tests)

    - [evidently.test_preset.data_stability module](api-reference/evidently.test_preset.md#module-evidently.test_preset.data_stability)

        - [`DataStabilityTestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.data_stability.DataStabilityTestPreset)

            - [`DataStabilityTestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.data_stability.DataStabilityTestPreset.generate_tests)

    - [evidently.test_preset.no_target_performance module](api-reference/evidently.test_preset.md#module-evidently.test_preset.no_target_performance)

        - [`NoTargetPerformanceTestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.no_target_performance.NoTargetPerformanceTestPreset)

            - [`NoTargetPerformanceTestPreset.columns`](api-reference/evidently.test_preset.md#evidently.test_preset.no_target_performance.NoTargetPerformanceTestPreset.columns)

            - [`NoTargetPerformanceTestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.no_target_performance.NoTargetPerformanceTestPreset.generate_tests)

    - [evidently.test_preset.regression module](api-reference/evidently.test_preset.md#module-evidently.test_preset.regression)

        - [`RegressionTestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.regression.RegressionTestPreset)

            - [`RegressionTestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.regression.RegressionTestPreset.generate_tests)

    - [evidently.test_preset.test_preset module](api-reference/evidently.test_preset.md#module-evidently.test_preset.test_preset)

        - [`TestPreset`](api-reference/evidently.test_preset.md#evidently.test_preset.test_preset.TestPreset)

            - [`TestPreset.generate_tests()`](api-reference/evidently.test_preset.md#evidently.test_preset.test_preset.TestPreset.generate_tests)

    - [Module contents](api-reference/evidently.test_preset.md#module-evidently.test_preset)

- [evidently.test_suite package](evidently.test_suite.md)

    - [Submodules](api-reference/evidently.test_suite.md#submodules)

    - [evidently.test_suite.test_suite module](api-reference/evidently.test_suite.md#module-evidently.test_suite.test_suite)

        - [`TestSuite`](api-reference/evidently.test_suite.md#evidently.test_suite.test_suite.TestSuite)

            - [`TestSuite.as_dict()`](api-reference/evidently.test_suite.md#evidently.test_suite.test_suite.TestSuite.as_dict)

            - [`TestSuite.run()`](api-reference/evidently.test_suite.md#evidently.test_suite.test_suite.TestSuite.run)

    - [Module contents](api-reference/evidently.test_suite.md#module-evidently.test_suite)

- [evidently.tests package](evidently.tests.md)

    - [Submodules](api-reference/evidently.tests.md#submodules)

    - [evidently.tests.base_test module](api-reference/evidently.tests.md#module-evidently.tests.base_test)

        - [`BaseCheckValueTest`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest)

            - [`BaseCheckValueTest.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.calculate_value_for_test)

            - [`BaseCheckValueTest.check()`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.check)

            - [`BaseCheckValueTest.get_condition()`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.get_condition)

            - [`BaseCheckValueTest.get_description()`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.get_description)

            - [`BaseCheckValueTest.groups()`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.groups)

            - [`BaseCheckValueTest.value`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseCheckValueTest.value)

        - [`BaseConditionsTest`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseConditionsTest)

            - [`BaseConditionsTest.condition`](api-reference/evidently.tests.md#evidently.tests.base_test.BaseConditionsTest.condition)

        - [`GroupData`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupData)

            - [`GroupData.description`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupData.description)

            - [`GroupData.id`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupData.id)

            - [`GroupData.severity`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupData.severity)

            - [`GroupData.sort_index`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupData.sort_index)

            - [`GroupData.title`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupData.title)

        - [`GroupTypeData`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupTypeData)

            - [`GroupTypeData.add_value()`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupTypeData.add_value)

            - [`GroupTypeData.id`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupTypeData.id)

            - [`GroupTypeData.title`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupTypeData.title)

            - [`GroupTypeData.values`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupTypeData.values)

        - [`GroupingTypes`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupingTypes)

            - [`GroupingTypes.ByClass`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupingTypes.ByClass)

            - [`GroupingTypes.ByFeature`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupingTypes.ByFeature)

            - [`GroupingTypes.TestGroup`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupingTypes.TestGroup)

            - [`GroupingTypes.TestType`](api-reference/evidently.tests.md#evidently.tests.base_test.GroupingTypes.TestType)

        - [`Test`](api-reference/evidently.tests.md#evidently.tests.base_test.Test)

            - [`Test.check()`](api-reference/evidently.tests.md#evidently.tests.base_test.Test.check)

            - [`Test.context`](api-reference/evidently.tests.md#evidently.tests.base_test.Test.context)

            - [`Test.get_result()`](api-reference/evidently.tests.md#evidently.tests.base_test.Test.get_result)

            - [`Test.group`](api-reference/evidently.tests.md#evidently.tests.base_test.Test.group)

            - [`Test.name`](api-reference/evidently.tests.md#evidently.tests.base_test.Test.name)

            - [`Test.set_context()`](api-reference/evidently.tests.md#evidently.tests.base_test.Test.set_context)

        - [`TestResult`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult)

            - [`TestResult.ERROR`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.ERROR)

            - [`TestResult.FAIL`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.FAIL)

            - [`TestResult.SKIPPED`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.SKIPPED)

            - [`TestResult.SUCCESS`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.SUCCESS)

            - [`TestResult.WARNING`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.WARNING)

            - [`TestResult.description`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.description)

            - [`TestResult.groups`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.groups)

            - [`TestResult.is_passed()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.is_passed)

            - [`TestResult.mark_as_error()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.mark_as_error)

            - [`TestResult.mark_as_fail()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.mark_as_fail)

            - [`TestResult.mark_as_success()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.mark_as_success)

            - [`TestResult.mark_as_warning()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.mark_as_warning)

            - [`TestResult.name`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.name)

            - [`TestResult.set_status()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.set_status)

            - [`TestResult.status`](api-reference/evidently.tests.md#evidently.tests.base_test.TestResult.status)

        - [`TestValueCondition`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition)

            - [`TestValueCondition.as_dict()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.as_dict)

            - [`TestValueCondition.check_value()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.check_value)

            - [`TestValueCondition.eq`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.eq)

            - [`TestValueCondition.gt`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.gt)

            - [`TestValueCondition.gte`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.gte)

            - [`TestValueCondition.has_condition()`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.has_condition)

            - [`TestValueCondition.is_in`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.is_in)

            - [`TestValueCondition.lt`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.lt)

            - [`TestValueCondition.lte`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.lte)

            - [`TestValueCondition.not_eq`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.not_eq)

            - [`TestValueCondition.not_in`](api-reference/evidently.tests.md#evidently.tests.base_test.TestValueCondition.not_in)

        - [`generate_column_tests()`](api-reference/evidently.tests.md#evidently.tests.base_test.generate_column_tests)

    - [evidently.tests.classification_performance_tests module](api-reference/evidently.tests.md#module-evidently.tests.classification_performance_tests)

        - [`ByClassClassificationTest`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.ByClassClassificationTest)

            - [`ByClassClassificationTest.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.ByClassClassificationTest.metric)

            - [`ByClassClassificationTest.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.ByClassClassificationTest.name)

        - [`SimpleClassificationTest`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest)

            - [`SimpleClassificationTest.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.calculate_value_for_test)

            - [`SimpleClassificationTest.get_condition()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.get_condition)

            - [`SimpleClassificationTest.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.get_value)

            - [`SimpleClassificationTest.group`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.group)

            - [`SimpleClassificationTest.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.metric)

            - [`SimpleClassificationTest.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTest.name)

        - [`SimpleClassificationTestTopK`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK)

            - [`SimpleClassificationTestTopK.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.calculate_value_for_test)

            - [`SimpleClassificationTestTopK.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.condition)

            - [`SimpleClassificationTestTopK.get_condition()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.get_condition)

            - [`SimpleClassificationTestTopK.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.metric)

            - [`SimpleClassificationTestTopK.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.name)

            - [`SimpleClassificationTestTopK.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.SimpleClassificationTestTopK.value)

        - [`TestAccuracyScore`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore)

            - [`TestAccuracyScore.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.condition)

            - [`TestAccuracyScore.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.get_description)

            - [`TestAccuracyScore.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.get_value)

            - [`TestAccuracyScore.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.metric)

            - [`TestAccuracyScore.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.name)

            - [`TestAccuracyScore.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScore.value)

        - [`TestAccuracyScoreRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer)

            - [`TestAccuracyScoreRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer.color_options)

            - [`TestAccuracyScoreRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer.render_html)

            - [`TestAccuracyScoreRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer.render_json)

        - [`TestF1ByClass`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClass)

            - [`TestF1ByClass.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClass.get_description)

            - [`TestF1ByClass.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClass.get_value)

            - [`TestF1ByClass.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClass.name)

        - [`TestF1ByClassRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClassRenderer)

            - [`TestF1ByClassRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClassRenderer.color_options)

            - [`TestF1ByClassRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClassRenderer.render_html)

            - [`TestF1ByClassRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ByClassRenderer.render_json)

        - [`TestF1Score`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score)

            - [`TestF1Score.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.condition)

            - [`TestF1Score.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.get_description)

            - [`TestF1Score.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.get_value)

            - [`TestF1Score.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.metric)

            - [`TestF1Score.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.name)

            - [`TestF1Score.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1Score.value)

        - [`TestF1ScoreRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ScoreRenderer)

            - [`TestF1ScoreRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ScoreRenderer.color_options)

            - [`TestF1ScoreRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ScoreRenderer.render_html)

            - [`TestF1ScoreRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestF1ScoreRenderer.render_json)

        - [`TestFNR`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR)

            - [`TestFNR.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.condition)

            - [`TestFNR.get_condition()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.get_condition)

            - [`TestFNR.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.get_description)

            - [`TestFNR.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.get_value)

            - [`TestFNR.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.metric)

            - [`TestFNR.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.name)

            - [`TestFNR.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNR.value)

        - [`TestFNRRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNRRenderer)

            - [`TestFNRRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNRRenderer.color_options)

            - [`TestFNRRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNRRenderer.render_html)

            - [`TestFNRRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFNRRenderer.render_json)

        - [`TestFPR`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR)

            - [`TestFPR.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.condition)

            - [`TestFPR.get_condition()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.get_condition)

            - [`TestFPR.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.get_description)

            - [`TestFPR.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.get_value)

            - [`TestFPR.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.metric)

            - [`TestFPR.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.name)

            - [`TestFPR.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPR.value)

        - [`TestFPRRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPRRenderer)

            - [`TestFPRRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPRRenderer.color_options)

            - [`TestFPRRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPRRenderer.render_html)

            - [`TestFPRRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestFPRRenderer.render_json)

        - [`TestLogLoss`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss)

            - [`TestLogLoss.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.condition)

            - [`TestLogLoss.get_condition()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.get_condition)

            - [`TestLogLoss.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.get_description)

            - [`TestLogLoss.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.get_value)

            - [`TestLogLoss.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.metric)

            - [`TestLogLoss.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.name)

            - [`TestLogLoss.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLoss.value)

        - [`TestLogLossRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLossRenderer)

            - [`TestLogLossRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLossRenderer.color_options)

            - [`TestLogLossRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLossRenderer.render_html)

            - [`TestLogLossRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestLogLossRenderer.render_json)

        - [`TestPrecisionByClass`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClass)

            - [`TestPrecisionByClass.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClass.get_description)

            - [`TestPrecisionByClass.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClass.get_value)

            - [`TestPrecisionByClass.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClass.name)

        - [`TestPrecisionByClassRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer)

            - [`TestPrecisionByClassRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer.color_options)

            - [`TestPrecisionByClassRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer.render_html)

            - [`TestPrecisionByClassRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer.render_json)

        - [`TestPrecisionScore`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore)

            - [`TestPrecisionScore.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.condition)

            - [`TestPrecisionScore.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.get_description)

            - [`TestPrecisionScore.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.get_value)

            - [`TestPrecisionScore.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.metric)

            - [`TestPrecisionScore.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.name)

            - [`TestPrecisionScore.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScore.value)

        - [`TestPrecisionScoreRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer)

            - [`TestPrecisionScoreRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer.color_options)

            - [`TestPrecisionScoreRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer.render_html)

            - [`TestPrecisionScoreRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer.render_json)

        - [`TestRecallByClass`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClass)

            - [`TestRecallByClass.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClass.get_description)

            - [`TestRecallByClass.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClass.get_value)

            - [`TestRecallByClass.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClass.name)

        - [`TestRecallByClassRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClassRenderer)

            - [`TestRecallByClassRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClassRenderer.color_options)

            - [`TestRecallByClassRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClassRenderer.render_html)

            - [`TestRecallByClassRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallByClassRenderer.render_json)

        - [`TestRecallScore`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore)

            - [`TestRecallScore.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.condition)

            - [`TestRecallScore.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.get_description)

            - [`TestRecallScore.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.get_value)

            - [`TestRecallScore.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.metric)

            - [`TestRecallScore.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.name)

            - [`TestRecallScore.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScore.value)

        - [`TestRecallScoreRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScoreRenderer)

            - [`TestRecallScoreRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScoreRenderer.color_options)

            - [`TestRecallScoreRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScoreRenderer.render_html)

            - [`TestRecallScoreRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRecallScoreRenderer.render_json)

        - [`TestRocAuc`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc)

            - [`TestRocAuc.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.condition)

            - [`TestRocAuc.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.get_description)

            - [`TestRocAuc.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.get_value)

            - [`TestRocAuc.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.metric)

            - [`TestRocAuc.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.name)

            - [`TestRocAuc.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAuc.value)

        - [`TestRocAucRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAucRenderer)

            - [`TestRocAucRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAucRenderer.color_options)

            - [`TestRocAucRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAucRenderer.render_html)

            - [`TestRocAucRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestRocAucRenderer.render_json)

        - [`TestTNR`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR)

            - [`TestTNR.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.condition)

            - [`TestTNR.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.get_description)

            - [`TestTNR.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.get_value)

            - [`TestTNR.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.metric)

            - [`TestTNR.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.name)

            - [`TestTNR.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNR.value)

        - [`TestTNRRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNRRenderer)

            - [`TestTNRRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNRRenderer.color_options)

            - [`TestTNRRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNRRenderer.render_html)

            - [`TestTNRRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTNRRenderer.render_json)

        - [`TestTPR`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR)

            - [`TestTPR.condition`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.condition)

            - [`TestTPR.get_description()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.get_description)

            - [`TestTPR.get_value()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.get_value)

            - [`TestTPR.metric`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.metric)

            - [`TestTPR.name`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.name)

            - [`TestTPR.value`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPR.value)

        - [`TestTPRRenderer`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPRRenderer)

            - [`TestTPRRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPRRenderer.color_options)

            - [`TestTPRRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPRRenderer.render_html)

            - [`TestTPRRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.classification_performance_tests.TestTPRRenderer.render_json)

    - [evidently.tests.data_drift_tests module](api-reference/evidently.tests.md#module-evidently.tests.data_drift_tests)

        - [`BaseDataDriftMetricsTest`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.BaseDataDriftMetricsTest)

            - [`BaseDataDriftMetricsTest.check()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.BaseDataDriftMetricsTest.check)

            - [`BaseDataDriftMetricsTest.group`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.BaseDataDriftMetricsTest.group)

            - [`BaseDataDriftMetricsTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.BaseDataDriftMetricsTest.metric)

        - [`TestAllFeaturesValueDrift`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestAllFeaturesValueDrift)

            - [`TestAllFeaturesValueDrift.generate()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestAllFeaturesValueDrift.generate)

        - [`TestColumnValueDrift`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift)

            - [`TestColumnValueDrift.check()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.check)

            - [`TestColumnValueDrift.column_name`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.column_name)

            - [`TestColumnValueDrift.group`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.group)

            - [`TestColumnValueDrift.metric`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.metric)

            - [`TestColumnValueDrift.name`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDrift.name)

        - [`TestColumnValueDriftRenderer`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDriftRenderer)

            - [`TestColumnValueDriftRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDriftRenderer.color_options)

            - [`TestColumnValueDriftRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDriftRenderer.render_html)

            - [`TestColumnValueDriftRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestColumnValueDriftRenderer.render_json)

        - [`TestCustomFeaturesValueDrift`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestCustomFeaturesValueDrift)

            - [`TestCustomFeaturesValueDrift.features`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestCustomFeaturesValueDrift.features)

            - [`TestCustomFeaturesValueDrift.generate()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestCustomFeaturesValueDrift.generate)

        - [`TestDataDriftResult`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestDataDriftResult)

            - [`TestDataDriftResult.features`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestDataDriftResult.features)

        - [`TestNumberOfDriftedColumns`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns)

            - [`TestNumberOfDriftedColumns.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.calculate_value_for_test)

            - [`TestNumberOfDriftedColumns.condition`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.condition)

            - [`TestNumberOfDriftedColumns.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.get_condition)

            - [`TestNumberOfDriftedColumns.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.get_description)

            - [`TestNumberOfDriftedColumns.metric`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.metric)

            - [`TestNumberOfDriftedColumns.name`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.name)

            - [`TestNumberOfDriftedColumns.value`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumns.value)

        - [`TestNumberOfDriftedColumnsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer)

            - [`TestNumberOfDriftedColumnsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer.color_options)

            - [`TestNumberOfDriftedColumnsRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer.render_html)

            - [`TestNumberOfDriftedColumnsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer.render_json)

        - [`TestShareOfDriftedColumns`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns)

            - [`TestShareOfDriftedColumns.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.calculate_value_for_test)

            - [`TestShareOfDriftedColumns.condition`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.condition)

            - [`TestShareOfDriftedColumns.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.get_condition)

            - [`TestShareOfDriftedColumns.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.get_description)

            - [`TestShareOfDriftedColumns.metric`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.metric)

            - [`TestShareOfDriftedColumns.name`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.name)

            - [`TestShareOfDriftedColumns.value`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumns.value)

        - [`TestShareOfDriftedColumnsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer)

            - [`TestShareOfDriftedColumnsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer.color_options)

            - [`TestShareOfDriftedColumnsRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer.render_html)

            - [`TestShareOfDriftedColumnsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer.render_json)

    - [evidently.tests.data_integrity_tests module](api-reference/evidently.tests.md#module-evidently.tests.data_integrity_tests)

        - [`BaseIntegrityByColumnsConditionTest`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest)

            - [`BaseIntegrityByColumnsConditionTest.column_name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest.column_name)

            - [`BaseIntegrityByColumnsConditionTest.data_integrity_metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest.data_integrity_metric)

            - [`BaseIntegrityByColumnsConditionTest.group`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest.group)

            - [`BaseIntegrityByColumnsConditionTest.groups()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest.groups)

        - [`BaseIntegrityColumnMissingValuesTest`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest)

            - [`BaseIntegrityColumnMissingValuesTest.column_name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest.column_name)

            - [`BaseIntegrityColumnMissingValuesTest.group`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest.group)

            - [`BaseIntegrityColumnMissingValuesTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest.metric)

        - [`BaseIntegrityMissingValuesValuesTest`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityMissingValuesValuesTest)

            - [`BaseIntegrityMissingValuesValuesTest.group`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityMissingValuesValuesTest.group)

            - [`BaseIntegrityMissingValuesValuesTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityMissingValuesValuesTest.metric)

        - [`BaseIntegrityOneColumnTest`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest)

            - [`BaseIntegrityOneColumnTest.column_name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest.column_name)

            - [`BaseIntegrityOneColumnTest.group`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest.group)

            - [`BaseIntegrityOneColumnTest.groups()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest.groups)

            - [`BaseIntegrityOneColumnTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest.metric)

        - [`BaseIntegrityValueTest`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityValueTest)

            - [`BaseIntegrityValueTest.group`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityValueTest.group)

            - [`BaseIntegrityValueTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseIntegrityValueTest.metric)

        - [`BaseTestMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer)

            - [`BaseTestMissingValuesRenderer.MISSING_VALUES_NAMING_MAPPING`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer.MISSING_VALUES_NAMING_MAPPING)

            - [`BaseTestMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer.color_options)

            - [`BaseTestMissingValuesRenderer.get_table_with_missing_values_and_percents_by_column()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer.get_table_with_missing_values_and_percents_by_column)

            - [`BaseTestMissingValuesRenderer.get_table_with_number_of_missing_values_by_one_missing_value()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer.get_table_with_number_of_missing_values_by_one_missing_value)

        - [`TestAllColumnsShareOfMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestAllColumnsShareOfMissingValues)

            - [`TestAllColumnsShareOfMissingValues.generate()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestAllColumnsShareOfMissingValues.generate)

        - [`TestColumnAllConstantValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValues)

            - [`TestColumnAllConstantValues.check()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValues.check)

            - [`TestColumnAllConstantValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValues.metric)

            - [`TestColumnAllConstantValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValues.name)

        - [`TestColumnAllConstantValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValuesRenderer)

            - [`TestColumnAllConstantValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValuesRenderer.color_options)

            - [`TestColumnAllConstantValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllConstantValuesRenderer.render_html)

        - [`TestColumnAllUniqueValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues)

            - [`TestColumnAllUniqueValues.check()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues.check)

            - [`TestColumnAllUniqueValues.column_name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues.column_name)

            - [`TestColumnAllUniqueValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues.metric)

            - [`TestColumnAllUniqueValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValues.name)

        - [`TestColumnAllUniqueValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValuesRenderer)

            - [`TestColumnAllUniqueValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValuesRenderer.color_options)

            - [`TestColumnAllUniqueValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnAllUniqueValuesRenderer.render_html)

        - [`TestColumnNumberOfDifferentMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues)

            - [`TestColumnNumberOfDifferentMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.calculate_value_for_test)

            - [`TestColumnNumberOfDifferentMissingValues.column_name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.column_name)

            - [`TestColumnNumberOfDifferentMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.condition)

            - [`TestColumnNumberOfDifferentMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.get_condition)

            - [`TestColumnNumberOfDifferentMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.get_description)

            - [`TestColumnNumberOfDifferentMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.metric)

            - [`TestColumnNumberOfDifferentMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.name)

            - [`TestColumnNumberOfDifferentMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues.value)

        - [`TestColumnNumberOfDifferentMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer)

            - [`TestColumnNumberOfDifferentMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer.color_options)

            - [`TestColumnNumberOfDifferentMissingValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer.render_html)

            - [`TestColumnNumberOfDifferentMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer.render_json)

        - [`TestColumnNumberOfMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues)

            - [`TestColumnNumberOfMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.calculate_value_for_test)

            - [`TestColumnNumberOfMissingValues.column_name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.column_name)

            - [`TestColumnNumberOfMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.condition)

            - [`TestColumnNumberOfMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.get_condition)

            - [`TestColumnNumberOfMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.get_description)

            - [`TestColumnNumberOfMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.metric)

            - [`TestColumnNumberOfMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.name)

            - [`TestColumnNumberOfMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues.value)

        - [`TestColumnNumberOfMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValuesRenderer)

            - [`TestColumnNumberOfMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValuesRenderer.color_options)

            - [`TestColumnNumberOfMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValuesRenderer.render_json)

        - [`TestColumnShareOfMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues)

            - [`TestColumnShareOfMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.calculate_value_for_test)

            - [`TestColumnShareOfMissingValues.column_name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.column_name)

            - [`TestColumnShareOfMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.condition)

            - [`TestColumnShareOfMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.get_condition)

            - [`TestColumnShareOfMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.get_description)

            - [`TestColumnShareOfMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.metric)

            - [`TestColumnShareOfMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.name)

            - [`TestColumnShareOfMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues.value)

        - [`TestColumnShareOfMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValuesRenderer)

            - [`TestColumnShareOfMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValuesRenderer.color_options)

            - [`TestColumnShareOfMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnShareOfMissingValuesRenderer.render_json)

        - [`TestColumnValueRegExp`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp)

            - [`TestColumnValueRegExp.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.calculate_value_for_test)

            - [`TestColumnValueRegExp.column_name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.column_name)

            - [`TestColumnValueRegExp.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.get_condition)

            - [`TestColumnValueRegExp.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.get_description)

            - [`TestColumnValueRegExp.group`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.group)

            - [`TestColumnValueRegExp.groups()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.groups)

            - [`TestColumnValueRegExp.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.metric)

            - [`TestColumnValueRegExp.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExp.name)

        - [`TestColumnValueRegExpRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExpRenderer)

            - [`TestColumnValueRegExpRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExpRenderer.color_options)

            - [`TestColumnValueRegExpRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnValueRegExpRenderer.render_html)

        - [`TestColumnsType`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType)

            - [`TestColumnsType.Result`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.Result)

            - [`TestColumnsType.check()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.check)

            - [`TestColumnsType.columns_type`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.columns_type)

            - [`TestColumnsType.group`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.group)

            - [`TestColumnsType.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.metric)

            - [`TestColumnsType.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsType.name)

        - [`TestColumnsTypeRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsTypeRenderer)

            - [`TestColumnsTypeRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsTypeRenderer.color_options)

            - [`TestColumnsTypeRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsTypeRenderer.render_html)

            - [`TestColumnsTypeRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestColumnsTypeRenderer.render_json)

        - [`TestNumberOfColumns`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns)

            - [`TestNumberOfColumns.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.calculate_value_for_test)

            - [`TestNumberOfColumns.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.condition)

            - [`TestNumberOfColumns.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.get_condition)

            - [`TestNumberOfColumns.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.get_description)

            - [`TestNumberOfColumns.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.metric)

            - [`TestNumberOfColumns.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.name)

            - [`TestNumberOfColumns.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumns.value)

        - [`TestNumberOfColumnsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer)

            - [`TestNumberOfColumnsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer.color_options)

            - [`TestNumberOfColumnsRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer.render_html)

            - [`TestNumberOfColumnsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer.render_json)

        - [`TestNumberOfColumnsWithMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues)

            - [`TestNumberOfColumnsWithMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.calculate_value_for_test)

            - [`TestNumberOfColumnsWithMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.condition)

            - [`TestNumberOfColumnsWithMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.get_condition)

            - [`TestNumberOfColumnsWithMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.get_description)

            - [`TestNumberOfColumnsWithMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.metric)

            - [`TestNumberOfColumnsWithMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.name)

            - [`TestNumberOfColumnsWithMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues.value)

        - [`TestNumberOfColumnsWithMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer)

            - [`TestNumberOfColumnsWithMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer.color_options)

            - [`TestNumberOfColumnsWithMissingValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer.render_html)

            - [`TestNumberOfColumnsWithMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer.render_json)

        - [`TestNumberOfConstantColumns`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns)

            - [`TestNumberOfConstantColumns.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.calculate_value_for_test)

            - [`TestNumberOfConstantColumns.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.condition)

            - [`TestNumberOfConstantColumns.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.get_condition)

            - [`TestNumberOfConstantColumns.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.get_description)

            - [`TestNumberOfConstantColumns.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.metric)

            - [`TestNumberOfConstantColumns.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.name)

            - [`TestNumberOfConstantColumns.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumns.value)

        - [`TestNumberOfConstantColumnsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer)

            - [`TestNumberOfConstantColumnsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer.color_options)

            - [`TestNumberOfConstantColumnsRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer.render_html)

            - [`TestNumberOfConstantColumnsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer.render_json)

        - [`TestNumberOfDifferentMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues)

            - [`TestNumberOfDifferentMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.calculate_value_for_test)

            - [`TestNumberOfDifferentMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.condition)

            - [`TestNumberOfDifferentMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.get_condition)

            - [`TestNumberOfDifferentMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.get_description)

            - [`TestNumberOfDifferentMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.metric)

            - [`TestNumberOfDifferentMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.name)

            - [`TestNumberOfDifferentMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues.value)

        - [`TestNumberOfDifferentMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer)

            - [`TestNumberOfDifferentMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer.color_options)

            - [`TestNumberOfDifferentMissingValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer.render_html)

            - [`TestNumberOfDifferentMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer.render_json)

        - [`TestNumberOfDuplicatedColumns`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns)

            - [`TestNumberOfDuplicatedColumns.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.calculate_value_for_test)

            - [`TestNumberOfDuplicatedColumns.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.condition)

            - [`TestNumberOfDuplicatedColumns.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.get_condition)

            - [`TestNumberOfDuplicatedColumns.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.get_description)

            - [`TestNumberOfDuplicatedColumns.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.metric)

            - [`TestNumberOfDuplicatedColumns.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.name)

            - [`TestNumberOfDuplicatedColumns.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns.value)

        - [`TestNumberOfDuplicatedColumnsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumnsRenderer)

            - [`TestNumberOfDuplicatedColumnsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumnsRenderer.color_options)

            - [`TestNumberOfDuplicatedColumnsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumnsRenderer.render_json)

        - [`TestNumberOfDuplicatedRows`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows)

            - [`TestNumberOfDuplicatedRows.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.calculate_value_for_test)

            - [`TestNumberOfDuplicatedRows.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.condition)

            - [`TestNumberOfDuplicatedRows.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.get_condition)

            - [`TestNumberOfDuplicatedRows.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.get_description)

            - [`TestNumberOfDuplicatedRows.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.metric)

            - [`TestNumberOfDuplicatedRows.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.name)

            - [`TestNumberOfDuplicatedRows.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows.value)

        - [`TestNumberOfDuplicatedRowsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRowsRenderer)

            - [`TestNumberOfDuplicatedRowsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRowsRenderer.color_options)

            - [`TestNumberOfDuplicatedRowsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRowsRenderer.render_json)

        - [`TestNumberOfEmptyColumns`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns)

            - [`TestNumberOfEmptyColumns.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.calculate_value_for_test)

            - [`TestNumberOfEmptyColumns.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.condition)

            - [`TestNumberOfEmptyColumns.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.get_condition)

            - [`TestNumberOfEmptyColumns.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.get_description)

            - [`TestNumberOfEmptyColumns.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.metric)

            - [`TestNumberOfEmptyColumns.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.name)

            - [`TestNumberOfEmptyColumns.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns.value)

        - [`TestNumberOfEmptyColumnsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumnsRenderer)

            - [`TestNumberOfEmptyColumnsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumnsRenderer.color_options)

            - [`TestNumberOfEmptyColumnsRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyColumnsRenderer.render_html)

        - [`TestNumberOfEmptyRows`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows)

            - [`TestNumberOfEmptyRows.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.calculate_value_for_test)

            - [`TestNumberOfEmptyRows.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.condition)

            - [`TestNumberOfEmptyRows.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.get_condition)

            - [`TestNumberOfEmptyRows.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.get_description)

            - [`TestNumberOfEmptyRows.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.metric)

            - [`TestNumberOfEmptyRows.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.name)

            - [`TestNumberOfEmptyRows.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfEmptyRows.value)

        - [`TestNumberOfMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues)

            - [`TestNumberOfMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.calculate_value_for_test)

            - [`TestNumberOfMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.condition)

            - [`TestNumberOfMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.get_condition)

            - [`TestNumberOfMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.get_description)

            - [`TestNumberOfMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.metric)

            - [`TestNumberOfMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.name)

            - [`TestNumberOfMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValues.value)

        - [`TestNumberOfMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer)

            - [`TestNumberOfMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer.color_options)

            - [`TestNumberOfMissingValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer.render_html)

            - [`TestNumberOfMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer.render_json)

        - [`TestNumberOfRows`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows)

            - [`TestNumberOfRows.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.calculate_value_for_test)

            - [`TestNumberOfRows.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.condition)

            - [`TestNumberOfRows.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.get_condition)

            - [`TestNumberOfRows.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.get_description)

            - [`TestNumberOfRows.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.metric)

            - [`TestNumberOfRows.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.name)

            - [`TestNumberOfRows.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRows.value)

        - [`TestNumberOfRowsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsRenderer)

            - [`TestNumberOfRowsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsRenderer.color_options)

            - [`TestNumberOfRowsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsRenderer.render_json)

        - [`TestNumberOfRowsWithMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues)

            - [`TestNumberOfRowsWithMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.calculate_value_for_test)

            - [`TestNumberOfRowsWithMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.condition)

            - [`TestNumberOfRowsWithMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.get_condition)

            - [`TestNumberOfRowsWithMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.get_description)

            - [`TestNumberOfRowsWithMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.metric)

            - [`TestNumberOfRowsWithMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.name)

            - [`TestNumberOfRowsWithMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues.value)

        - [`TestNumberOfRowsWithMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValuesRenderer)

            - [`TestNumberOfRowsWithMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValuesRenderer.color_options)

            - [`TestNumberOfRowsWithMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValuesRenderer.render_json)

        - [`TestShareOfColumnsWithMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues)

            - [`TestShareOfColumnsWithMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.calculate_value_for_test)

            - [`TestShareOfColumnsWithMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.condition)

            - [`TestShareOfColumnsWithMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.get_condition)

            - [`TestShareOfColumnsWithMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.get_description)

            - [`TestShareOfColumnsWithMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.metric)

            - [`TestShareOfColumnsWithMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.name)

            - [`TestShareOfColumnsWithMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues.value)

        - [`TestShareOfColumnsWithMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer)

            - [`TestShareOfColumnsWithMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer.color_options)

            - [`TestShareOfColumnsWithMissingValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer.render_html)

            - [`TestShareOfColumnsWithMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer.render_json)

        - [`TestShareOfMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues)

            - [`TestShareOfMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.calculate_value_for_test)

            - [`TestShareOfMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.condition)

            - [`TestShareOfMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.get_condition)

            - [`TestShareOfMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.get_description)

            - [`TestShareOfMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.metric)

            - [`TestShareOfMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.name)

            - [`TestShareOfMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValues.value)

        - [`TestShareOfMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer)

            - [`TestShareOfMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer.color_options)

            - [`TestShareOfMissingValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer.render_html)

            - [`TestShareOfMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer.render_json)

        - [`TestShareOfRowsWithMissingValues`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues)

            - [`TestShareOfRowsWithMissingValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.calculate_value_for_test)

            - [`TestShareOfRowsWithMissingValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.condition)

            - [`TestShareOfRowsWithMissingValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.get_condition)

            - [`TestShareOfRowsWithMissingValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.get_description)

            - [`TestShareOfRowsWithMissingValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.metric)

            - [`TestShareOfRowsWithMissingValues.name`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.name)

            - [`TestShareOfRowsWithMissingValues.value`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues.value)

        - [`TestShareOfRowsWithMissingValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValuesRenderer)

            - [`TestShareOfRowsWithMissingValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValuesRenderer.color_options)

            - [`TestShareOfRowsWithMissingValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValuesRenderer.render_json)

    - [evidently.tests.data_quality_tests module](api-reference/evidently.tests.md#module-evidently.tests.data_quality_tests)

        - [`BaseDataQualityCorrelationsMetricsValueTest`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest)

            - [`BaseDataQualityCorrelationsMetricsValueTest.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest.group)

            - [`BaseDataQualityCorrelationsMetricsValueTest.method`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest.method)

            - [`BaseDataQualityCorrelationsMetricsValueTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest.metric)

        - [`BaseDataQualityMetricsValueTest`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityMetricsValueTest)

            - [`BaseDataQualityMetricsValueTest.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityMetricsValueTest.group)

            - [`BaseDataQualityMetricsValueTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityMetricsValueTest.metric)

        - [`BaseDataQualityValueListMetricsTest`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest)

            - [`BaseDataQualityValueListMetricsTest.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.column_name)

            - [`BaseDataQualityValueListMetricsTest.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.group)

            - [`BaseDataQualityValueListMetricsTest.groups()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.groups)

            - [`BaseDataQualityValueListMetricsTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.metric)

            - [`BaseDataQualityValueListMetricsTest.values`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest.values)

        - [`BaseDataQualityValueRangeMetricsTest`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest)

            - [`BaseDataQualityValueRangeMetricsTest.column`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.column)

            - [`BaseDataQualityValueRangeMetricsTest.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.group)

            - [`BaseDataQualityValueRangeMetricsTest.groups()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.groups)

            - [`BaseDataQualityValueRangeMetricsTest.left`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.left)

            - [`BaseDataQualityValueRangeMetricsTest.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.metric)

            - [`BaseDataQualityValueRangeMetricsTest.right`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest.right)

        - [`BaseFeatureDataQualityMetricsTest`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest)

            - [`BaseFeatureDataQualityMetricsTest.check()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest.check)

            - [`BaseFeatureDataQualityMetricsTest.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest.column_name)

            - [`BaseFeatureDataQualityMetricsTest.groups()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest.groups)

        - [`TestAllColumnsMostCommonValueShare`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestAllColumnsMostCommonValueShare)

            - [`TestAllColumnsMostCommonValueShare.generate()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestAllColumnsMostCommonValueShare.generate)

        - [`TestCatColumnsOutOfListValues`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCatColumnsOutOfListValues)

            - [`TestCatColumnsOutOfListValues.generate()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCatColumnsOutOfListValues.generate)

        - [`TestColumnValueMax`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax)

            - [`TestColumnValueMax.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.calculate_value_for_test)

            - [`TestColumnValueMax.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.column_name)

            - [`TestColumnValueMax.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.condition)

            - [`TestColumnValueMax.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.get_condition)

            - [`TestColumnValueMax.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.get_description)

            - [`TestColumnValueMax.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.metric)

            - [`TestColumnValueMax.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.name)

            - [`TestColumnValueMax.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMax.value)

        - [`TestColumnValueMaxRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMaxRenderer)

            - [`TestColumnValueMaxRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMaxRenderer.color_options)

            - [`TestColumnValueMaxRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMaxRenderer.render_html)

        - [`TestColumnValueMean`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean)

            - [`TestColumnValueMean.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.calculate_value_for_test)

            - [`TestColumnValueMean.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.column_name)

            - [`TestColumnValueMean.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.condition)

            - [`TestColumnValueMean.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.get_condition)

            - [`TestColumnValueMean.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.get_description)

            - [`TestColumnValueMean.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.metric)

            - [`TestColumnValueMean.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.name)

            - [`TestColumnValueMean.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMean.value)

        - [`TestColumnValueMeanRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMeanRenderer)

            - [`TestColumnValueMeanRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMeanRenderer.color_options)

            - [`TestColumnValueMeanRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMeanRenderer.render_html)

        - [`TestColumnValueMedian`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian)

            - [`TestColumnValueMedian.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.calculate_value_for_test)

            - [`TestColumnValueMedian.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.column_name)

            - [`TestColumnValueMedian.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.condition)

            - [`TestColumnValueMedian.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.get_condition)

            - [`TestColumnValueMedian.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.get_description)

            - [`TestColumnValueMedian.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.metric)

            - [`TestColumnValueMedian.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.name)

            - [`TestColumnValueMedian.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedian.value)

        - [`TestColumnValueMedianRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedianRenderer)

            - [`TestColumnValueMedianRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedianRenderer.color_options)

            - [`TestColumnValueMedianRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMedianRenderer.render_html)

        - [`TestColumnValueMin`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin)

            - [`TestColumnValueMin.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.calculate_value_for_test)

            - [`TestColumnValueMin.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.column_name)

            - [`TestColumnValueMin.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.condition)

            - [`TestColumnValueMin.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.get_condition)

            - [`TestColumnValueMin.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.get_description)

            - [`TestColumnValueMin.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.metric)

            - [`TestColumnValueMin.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.name)

            - [`TestColumnValueMin.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMin.value)

        - [`TestColumnValueMinRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMinRenderer)

            - [`TestColumnValueMinRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMinRenderer.color_options)

            - [`TestColumnValueMinRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueMinRenderer.render_html)

        - [`TestColumnValueStd`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd)

            - [`TestColumnValueStd.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.calculate_value_for_test)

            - [`TestColumnValueStd.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.column_name)

            - [`TestColumnValueStd.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.condition)

            - [`TestColumnValueStd.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.get_condition)

            - [`TestColumnValueStd.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.get_description)

            - [`TestColumnValueStd.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.metric)

            - [`TestColumnValueStd.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.name)

            - [`TestColumnValueStd.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStd.value)

        - [`TestColumnValueStdRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStdRenderer)

            - [`TestColumnValueStdRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStdRenderer.color_options)

            - [`TestColumnValueStdRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestColumnValueStdRenderer.render_html)

        - [`TestConflictPrediction`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction)

            - [`TestConflictPrediction.check()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction.check)

            - [`TestConflictPrediction.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction.group)

            - [`TestConflictPrediction.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction.metric)

            - [`TestConflictPrediction.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictPrediction.name)

        - [`TestConflictTarget`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget)

            - [`TestConflictTarget.check()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget.check)

            - [`TestConflictTarget.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget.group)

            - [`TestConflictTarget.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget.metric)

            - [`TestConflictTarget.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestConflictTarget.name)

        - [`TestCorrelationChanges`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges)

            - [`TestCorrelationChanges.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.calculate_value_for_test)

            - [`TestCorrelationChanges.corr_diff`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.corr_diff)

            - [`TestCorrelationChanges.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.get_condition)

            - [`TestCorrelationChanges.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.get_description)

            - [`TestCorrelationChanges.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.group)

            - [`TestCorrelationChanges.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.metric)

            - [`TestCorrelationChanges.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChanges.name)

        - [`TestCorrelationChangesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChangesRenderer)

            - [`TestCorrelationChangesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChangesRenderer.color_options)

            - [`TestCorrelationChangesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestCorrelationChangesRenderer.render_html)

        - [`TestHighlyCorrelatedColumns`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns)

            - [`TestHighlyCorrelatedColumns.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.calculate_value_for_test)

            - [`TestHighlyCorrelatedColumns.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.condition)

            - [`TestHighlyCorrelatedColumns.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.get_condition)

            - [`TestHighlyCorrelatedColumns.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.get_description)

            - [`TestHighlyCorrelatedColumns.method`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.method)

            - [`TestHighlyCorrelatedColumns.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.metric)

            - [`TestHighlyCorrelatedColumns.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.name)

            - [`TestHighlyCorrelatedColumns.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns.value)

        - [`TestHighlyCorrelatedColumnsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer)

            - [`TestHighlyCorrelatedColumnsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer.color_options)

            - [`TestHighlyCorrelatedColumnsRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer.render_html)

            - [`TestHighlyCorrelatedColumnsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer.render_json)

        - [`TestMeanInNSigmas`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas)

            - [`TestMeanInNSigmas.check()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.check)

            - [`TestMeanInNSigmas.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.column_name)

            - [`TestMeanInNSigmas.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.group)

            - [`TestMeanInNSigmas.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.metric)

            - [`TestMeanInNSigmas.n_sigmas`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.n_sigmas)

            - [`TestMeanInNSigmas.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmas.name)

        - [`TestMeanInNSigmasRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer)

            - [`TestMeanInNSigmasRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer.color_options)

            - [`TestMeanInNSigmasRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer.render_html)

            - [`TestMeanInNSigmasRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer.render_json)

        - [`TestMostCommonValueShare`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare)

            - [`TestMostCommonValueShare.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.calculate_value_for_test)

            - [`TestMostCommonValueShare.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.column_name)

            - [`TestMostCommonValueShare.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.condition)

            - [`TestMostCommonValueShare.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.get_condition)

            - [`TestMostCommonValueShare.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.get_description)

            - [`TestMostCommonValueShare.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.metric)

            - [`TestMostCommonValueShare.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.name)

            - [`TestMostCommonValueShare.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShare.value)

        - [`TestMostCommonValueShareRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer)

            - [`TestMostCommonValueShareRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer.color_options)

            - [`TestMostCommonValueShareRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer.render_html)

            - [`TestMostCommonValueShareRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer.render_json)

        - [`TestNumColumnsMeanInNSigmas`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumColumnsMeanInNSigmas)

            - [`TestNumColumnsMeanInNSigmas.generate()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumColumnsMeanInNSigmas.generate)

        - [`TestNumColumnsOutOfRangeValues`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumColumnsOutOfRangeValues)

            - [`TestNumColumnsOutOfRangeValues.generate()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumColumnsOutOfRangeValues.generate)

        - [`TestNumberOfOutListValues`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues)

            - [`TestNumberOfOutListValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.calculate_value_for_test)

            - [`TestNumberOfOutListValues.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.column_name)

            - [`TestNumberOfOutListValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.condition)

            - [`TestNumberOfOutListValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.get_condition)

            - [`TestNumberOfOutListValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.get_description)

            - [`TestNumberOfOutListValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.metric)

            - [`TestNumberOfOutListValues.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.name)

            - [`TestNumberOfOutListValues.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.value)

            - [`TestNumberOfOutListValues.values`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValues.values)

        - [`TestNumberOfOutListValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValuesRenderer)

            - [`TestNumberOfOutListValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValuesRenderer.color_options)

            - [`TestNumberOfOutListValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutListValuesRenderer.render_html)

        - [`TestNumberOfOutRangeValues`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues)

            - [`TestNumberOfOutRangeValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.calculate_value_for_test)

            - [`TestNumberOfOutRangeValues.column`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.column)

            - [`TestNumberOfOutRangeValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.condition)

            - [`TestNumberOfOutRangeValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.get_condition)

            - [`TestNumberOfOutRangeValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.get_description)

            - [`TestNumberOfOutRangeValues.left`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.left)

            - [`TestNumberOfOutRangeValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.metric)

            - [`TestNumberOfOutRangeValues.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.name)

            - [`TestNumberOfOutRangeValues.right`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.right)

            - [`TestNumberOfOutRangeValues.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValues.value)

        - [`TestNumberOfOutRangeValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValuesRenderer)

            - [`TestNumberOfOutRangeValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValuesRenderer.color_options)

            - [`TestNumberOfOutRangeValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfOutRangeValuesRenderer.render_html)

        - [`TestNumberOfUniqueValues`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues)

            - [`TestNumberOfUniqueValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.calculate_value_for_test)

            - [`TestNumberOfUniqueValues.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.column_name)

            - [`TestNumberOfUniqueValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.condition)

            - [`TestNumberOfUniqueValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.get_condition)

            - [`TestNumberOfUniqueValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.get_description)

            - [`TestNumberOfUniqueValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.metric)

            - [`TestNumberOfUniqueValues.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.name)

            - [`TestNumberOfUniqueValues.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValues.value)

        - [`TestNumberOfUniqueValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValuesRenderer)

            - [`TestNumberOfUniqueValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValuesRenderer.color_options)

            - [`TestNumberOfUniqueValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestNumberOfUniqueValuesRenderer.render_html)

        - [`TestPredictionFeaturesCorrelations`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations)

            - [`TestPredictionFeaturesCorrelations.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.calculate_value_for_test)

            - [`TestPredictionFeaturesCorrelations.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.condition)

            - [`TestPredictionFeaturesCorrelations.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.get_condition)

            - [`TestPredictionFeaturesCorrelations.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.get_description)

            - [`TestPredictionFeaturesCorrelations.method`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.method)

            - [`TestPredictionFeaturesCorrelations.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.metric)

            - [`TestPredictionFeaturesCorrelations.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.name)

            - [`TestPredictionFeaturesCorrelations.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations.value)

        - [`TestPredictionFeaturesCorrelationsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer)

            - [`TestPredictionFeaturesCorrelationsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer.color_options)

            - [`TestPredictionFeaturesCorrelationsRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer.render_html)

            - [`TestPredictionFeaturesCorrelationsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer.render_json)

        - [`TestShareOfOutListValues`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues)

            - [`TestShareOfOutListValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.calculate_value_for_test)

            - [`TestShareOfOutListValues.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.column_name)

            - [`TestShareOfOutListValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.condition)

            - [`TestShareOfOutListValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.get_condition)

            - [`TestShareOfOutListValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.get_description)

            - [`TestShareOfOutListValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.metric)

            - [`TestShareOfOutListValues.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.name)

            - [`TestShareOfOutListValues.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.value)

            - [`TestShareOfOutListValues.values`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValues.values)

        - [`TestShareOfOutListValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer)

            - [`TestShareOfOutListValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer.color_options)

            - [`TestShareOfOutListValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer.render_html)

            - [`TestShareOfOutListValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer.render_json)

        - [`TestShareOfOutRangeValues`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues)

            - [`TestShareOfOutRangeValues.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.calculate_value_for_test)

            - [`TestShareOfOutRangeValues.column`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.column)

            - [`TestShareOfOutRangeValues.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.condition)

            - [`TestShareOfOutRangeValues.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.get_condition)

            - [`TestShareOfOutRangeValues.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.get_description)

            - [`TestShareOfOutRangeValues.left`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.left)

            - [`TestShareOfOutRangeValues.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.metric)

            - [`TestShareOfOutRangeValues.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.name)

            - [`TestShareOfOutRangeValues.right`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.right)

            - [`TestShareOfOutRangeValues.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValues.value)

        - [`TestShareOfOutRangeValuesRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer)

            - [`TestShareOfOutRangeValuesRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer.color_options)

            - [`TestShareOfOutRangeValuesRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer.render_html)

            - [`TestShareOfOutRangeValuesRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer.render_json)

        - [`TestTargetFeaturesCorrelations`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations)

            - [`TestTargetFeaturesCorrelations.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.calculate_value_for_test)

            - [`TestTargetFeaturesCorrelations.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.condition)

            - [`TestTargetFeaturesCorrelations.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.get_condition)

            - [`TestTargetFeaturesCorrelations.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.get_description)

            - [`TestTargetFeaturesCorrelations.method`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.method)

            - [`TestTargetFeaturesCorrelations.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.metric)

            - [`TestTargetFeaturesCorrelations.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.name)

            - [`TestTargetFeaturesCorrelations.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations.value)

        - [`TestTargetFeaturesCorrelationsRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer)

            - [`TestTargetFeaturesCorrelationsRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer.color_options)

            - [`TestTargetFeaturesCorrelationsRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer.render_html)

            - [`TestTargetFeaturesCorrelationsRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer.render_json)

        - [`TestTargetPredictionCorrelation`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation)

            - [`TestTargetPredictionCorrelation.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.calculate_value_for_test)

            - [`TestTargetPredictionCorrelation.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.condition)

            - [`TestTargetPredictionCorrelation.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.get_condition)

            - [`TestTargetPredictionCorrelation.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.get_description)

            - [`TestTargetPredictionCorrelation.method`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.method)

            - [`TestTargetPredictionCorrelation.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.metric)

            - [`TestTargetPredictionCorrelation.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.name)

            - [`TestTargetPredictionCorrelation.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestTargetPredictionCorrelation.value)

        - [`TestUniqueValuesShare`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare)

            - [`TestUniqueValuesShare.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.calculate_value_for_test)

            - [`TestUniqueValuesShare.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.column_name)

            - [`TestUniqueValuesShare.condition`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.condition)

            - [`TestUniqueValuesShare.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.get_condition)

            - [`TestUniqueValuesShare.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.get_description)

            - [`TestUniqueValuesShare.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.metric)

            - [`TestUniqueValuesShare.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.name)

            - [`TestUniqueValuesShare.value`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShare.value)

        - [`TestUniqueValuesShareRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShareRenderer)

            - [`TestUniqueValuesShareRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShareRenderer.color_options)

            - [`TestUniqueValuesShareRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestUniqueValuesShareRenderer.render_html)

        - [`TestValueList`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueList)

            - [`TestValueList.check()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.check)

            - [`TestValueList.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.column_name)

            - [`TestValueList.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.group)

            - [`TestValueList.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.metric)

            - [`TestValueList.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.name)

            - [`TestValueList.values`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueList.values)

        - [`TestValueListRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueListRenderer)

            - [`TestValueListRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueListRenderer.color_options)

            - [`TestValueListRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueListRenderer.render_html)

            - [`TestValueListRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueListRenderer.render_json)

        - [`TestValueQuantile`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile)

            - [`TestValueQuantile.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.calculate_value_for_test)

            - [`TestValueQuantile.column_name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.column_name)

            - [`TestValueQuantile.get_condition()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.get_condition)

            - [`TestValueQuantile.get_description()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.get_description)

            - [`TestValueQuantile.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.group)

            - [`TestValueQuantile.groups()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.groups)

            - [`TestValueQuantile.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.metric)

            - [`TestValueQuantile.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.name)

            - [`TestValueQuantile.quantile`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantile.quantile)

        - [`TestValueQuantileRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantileRenderer)

            - [`TestValueQuantileRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantileRenderer.color_options)

            - [`TestValueQuantileRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueQuantileRenderer.render_html)

        - [`TestValueRange`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange)

            - [`TestValueRange.check()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.check)

            - [`TestValueRange.column`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.column)

            - [`TestValueRange.group`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.group)

            - [`TestValueRange.left`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.left)

            - [`TestValueRange.metric`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.metric)

            - [`TestValueRange.name`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.name)

            - [`TestValueRange.right`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRange.right)

        - [`TestValueRangeRenderer`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRangeRenderer)

            - [`TestValueRangeRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRangeRenderer.color_options)

            - [`TestValueRangeRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.data_quality_tests.TestValueRangeRenderer.render_html)

    - [evidently.tests.regression_performance_tests module](api-reference/evidently.tests.md#module-evidently.tests.regression_performance_tests)

        - [`BaseRegressionPerformanceMetricsTest`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.BaseRegressionPerformanceMetricsTest)

            - [`BaseRegressionPerformanceMetricsTest.group`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.BaseRegressionPerformanceMetricsTest.group)

            - [`BaseRegressionPerformanceMetricsTest.metric`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.BaseRegressionPerformanceMetricsTest.metric)

        - [`TestValueAbsMaxError`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError)

            - [`TestValueAbsMaxError.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.calculate_value_for_test)

            - [`TestValueAbsMaxError.condition`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.condition)

            - [`TestValueAbsMaxError.get_condition()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.get_condition)

            - [`TestValueAbsMaxError.get_description()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.get_description)

            - [`TestValueAbsMaxError.metric`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.metric)

            - [`TestValueAbsMaxError.name`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.name)

            - [`TestValueAbsMaxError.value`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxError.value)

        - [`TestValueAbsMaxErrorRenderer`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer)

            - [`TestValueAbsMaxErrorRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer.color_options)

            - [`TestValueAbsMaxErrorRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer.render_html)

            - [`TestValueAbsMaxErrorRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer.render_json)

        - [`TestValueMAE`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE)

            - [`TestValueMAE.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.calculate_value_for_test)

            - [`TestValueMAE.condition`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.condition)

            - [`TestValueMAE.get_condition()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.get_condition)

            - [`TestValueMAE.get_description()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.get_description)

            - [`TestValueMAE.metric`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.metric)

            - [`TestValueMAE.name`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.name)

            - [`TestValueMAE.value`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAE.value)

        - [`TestValueMAERenderer`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAERenderer)

            - [`TestValueMAERenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAERenderer.color_options)

            - [`TestValueMAERenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAERenderer.render_html)

            - [`TestValueMAERenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAERenderer.render_json)

        - [`TestValueMAPE`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE)

            - [`TestValueMAPE.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.calculate_value_for_test)

            - [`TestValueMAPE.condition`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.condition)

            - [`TestValueMAPE.get_condition()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.get_condition)

            - [`TestValueMAPE.get_description()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.get_description)

            - [`TestValueMAPE.metric`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.metric)

            - [`TestValueMAPE.name`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.name)

            - [`TestValueMAPE.value`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPE.value)

        - [`TestValueMAPERenderer`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPERenderer)

            - [`TestValueMAPERenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPERenderer.color_options)

            - [`TestValueMAPERenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPERenderer.render_html)

            - [`TestValueMAPERenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMAPERenderer.render_json)

        - [`TestValueMeanError`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError)

            - [`TestValueMeanError.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.calculate_value_for_test)

            - [`TestValueMeanError.condition`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.condition)

            - [`TestValueMeanError.get_condition()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.get_condition)

            - [`TestValueMeanError.get_description()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.get_description)

            - [`TestValueMeanError.metric`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.metric)

            - [`TestValueMeanError.name`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.name)

            - [`TestValueMeanError.value`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanError.value)

        - [`TestValueMeanErrorRenderer`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer)

            - [`TestValueMeanErrorRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer.color_options)

            - [`TestValueMeanErrorRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer.render_html)

            - [`TestValueMeanErrorRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer.render_json)

        - [`TestValueR2Score`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score)

            - [`TestValueR2Score.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.calculate_value_for_test)

            - [`TestValueR2Score.condition`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.condition)

            - [`TestValueR2Score.get_condition()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.get_condition)

            - [`TestValueR2Score.get_description()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.get_description)

            - [`TestValueR2Score.metric`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.metric)

            - [`TestValueR2Score.name`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.name)

            - [`TestValueR2Score.value`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2Score.value)

        - [`TestValueR2ScoreRenderer`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer)

            - [`TestValueR2ScoreRenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer.color_options)

            - [`TestValueR2ScoreRenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer.render_html)

            - [`TestValueR2ScoreRenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer.render_json)

        - [`TestValueRMSE`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE)

            - [`TestValueRMSE.calculate_value_for_test()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.calculate_value_for_test)

            - [`TestValueRMSE.condition`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.condition)

            - [`TestValueRMSE.get_condition()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.get_condition)

            - [`TestValueRMSE.get_description()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.get_description)

            - [`TestValueRMSE.metric`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.metric)

            - [`TestValueRMSE.name`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.name)

            - [`TestValueRMSE.value`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSE.value)

        - [`TestValueRMSERenderer`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSERenderer)

            - [`TestValueRMSERenderer.color_options`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSERenderer.color_options)

            - [`TestValueRMSERenderer.render_html()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSERenderer.render_html)

            - [`TestValueRMSERenderer.render_json()`](api-reference/evidently.tests.md#evidently.tests.regression_performance_tests.TestValueRMSERenderer.render_json)

    - [evidently.tests.utils module](api-reference/evidently.tests.md#module-evidently.tests.utils)

        - [`approx()`](api-reference/evidently.tests.md#evidently.tests.utils.approx)

        - [`dataframes_to_table()`](api-reference/evidently.tests.md#evidently.tests.utils.dataframes_to_table)

        - [`plot_boxes()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_boxes)

        - [`plot_check()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_check)

        - [`plot_conf_mtrx()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_conf_mtrx)

        - [`plot_correlations()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_correlations)

        - [`plot_dicts_to_table()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_dicts_to_table)

        - [`plot_metric_value()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_metric_value)

        - [`plot_rates()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_rates)

        - [`plot_roc_auc()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_roc_auc)

        - [`plot_value_counts_tables()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_value_counts_tables)

        - [`plot_value_counts_tables_ref_curr()`](api-reference/evidently.tests.md#evidently.tests.utils.plot_value_counts_tables_ref_curr)

        - [`regression_perf_plot()`](api-reference/evidently.tests.md#evidently.tests.utils.regression_perf_plot)

    - [Module contents](api-reference/evidently.tests.md#module-evidently.tests)

- [evidently.utils package](evidently.utils.md)

    - [Submodules](api-reference/evidently.utils.md#submodules)

    - [evidently.utils.data_operations module](api-reference/evidently.utils.md#module-evidently.utils.data_operations)

        - [`DatasetColumns`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns)

            - [`DatasetColumns.as_dict()`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.as_dict)

            - [`DatasetColumns.cat_feature_names`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.cat_feature_names)

            - [`DatasetColumns.datetime_feature_names`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.datetime_feature_names)

            - [`DatasetColumns.get_all_columns_list()`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.get_all_columns_list)

            - [`DatasetColumns.get_all_features_list()`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.get_all_features_list)

            - [`DatasetColumns.get_features_len()`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.get_features_len)

            - [`DatasetColumns.num_feature_names`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.num_feature_names)

            - [`DatasetColumns.target_names`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.target_names)

            - [`DatasetColumns.target_type`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.target_type)

            - [`DatasetColumns.task`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.task)

            - [`DatasetColumns.utility_columns`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetColumns.utility_columns)

        - [`DatasetUtilityColumns`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns)

            - [`DatasetUtilityColumns.as_dict()`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.as_dict)

            - [`DatasetUtilityColumns.date`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.date)

            - [`DatasetUtilityColumns.id_column`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.id_column)

            - [`DatasetUtilityColumns.prediction`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.prediction)

            - [`DatasetUtilityColumns.target`](api-reference/evidently.utils.md#evidently.utils.data_operations.DatasetUtilityColumns.target)

        - [`process_columns()`](api-reference/evidently.utils.md#evidently.utils.data_operations.process_columns)

        - [`recognize_column_type()`](api-reference/evidently.utils.md#evidently.utils.data_operations.recognize_column_type)

        - [`recognize_task()`](api-reference/evidently.utils.md#evidently.utils.data_operations.recognize_task)

        - [`replace_infinity_values_to_nan()`](api-reference/evidently.utils.md#evidently.utils.data_operations.replace_infinity_values_to_nan)

    - [evidently.utils.data_preprocessing module](api-reference/evidently.utils.md#module-evidently.utils.data_preprocessing)

        - [`ColumnDefinition`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnDefinition)

            - [`ColumnDefinition.column_name`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnDefinition.column_name)

            - [`ColumnDefinition.column_type`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnDefinition.column_type)

        - [`ColumnPresenceState`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnPresenceState)

            - [`ColumnPresenceState.Missing`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnPresenceState.Missing)

            - [`ColumnPresenceState.Partially`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnPresenceState.Partially)

            - [`ColumnPresenceState.Present`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnPresenceState.Present)

        - [`ColumnType`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnType)

            - [`ColumnType.Categorical`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnType.Categorical)

            - [`ColumnType.Datetime`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnType.Datetime)

            - [`ColumnType.Numerical`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.ColumnType.Numerical)

        - [`DataDefinition`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition)

            - [`DataDefinition.classification_labels()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.classification_labels)

            - [`DataDefinition.get_columns()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_columns)

            - [`DataDefinition.get_datetime_column()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_datetime_column)

            - [`DataDefinition.get_id_column()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_id_column)

            - [`DataDefinition.get_prediction_columns()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_prediction_columns)

            - [`DataDefinition.get_target_column()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.get_target_column)

            - [`DataDefinition.task()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.DataDefinition.task)

        - [`PredictionColumns`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.PredictionColumns)

            - [`PredictionColumns.get_columns_list()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.PredictionColumns.get_columns_list)

            - [`PredictionColumns.predicted_values`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.PredictionColumns.predicted_values)

            - [`PredictionColumns.prediction_probas`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.PredictionColumns.prediction_probas)

        - [`create_data_definition()`](api-reference/evidently.utils.md#evidently.utils.data_preprocessing.create_data_definition)

    - [evidently.utils.generators module](api-reference/evidently.utils.md#module-evidently.utils.generators)

        - [`BaseGenerator`](api-reference/evidently.utils.md#evidently.utils.generators.BaseGenerator)

            - [`BaseGenerator.generate()`](api-reference/evidently.utils.md#evidently.utils.generators.BaseGenerator.generate)

        - [`make_generator_by_columns()`](api-reference/evidently.utils.md#evidently.utils.generators.make_generator_by_columns)

    - [evidently.utils.numpy_encoder module](api-reference/evidently.utils.md#module-evidently.utils.numpy_encoder)

        - [`NumpyEncoder`](api-reference/evidently.utils.md#evidently.utils.numpy_encoder.NumpyEncoder)

            - [`NumpyEncoder.default()`](api-reference/evidently.utils.md#evidently.utils.numpy_encoder.NumpyEncoder.default)

    - [evidently.utils.types module](api-reference/evidently.utils.md#module-evidently.utils.types)

        - [`ApproxValue`](api-reference/evidently.utils.md#evidently.utils.types.ApproxValue)

            - [`ApproxValue.DEFAULT_ABSOLUTE`](api-reference/evidently.utils.md#evidently.utils.types.ApproxValue.DEFAULT_ABSOLUTE)

            - [`ApproxValue.DEFAULT_RELATIVE`](api-reference/evidently.utils.md#evidently.utils.types.ApproxValue.DEFAULT_RELATIVE)

            - [`ApproxValue.as_dict()`](api-reference/evidently.utils.md#evidently.utils.types.ApproxValue.as_dict)

            - [`ApproxValue.tolerance`](api-reference/evidently.utils.md#evidently.utils.types.ApproxValue.tolerance)

            - [`ApproxValue.value`](api-reference/evidently.utils.md#evidently.utils.types.ApproxValue.value)

    - [evidently.utils.visualizations module](api-reference/evidently.utils.md#module-evidently.utils.visualizations)

        - [`Distribution`](api-reference/evidently.utils.md#evidently.utils.visualizations.Distribution)

            - [`Distribution.x`](api-reference/evidently.utils.md#evidently.utils.visualizations.Distribution.x)

            - [`Distribution.y`](api-reference/evidently.utils.md#evidently.utils.visualizations.Distribution.y)

        - [`get_distribution_for_category_column()`](api-reference/evidently.utils.md#evidently.utils.visualizations.get_distribution_for_category_column)

        - [`get_distribution_for_column()`](api-reference/evidently.utils.md#evidently.utils.visualizations.get_distribution_for_column)

        - [`get_distribution_for_numerical_column()`](api-reference/evidently.utils.md#evidently.utils.visualizations.get_distribution_for_numerical_column)

        - [`make_hist_df()`](api-reference/evidently.utils.md#evidently.utils.visualizations.make_hist_df)

        - [`make_hist_for_cat_plot()`](api-reference/evidently.utils.md#evidently.utils.visualizations.make_hist_for_cat_plot)

        - [`make_hist_for_num_plot()`](api-reference/evidently.utils.md#evidently.utils.visualizations.make_hist_for_num_plot)

        - [`plot_boxes()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_boxes)

        - [`plot_cat_cat_rel()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_cat_cat_rel)

        - [`plot_cat_feature_in_time()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_cat_feature_in_time)

        - [`plot_conf_mtrx()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_conf_mtrx)

        - [`plot_distr()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_distr)

        - [`plot_distr_subplots()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_distr_subplots)

        - [`plot_distr_with_log_button()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_distr_with_log_button)

        - [`plot_error_bias_colored_scatter()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_error_bias_colored_scatter)

        - [`plot_line_in_time()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_line_in_time)

        - [`plot_num_feature_in_time()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_num_feature_in_time)

        - [`plot_num_num_rel()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_num_num_rel)

        - [`plot_pred_actual_time()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_pred_actual_time)

        - [`plot_scatter()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_scatter)

        - [`plot_scatter_for_data_drift()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_scatter_for_data_drift)

        - [`plot_time_feature_distr()`](api-reference/evidently.utils.md#evidently.utils.visualizations.plot_time_feature_distr)

    - [Module contents](api-reference/evidently.utils.md#module-evidently.utils)

- [evidently.widgets package](evidently.widgets.md)

    - [Module contents](api-reference/evidently.widgets.md#module-evidently.widgets)


## Module contents
