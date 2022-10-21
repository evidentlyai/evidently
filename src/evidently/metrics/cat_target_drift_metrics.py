#!/usr/bin/env python
# coding: utf-8
from typing import List
from typing import Optional
from typing import Sequence

import dataclasses
import pandas as pd
from dataclasses import dataclass

from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import ensure_prediction_column_is_string
from evidently.calculations.data_drift import get_one_column_drift
from evidently.calculations.data_quality import get_rows_count
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider
from evidently.options import QualityMetricsOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import HistogramData
from evidently.renderers.html_widgets import histogram
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import replace_infinity_values_to_nan
from evidently.utils.visualizations import make_hist_for_cat_plot


@dataclass
class CatTargetDriftAnalyzerResults:
    """Class for all results of category target drift calculations"""

    columns: DatasetColumns
    target_metrics: Optional[ColumnDataDriftMetrics] = None
    prediction_metrics: Optional[ColumnDataDriftMetrics] = None
    target_histogram_data: pd.Series = None
    prediction_histogram_data: pd.Series = None
    reference_data_count: int = 0
    current_data_count: int = 0


class CatTargetDriftMetrics(Metric[CatTargetDriftAnalyzerResults]):
    def __init__(
        self, options: Optional[DataDriftOptions] = None, quality_options: Optional[QualityMetricsOptions] = None
    ):
        if options is None:
            options = DataDriftOptions()
        if quality_options is None:
            quality_options = QualityMetricsOptions()
        self.options = options
        self.quality_options = quality_options

    def get_parameters(self) -> tuple:
        return ()

    def calculate(self, data: InputData) -> CatTargetDriftAnalyzerResults:
        """Calculate the target and prediction drifts.

        With default options, uses a chi² test when number of labels is greater than 2.
        Otherwise, uses a z-test.

        Notes:
            Be aware that any nan or infinity values will be dropped from the dataframes in place.

            You can also provide a custom function that computes a statistic by adding special
            `DataDriftOptions` object to the `option_provider` of the class.::

                options = DataDriftOptions(cat_target_stattest_func=...)
                analyzer.options_prover.add(options)

            Such a function takes two arguments:::

                def(reference_data: pd.Series, current_data: pd.Series):
                   ...

            and returns arbitrary number (like a p_value from the other tests ;-))
        Args:
            data: data for metric calculations.
        Returns:
            A dictionary that contains some meta information as well as `metrics` for either target or prediction
            columns or both. The `*_drift` column in `metrics` contains a computed p_value from tests.
        """
        if data.reference_data is None:
            raise ValueError("reference_data should be present")

        reference_data = data.reference_data.copy()

        if data.current_data is None:
            raise ValueError("current_data should be present")

        current_data = data.current_data.copy()
        provider = OptionsProvider()
        options = provider.get(DataDriftOptions)
        columns = process_columns(reference_data, data.column_mapping)
        target_column = columns.utility_columns.target

        if not isinstance(target_column, str) and isinstance(target_column, Sequence):
            raise ValueError("target should not be a sequence")

        classification_threshold = self.quality_options.classification_threshold
        prediction_column = ensure_prediction_column_is_string(
            prediction_column=columns.utility_columns.prediction,
            current_data=current_data,
            reference_data=reference_data,
            threshold=classification_threshold,
        )

        result = CatTargetDriftAnalyzerResults(
            columns=columns,
            reference_data_count=get_rows_count(reference_data),
            current_data_count=get_rows_count(current_data),
        )

        # consider replacing only values in target and prediction column
        reference_data = replace_infinity_values_to_nan(reference_data)
        current_data = replace_infinity_values_to_nan(current_data)

        if target_column is not None:
            result.target_metrics = get_one_column_drift(
                current_data=current_data,
                reference_data=reference_data,
                column_name=target_column,
                dataset_columns=columns,
                options=options,
                column_type="cat",
            )

            result.target_histogram_data = make_hist_for_cat_plot(
                current_data[target_column],
                reference_data[target_column] if reference_data is not None else None,
                normalize=True,
            )

        if prediction_column is not None:
            result.prediction_metrics = get_one_column_drift(
                current_data=current_data,
                reference_data=reference_data,
                column_name=prediction_column,
                dataset_columns=columns,
                options=options,
                column_type="cat",
            )
            result.prediction_histogram_data = make_hist_for_cat_plot(
                current_data[prediction_column],
                reference_data[prediction_column] if reference_data is not None else None,
                normalize=True,
            )
        return result


@default_renderer(wrap_type=CatTargetDriftMetrics)
class CatTargetDriftRenderer(MetricRenderer):
    def render_json(self, obj: CatTargetDriftMetrics) -> dict:
        return dataclasses.asdict(obj.get_result())

    def render_html(self, obj: CatTargetDriftMetrics) -> List[BaseWidgetInfo]:
        result = []
        target_metrics = obj.get_result().target_metrics
        if target_metrics is None:
            raise ValueError("no target column was provided")
        output_sim_test = "detected" if target_metrics.drift_detected else "not detected"
        result.append(
            _hist(
                obj.get_result().target_histogram_data,
                f"Target Drift: {output_sim_test},"
                f" drift score={round(target_metrics.drift_score, 6)}"
                f" ({target_metrics.stattest_name})",
            )
        )
        prediction_metrics = obj.get_result().prediction_metrics
        prediction_hist_data = obj.get_result().prediction_histogram_data
        if prediction_hist_data is not None and prediction_metrics is not None:
            output_sim_test = "detected" if prediction_metrics.drift_detected else "not detected"
            result.append(
                _hist(
                    prediction_hist_data,
                    f"Target Drift: {output_sim_test},"
                    f" drift score={round(prediction_metrics.drift_score, 6)}"
                    f" ({prediction_metrics.stattest_name})",
                )
            )

        return result


def _hist(histogram_data, title):
    curr_hist_data = histogram_data["current"]
    curr_hist = HistogramData(
        "current",
        curr_hist_data["x"],
        curr_hist_data["count"],
    )
    ref_hist_data = histogram_data.get("reference", None)
    ref_hist = None
    if ref_hist_data is not None:
        ref_hist = HistogramData(
            "reference",
            ref_hist_data["x"],
            ref_hist_data["count"],
        )
    return histogram(title=title, primary_hist=curr_hist, secondary_hist=ref_hist)
