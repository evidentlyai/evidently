from typing import List
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd

from evidently.base_metric import ColumnMetric
from evidently.base_metric import ColumnName
from evidently.base_metric import ColumnNotFound
from evidently.base_metric import DataDefinition
from evidently.base_metric import InputData
from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import ColumnType
from evidently.calculations.data_drift import DistributionIncluded
from evidently.calculations.data_drift import DriftStatsField
from evidently.calculations.data_drift import ScatterField
from evidently.calculations.data_drift import get_distribution_for_column
from evidently.calculations.data_drift import get_stattest
from evidently.calculations.data_drift import get_text_data_for_plots
from evidently.calculations.stattests import PossibleStatTestType
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import widget_tabs
from evidently.renderers.render_utils import get_distribution_plot_figure
from evidently.utils.visualizations import plot_scatter_for_data_drift


def get_one_column_drift(
    *,
    current_feature_data: pd.Series,
    reference_feature_data: pd.Series,
    index_data: pd.Series,
    datetime_data: Optional[pd.Series],
    column: ColumnName,
    options: DataDriftOptions,
    data_definition: DataDefinition,
    column_type: ColumnType,
) -> ColumnDataDriftMetrics:
    if column_type not in (ColumnType.Numerical, ColumnType.Categorical, ColumnType.Text):
        raise ValueError(f"Cannot calculate drift metric for column '{column}' with type {column_type}")

    target = data_definition.get_target_column()
    stattest = None
    threshold = None
    if column.is_main_dataset():
        if target and column.name == target.column_name and column_type == ColumnType.Numerical:
            stattest = options.num_target_stattest_func

        elif target and column.name == target.column_name and column_type == ColumnType.Categorical:
            stattest = options.cat_target_stattest_func

        if not stattest:
            stattest = options.get_feature_stattest_func(column.name, column_type.value)

        threshold = options.get_threshold(column.name, column_type.value)
    current_column = current_feature_data
    reference_column = reference_feature_data

    # clean and check the column in reference dataset
    reference_column = reference_column.replace([-np.inf, np.inf], np.nan).dropna()

    if reference_column.empty:
        raise ValueError(
            f"An empty column '{column.name}' was provided for drift calculation in the reference dataset."
        )

    # clean and check the column in current dataset
    current_column = current_column.replace([-np.inf, np.inf], np.nan).dropna()

    if current_column.empty:
        raise ValueError(f"An empty column '{column.name}' was provided for drift calculation in the current dataset.")

    current_distribution = None
    reference_distribution = None
    current_small_distribution = None
    reference_small_distribution = None
    current_correlations = None
    reference_correlations = None

    typical_examples_cur = None
    typical_examples_ref = None
    typical_words_cur = None
    typical_words_ref = None

    if column_type == ColumnType.Numerical:
        if not pd.api.types.is_numeric_dtype(reference_column):
            raise ValueError(f"Column '{column}' in reference dataset should contain numerical values only.")

        if not pd.api.types.is_numeric_dtype(current_column):
            raise ValueError(f"Column '{column}' in current dataset should contain numerical values only.")

    drift_test_function = get_stattest(reference_column, current_column, column_type.value, stattest)
    drift_result = drift_test_function(reference_column, current_column, column_type.value, threshold)

    scatter: Optional[ScatterField] = None
    if column_type == ColumnType.Numerical:
        current_nbinsx = options.get_nbinsx(column.name)
        current_small_distribution = [
            t.tolist()
            for t in np.histogram(
                current_column[np.isfinite(current_column)],
                bins=current_nbinsx,
                density=True,
            )
        ]
        reference_small_distribution = [
            t.tolist()
            for t in np.histogram(
                reference_column[np.isfinite(reference_column)],
                bins=current_nbinsx,
                density=True,
            )
        ]
        current_scatter = {column.display_name: current_column}
        if datetime_data is not None:
            current_scatter["Timestamp"] = datetime_data
            x_name = "Timestamp"
        else:
            current_scatter["Index"] = index_data
            x_name = "Index"

        plot_shape = {}
        reference_mean = reference_column.mean()
        reference_std = reference_column.std()
        plot_shape["y0"] = reference_mean - reference_std
        plot_shape["y1"] = reference_mean + reference_std
        scatter = ScatterField(scatter=current_scatter, x_name=x_name, plot_shape=plot_shape)

    elif column_type == ColumnType.Categorical:
        reference_counts = reference_column.value_counts(sort=False)
        current_counts = current_column.value_counts(sort=False)
        keys = set(reference_counts.keys()).union(set(current_counts.keys()))

        for key in keys:
            if key not in reference_counts:
                reference_counts.loc[key] = 0
            if key not in current_counts:
                current_counts.loc[key] = 0

        reference_small_distribution = list(
            reversed(
                list(
                    map(
                        list,
                        zip(*sorted(reference_counts.items(), key=lambda x: str(x[0]))),
                    )
                )
            )
        )
        current_small_distribution = list(
            reversed(
                list(
                    map(
                        list,
                        zip(*sorted(current_counts.items(), key=lambda x: str(x[0]))),
                    )
                )
            )
        )
    if column_type != ColumnType.Text:
        prediction = data_definition.get_prediction_columns()
        labels = data_definition.classification_labels()
        predicted_values = prediction.predicted_values if prediction else None
        if (
            column_type == ColumnType.Categorical
            and labels is not None
            and (
                (target and column.name == target.column_name)
                or (
                    predicted_values
                    and isinstance(predicted_values.column_name, str)
                    and column.name == predicted_values.column_name
                )
            )
        ):
            column_values = np.union1d(current_column.unique(), reference_column.unique())
            target_names = labels if isinstance(labels, list) else list(labels.values())
            new_values = np.setdiff1d(list(target_names), column_values)
            if len(new_values) > 0:
                raise ValueError(f"Values {new_values} not presented in 'target_names'")
            else:
                current_column = current_column.map(target_names)
                reference_column = reference_column.map(target_names)
        current_distribution, reference_distribution = get_distribution_for_column(
            column_type=column_type.value,
            current=current_column,
            reference=reference_column,
        )
        if reference_distribution is None:
            raise ValueError(f"Cannot calculate reference distribution for column '{column}'.")

    elif column_type == ColumnType.Text and drift_result.drifted:
        (
            typical_examples_cur,
            typical_examples_ref,
            typical_words_cur,
            typical_words_ref,
        ) = get_text_data_for_plots(reference_column, current_column)

    metrics = ColumnDataDriftMetrics(
        column_name=column.display_name,
        column_type=column_type.value,
        stattest_name=drift_test_function.display_name,
        drift_score=drift_result.drift_score,
        drift_detected=drift_result.drifted,
        stattest_threshold=drift_result.actual_threshold,
        current=DriftStatsField(
            distribution=current_distribution,
            small_distribution=DistributionIncluded(x=current_small_distribution[1], y=current_small_distribution[0])
            if current_small_distribution
            else None,
            correlations=current_correlations,
            characteristic_examples=typical_examples_cur,
            characteristic_words=typical_words_cur,
        ),
        reference=DriftStatsField(
            distribution=reference_distribution,
            small_distribution=DistributionIncluded(
                x=reference_small_distribution[1], y=reference_small_distribution[0]
            )
            if reference_small_distribution
            else None,
            characteristic_examples=typical_examples_ref,
            characteristic_words=typical_words_ref,
            correlations=reference_correlations,
        ),
        scatter=scatter,
    )

    return metrics


