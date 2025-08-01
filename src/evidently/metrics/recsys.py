from abc import ABC
from typing import ClassVar
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.core.metric_types import TMetricResult
from evidently.core.report import Context
from evidently.core.report import Report
from evidently.core.report import _default_input_data_generator
from evidently.legacy.base_metric import InputData
from evidently.legacy.metrics import FBetaTopKMetric
from evidently.legacy.metrics import HitRateKMetric
from evidently.legacy.metrics import MAPKMetric
from evidently.legacy.metrics import MRRKMetric
from evidently.legacy.metrics import NDCGKMetric
from evidently.legacy.metrics import PrecisionTopKMetric
from evidently.legacy.metrics import RecallTopKMetric
from evidently.legacy.metrics.recsys.base_top_k import TopKMetric
from evidently.legacy.metrics.recsys.base_top_k import TopKMetricResult
from evidently.legacy.metrics.recsys.scores_distribution import ScoreDistribution as ScoreDistributionLegacy
from evidently.legacy.metrics.recsys.scores_distribution import ScoreDistributionResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.utils.data_preprocessing import create_data_definition
from evidently.metrics._legacy import LegacyMetricCalculation
from evidently.tests import Reference
from evidently.tests import eq


class TopKBase(SingleValueMetric):
    k: int
    min_rel_score: Optional[int] = None
    no_feedback_users: bool = False
    ranking_name: str = "default"

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


TTopKBase = TypeVar("TTopKBase", bound=TopKBase)


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


class LegacyTopKCalculation(
    LegacyMetricCalculation[
        SingleValue,
        TTopKBase,
        TopKMetricResult,
        TopKMetric,
    ],
    SingleValueCalculation,
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
        current = self.result(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, self.result(legacy_result.reference[legacy_result.k - 1])

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_ranking_input_data(context, task_name)


class NDCG(TopKBase):
    pass


class NDCGCalculation(LegacyTopKCalculation[NDCG]):
    __legacy_metric_type__: ClassVar = NDCGKMetric

    def display_name(self) -> str:
        return "NDCG@k"


class MRR(TopKBase):
    pass


class MRRCalculation(LegacyTopKCalculation[MRR]):
    __legacy_metric_type__: ClassVar = MRRKMetric

    def display_name(self) -> str:
        return "MRR@k"


class HitRate(TopKBase):
    pass


class HitRateCalculation(LegacyTopKCalculation[HitRate]):
    __legacy_metric_type__: ClassVar = HitRateKMetric

    def display_name(self) -> str:
        return "HitRate@k"


class MAP(TopKBase):
    pass


class MAPCalculation(LegacyTopKCalculation[MAP]):
    __legacy_metric_type__: ClassVar = MAPKMetric

    def display_name(self) -> str:
        return "MAP@k"


class RecallTopK(TopKBase):
    pass


class RecallTopKCalculation(LegacyTopKCalculation[RecallTopK]):
    __legacy_metric_type__: ClassVar = RecallTopKMetric

    def display_name(self) -> str:
        return "Recall@k"


class PrecisionTopK(TopKBase):
    pass


class PrecisionTopKCalculation(LegacyTopKCalculation[PrecisionTopK]):
    __legacy_metric_type__: ClassVar = PrecisionTopKMetric

    def display_name(self) -> str:
        return "Precision@k"


class FBetaTopK(TopKBase):
    beta: Optional[float] = 1.0


class FBetaTopKCalculation(LegacyTopKCalculation[FBetaTopK]):
    def display_name(self) -> str:
        return f"F{self.metric.beta}@k"

    def legacy_metric(self):
        return FBetaTopKMetric(
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
        if legacy_result.reference_entropy is None:
            return current
        return current, self.result(legacy_result.reference_entropy)

    def display_name(self) -> str:
        return "Score distribution"

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
