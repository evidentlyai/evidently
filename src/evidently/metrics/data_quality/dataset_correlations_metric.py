import copy
import dataclasses
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd
from sympy import N

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.calculations.data_quality import calculate_correlations
from evidently.features.non_letter_character_percentage_feature import NonLetterCharacterPercentage
from evidently.features.OOV_words_percentage_feature import OOVWordsPercentage
from evidently.features.text_length_feature import TextLength
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import HeatmapData
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import get_heatmaps_widget
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import widget_tabs
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.data_preprocessing import ColumnType
from evidently.calculations.classification_performance import get_prediction_data


@dataclasses.dataclass
class CorrelationStats:
    target_prediction_correlation: Optional[float] = None
    abs_max_target_features_correlation: Optional[float] = None
    abs_max_prediction_features_correlation: Optional[float] = None
    abs_max_correlation: Optional[float] = None
    abs_max_features_correlation: Optional[float] = None


@dataclasses.dataclass
class DatasetCorrelation:
    correlation: Dict[str, pd.DataFrame]
    stats: Dict[str, CorrelationStats]
    correlations_calculate: Optional[Dict[str, pd.DataFrame]]


@dataclasses.dataclass
class DatasetCorrelationsMetricResult:
    current: DatasetCorrelation
    reference: Optional[DatasetCorrelation]
    target_correlation: Optional[str]
    prediction_labels_name: Optional[str]

import logging
class DatasetCorrelationsMetric(Metric[DatasetCorrelationsMetricResult]):
    """Calculate different correlations with target, predictions and features"""

    text_features_gen: Optional[
        Dict[str, Dict[str, Union[TextLength, NonLetterCharacterPercentage, OOVWordsPercentage]]]
    ]

    def __init__(self):
        self.text_features_gen = None

    def required_features(self, data_definition: DataDefinition):
        if len(data_definition.get_columns("text_features")) > 0:
            text_cols = [col.column_name for col in data_definition.get_columns("text_features")]
            text_features_gen = {}
            text_features_gen_result = []
            for col in text_cols:
                col_dict: Dict[str, Union[TextLength, NonLetterCharacterPercentage, OOVWordsPercentage]] = {}
                col_dict[f"{col}: Text Length"] = TextLength(col)
                col_dict[f"{col}: Non Letter Character %"] = NonLetterCharacterPercentage(col)
                col_dict[f"{col}: OOV %"] = OOVWordsPercentage(col)

                text_features_gen_result += [
                    col_dict[f"{col}: Text Length"],
                    col_dict[f"{col}: Non Letter Character %"],
                    col_dict[f"{col}: OOV %"],
                ]
                text_features_gen[col] = col_dict
            self.text_features_gen = text_features_gen

            return text_features_gen_result
        else:
            return []

    def get_parameters(self) -> tuple:
        return ()

    @staticmethod
    def _get_correlations_stats(correlation: pd.DataFrame, columns: DatasetColumns) -> CorrelationStats:
        correlation_matrix = correlation.copy()
        target_name = columns.utility_columns.target
        prediction_name = columns.utility_columns.prediction
        columns_corr = [i for i in correlation_matrix.columns if i not in [target_name, prediction_name]]
        # fill diagonal with 1 values for getting abs max values
        np.fill_diagonal(correlation_matrix.values, 0)

        if (
            isinstance(prediction_name, str)
            and prediction_name in correlation_matrix
            and target_name in correlation_matrix
        ):
            target_prediction_correlation = correlation_matrix.loc[prediction_name, target_name]

            if pd.isnull(target_prediction_correlation):
                target_prediction_correlation = None

        else:
            target_prediction_correlation = None

        if target_name in correlation_matrix:
            abs_max_target_features_correlation = correlation_matrix.loc[target_name, columns_corr].abs().max()

            if pd.isnull(abs_max_target_features_correlation):
                abs_max_target_features_correlation = None

        else:
            abs_max_target_features_correlation = None

        if isinstance(prediction_name, str) and prediction_name in correlation_matrix:
            abs_max_prediction_features_correlation = correlation_matrix.loc[prediction_name, columns_corr].abs().max()

            if pd.isnull(abs_max_prediction_features_correlation):
                abs_max_prediction_features_correlation = None

        else:
            abs_max_prediction_features_correlation = None

        abs_max_correlation = correlation_matrix.abs().max().max()

        if pd.isnull(abs_max_correlation):
            abs_max_correlation = None

        abs_max_features_correlation = correlation_matrix.loc[columns_corr, columns_corr].abs().max().max()

        if pd.isnull(abs_max_features_correlation):
            abs_max_features_correlation = None

        return CorrelationStats(
            target_prediction_correlation=target_prediction_correlation,
            abs_max_target_features_correlation=abs_max_target_features_correlation,
            abs_max_prediction_features_correlation=abs_max_prediction_features_correlation,
            abs_max_correlation=abs_max_correlation,
            abs_max_features_correlation=abs_max_features_correlation,
        )

    def _get_correlations(
        self,
        dataset: pd.DataFrame,
        columns: DatasetColumns,
        add_text_columns: Optional[list],
    ) -> DatasetCorrelation:
        # process predictions. If task == 'classification' add prediction labels
        
        if add_text_columns is not None:
            correlations_calculate = calculate_correlations(dataset, columns, sum(add_text_columns, []))
            correlations = copy.deepcopy(correlations_calculate)
            for name, correlation in correlations_calculate.items():
                if name != "cramer_v":
                    for col_idx in add_text_columns:
                        correlation.loc[col_idx, col_idx] = 0
                    correlations_calculate[name] = correlation
        else:
            correlations_calculate = calculate_correlations(dataset, columns)
            correlations = copy.deepcopy(correlations_calculate)

        stats = {
            name: self._get_correlations_stats(correlation, columns)
            for name, correlation in correlations_calculate.items()
        }

        return DatasetCorrelation(
            correlation=correlations,
            stats=stats,
            correlations_calculate=correlations_calculate,
        )

    def calculate(self, data: InputData) -> DatasetCorrelationsMetricResult:
        prediction_labels_name: Optional[str] = None
        target_correlation: Optional[str] = None
        columns = process_columns(data.current_data, data.column_mapping)
        curr_df = data.current_data.copy()
        ref_df: Optional[pd.DataFrame] = None
        if data.reference_data is not None:
            ref_df = data.reference_data.copy()

        target_type = data.data_definition.get_target_column().column_type
        if target_type == ColumnType.Numerical:
            target_correlation = 'pearson'
        elif target_type == ColumnType.Categorical:
            target_correlation = 'cramer_v'
        
        if not isinstance(columns.utility_columns.prediction, str):
            prediction_data = data.data_definition.get_prediction_columns()
            if prediction_data.predicted_values is None:
                prediction_labels_name = 'prediction_labels'
                prediction_curr = get_prediction_data(curr_df, columns, data.column_mapping.pos_label)
                curr_df[prediction_labels_name] = prediction_curr.labels.values
                if ref_df is not None:
                    prediction_ref = get_prediction_data(ref_df, columns, data.column_mapping.pos_label)
                    ref_df[prediction_labels_name] = prediction_ref.labels.values
            else:
                prediction_labels_name = prediction_data.predicted_values.name()
            columns.utility_columns.prediction = prediction_labels_name


        # process text columns
        text_columns = []
        if self.text_features_gen is not None:
            for col in list(self.text_features_gen.keys()):
                curr_text_df = pd.concat(
                    [data.get_current_column(x.feature_name()) for x in list(self.text_features_gen[col].values())],
                    axis=1,
                )
                curr_text_df.columns = list(self.text_features_gen[col].keys())
                text_columns.append(list(curr_text_df.columns))
                curr_df = pd.concat(
                    [curr_df.copy().reset_index(drop=True), curr_text_df.reset_index(drop=True)],
                    axis=1,
                )

                if ref_df is not None:
                    ref_text_df = pd.concat(
                        [
                            data.get_reference_column(x.feature_name())
                            for x in list(self.text_features_gen[col].values())
                        ],
                        axis=1,
                    )
                    ref_text_df.columns = list(self.text_features_gen[col].keys())
                    ref_df = pd.concat(
                        [ref_df.copy().reset_index(drop=True), ref_text_df.reset_index(drop=True)],
                        axis=1,
                    )

        current_correlations = self._get_correlations(dataset=curr_df, columns=columns, add_text_columns=text_columns)

        if ref_df is not None:
            reference_correlation: Optional[DatasetCorrelation] = self._get_correlations(
                dataset=ref_df, columns=columns, add_text_columns=text_columns
            )

        else:
            reference_correlation = None
        logging.warning(target_correlation)

        return DatasetCorrelationsMetricResult(
            current=current_correlations,
            reference=reference_correlation,
            target_correlation=target_correlation,
            prediction_labels_name=prediction_labels_name,
        )


