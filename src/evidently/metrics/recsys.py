from abc import ABC
from typing import ClassVar
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import pandas as pd

from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import DataframeMetric
from evidently.core.metric_types import DataframeValue
from evidently.core.metric_types import Metric
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.core.metric_types import TMetricResult
from evidently.core.report import Context
from evidently.core.report import Report
from evidently.core.report import _default_input_data_generator
from evidently.legacy.base_metric import InputData
from evidently.legacy.metrics import DiversityMetric as LegacyDiversityMetric
from evidently.legacy.metrics import FBetaTopKMetric as LegacyFBetaTopKMetric
from evidently.legacy.metrics import HitRateKMetric as LegacyHitRateKMetric
from evidently.legacy.metrics import ItemBiasMetric as LegacyItemBiasMetric
from evidently.legacy.metrics import MAPKMetric as LegacyMAPKMetric
from evidently.legacy.metrics import MRRKMetric as LegacyMRRKMetric
from evidently.legacy.metrics import NDCGKMetric as LegacyNDCGKMetric
from evidently.legacy.metrics import NoveltyMetric as LegacyNoveltyMetric
from evidently.legacy.metrics import PersonalizationMetric as LegacyPersonalizationMetric
from evidently.legacy.metrics import PopularityBias as LegacyPopularityBias
from evidently.legacy.metrics import PrecisionTopKMetric as LegacyPrecisionTopKMetric
from evidently.legacy.metrics import RecallTopKMetric as LegacyRecallTopKMetric
from evidently.legacy.metrics import RecCasesTable as LegacyRecCasesTable
from evidently.legacy.metrics import SerendipityMetric as LegacySerendipityMetric
from evidently.legacy.metrics import UserBiasMetric as LegacyUserBiasMetric
from evidently.legacy.metrics.recsys.base_top_k import TopKMetric
from evidently.legacy.metrics.recsys.base_top_k import TopKMetricResult
from evidently.legacy.metrics.recsys.diversity import DiversityMetricResult
from evidently.legacy.metrics.recsys.item_bias import ItemBiasMetricResult
from evidently.legacy.metrics.recsys.novelty import NoveltyMetricResult
from evidently.legacy.metrics.recsys.personalisation import PersonalizationMetricResult
from evidently.legacy.metrics.recsys.popularity_bias import PopularityBiasResult
from evidently.legacy.metrics.recsys.rec_examples import RecCasesTableResults
from evidently.legacy.metrics.recsys.scores_distribution import ScoreDistribution as ScoreDistributionLegacy
from evidently.legacy.metrics.recsys.scores_distribution import ScoreDistributionResult
from evidently.legacy.metrics.recsys.serendipity import SerendipityMetricResult
from evidently.legacy.metrics.recsys.user_bias import UserBiasMetricResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.utils.data_preprocessing import create_data_definition
from evidently.metrics._legacy import LegacyMetricCalculation
from evidently.tests import Reference
from evidently.tests import eq


def _gen_ranking_input_data(context: "Context", task_name: Optional[str]) -> InputData:
    default_data = _default_input_data_generator(context, None)
    if task_name is None:
        return default_data
    ranking = context.data_definition.get_ranking(task_name)
    if ranking is not None:
        default_data.column_mapping.user_id = ranking.user_id
        default_data.column_mapping.item_id = ranking.item_id
        default_data.column_mapping.recommendations_type = ranking.recommendations_type
        default_data.column_mapping.target = ranking.target
        default_data.column_mapping.prediction = ranking.prediction
        default_data.data_definition = create_data_definition(
            default_data.reference_data,
            default_data.current_data,
            default_data.column_mapping,
        )
    return default_data


class TopKBase(DataframeMetric):
    k: int
    min_rel_score: Optional[int] = None
    no_feedback_users: bool = False
    ranking_name: str = "default"


TTopKBase = TypeVar("TTopKBase", bound=TopKBase)


class LegacyTopKCalculation(
    LegacyMetricCalculation[
        DataframeValue,
        TTopKBase,
        TopKMetricResult,
        TopKMetric,
    ],
    Generic[TTopKBase],
    ABC,
):
    __legacy_metric_type__: ClassVar[Type[TopKMetric]]

    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self):
        return self.__legacy_metric_type__(
            k=self.metric.k, min_rel_score=self.metric.min_rel_score, no_feedback_users=self.metric.no_feedback_users
        )

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current_series = legacy_result.current
        current_df = pd.DataFrame(
            {
                "rank": current_series.index + 1,  # Convert 0-based to 1-based ranking
                "value": current_series.values,
            }
        )
        current_value = DataframeValue(display_name=self.display_name(), value=current_df)
        current_value.widget = render

        if legacy_result.reference is None:
            return current_value

        reference_series = legacy_result.reference
        reference_df = pd.DataFrame(
            {
                "rank": reference_series.index + 1,  # Convert 0-based to 1-based ranking
                "value": reference_series.values,
            }
        )
        reference_value = DataframeValue(display_name=self.display_name(), value=reference_df)
        reference_value.widget = []

        return current_value, reference_value

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class NDCG(TopKBase):
    pass


