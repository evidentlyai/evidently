import math

import pandas as pd
import pytest

from evidently import DataDefinition
from evidently import Dataset
from evidently import Recsys
from evidently import Report
from evidently.metrics import MAP
from evidently.metrics import MRR
from evidently.metrics import NDCG
from evidently.metrics import FBetaTopK
from evidently.metrics import HitRate
from evidently.metrics import PrecisionTopK
from evidently.metrics import RecallTopK


def ranking_dataset(size, relevant_rank):
    return Dataset.from_pandas(
        pd.DataFrame(
            {
                "user_id": ["u"] * size,
                "item_id": list(range(size)),
                "prediction": list(range(1, size + 1)),
                "target": [int(rank == relevant_rank) for rank in range(1, size + 1)],
            }
        ),
        data_definition=DataDefinition(ranking=[Recsys(recommendations_type="rank")]),
    )


@pytest.mark.parametrize(
    "metric_type,relevant_rank",
    [(NDCG, 2), (MRR, 2), (HitRate, 2), (PrecisionTopK, 2), (RecallTopK, 2), (MAP, 2), (FBetaTopK, 1)],
)
@pytest.mark.parametrize("current_size", [3, 12])
@pytest.mark.parametrize("with_reference", [False, True])
def test_top_k_results_use_one_based_ranks(metric_type, relevant_rank, current_size, with_reference):
    metric = metric_type(k=2)
    snapshot = Report([metric]).run(
        ranking_dataset(current_size, relevant_rank),
        ranking_dataset(3, relevant_rank) if with_reference else None,
    )
    current = snapshot._context.get_metric_result(metric).value
    results = [(current, min(current_size, 10))]
    if with_reference:
        reference = snapshot._context._reference_metrics[metric.metric_id].value
        reference_size = min(current_size, 10) if metric_type in (MRR, HitRate) else 3
        results.append((reference, reference_size))

    for result, size in results:
        ranks = list(range(1, size + 1))
        assert result["rank"].tolist() == ranks
        if metric_type is NDCG:
            expected = [0] + [1 / math.log2(3)] * (size - 1)
        elif metric_type in (MRR, MAP):
            expected = [0] + [0.5] * (size - 1)
        elif metric_type in (HitRate, RecallTopK):
            expected = [0] + [1] * (size - 1)
        elif metric_type is PrecisionTopK:
            expected = [0] + [1 / k for k in ranks[1:]]
        else:
            expected = [2 / (k + 1) for k in ranks]
        assert result["value"].tolist() == pytest.approx(expected)