@default_renderer(wrap_type=DatasetCorrelationsMetric)
class DataQualityCorrelationMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DatasetCorrelationsMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result["current"].pop("correlation", None)
        result["current"].pop("correlations_calculate", None)
        result["current"].pop("target_correlation", None)

        if result["reference"]:
            result["reference"].pop("correlation", None)
            result["reference"].pop("correlations_calculate", None)
            result["reference"].pop("target_correlation", None)

        return result

    def _get_heatmaps(self, metric_result: DatasetCorrelationsMetricResult) -> BaseWidgetInfo:
        tabs = []
        curr_corr_result = metric_result.current.correlation
        for correlation_method in curr_corr_result:
            current_correlation = curr_corr_result[correlation_method]

            if metric_result.reference is not None:
                ref_corr_result = metric_result.reference.correlation
                reference_heatmap_data: Optional[HeatmapData] = HeatmapData(
                    name="Reference", matrix=ref_corr_result[correlation_method]
                )

            else:
                reference_heatmap_data = None

            tabs.append(
                TabData(
                    title=correlation_method,
                    widget=get_heatmaps_widget(
                        primary_data=HeatmapData(name="Current", matrix=current_correlation),
                        secondary_data=reference_heatmap_data,
                        color_options=self.color_options,
                    ),
                )
            )

        return widget_tabs(title="", tabs=tabs)

    def render_html(self, obj: DatasetCorrelationsMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label="Dataset Correlations Metric"),
            self._get_heatmaps(metric_result=metric_result),
        ]
        return result