class NDCGCalculation(LegacyTopKCalculation[NDCG]):
    __legacy_metric_type__: ClassVar = LegacyNDCGKMetric

    def display_name(self) -> str:
        return "NDCG@k"


class MRR(TopKBase):
    pass


class MRRCalculation(LegacyTopKCalculation[MRR]):
    __legacy_metric_type__: ClassVar = LegacyMRRKMetric

    def display_name(self) -> str:
        return "MRR@k"


class HitRate(TopKBase):
    pass


class HitRateCalculation(LegacyTopKCalculation[HitRate]):
    __legacy_metric_type__: ClassVar = LegacyHitRateKMetric

    def display_name(self) -> str:
        return "HitRate@k"


class MAP(TopKBase):
    pass


class MAPCalculation(LegacyTopKCalculation[MAP]):
    __legacy_metric_type__: ClassVar = LegacyMAPKMetric

    def display_name(self) -> str:
        return "MAP@k"


class RecallTopK(TopKBase):
    pass


class RecallTopKCalculation(LegacyTopKCalculation[RecallTopK]):
    __legacy_metric_type__: ClassVar = LegacyRecallTopKMetric

    def display_name(self) -> str:
        return "Recall@k"


class PrecisionTopK(TopKBase):
    pass


class PrecisionTopKCalculation(LegacyTopKCalculation[PrecisionTopK]):
    __legacy_metric_type__: ClassVar = LegacyPrecisionTopKMetric

    def display_name(self) -> str:
        return "Precision@k"


class FBetaTopK(TopKBase):
    beta: Optional[float] = 1.0


class FBetaTopKCalculation(LegacyTopKCalculation[FBetaTopK]):
    def display_name(self) -> str:
        return f"F{self.metric.beta}@k"

    def legacy_metric(self):
        return LegacyFBetaTopKMetric(
            k=self.metric.k,
            min_rel_score=self.metric.min_rel_score,
            no_feedback_users=self.metric.no_feedback_users,
            beta=self.metric.beta,
        )