class ColumnDriftMetric(ColumnMetric[ColumnDataDriftMetrics]):
    """Calculate drift metric for a column"""

    column: ColumnName

    stattest: Optional[PossibleStatTestType]
    stattest_threshold: Optional[float]

    def __init__(
        self,
        column_name: Union[ColumnName, str],
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
    ):
        if isinstance(column_name, str):
            column = ColumnName.main_dataset(column_name)
        else:
            column = column_name
        self.column = column
        self.column_name = column.name
        self.stattest = stattest
        self.stattest_threshold = stattest_threshold

    def get_parameters(self) -> tuple:
        return self.column, self.stattest_threshold, self.stattest

    def calculate(self, data: InputData) -> ColumnDataDriftMetrics:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        try:
            current_feature_data = data.get_current_column(self.column)
        except ColumnNotFound as ex:
            raise ValueError(f"Cannot find column '{ex.column_name}' in current dataset")
        try:
            reference_feature_data = data.get_reference_column(self.column)
        except ColumnNotFound as ex:
            raise ValueError(f"Cannot find column '{ex.column_name}' in reference dataset")

        column_type = ColumnType.Numerical
        if self.column.is_main_dataset():
            column_type = data.data_definition.get_column(self.column.name).column_type
        datetime_column = data.data_definition.get_datetime_column()
        options = DataDriftOptions(all_features_stattest=self.stattest, threshold=self.stattest_threshold)
        drift_result = get_one_column_drift(
            current_feature_data=current_feature_data,
            reference_feature_data=reference_feature_data,
            column=self.column,
            index_data=data.current_data.index,
            column_type=column_type,
            datetime_data=data.current_data[datetime_column.column_name] if datetime_column else None,
            data_definition=data.data_definition,
            options=options,
        )

        return ColumnDataDriftMetrics(
            column_name=drift_result.column_name,
            column_type=drift_result.column_type,
            stattest_name=drift_result.stattest_name,
            stattest_threshold=drift_result.stattest_threshold,
            drift_score=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            current=drift_result.current,
            scatter=drift_result.scatter,
            reference=drift_result.reference,
        )


