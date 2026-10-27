import pandas as pd
import pytest

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.core.datasets import Recsys
from evidently.metrics import recsys


@pytest.mark.parametrize(
    "metric_type",
    [recsys.PrecisionTopK, recsys.RecallTopK, recsys.FBetaTopK, recsys.MAP, recsys.MRR, recsys.NDCG, recsys.HitRate],
)
def test_recsys_score_ties_match_explicit_ranks(metric_type):
    current = pd.DataFrame({"user_id": ["a"] * 3, "item_id": [0, 1, 2], "prediction": [0.5] * 3, "target": [1, 0, 0]})
    values = []
    references = []
    for recommendations_type in ("score", "rank"):
        df = current.copy(deep=True)
        reference = current.iloc[::-1].copy()
        if recommendations_type == "rank":
            df["prediction"] = [1, 2, 3]
            reference["prediction"] = [1, 2, 3]
        originals = [frame.copy(deep=True) for frame in (df, reference)]
        definition = DataDefinition(ranking=[Recsys(recommendations_type=recommendations_type)])
        dataset = Dataset.from_pandas(df, definition)
        reference_dataset = Dataset.from_pandas(reference, definition)
        metric = metric_type(k=1)
        snapshot = Report(metrics=[metric]).run(current_data=dataset, reference_data=reference_dataset)
        values.append(snapshot._context.get_metric_result(metric.metric_id).value)
        references.append(snapshot._context.get_reference_metric_result(metric.metric_id).value)
        for actual, original in zip((df, reference), originals):
            pd.testing.assert_frame_equal(actual, original)

    pd.testing.assert_frame_equal(values[0], values[1])
    pd.testing.assert_frame_equal(references[0], references[1])
    assert values[0].iloc[0]["value"] == pytest.approx(1.0)
    # F-beta currently returns NaN when both precision and recall are zero.
    if metric_type is recsys.FBetaTopK:
        assert pd.isna(references[0].iloc[0]["value"])
    else:
        assert references[0].iloc[0]["value"] == pytest.approx(0.0)
