from abc import ABC
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import dataclasses

import numpy as np
import pandas as pd

from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.metrics import DataDriftMetrics
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.renderers.base_renderer import DetailsInfo
from evidently.renderers.base_renderer import default_renderer
from evidently.tests.base_test import Test
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import TestResult
from evidently.tests.base_test import TestValueCondition
from evidently.tests.utils import plot_distr
from evidently.tests.utils import Numeric


@dataclasses.dataclass
class TestDataDriftResult(TestResult):
    features: Dict[str, Tuple[str, float, float]]


class BaseDataDriftMetricsTest(BaseCheckValueTest, ABC):
    group = "data_drift"
    metric: DataDriftMetrics

    def __init__(
        self,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
        metric: Optional[DataDriftMetrics] = None,
        options: Optional[DataDriftOptions] = None,
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataDriftMetrics(options=options)

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

    def check(self):
        result = super().check()
        metrics = self.metric.get_result().analyzer_result.metrics

        return TestDataDriftResult(
            name=result.name,
            description=result.description,
            status=result.status,
            features={
                feature: (
                    data.stattest_name,
                    np.round(data.p_value, 3),
                    data.threshold,
                    "Detected" if data.drift_detected else "Not Detected",
                )
                for feature, data in metrics.features.items()
            },
        )


class TestNumberOfDriftedFeatures(BaseDataDriftMetricsTest):
    name = "Number of Drifted Features"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition
        else:
            return TestValueCondition(lt=max(0, self.metric.get_result().analyzer_result.metrics.n_features // 3))

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().analyzer_result.metrics.n_drifted_features

    def get_description(self, value: Numeric) -> str:
        n_features = self.metric.get_result().analyzer_result.metrics.n_features
        return (
            f"The drift is detected for {value} out of {n_features} features. "
            f"The test threshold is {self.get_condition()}."
        )


class TestShareOfDriftedFeatures(BaseDataDriftMetricsTest):
    name = "Share of Drifted Features"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition
        else:
            return TestValueCondition(lt=0.3)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().analyzer_result.metrics.share_drifted_features

    def get_description(self, value: Numeric) -> str:
        n_drifted_features = self.metric.get_result().analyzer_result.metrics.n_drifted_features
        n_features = self.metric.get_result().analyzer_result.metrics.n_features
        return (
            f"The drift is detected for {value * 100:.3g}% features "
            f"({n_drifted_features} out of {n_features}). The test threshold is {self.get_condition()}"
        )


class TestFeatureValueDrift(Test):
    name = "Drift per Feature"
    group = "data_drift"
    metric: DataDriftMetrics
    column_name: str

    def __init__(
        self,
        column_name: str,
        metric: Optional[DataDriftMetrics] = None,
        options: Optional[DataDriftOptions] = None,
    ):
        self.column_name = column_name

        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataDriftMetrics(options=options)

    def check(self):
        drift_info = self.metric.get_result().analyzer_result.metrics

        if self.column_name not in drift_info.features:
            result_status = TestResult.ERROR
            description = f"Cannot find column {self.column_name} in the dataset"

        else:
            p_value = np.round(drift_info.features[self.column_name].p_value, 3)
            stattest_name = drift_info.features[self.column_name].stattest_name
            threshold = drift_info.features[self.column_name].threshold
            description = (
                f"The drift score for the feature {self.column_name} is {p_value:.3g}. "
                f"The drift detection method is {stattest_name}. "
                f"The drift detection threshold is {threshold}."
            )

            if not drift_info.features[self.column_name].drift_detected:
                result_status = TestResult.SUCCESS

            else:
                result_status = TestResult.FAIL

        return TestResult(name=self.name, description=description, status=result_status)


@default_renderer(test_type=TestNumberOfDriftedFeatures)
class TestNumberOfDriftedFeaturesRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfDriftedFeatures) -> dict:
        base = super().render_json(obj)
        base["parameters"]["features"] = {
            feature: {"stattest": data[0], "score": np.round(data[1], 3), "threshold": data[2], "data_drift": data[3]}
            for feature, data in obj.get_result().features.items()
        }
        return base

    def render_html(self, obj: TestNumberOfDriftedFeatures) -> TestHtmlInfo:
        info = super().render_html(obj)
        df = pd.DataFrame(
            data=[[feature] + list(data) for feature, data in obj.get_result().features.items()],
            columns=["Feature name", "Stattest", "Drift score", "Threshold", "Data Drift"],
        )
        df = df.sort_values("Data Drift")
        info.details = [
            DetailsInfo(
                id="drift_table",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={"header": df.columns.to_list(), "data": df.values},
                    size=2,
                ),
            ),
        ]
        return info


@default_renderer(test_type=TestShareOfDriftedFeatures)
class TestShareOfDriftedFeaturesRenderer(TestRenderer):
    def render_json(self, obj: TestShareOfDriftedFeatures) -> dict:
        base = super().render_json(obj)
        base["parameters"]["features"] = {
            feature: {"stattest": data[0], "score": np.round(data[1], 3), "threshold": data[2], "data_drift": data[3]}
            for feature, data in obj.get_result().features.items()
        }
        return base

    def render_html(self, obj: TestShareOfDriftedFeatures) -> TestHtmlInfo:
        info = super().render_html(obj)
        df = pd.DataFrame(
            data=[[feature] + list(data) for feature, data in obj.get_result().features.items()],
            columns=["Feature name", "Stattest", "Drift score", "Threshold", "Data Drift"],
        )
        df = df.sort_values("Data Drift")
        info.details = [
            DetailsInfo(
                id="drift_table",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={"header": df.columns.to_list(), "data": df.values},
                    size=2,
                ),
            ),
        ]
        return info


@default_renderer(test_type=TestFeatureValueDrift)
class TestFeatureValueDriftRenderer(TestRenderer):
    def render_json(self, obj: TestFeatureValueDrift) -> dict:
        feature_name = obj.column_name
        drift_data = obj.metric.get_result().analyzer_result.metrics.features[feature_name]
        base = super().render_json(obj)
        base["parameters"]["features"] = {
            feature_name: {
                "stattest": drift_data.stattest_name,
                "score": np.round(drift_data.p_value, 3),
                "threshold": drift_data.threshold,
                "data_drift": drift_data.drift_detected,
            }
        }
        return base

    def render_html(self, obj: TestFeatureValueDrift) -> TestHtmlInfo:
        feature_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plots[feature_name]["current"]
        ref_distr = obj.metric.get_result().distr_for_plots[feature_name]["reference"]
        fig = plot_distr(curr_distr, ref_distr)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=feature_name,
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info
