from abc import ABC
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueMetric
from evidently.future.metric_types import TMetricResult
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.report import Context
from evidently.future.report import Report
from evidently.metrics import FBetaTopKMetric
from evidently.metrics import HitRateKMetric
from evidently.metrics import MAPKMetric
from evidently.metrics import MRRKMetric
from evidently.metrics import NDCGKMetric
from evidently.metrics import PrecisionTopKMetric
from evidently.metrics import RecallTopKMetric
from evidently.metrics.recsys.base_top_k import TopKMetric
from evidently.metrics.recsys.base_top_k import TopKMetricResult
from evidently.model.widget import BaseWidgetInfo


class TopKBase(SingleValueMetric):
    k: int
    min_rel_score: Optional[int] = None
    no_feedback_users: bool = False


TTopKBase = TypeVar("TTopKBase", bound=TopKBase)


class LegacyTopKCalculation(
    LegacyMetricCalculation[
        SingleValue,
        TTopKBase,
        TopKMetricResult,
        TopKMetric,
    ],
    Generic[TTopKBase],
    ABC,
):
    pass


class NDCG(TopKBase):
    pass


class NDCGCalculation(LegacyTopKCalculation[NDCG]):
    def display_name(self) -> str:
        return "NDCG@k"

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = SingleValue(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, SingleValue(legacy_result.reference[legacy_result.k - 1])

    def legacy_metric(self):
        return NDCGKMetric(
            k=self.metric.k, min_rel_score=self.metric.min_rel_score, no_feedback_users=self.metric.no_feedback_users
        )


class MRR(TopKBase):
    pass


class MRRCalculation(LegacyTopKCalculation[MRR]):
    def display_name(self) -> str:
        return "MRR@k"

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = SingleValue(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, SingleValue(legacy_result.reference[legacy_result.k - 1])

    def legacy_metric(self):
        return MRRKMetric(
            k=self.metric.k, min_rel_score=self.metric.min_rel_score, no_feedback_users=self.metric.no_feedback_users
        )


class HitRate(TopKBase):
    pass


class HitRateCalculation(LegacyTopKCalculation[HitRate]):
    def display_name(self) -> str:
        return "HitRate@k"

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = SingleValue(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, SingleValue(legacy_result.reference[legacy_result.k - 1])

    def legacy_metric(self):
        return HitRateKMetric(
            k=self.metric.k, min_rel_score=self.metric.min_rel_score, no_feedback_users=self.metric.no_feedback_users
        )


class MAP(TopKBase):
    pass


class MAPCalculation(LegacyTopKCalculation[MAP]):
    def display_name(self) -> str:
        return "MAP@k"

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = SingleValue(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, SingleValue(legacy_result.reference[legacy_result.k - 1])

    def legacy_metric(self):
        return MAPKMetric(
            k=self.metric.k, min_rel_score=self.metric.min_rel_score, no_feedback_users=self.metric.no_feedback_users
        )


class RecallTopK(TopKBase):
    pass


class RecallTopKCalculation(LegacyTopKCalculation[RecallTopK]):
    def display_name(self) -> str:
        return "Recall@k"

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = SingleValue(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, SingleValue(legacy_result.reference[legacy_result.k - 1])

    def legacy_metric(self):
        return RecallTopKMetric(
            k=self.metric.k, min_rel_score=self.metric.min_rel_score, no_feedback_users=self.metric.no_feedback_users
        )


class PrecisionTopK(TopKBase):
    pass


class PrecisionTopKCalculation(LegacyTopKCalculation[PrecisionTopK]):
    def display_name(self) -> str:
        return "Precision@k"

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = SingleValue(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, SingleValue(legacy_result.reference[legacy_result.k - 1])

    def legacy_metric(self):
        return PrecisionTopKMetric(
            k=self.metric.k, min_rel_score=self.metric.min_rel_score, no_feedback_users=self.metric.no_feedback_users
        )


class FBetaTopK(TopKBase):
    beta: Optional[float] = 1.0


class FBetaTopKCalculation(LegacyTopKCalculation[FBetaTopK]):
    def display_name(self) -> str:
        return f"F{self.metric.beta}@k"

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = SingleValue(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, SingleValue(legacy_result.reference[legacy_result.k - 1])

    def legacy_metric(self):
        return FBetaTopKMetric(
            k=self.metric.k,
            min_rel_score=self.metric.min_rel_score,
            no_feedback_users=self.metric.no_feedback_users,
            beta=self.metric.beta,
        )


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
        from evidently.future.datasets import DataDefinition
        from evidently.future.datasets import Dataset
        from evidently.future.datasets import Recsys

        dataset = Dataset.from_pandas(
            df, data_definition=DataDefinition(numerical_columns=["target", "prediction"], ranking=[Recsys()])
        )
        report = Report(
            [
                NDCG(k=3, no_feedback_users=True),
                MRR(k=3),
                HitRate(k=3),
                # ScoreDistribution(),
                MAP(k=3),
                RecallTopK(k=3),
                PrecisionTopK(k=3),
                FBetaTopK(k=3),
            ]
        )
        snapshot_v2 = report.run(dataset, None)

        from evidently.future.backport import snapshot_v2_to_v1

        snapshot_v1 = snapshot_v2_to_v1(snapshot_v2)
        return snapshot_v1

    sn = create_snapshot(10)
    sn.save("ndcg.json")


if __name__ == "__main__":
    main()