@default_renderer(wrap_type=ColumnDriftMetric)
class ColumnDriftMetricRenderer(MetricRenderer):
    def render_html(self, obj: ColumnDriftMetric) -> List[BaseWidgetInfo]:
        result: ColumnDataDriftMetrics = obj.get_result()

        if result.drift_detected:
            drift = "detected"

        else:
            drift = "not detected"

        drift_score = round(result.drift_score, 3)

        tabs = []

        # fig_json = fig.to_plotly_json()
        if result.scatter is not None:
            scatter_fig = plot_scatter_for_data_drift(
                curr_y=result.scatter.scatter[result.column_name],
                curr_x=result.scatter.scatter[result.scatter.x_name],
                y0=result.scatter.plot_shape["y0"],
                y1=result.scatter.plot_shape["y1"],
                y_name=result.column_name,
                x_name=result.scatter.x_name,
                color_options=self.color_options,
            )
            tabs.append(TabData("DATA DRIFT", plotly_figure(title="", figure=scatter_fig)))

        if result.current.distribution is not None and result.reference.distribution is not None:
            distr_fig = get_distribution_plot_figure(
                current_distribution=result.current.distribution,
                reference_distribution=result.reference.distribution,
                color_options=self.color_options,
            )
            # figures.append(GraphData.figure("DATA DISTRIBUTION", distr_fig))
            tabs.append(TabData("DATA DISTRIBUTION", plotly_figure(title="", figure=distr_fig)))

        if (
            result.current.characteristic_examples is not None
            and result.reference.characteristic_examples is not None
            and result.current.characteristic_words is not None
            and result.reference.characteristic_words is not None
        ):
            current_table_words = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.current.characteristic_words],
            )
            reference_table_words = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.reference.characteristic_words],
            )
            current_table_examples = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.current.characteristic_examples],
            )
            reference_table_examples = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.reference.characteristic_examples],
            )

            tabs = [
                TabData(title="current: characteristic words", widget=current_table_words),
                TabData(
                    title="reference: characteristic words",
                    widget=reference_table_words,
                ),
                TabData(
                    title="current: characteristic examples",
                    widget=current_table_examples,
                ),
                TabData(
                    title="reference: characteristic examples",
                    widget=reference_table_examples,
                ),
            ]
        render_result = [
            counter(
                counters=[
                    CounterData(
                        (
                            f"Data drift {drift}. "
                            f"Drift detection method: {result.stattest_name}. "
                            f"Drift score: {drift_score}"
                        ),
                        f"Drift in column '{result.column_name}'",
                    )
                ],
                title="",
            )
        ]
        if len(tabs) > 0:
            render_result.append(
                widget_tabs(
                    title="",
                    tabs=tabs,
                )
            )

        return render_result
