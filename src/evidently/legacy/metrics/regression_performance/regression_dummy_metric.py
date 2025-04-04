from typing import List
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.metrics.regression_performance.regression_quality import RegressionQualityMetric
from evidently.legacy.metrics.utils import root_mean_squared_error_compat
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import header_text
from evidently.legacy.renderers.html_widgets import table_data
from evidently.legacy.utils.data_operations import process_columns


class RegressionDummyMetricResults(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:RegressionDummyMetricResults"

    rmse_default: float
    mean_abs_error_default: float
    mean_abs_perc_error_default: float
    abs_error_max_default: float
    mean_abs_error_by_ref: Optional[float] = None
    mean_abs_error: Optional[float] = None
    mean_abs_perc_error_by_ref: Optional[float] = None
    mean_abs_perc_error: Optional[float] = None
    rmse_by_ref: Optional[float] = None
    rmse: Optional[float] = None
    abs_error_max_by_ref: Optional[float] = None
    abs_error_max: Optional[float] = None


class RegressionDummyMetric(Metric[RegressionDummyMetricResults]):
    class Config:
        type_alias = "evidently:metric:RegressionDummyMetric"

    _quality_metric: RegressionQualityMetric

    def __init__(self, options: AnyOptions = None):
        super().__init__(options=options)
        self._quality_metric = RegressionQualityMetric()

    @property
    def quality_metric(self):
        return self._quality_metric

    def calculate(self, data: InputData) -> RegressionDummyMetricResults:
        quality_metric: Optional[RegressionQualityMetric]
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction

        if target_name is None:
            raise ValueError("The column 'target' should present")
        if prediction_name is None:
            quality_metric = None
        else:
            quality_metric = self.quality_metric
        if prediction_name is not None and not isinstance(prediction_name, str):
            raise ValueError("Expect one column for prediction. List of columns was provided.")

        # dummy by current
        # mae
        dummy_preds = data.current_data[target_name].median()
        mean_abs_error_default = mean_absolute_error(
            y_true=data.current_data[target_name],
            y_pred=[dummy_preds] * data.current_data.shape[0],
        )
        # rmse
        dummy_preds = data.current_data[target_name].mean()
        rmse_default = root_mean_squared_error_compat(
            y_true=data.current_data[target_name],
            y_pred=[dummy_preds] * data.current_data.shape[0],
        )
        # mape default values
        # optimal constant for mape
        s = data.current_data[target_name]
        inv_y = 1.0 / s[s != 0].values  # type: ignore[operator]
        w = inv_y / sum(inv_y)  # type: ignore[operator,arg-type]
        idxs = np.argsort(w)
        sorted_w = w[idxs]
        sorted_w_cumsum = np.cumsum(sorted_w)
        idx = np.where(sorted_w_cumsum > 0.5)[0][0]
        pos = idxs[idx]
        dummy_preds = s[s != 0].values[pos]

        mean_abs_perc_error_default = (
            mean_absolute_percentage_error(
                y_true=data.current_data[target_name],
                y_pred=[dummy_preds] * data.current_data.shape[0],
            )
            * 100
        )
        # max error default values
        y_true = data.current_data[target_name]
        abs_error_max_default = np.abs(y_true - y_true.median()).max()

        # dummy by reference
        mean_abs_error_by_ref: Optional[float] = None
        mean_abs_perc_error_by_ref: Optional[float] = None
        rmse_by_ref: Optional[float] = None
        abs_error_max_by_ref: Optional[float] = None
        if data.reference_data is not None:
            # mae
            dummy_preds = data.reference_data[target_name].median()
            mean_abs_error_by_ref = mean_absolute_error(
                y_true=data.current_data[target_name],
                y_pred=[dummy_preds] * data.current_data.shape[0],
            )
            # rmse
            dummy_preds = data.reference_data[target_name].mean()
            rmse_by_ref = root_mean_squared_error_compat(
                y_true=data.current_data[target_name],
                y_pred=[dummy_preds] * data.current_data.shape[0],
            )
            # mape default values
            # optimal constant for mape
            s = data.reference_data[target_name]
            inv_y = 1.0 / s[s != 0].values  # type: ignore[operator]
            w = inv_y / sum(inv_y)  # type: ignore[operator,arg-type]
            idxs = np.argsort(w)
            sorted_w = w[idxs]
            sorted_w_cumsum = np.cumsum(sorted_w)
            idx = np.where(sorted_w_cumsum > 0.5)[0][0]
            pos = idxs[idx]
            dummy_preds = s[s != 0].values[pos]

            mean_abs_perc_error_by_ref = (
                mean_absolute_percentage_error(
                    y_true=data.current_data[target_name],
                    y_pred=[dummy_preds] * data.current_data.shape[0],
                )
                * 100
            )
            # max error default values
            y_true = data.current_data[target_name]
            y_pred = data.reference_data[target_name].median()
            abs_error_max_by_ref = np.abs(y_true - y_pred).max()

        return RegressionDummyMetricResults(
            rmse_default=rmse_default,
            mean_abs_error_default=mean_abs_error_default,
            mean_abs_perc_error_default=mean_abs_perc_error_default,
            abs_error_max_default=abs_error_max_default,
            mean_abs_error_by_ref=mean_abs_error_by_ref,
            mean_abs_error=(quality_metric.get_result().current.mean_abs_error if quality_metric is not None else None),
            mean_abs_perc_error_by_ref=mean_abs_perc_error_by_ref,
            mean_abs_perc_error=(
                quality_metric.get_result().current.mean_abs_perc_error if quality_metric is not None else None
            ),
            rmse_by_ref=rmse_by_ref,
            rmse=quality_metric.get_result().current.rmse if quality_metric is not None else None,
            abs_error_max_by_ref=abs_error_max_by_ref,
            abs_error_max=(quality_metric.get_result().current.abs_error_max if quality_metric is not None else None),
        )


@default_renderer(wrap_type=RegressionDummyMetric)
class RegressionDummyMetricRenderer(MetricRenderer):
    def render_html(self, obj: RegressionDummyMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        in_table_data = pd.DataFrame(data=["MAE", "RMSE", "MAPE", "MAX_ERROR"])
        columns = ["Metric"]
        if (
            metric_result.abs_error_max_by_ref is not None
            and metric_result.mean_abs_perc_error_by_ref is not None
            and metric_result.rmse_by_ref is not None
            and metric_result.mean_abs_error_by_ref is not None
        ):
            in_table_data["by_ref"] = [
                metric_result.mean_abs_error_by_ref,
                metric_result.rmse_by_ref,
                metric_result.mean_abs_perc_error_by_ref,
                metric_result.abs_error_max_by_ref,
            ]
            columns.append("Dummy (by rerefence)")
        in_table_data["by_carr"] = [
            metric_result.mean_abs_error_default,
            metric_result.rmse_default,
            metric_result.mean_abs_perc_error_default,
            metric_result.abs_error_max_default,
        ]
        if "Dummy (by rerefence)" in columns:
            columns.append("Dummy (by current)")
        else:
            columns.append("Dummy")
        if (
            metric_result.mean_abs_error is not None
            and metric_result.rmse is not None
            and metric_result.mean_abs_perc_error is not None
            and metric_result.abs_error_max is not None
        ):
            in_table_data["model_quality"] = [
                metric_result.mean_abs_error,
                metric_result.rmse,
                metric_result.mean_abs_perc_error,
                metric_result.abs_error_max,
            ]
            columns.append("Model")

        return [
            header_text(label="Dummy Regression Quality"),
            table_data(
                column_names=columns,
                data=np.around(in_table_data, 3).values,  # type: ignore[attr-defined]
                title="",
            ),
        ]
