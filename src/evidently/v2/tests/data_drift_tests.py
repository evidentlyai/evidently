from numbers import Number
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import dataclasses

import numpy as np

from evidently.model.widget import BaseWidgetInfo
from evidently.v2.metrics import DataDriftMetrics
from evidently.v2.renderers.base_renderer import TestRenderer, TestHtmlInfo, DetailsInfo, default_renderer
from evidently.v2.tests.base_test import BaseCheckValueTest, TestResult
from evidently.v2.tests.utils import plot_distr

@dataclasses.dataclass
class TestDataDriftResult(TestResult):
    features: Dict[str, Tuple[str, float, float]]


class BaseDataDriftMetricsTest(BaseCheckValueTest):
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
        metric: Optional[DataDriftMetrics] = None
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataDriftMetrics()

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

    def check(self):
        result = super().check()
        metrics = self.metric.get_result().analyzer_result.metrics

        return TestDataDriftResult(
            name=result.name,
            description=result.description,
            status=result.status,
            features={feature: (data.stattest_name, np.round(data.p_value, 3), data.threshold, str(data.drift_detected))
                      for feature, data in metrics.features.items()}
        )


class TestNumberOfDriftedFeatures(BaseDataDriftMetricsTest):
    name = "Test Number of Drifted Features"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().analyzer_result.metrics.n_drifted_features

    def get_description(self, value: Number) -> str:
        return f"Number of drifted features is {value}"


class TestShareOfDriftedFeatures(BaseDataDriftMetricsTest):
    name = "Test Share of Drifted Features"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().analyzer_result.metrics.share_drifted_features

    def get_description(self, value: Number) -> str:
        return f"Share drifted features is {value}"


class TestFeatureValueDrift(BaseDataDriftMetricsTest):
    name = "Test a Feature Drift Value"
    feature_name: str

    def __init__(
        self,
        feature_name: str,
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        metric: Optional[DataDriftMetrics] = None
    ):
        self.feature_name = feature_name
        super().__init__(
            eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in, metric=metric
        )

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().analyzer_result.metrics.features[self.feature_name].p_value

    def get_description(self, value: Number) -> str:
        return f"Drift score for feature {self.feature_name} is {np.round(value, 3)}"


@default_renderer(test_type=TestNumberOfDriftedFeatures)
class TestNumberOfDriftedFeaturesRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfDriftedFeatures) -> dict:
        base = super().render_json(obj)
        base['features'] = {feature: dict(stattest=data[0], score=np.round(data[1],  3), threshold=data[2], 
                            data_drift=data[3])
                            for feature, data in obj.get_result().features.items()}
        return base

    def render_html(self, obj: TestNumberOfDriftedFeatures) -> TestHtmlInfo:
        info = super().render_html(obj)
        info.details = [
            DetailsInfo(
                id="drift_table",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={
                        "header": ["Feature name", "Stattest", "Drift score", "Threshold", "Data Drift"],
                        "data": [[feature] + list(data) for feature, data in obj.get_result().features.items()]
                    },
                    size=2,
                )
            ),
        ]
        return info

@default_renderer(test_type=TestShareOfDriftedFeatures)
class TestShareOfDriftedFeaturesRenderer(TestRenderer):
    def render_json(self, obj: TestShareOfDriftedFeatures) -> dict:
        base = super().render_json(obj)
        base['features'] = {feature: dict(stattest=data[0], score=np.round(data[1],  3), threshold=data[2], 
                            data_drift=data[3])
                            for feature, data in obj.get_result().features.items()}
        return base

    def render_html(self, obj: TestShareOfDriftedFeatures) -> TestHtmlInfo:
        info = super().render_html(obj)
        info.details = [
            DetailsInfo(
                id="drift_table",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={
                        "header": ["Feature name", "Stattest", "Drift score", "Threshold", "Data Drift"],
                        "data": [[feature] + list(data) for feature, data in obj.get_result().features.items()]
                    },
                    size=2,
                )
            ),
        ]
        return info

@default_renderer(test_type=TestFeatureValueDrift)
class TestFeatureValueDriftRenderer(TestRenderer):
    def render_json(self, obj: TestFeatureValueDrift) -> dict:
        feature_name = obj.feature_name
        data = obj.get_result().features[feature_name]
        base = super().render_json(obj)
        base = {feature_name: dict(stattest=data[0], score=np.round(data[1],  3), threshold=data[2], 
                            data_drift=data[3])}
        return base

    def render_html(self, obj: TestNumberOfDriftedFeatures) -> TestHtmlInfo:
        feature_name = obj.feature_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plots[feature_name]['current']
        ref_distr = obj.metric.get_result().distr_for_plots[feature_name]['reference']
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
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info
