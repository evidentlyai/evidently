from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns
from evidently.utils.visualizations import plot_error_bias_colored_scatter


@dataclasses.dataclass
class RegressionTopErrorMetricResults:
    curr_mean_err_per_group: Dict[str, Dict[str, float]]
    curr_scatter: Dict[str, Dict[str, pd.Series]]
    ref_mean_err_per_group: Optional[Dict[str, Dict[str, float]]]
    ref_scatter: Optional[Dict[str, Dict[str, pd.Series]]]


class RegressionTopErrorMetric(Metric[RegressionTopErrorMetricResults]):
    def calculate(self, data: InputData) -> RegressionTopErrorMetricResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        curr_df = data.current_data
        ref_df = data.reference_data
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' columns should be present")
        if not isinstance(prediction_name, str):
            raise ValueError("Expect one column for prediction. List of columns was provided.")
        curr_df = self._make_df_for_plot(curr_df, target_name, prediction_name, None)
        curr_error = curr_df[prediction_name] - curr_df[target_name]
        quantile_5 = np.quantile(curr_error, 0.05)
        quantile_95 = np.quantile(curr_error, 0.95)

        curr_df["Error bias"] = list(
            map(
                lambda x: "Underestimation" if x <= quantile_5 else "Majority" if x < quantile_95 else "Overestimation",
                curr_error,
            )
        )
        curr_scatter = self._get_data_for_scatter(curr_df, target_name, prediction_name)
        curr_mean_err_per_group = self._calculate_underperformance(curr_error, quantile_5, quantile_95)

        ref_scatter = None
        ref_mean_err_per_group = None
        if ref_df is not None:
            ref_df = self._make_df_for_plot(ref_df, target_name, prediction_name, None)
            ref_error = ref_df[prediction_name] - ref_df[target_name]
            quantile_5 = np.quantile(ref_error, 0.05)
            quantile_95 = np.quantile(ref_error, 0.95)

            ref_df["Error bias"] = list(
                map(
                    lambda x: "Underestimation"
                    if x <= quantile_5
                    else "Majority"
                    if x < quantile_95
                    else "Overestimation",
                    ref_error,
                )
            )
            ref_scatter = self._get_data_for_scatter(ref_df, target_name, prediction_name)
            ref_mean_err_per_group = self._calculate_underperformance(ref_error, quantile_5, quantile_95)
        return RegressionTopErrorMetricResults(
            curr_mean_err_per_group=curr_mean_err_per_group,
            curr_scatter=curr_scatter,
            ref_mean_err_per_group=ref_mean_err_per_group,
            ref_scatter=ref_scatter,
        )

    def _make_df_for_plot(self, df, target_name: str, prediction_name: str, datetime_column_name: Optional[str]):
        result = df.replace([np.inf, -np.inf], np.nan)
        if datetime_column_name is not None:
            result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name, datetime_column_name])
            return result.sort_values(datetime_column_name)
        result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name])
        return result.sort_index()

    def _get_data_for_scatter(self, df: pd.DataFrame, target_name: str, prediction_name: str):
        scatter = {}
        scatter["Underestimation"] = {
            "Predicted value": df.loc[df["Error bias"] == "Underestimation", prediction_name],
            "Actual value": df.loc[df["Error bias"] == "Underestimation", target_name],
        }
        scatter["Majority"] = {
            "Predicted value": df.loc[df["Error bias"] == "Majority", prediction_name],
            "Actual value": df.loc[df["Error bias"] == "Majority", target_name],
        }
        scatter["Overestimation"] = {
            "Predicted value": df.loc[df["Error bias"] == "Overestimation", prediction_name],
            "Actual value": df.loc[df["Error bias"] == "Overestimation", target_name],
        }
        return scatter

    def _calculate_underperformance(
        self, error: pd.Series, quantile_5: float, quantile_95: float, conf_interval_n_sigmas: int = 1
    ):

        mae_under = np.mean(error[error <= quantile_5])
        mae_exp = np.mean(error[(error > quantile_5) & (error < quantile_95)])
        mae_over = np.mean(error[error >= quantile_95])

        sd_under = np.std(error[error <= quantile_5], ddof=1)
        sd_exp = np.std(error[(error > quantile_5) & (error < quantile_95)], ddof=1)
        sd_over = np.std(error[error >= quantile_95], ddof=1)

        return {
            "majority": {"mean_error": float(mae_exp), "std_error": conf_interval_n_sigmas * float(sd_exp)},
            "underestimation": {"mean_error": float(mae_under), "std_error": conf_interval_n_sigmas * float(sd_under)},
            "overestimation": {"mean_error": float(mae_over), "std_error": conf_interval_n_sigmas * float(sd_over)},
        }


@default_renderer(wrap_type=RegressionTopErrorMetric)
class RegressionTopErrorMetricRenderer(MetricRenderer):
    def render_html(self, obj: RegressionTopErrorMetric) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        curr_mean_err_per_group = result.curr_mean_err_per_group
        curr_scatter = result.curr_scatter
        ref_mean_err_per_group = result.ref_mean_err_per_group
        ref_scatter = result.ref_scatter

        res = [
            header_text(label="Error Bias Table"),
            counter(
                title="Current: Mean Error per Group (+/- std)",
                counters=[
                    CounterData("Majority(90%)", self._format_value(curr_mean_err_per_group, "majority")),
                    CounterData("Underestimation(5%)", self._format_value(curr_mean_err_per_group, "underestimation")),
                    CounterData("Overestimation(5%)", self._format_value(curr_mean_err_per_group, "overestimation")),
                ],
            ),
        ]
        if ref_mean_err_per_group is not None:
            res.append(
                counter(
                    title="Current: Mean Error per Group (+/- std)",
                    counters=[
                        CounterData("Majority(90%)", self._format_value(ref_mean_err_per_group, "majority")),
                        CounterData(
                            "Underestimation(5%)", self._format_value(ref_mean_err_per_group, "underestimation")
                        ),
                        CounterData("Overestimation(5%)", self._format_value(ref_mean_err_per_group, "overestimation")),
                    ],
                )
            )
        res.append(header_text(label="Predicted vs Actual per Group"))
        fig = plot_error_bias_colored_scatter(curr_scatter, ref_scatter)

        res.append(
            BaseWidgetInfo(
                title="",
                size=2,
                type="big_graph",
                params={"data": fig["data"], "layout": fig["layout"]},
            )
        )
        return res

    def _format_value(self, result, counter_type):
        return f"{round(result[counter_type]['mean_error'], 2)}" f" ({round(result[counter_type]['std_error'], 2)})"
