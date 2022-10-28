from abc import ABC
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import dataclasses
import numpy as np
import pandas as pd

from evidently.metrics import DataDriftTable
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import DetailsInfo
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import table_data
from evidently.renderers.render_utils import get_distribution_plot_figure
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import GroupData
from evidently.tests.base_test import GroupingTypes
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestResult
from evidently.tests.base_test import TestValueCondition
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.generators import BaseGenerator
from evidently.utils.types import Numeric

DATA_DRIFT_GROUP = GroupData("data_drift", "Data Drift", "")
GroupingTypes.TestGroup.add_value(DATA_DRIFT_GROUP)


@dataclasses.dataclass
class TestDataDriftResult(TestResult):
    features: Dict[str, Tuple[str, float, float]] = dataclasses.field(default_factory=dict)


class BaseDataDriftMetricsTest(BaseCheckValueTest, ABC):
    group = DATA_DRIFT_GROUP.id
    metric: DataDriftTable

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
        metric: Optional[DataDriftTable] = None,
        options: Optional[DataDriftOptions] = None,
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataDriftTable(options=options)

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

    def check(self):
        result = super().check()
        metrics = self.metric.get_result()

        return TestDataDriftResult(
            name=result.name,
            description=result.description,
            status=result.status,
            features={
                feature: (
                    data.stattest_name,
                    np.round(data.drift_score, 3),
                    data.threshold,
                    "Detected" if data.drift_detected else "Not Detected",
                )
                for feature, data in metrics.drift_by_columns.items()
            },
        )


class TestNumberOfDriftedColumns(BaseDataDriftMetricsTest):
    name = "Number of Drifted Features"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        else:
            return TestValueCondition(lt=max(0, self.metric.get_result().number_of_columns // 3))

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().number_of_drifted_columns

    def get_description(self, value: Numeric) -> str:
        n_features = self.metric.get_result().number_of_columns
        return (
            f"The drift is detected for {value} out of {n_features} features. "
            f"The test threshold is {self.get_condition()}."
        )


class TestShareOfDriftedColumns(BaseDataDriftMetricsTest):
    name = "Share of Drifted Columns"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        else:
            return TestValueCondition(lt=0.3)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().share_of_drifted_columns

    def get_description(self, value: Numeric) -> str:
        n_drifted_features = self.metric.get_result().number_of_drifted_columns
        n_features = self.metric.get_result().number_of_columns
        return (
            f"The drift is detected for {value * 100:.3g}% features "
            f"({n_drifted_features} out of {n_features}). The test threshold is {self.get_condition()}"
        )


class TestColumnValueDrift(Test):
    name = "Drift per Column"
    group = DATA_DRIFT_GROUP.id
    metric: DataDriftTable
    column_name: str

    def __init__(
        self,
        column_name: str,
        metric: Optional[DataDriftTable] = None,
        options: Optional[DataDriftOptions] = None,
    ):
        self.column_name = column_name

        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataDriftTable(options=options)

    def check(self):
        drift_info = self.metric.get_result()

        if self.column_name not in drift_info.drift_by_columns:
            result_status = TestResult.ERROR
            description = f"Cannot find column {self.column_name} in the dataset"

        else:
            p_value = np.round(drift_info.drift_by_columns[self.column_name].drift_score, 3)
            stattest_name = drift_info.drift_by_columns[self.column_name].stattest_name
            threshold = drift_info.drift_by_columns[self.column_name].threshold
            description = (
                f"The drift score for the feature **{self.column_name}** is {p_value:.3g}. "
                f"The drift detection method is {stattest_name}. "
                f"The drift detection threshold is {threshold}."
            )

            if not drift_info.drift_by_columns[self.column_name].drift_detected:
                result_status = TestResult.SUCCESS

            else:
                result_status = TestResult.FAIL

        return TestResult(
            name=self.name,
            description=description,
            status=result_status,
            groups={
                GroupingTypes.ByFeature.id: self.column_name,
            },
        )


class TestAllFeaturesValueDrift(BaseGenerator):
    """Create value drift tests for numeric and category features"""

    def generate(self, columns_info: DatasetColumns) -> List[TestColumnValueDrift]:
        return [
            TestColumnValueDrift(column_name=name)
            for name in columns_info.get_all_features_list(include_datetime_feature=False)
        ]


class TestCustomFeaturesValueDrift(BaseGenerator):
    """Create value drift tests for specified features"""

    features: List[str]

    def __init__(self, features: List[str]):
        self.features = features

    def generate(self, columns_info: DatasetColumns) -> List[TestColumnValueDrift]:
        return [TestColumnValueDrift(column_name=name) for name in self.features]


@default_renderer(wrap_type=TestNumberOfDriftedColumns)
class TestNumberOfDriftedColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfDriftedColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["features"] = {
            feature: {"stattest": data[0], "score": np.round(data[1], 3), "threshold": data[2], "data_drift": data[3]}
            for feature, data in obj.get_result().features.items()
        }
        return base

    def render_html(self, obj: TestNumberOfDriftedColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        df = pd.DataFrame(
            data=[[feature] + list(data) for feature, data in obj.get_result().features.items()],
            columns=["Feature name", "Stattest", "Drift score", "Threshold", "Data Drift"],
        )
        df = df.sort_values("Data Drift")
        info.with_details(title="Drift Table", info=table_data(column_names=df.columns.to_list(), data=df.values))
        return info


@default_renderer(wrap_type=TestShareOfDriftedColumns)
class TestShareOfDriftedColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestShareOfDriftedColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["features"] = {
            feature: {"stattest": data[0], "score": np.round(data[1], 3), "threshold": data[2], "data_drift": data[3]}
            for feature, data in obj.get_result().features.items()
        }
        return base

    def render_html(self, obj: TestShareOfDriftedColumns) -> TestHtmlInfo:
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


@default_renderer(wrap_type=TestColumnValueDrift)
class TestColumnValueDriftRenderer(TestRenderer):
    def render_json(self, obj: TestColumnValueDrift) -> dict:
        feature_name = obj.column_name
        drift_data = obj.metric.get_result().drift_by_columns[feature_name]
        base = super().render_json(obj)
        base["parameters"]["features"] = {
            feature_name: {
                "stattest": drift_data.stattest_name,
                "score": np.round(drift_data.drift_score, 3),
                "threshold": drift_data.threshold,
                "data_drift": drift_data.drift_detected,
            }
        }
        return base

    def render_html(self, obj: TestColumnValueDrift) -> TestHtmlInfo:
        result = obj.metric.get_result()
        column_name = obj.column_name
        info = super().render_html(obj)
        column_info = result.drift_by_columns[column_name]
        fig = get_distribution_plot_figure(
            current_distribution=column_info.current_distribution,
            reference_distribution=column_info.reference_distribution,
            color_options=self.color_options,
        )
        info.with_details(f"{column_name}", plotly_figure(title="", figure=fig))
        return info
