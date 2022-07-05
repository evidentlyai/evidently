from abc import ABC
from numbers import Number
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
from evidently.v2.metrics import DataDriftMetrics
from evidently.v2.renderers.base_renderer import TestRenderer
from evidently.v2.renderers.base_renderer import TestHtmlInfo
from evidently.v2.renderers.base_renderer import DetailsInfo
from evidently.v2.renderers.base_renderer import default_renderer
from evidently.v2.tests.base_test import BaseCheckValueTest
from evidently.v2.tests.base_test import Test
from evidently.v2.tests.base_test import TestResult
from evidently.v2.tests.base_test import TestValueCondition
from evidently.v2.tests.utils import plot_distr


@dataclasses.dataclass
class TestDataDriftResult(TestResult):
    features: Dict[str, Tuple[str, float, float]]


class BaseDataDriftMetricsTest(BaseCheckValueTest, ABC):
    group = "data_drift"
    metric: DataDriftMetrics

    def __init__(
        self,
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
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
    name = "Test Number of Drifted Features"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition
        else:
            return TestValueCondition(lt=max(0, self.metric.get_result().analyzer_result.metrics.n_features // 3))

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().analyzer_result.metrics.n_drifted_features

    def get_description(self, value: Number) -> str:
        return f"Drift is detected for {value} out of {self.metric.get_result().analyzer_result.metrics.n_features} \
            features. Threshold: [{self.get_condition()}]"


class TestShareOfDriftedFeatures(BaseDataDriftMetricsTest):
    name = "Test Share of Drifted Features"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition
        else:
            return TestValueCondition(lt=0.3)

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().analyzer_result.metrics.share_drifted_features

    def get_description(self, value: Number) -> str:
        return f"Drift is detected for {np.round(value, 3) * 100}% features \
        ({self.metric.get_result().analyzer_result.metrics.n_drifted_features} out of \
        {self.metric.get_result().analyzer_result.metrics.n_features}). Threshold: [{self.get_condition()}]"


class TestFeatureValueDrift(Test):
    name = "Test Drift Per Feature"
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
                f"Drift score for feature {self.column_name} is {p_value}. {stattest_name}. "
                f"Drift Detection Threshold is {threshold}."
            )

            if drift_info.features[self.column_name].drift_detected:
                result_status = TestResult.SUCCESS

            else:
                result_status = TestResult.FAIL

        return TestResult(name=self.name, description=description, status=result_status)


@default_renderer(test_type=TestNumberOfDriftedFeatures)
class TestNumberOfDriftedFeaturesRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfDriftedFeatures) -> dict:
        base = super().render_json(obj)
        base["features"] = {
            feature: dict(stattest=data[0], score=np.round(data[1], 3), threshold=data[2], data_drift=data[3])
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
        base["features"] = {
            feature: dict(stattest=data[0], score=np.round(data[1], 3), threshold=data[2], data_drift=data[3])
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
        base = super().render_json(obj)
        feature_name = obj.column_name
        drift_data = obj.metric.get_result().analyzer_result.metrics.features[feature_name]
        base["features"] = {
            feature_name: {
                "stattest": drift_data.stattest_name,
                "score": drift_data.p_value,
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