class ScoreDistribution(SingleValueMetric):
    k: int
    ranking_name: str = "default"

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class ScoreDistributionCalculation(
    LegacyMetricCalculation[SingleValue, ScoreDistribution, ScoreDistributionResult, ScoreDistributionLegacy],
    SingleValueCalculation,
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> ScoreDistributionLegacy:
        return ScoreDistributionLegacy(k=self.metric.k)

    def calculate_value(
        self, context: "Context", legacy_result: ScoreDistributionResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = self.result(legacy_result.current_entropy)
        current.widget = render
        if legacy_result.reference_entropy is None:
            return current
        return current, self.result(legacy_result.reference_entropy)

    def display_name(self) -> str:
        return "Score distribution"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class PopularityBiasMetric(SingleValueMetric):
    k: int
    normalize_arp: bool = False
    ranking_name: str = "default"
    metric: Literal["arp", "coverage", "gini"] = "arp"

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class PopularityBiasCalculation(
    LegacyMetricCalculation[SingleValue, PopularityBiasMetric, PopularityBiasResult, LegacyPopularityBias],
    SingleValueCalculation,
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> LegacyPopularityBias:
        return LegacyPopularityBias(k=self.metric.k, normalize_arp=self.metric.normalize_arp)

    def calculate_value(
        self, context: "Context", legacy_result: PopularityBiasResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        # PopularityBiasResult has: current_apr, current_coverage, current_gini
        if self.metric.metric == "coverage":
            current = self.result(legacy_result.current_coverage)
            current.widget = render
            if legacy_result.reference_coverage is None:
                return current
            return current, self.result(legacy_result.reference_coverage)
        if self.metric.metric == "gini":
            current = self.result(legacy_result.current_gini)
            current.widget = render
            if legacy_result.reference_gini is None:
                return current
            return current, self.result(legacy_result.reference_gini)
        # default to apr
        current = self.result(legacy_result.current_apr)
        current.widget = render
        if legacy_result.reference_apr is None:
            return current
        return current, self.result(legacy_result.reference_apr)

    def display_name(self) -> str:
        return f"Popularity Bias ({self.metric.metric})"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class Personalization(SingleValueMetric):
    k: int
    ranking_name: str = "default"

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class PersonalizationCalculation(
    LegacyMetricCalculation[SingleValue, Personalization, PersonalizationMetricResult, LegacyPersonalizationMetric],
    SingleValueCalculation,
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> LegacyPersonalizationMetric:
        return LegacyPersonalizationMetric(k=self.metric.k)

    def calculate_value(
        self, context: "Context", legacy_result: PersonalizationMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = self.result(legacy_result.current_value)
        current.widget = render
        if legacy_result.reference_value is None:
            return current
        return current, self.result(legacy_result.reference_value)

    def display_name(self) -> str:
        return "Personalization"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class Diversity(SingleValueMetric):
    k: int
    item_features: List[str]
    ranking_name: str = "default"

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class DiversityCalculation(
    LegacyMetricCalculation[SingleValue, Diversity, DiversityMetricResult, LegacyDiversityMetric],
    SingleValueCalculation,
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> LegacyDiversityMetric:
        return LegacyDiversityMetric(k=self.metric.k, item_features=self.metric.item_features)

    def calculate_value(
        self, context: "Context", legacy_result: DiversityMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = self.result(legacy_result.current_value)
        current.widget = render
        if legacy_result.reference_value is None:
            return current
        return current, self.result(legacy_result.reference_value)

    def display_name(self) -> str:
        return "Diversity"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class Serendipity(SingleValueMetric):
    k: int
    item_features: List[str]
    ranking_name: str = "default"

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class SerendipityCalculation(
    LegacyMetricCalculation[SingleValue, Serendipity, SerendipityMetricResult, LegacySerendipityMetric],
    SingleValueCalculation,
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> LegacySerendipityMetric:
        return LegacySerendipityMetric(k=self.metric.k, item_features=self.metric.item_features)

    def calculate_value(
        self, context: "Context", legacy_result: SerendipityMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = self.result(legacy_result.current_value)
        current.widget = render
        if legacy_result.reference_value is None:
            return current
        return current, self.result(legacy_result.reference_value)

    def display_name(self) -> str:
        return "Serendipity"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class Novelty(SingleValueMetric):
    k: int
    ranking_name: str = "default"

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class NoveltyCalculation(
    LegacyMetricCalculation[SingleValue, Novelty, NoveltyMetricResult, LegacyNoveltyMetric],
    SingleValueCalculation,
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> LegacyNoveltyMetric:
        return LegacyNoveltyMetric(k=self.metric.k)

    def calculate_value(
        self, context: "Context", legacy_result: NoveltyMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = self.result(legacy_result.current_value)
        current.widget = render
        if legacy_result.reference_value is None:
            return current
        return current, self.result(legacy_result.reference_value)

    def display_name(self) -> str:
        return "Novelty"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class ItemBias(Metric):
    k: int
    column_name: str
    distribution: Literal["default", "train"] = "default"
    ranking_name: str = "default"

    def get_bound_tests(self, context: "Context") -> List[BoundTest]:
        return []


class ItemBiasCalculation(
    LegacyMetricCalculation[DataframeValue, ItemBias, ItemBiasMetricResult, LegacyItemBiasMetric],
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> LegacyItemBiasMetric:
        return LegacyItemBiasMetric(k=self.metric.k, column_name=self.metric.column_name)

    def calculate_value(
        self, context: "Context", legacy_result: ItemBiasMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        return _bias_result(self.metric, legacy_result, render, self.display_name())

    def display_name(self) -> str:
        return f"Item Bias ({self.metric.column_name}, {self.metric.distribution})"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class UserBias(Metric):
    column_name: str
    distribution: Literal["default", "train"] = "default"
    ranking_name: str = "default"

    def get_bound_tests(self, context: "Context") -> List[BoundTest]:
        return []


class UserBiasCalculation(
    LegacyMetricCalculation[DataframeValue, UserBias, UserBiasMetricResult, LegacyUserBiasMetric],
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> LegacyUserBiasMetric:
        return LegacyUserBiasMetric(column_name=self.metric.column_name)

    def calculate_value(
        self, context: "Context", legacy_result: UserBiasMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        return _bias_result(self.metric, legacy_result, render, self.display_name())

    def display_name(self) -> str:
        return f"User Bias ({self.metric.column_name}, {self.metric.distribution})"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


def _bias_result(
    metric: Union[ItemBias, UserBias],
    legacy_result: Union[ItemBiasMetricResult, UserBiasMetricResult],
    render: List[BaseWidgetInfo],
    display_name: str,
) -> TMetricResult:
    if metric.distribution == "train":
        current_distr = legacy_result.current_train_distr
        reference_distr = legacy_result.reference_train_distr
    else:  # default
        current_distr = legacy_result.current_distr
        reference_distr = legacy_result.reference_distr

    # Fix for legacy bug: x (bin edges) and y (counts) have different lengths
    # We need to use bin centers instead of bin edges
    if current_distr is not None:
        if len(current_distr.x) == len(current_distr.y) + 1:
            # x is bin edges, y is counts - convert to bin centers
            bin_centers = (current_distr.x[:-1] + current_distr.x[1:]) / 2  #  type: ignore[operator]
            current_df = pd.DataFrame({"x": bin_centers, "y": current_distr.y})
        else:
            # Already correct lengths
            current_df = pd.DataFrame({"x": current_distr.x, "y": current_distr.y})
    else:
        current_df = pd.DataFrame({"x": [], "y": []})

    current_value = DataframeValue(display_name=display_name, value=current_df)
    current_value.widget = render

    if reference_distr is None:
        return current_value

    # Apply same fix to reference distribution
    if reference_distr is not None:
        if len(reference_distr.x) == len(reference_distr.y) + 1:
            # x is bin edges, y is counts - convert to bin centers
            ref_bin_centers = (reference_distr.x[:-1] + reference_distr.x[1:]) / 2  #  type: ignore[operator]
            reference_df = pd.DataFrame({"x": ref_bin_centers, "y": reference_distr.y})
        else:
            # Already correct lengths
            reference_df = pd.DataFrame({"x": reference_distr.x, "y": reference_distr.y})
    else:
        reference_df = pd.DataFrame({"x": [], "y": []})

    reference_value = DataframeValue(display_name=display_name, value=reference_df)
    reference_value.widget = []
    return current_value, reference_value


class RecCasesTable(DataframeMetric):
    user_ids: Optional[List[Union[int, str]]] = None
    display_features: Optional[List[str]] = None
    ranking_name: str = "default"


class RecCasesTableCalculation(
    LegacyMetricCalculation[DataframeValue, RecCasesTable, RecCasesTableResults, LegacyRecCasesTable],
):
    def task_name(self) -> Optional[str]:
        return self.metric.ranking_name

    def legacy_metric(self) -> LegacyRecCasesTable:
        return LegacyRecCasesTable(user_ids=self.metric.user_ids, display_features=self.metric.display_features)

    def calculate_value(
        self, context: "Context", legacy_result: RecCasesTableResults, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        # RecCasesTableResults has current: Dict[str, pd.DataFrame] and reference: Dict[str, pd.DataFrame]
        # Each dataframe contains [prediction_name, item_id] + display_features columns
        # We need to merge all dataframes with an additional user_id column
        current_dfs = []
        for user_id, df in legacy_result.current.items():
            df_with_user = df.copy()
            df_with_user["user_id"] = user_id
            current_dfs.append(df_with_user)

        if current_dfs:
            current_merged = pd.concat(current_dfs, ignore_index=True)
        else:
            current_merged = pd.DataFrame()

        current_value = DataframeValue(display_name=self.display_name(), value=current_merged)
        current_value.widget = render

        if not legacy_result.reference:
            return current_value

        reference_dfs = []
        for user_id, df in legacy_result.reference.items():
            df_with_user = df.copy()
            df_with_user["user_id"] = user_id
            reference_dfs.append(df_with_user)

        if reference_dfs:
            reference_merged = pd.concat(reference_dfs, ignore_index=True)
        else:
            reference_merged = pd.DataFrame()

        reference_value = DataframeValue(display_name=self.display_name(), value=reference_merged)
        reference_value.widget = []

        return current_value, reference_value

    def display_name(self) -> str:
        return "Recommendation Cases Table"

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


def main():
    import pandas as pd

    def create_snapshot(i):
        df = pd.DataFrame(
            {
                "user_id": [i % 3 for i in range(i + 5)],
                "target": [0.5 for i in range(i + 5)],
                "prediction": [0.5 for i in range(i + 5)],
            }
        )
        from evidently.core.datasets import DataDefinition
        from evidently.core.datasets import Dataset
        from evidently.core.datasets import Recsys

        dataset = Dataset.from_pandas(
            df, data_definition=DataDefinition(numerical_columns=["target", "prediction"], ranking=[Recsys()])
        )
        report = Report(
            [
                NDCG(k=3, no_feedback_users=True),
                MRR(k=3),
                HitRate(k=3),
                ScoreDistribution(k=3),
                MAP(k=3),
                RecallTopK(k=3),
                PrecisionTopK(k=3),
                FBetaTopK(k=3),
            ]
        )
        snapshot_v2 = report.run(dataset, None)

        from evidently.ui.backport import snapshot_v2_to_v1

        snapshot_v1 = snapshot_v2_to_v1(snapshot_v2)
        return snapshot_v1

    sn = create_snapshot(10)
    sn.save("ndcg.json")


if __name__ == "__main__":
    main()
