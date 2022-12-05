from abc import ABC
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import dataclasses
import numpy as np
import pandas as pd

from evidently.calculations.stattests import PossibleStatTestType
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import DataDriftTable
from evidently.model.widget import BaseWidgetInfo
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
from evidently.utils.data_drift_utils import resolve_stattest_threshold
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
        columns: Optional[List[str]] = None,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
        stattest: Optional[PossibleStatTestType] = None,
        cat_stattest: Optional[PossibleStatTestType] = None,
        num_stattest: Optional[PossibleStatTestType] = None,
        per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
        stattest_threshold: Optional[float] = None,
        cat_stattest_threshold: Optional[float] = None,
        num_stattest_threshold: Optional[float] = None,
        per_column_stattest_threshold: Optional[Dict[str, float]] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        self.metric = DataDriftTable(
            columns=columns,
            stattest=stattest,
            cat_stattest=cat_stattest,
            num_stattest=num_stattest,
            per_column_stattest=per_column_stattest,
            stattest_threshold=stattest_threshold,
            cat_stattest_threshold=cat_stattest_threshold,
            num_stattest_threshold=num_stattest_threshold,
            per_column_stattest_threshold=per_column_stattest_threshold,
        )

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


class TestColumnDrift(Test):
    name = "Drift per Column"
    group = DATA_DRIFT_GROUP.id
    metric: ColumnDriftMetric
    column_name: str

    def __init__(
        self,
        column_name: str,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
    ):
        self.column_name = column_name
        self.metric = ColumnDriftMetric(
            column_name=column_name, stattest=stattest, stattest_threshold=stattest_threshold
        )

    def check(self):
        drift_info = self.metric.get_result()

        p_value = np.round(drift_info.drift_score, 3)
        stattest_name = drift_info.stattest_name
        threshold = drift_info.stattest_threshold
        description = (
            f"The drift score for the feature **{self.column_name}** is {p_value:.3g}. "
            f"The drift detection method is {stattest_name}. "
            f"The drift detection threshold is {threshold}."
        )

        if not drift_info.drift_detected:
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

    columns: Optional[List[str]]
    stattest: Optional[PossibleStatTestType]
    cat_stattest: Optional[PossibleStatTestType]
    num_stattest: Optional[PossibleStatTestType]
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]]
    stattest_threshold: Optional[float]
    cat_stattest_threshold: Optional[float]
    num_stattest_threshold: Optional[float]
    per_column_stattest_threshold: Optional[Dict[str, float]]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        stattest: Optional[PossibleStatTestType] = None,
        cat_stattest: Optional[PossibleStatTestType] = None,
        num_stattest: Optional[PossibleStatTestType] = None,
        per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
        stattest_threshold: Optional[float] = None,
        cat_stattest_threshold: Optional[float] = None,
        num_stattest_threshold: Optional[float] = None,
        per_column_stattest_threshold: Optional[Dict[str, float]] = None,
    ):
        self.columns = columns
        self.stattest = stattest
        self.cat_stattest = cat_stattest
        self.num_stattest = num_stattest
        self.per_column_stattest = per_column_stattest
        self.stattest_threshold = stattest_threshold
        self.cat_stattest_threshold = cat_stattest_threshold
        self.num_stattest_threshold = num_stattest_threshold
        self.per_column_stattest_threshold = per_column_stattest_threshold

    def generate(self, columns_info: DatasetColumns) -> List[TestColumnDrift]:
        results = []
        for name in columns_info.cat_feature_names:
            if self.columns and name not in self.columns:
                continue
            stattest, threshold = resolve_stattest_threshold(
                name,
                "cat",
                self.stattest,
                self.cat_stattest,
                self.num_stattest,
                self.per_column_stattest,
                self.stattest_threshold,
                self.cat_stattest_threshold,
                self.num_stattest_threshold,
                self.per_column_stattest_threshold,
            )
            results.append(TestColumnDrift(column_name=name, stattest=stattest, stattest_threshold=threshold))
        for name in columns_info.num_feature_names:
            if self.columns and name not in self.columns:
                continue
            stattest, threshold = resolve_stattest_threshold(
                name,
                "num",
                self.stattest,
                self.cat_stattest,
                self.num_stattest,
                self.per_column_stattest,
                self.stattest_threshold,
                self.cat_stattest_threshold,
                self.num_stattest_threshold,
                self.per_column_stattest_threshold,
            )
            results.append(TestColumnDrift(column_name=name, stattest=stattest, stattest_threshold=threshold))
        return results


class TestCustomFeaturesValueDrift(BaseGenerator):
    """Create value drift tests for specified features"""

    features: List[str]
    stattest: Optional[PossibleStatTestType] = None
    cat_stattest: Optional[PossibleStatTestType] = None
    num_stattest: Optional[PossibleStatTestType] = None
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None
    stattest_threshold: Optional[float] = None
    cat_stattest_threshold: Optional[float] = None
    num_stattest_threshold: Optional[float] = None
    per_column_stattest_threshold: Optional[Dict[str, float]] = None

    def __init__(
        self,
        features: List[str],
        stattest: Optional[PossibleStatTestType] = None,
        cat_stattest: Optional[PossibleStatTestType] = None,
        num_stattest: Optional[PossibleStatTestType] = None,
        per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
        stattest_threshold: Optional[float] = None,
        cat_stattest_threshold: Optional[float] = None,
        num_stattest_threshold: Optional[float] = None,
        per_column_stattest_threshold: Optional[Dict[str, float]] = None,
    ):
        self.features = features
        self.stattest = stattest
        self.cat_stattest = cat_stattest
        self.num_stattest = num_stattest
        self.per_column_stattest = per_column_stattest
        self.stattest_threshold = stattest_threshold
        self.cat_stattest_threshold = cat_stattest_threshold
        self.num_features_threshold = num_stattest_threshold
        self.per_feature_threshold = per_column_stattest_threshold

    def generate(self, columns_info: DatasetColumns) -> List[TestColumnDrift]:
        result = []
        for name in self.features:
            stattest, threshold = resolve_stattest_threshold(
                name,
                "cat"
                if name in columns_info.cat_feature_names
                else "num"
                if columns_info.num_feature_names
                else "datetime",
                self.stattest,
                self.cat_stattest,
                self.num_stattest,
                self.per_column_stattest,
                self.stattest_threshold,
                self.cat_stattest_threshold,
                self.num_stattest_threshold,
                self.per_column_stattest_threshold,
            )
            result.append(
                TestColumnDrift(
                    column_name=name,
                    stattest=stattest,
                    stattest_threshold=threshold,
                )
            )
        return result


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


@default_renderer(wrap_type=TestColumnDrift)
class TestColumnDriftRenderer(TestRenderer):
    def render_json(self, obj: TestColumnDrift) -> dict:
        feature_name = obj.column_name
        drift_data = obj.metric.get_result()
        base = super().render_json(obj)
        base["parameters"]["features"] = {
            feature_name: {
                "stattest_name": drift_data.stattest_name,
                "score": np.round(drift_data.drift_score, 3),
                "stattest_threshold": drift_data.stattest_threshold,
                "data_drift": drift_data.drift_detected,
            }
        }
        return base

    def render_html(self, obj: TestColumnDrift) -> TestHtmlInfo:
        result = obj.metric.get_result()
        column_name = obj.column_name
        info = super().render_html(obj)
        fig = get_distribution_plot_figure(
            current_distribution=result.current_distribution,
            reference_distribution=result.reference_distribution,
            color_options=self.color_options,
        )
        info.with_details(f"{column_name}", plotly_figure(title="", figure=fig))
        return info
