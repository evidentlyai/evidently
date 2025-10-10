from typing import List
from typing import Optional
from typing import Sequence

from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.metric_types import Metric
from evidently.core.report import Context
from evidently.metrics.recsys import MAP
from evidently.metrics.recsys import MRR
from evidently.metrics.recsys import NDCG
from evidently.metrics.recsys import Diversity
from evidently.metrics.recsys import FBetaTopK
from evidently.metrics.recsys import HitRate
from evidently.metrics.recsys import ItemBias
from evidently.metrics.recsys import Novelty
from evidently.metrics.recsys import Personalization
from evidently.metrics.recsys import PopularityBiasMetric
from evidently.metrics.recsys import PrecisionTopK
from evidently.metrics.recsys import RecallTopK
from evidently.metrics.recsys import RecCasesTable
from evidently.metrics.recsys import ScoreDistribution
from evidently.metrics.recsys import Serendipity
from evidently.metrics.recsys import UserBias


class RecsysPreset(MetricContainer):
    """Metric preset for recsys performance analysis.

    Contains metrics:
    - PrecisionTopK (DataframeValue with rank and value columns)
    - RecallTopK (DataframeValue with rank and value columns)
    - FBetaTopK (DataframeValue with rank and value columns)
    - MAP (DataframeValue with rank and value columns)
    - NDCG (DataframeValue with rank and value columns)
    - MRR (DataframeValue with rank and value columns)
    - HitRate (DataframeValue with rank and value columns)
    - ScoreDistribution (SingleValue)
    - PopularityBiasMetric (SingleValue)
    - Personalization (SingleValue)
    - Diversity (SingleValue, requires item_features)
    - Serendipity (SingleValue, requires item_features)
    - Novelty (SingleValue)
    - ItemBias (DataframeValue with x,y columns, requires item_bias_columns)
    - UserBias (DataframeValue with x,y columns, requires user_bias_columns)
    - RecCasesTable (DataframeValue)
    """

    k: int
    min_rel_score: Optional[int] = None
    no_feedback_users: bool = False
    ranking_name: str = "default"
    beta: Optional[float] = 1.0
    normalize_arp: bool = False
    user_ids: Optional[List[str]] = None
    display_features: Optional[List[str]] = None
    item_features: Optional[List[str]] = None
    user_bias_columns: Optional[List[str]] = None
    item_bias_columns: Optional[List[str]] = None

    def __init__(
        self,
        k: int,
        min_rel_score: Optional[int] = None,
        no_feedback_users: bool = False,
        ranking_name: str = "default",
        beta: Optional[float] = 1.0,
        normalize_arp: bool = False,
        user_ids: Optional[List[str]] = None,
        display_features: Optional[List[str]] = None,
        item_features: Optional[List[str]] = None,
        user_bias_columns: Optional[List[str]] = None,
        item_bias_columns: Optional[List[str]] = None,
        include_tests: bool = True,
    ):
        self.k = k
        self.min_rel_score = min_rel_score
        self.no_feedback_users = no_feedback_users
        self.ranking_name = ranking_name
        self.beta = beta
        self.normalize_arp = normalize_arp
        self.user_ids = user_ids
        self.display_features = display_features
        self.item_features = item_features
        self.user_bias_columns = user_bias_columns
        self.item_bias_columns = item_bias_columns
        super().__init__(include_tests=include_tests)

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        is_train_data = "current_train_data" in context.additional_data
        metrics: List[Metric] = [
            # Core TopK metrics (return DataframeValue with rank and value columns)
            PrecisionTopK(
                k=self.k,
                min_rel_score=self.min_rel_score,
                no_feedback_users=self.no_feedback_users,
                ranking_name=self.ranking_name,
            ),
            RecallTopK(
                k=self.k,
                min_rel_score=self.min_rel_score,
                no_feedback_users=self.no_feedback_users,
                ranking_name=self.ranking_name,
            ),
            FBetaTopK(
                k=self.k,
                min_rel_score=self.min_rel_score,
                no_feedback_users=self.no_feedback_users,
                ranking_name=self.ranking_name,
                beta=self.beta,
            ),
            MAP(
                k=self.k,
                min_rel_score=self.min_rel_score,
                no_feedback_users=self.no_feedback_users,
                ranking_name=self.ranking_name,
            ),
            NDCG(
                k=self.k,
                min_rel_score=self.min_rel_score,
                no_feedback_users=self.no_feedback_users,
                ranking_name=self.ranking_name,
            ),
            MRR(
                k=self.k,
                min_rel_score=self.min_rel_score,
                no_feedback_users=self.no_feedback_users,
                ranking_name=self.ranking_name,
            ),
            HitRate(
                k=self.k,
                min_rel_score=self.min_rel_score,
                no_feedback_users=self.no_feedback_users,
                ranking_name=self.ranking_name,
            ),
            # Score distribution
            ScoreDistribution(
                k=self.k,
                ranking_name=self.ranking_name,
            ),
            # Recommendation cases table
            RecCasesTable(
                user_ids=self.user_ids,
                display_features=self.display_features,
                ranking_name=self.ranking_name,
            ),
            # Personalization
            Personalization(
                k=self.k,
                ranking_name=self.ranking_name,
            ),
        ]

        # Add metrics that require training data
        if is_train_data:
            metrics.append(
                PopularityBiasMetric(
                    k=self.k,
                    normalize_arp=self.normalize_arp,
                    ranking_name=self.ranking_name,
                )
            )
            metrics.append(
                Novelty(
                    k=self.k,
                    ranking_name=self.ranking_name,
                )
            )

        # Add metrics that require item features
        if self.item_features is not None:
            metrics.append(
                Diversity(
                    k=self.k,
                    item_features=self.item_features,
                    ranking_name=self.ranking_name,
                )
            )
            if is_train_data:
                metrics.append(
                    Serendipity(
                        k=self.k,
                        item_features=self.item_features,
                        ranking_name=self.ranking_name,
                    )
                )

        # Add bias metrics that require training data
        if is_train_data:
            if self.item_bias_columns is not None:
                for col in self.item_bias_columns:
                    # Add both default and train distributions
                    metrics.append(
                        ItemBias(
                            k=self.k,
                            column_name=col,
                            distribution="default",
                            ranking_name=self.ranking_name,
                        )
                    )
                    metrics.append(
                        ItemBias(
                            k=self.k,
                            column_name=col,
                            distribution="train",
                            ranking_name=self.ranking_name,
                        )
                    )
            if self.user_bias_columns is not None:
                for col in self.user_bias_columns:
                    # Add both default and train distributions
                    metrics.append(
                        UserBias(
                            column_name=col,
                            distribution="default",
                            ranking_name=self.ranking_name,
                        )
                    )
                    metrics.append(
                        UserBias(
                            column_name=col,
                            distribution="train",
                            ranking_name=self.ranking_name,
                        )
                    )

        return metrics
