from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import get_dataset_drift
from evidently.calculations.data_drift import get_one_column_drift
from evidently.calculations.stattests import PossibleStatTestType
from evidently.core import ColumnType as ColumnType_data
from evidently.descriptors import OOV
from evidently.descriptors import NonLetterCharacterPercentage
from evidently.descriptors import TextLength
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature
from evidently.metric_results import DatasetColumns
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import ColumnDefinition
from evidently.renderers.html_widgets import ColumnType
from evidently.renderers.html_widgets import RichTableDataRow
from evidently.renderers.html_widgets import RowDetails
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import rich_table_data
from evidently.renderers.render_utils import get_distribution_plot_figure
from evidently.utils.data_operations import process_columns
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.visualizations import plot_scatter_for_data_drift


class TextDescriptorsDriftMetricResults(MetricResult):
    number_of_columns: int
    number_of_drifted_columns: int
    share_of_drifted_columns: float
    dataset_drift: bool
    drift_by_columns: Dict[str, ColumnDataDriftMetrics]
    dataset_columns: DatasetColumns


class TextDescriptorsDriftMetric(Metric[TextDescriptorsDriftMetricResults]):
    column_name: str
    options: DataDriftOptions
    generated_text_features: Dict[str, GeneratedFeature]

    def __init__(
        self,
        column_name: str,
        descriptors: Optional[Dict[str, FeatureDescriptor]] = None,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
    ):
        self.column_name = column_name
        self.options = DataDriftOptions(all_features_stattest=stattest, all_features_threshold=stattest_threshold)
        if descriptors:
            self.descriptors = descriptors
        else:
            self.descriptors = {
                "Text Length": TextLength(),
                "Non Letter Character %": NonLetterCharacterPercentage(),
                "OOV %": OOV(),
            }
        self.generated_text_features = {}

    def required_features(self, data_definition: DataDefinition):
        column_type = data_definition.get_column(self.column_name).column_type
        if column_type == ColumnType_data.Text:
            self.generated_text_features = {
                name: desc.feature(self.column_name) for name, desc in self.descriptors.items()
            }
            return list(self.generated_text_features.values())
        return []

    def get_parameters(self) -> tuple:
        return self.column_name, self.options

    def calculate(self, data: InputData) -> TextDescriptorsDriftMetricResults:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")
        curr_text_df = pd.concat(
            [data.get_current_column(x.feature_name()) for x in list(self.generated_text_features.values())],
            axis=1,
        )
        curr_text_df.columns = list(self.generated_text_features.keys())

        ref_text_df = pd.concat(
            [data.get_reference_column(x.feature_name()) for x in list(self.generated_text_features.values())],
            axis=1,
        )
        ref_text_df.columns = list(self.generated_text_features.keys())
        # text_dataset_columns = DatasetColumns(num_feature_names=curr_text_df.columns)
        text_dataset_columns = process_columns(ref_text_df, ColumnMapping(numerical_features=ref_text_df.columns))

        drift_by_columns = {}
        for col in curr_text_df.columns:
            drift_by_columns[col] = get_one_column_drift(
                current_data=curr_text_df,
                reference_data=ref_text_df,
                column_name=col,
                options=self.options,
                dataset_columns=text_dataset_columns,
            )
        dataset_drift = get_dataset_drift(drift_by_columns, 0)

        return TextDescriptorsDriftMetricResults(
            number_of_columns=curr_text_df.shape[1],
            number_of_drifted_columns=dataset_drift.number_of_drifted_columns,
            share_of_drifted_columns=dataset_drift.dataset_drift_score,
            dataset_drift=dataset_drift.dataset_drift,
            drift_by_columns=drift_by_columns,
            dataset_columns=text_dataset_columns,
        )


@default_renderer(wrap_type=TextDescriptorsDriftMetric)
class DataDriftTableRenderer(MetricRenderer):
    def _generate_column_params(self, column_name: str, data: ColumnDataDriftMetrics) -> Optional[RichTableDataRow]:
        details = RowDetails()
        if (
            data.current.small_distribution is None
            or data.reference.small_distribution is None
            or data.current.distribution is None
        ):
            return None

        current_small_hist = data.current.small_distribution
        ref_small_hist = data.reference.small_distribution
        data_drift = "Detected" if data.drift_detected else "Not Detected"
        if data.column_type == "num" and data.scatter is not None:
            scatter_fig = plot_scatter_for_data_drift(
                curr_y=data.scatter.scatter[data.column_name],
                curr_x=data.scatter.scatter[data.scatter.x_name],
                y0=data.scatter.plot_shape["y0"],
                y1=data.scatter.plot_shape["y1"],
                y_name=data.column_name,
                x_name=data.scatter.x_name,
                color_options=self.color_options,
            )
            scatter = plotly_figure(title="", figure=scatter_fig)
            details.with_part("DATA DRIFT", info=scatter)
            fig = get_distribution_plot_figure(
                current_distribution=data.current.distribution,
                reference_distribution=data.reference.distribution,
                color_options=self.color_options,
            )
            distribution = plotly_figure(title="", figure=fig)
            details.with_part("DATA DISTRIBUTION", info=distribution)
            return RichTableDataRow(
                details=details,
                fields={
                    "column_name": column_name,
                    "column_type": data.column_type,
                    "stattest_name": data.stattest_name,
                    "reference_distribution": {
                        "x": ref_small_hist.x,
                        "y": ref_small_hist.y,
                    },
                    "current_distribution": {
                        "x": current_small_hist.x,
                        "y": current_small_hist.y,
                    },
                    "data_drift": data_drift,
                    "drift_score": round(data.drift_score, 6),
                },
            )
        else:
            return None

    def render_html(self, obj: TextDescriptorsDriftMetric) -> List[BaseWidgetInfo]:
        results = obj.get_result()
        color_options = self.color_options

        # set params data
        params_data = []

        # sort columns by drift score
        columns = sorted(
            results.drift_by_columns.keys(),
            key=lambda x: results.drift_by_columns[x].drift_score,
            reverse=True,
        )

        for column_name in columns:
            column_params = self._generate_column_params(column_name, results.drift_by_columns[column_name])

            if column_params is not None:
                params_data.append(column_params)

        drift_percents = round(results.share_of_drifted_columns * 100, 3)

        return [
            header_text(label=f"Text Descriptors Drift for column '{obj.column_name}'"),
            rich_table_data(
                title=f"Drift is detected for {drift_percents}% of columns "
                f"({results.number_of_drifted_columns} out of {results.number_of_columns}).",
                columns=[
                    ColumnDefinition("Column", "column_name"),
                    ColumnDefinition("Type", "column_type"),
                    ColumnDefinition(
                        "Reference Distribution",
                        "reference_distribution",
                        ColumnType.HISTOGRAM,
                        options={
                            "xField": "x",
                            "yField": "y",
                            "color": color_options.primary_color,
                        },
                    ),
                    ColumnDefinition(
                        "Current Distribution",
                        "current_distribution",
                        ColumnType.HISTOGRAM,
                        options={
                            "xField": "x",
                            "yField": "y",
                            "color": color_options.primary_color,
                        },
                    ),
                    ColumnDefinition("Data Drift", "data_drift"),
                    ColumnDefinition("Stat Test", "stattest_name"),
                    ColumnDefinition("Drift Score", "drift_score"),
                ],
                data=params_data,
            ),
        ]
