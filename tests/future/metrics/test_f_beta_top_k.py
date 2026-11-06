import numpy as np
import pandas as pd
import pytest

from evidently import DataDefinition
from evidently import Dataset
from evidently import Recsys
from evidently import Report
from evidently.metrics import FBetaTopK


@pytest.mark.parametrize(
    "beta,current_last,reference_second", [(0.5, 5 / 13, 5 / 9), (1.0, 1 / 2, 2 / 3), (2.0, 5 / 7, 5 / 6)]
)
@pytest.mark.parametrize("no_feedback_users", [False, True])
@pytest.mark.parametrize("with_reference", [False, True])
def test_fbeta_no_relevant_items_at_cutoff(beta, current_last, reference_second, no_feedback_users, with_reference):
    current = pd.DataFrame(
        {
            "user_id": ["a", "a", "a", "b", "b", "b"],
            "item_id": [1, 2, 3, 1, 2, 3],
            "prediction": [1, 2, 3, 1, 2, 3],
            "target": [0, 0, 1, 0, 0, 0],
        }
    )
    definition = DataDefinition(ranking=[Recsys(recommendations_type="rank")])
    reference = (
        Dataset.from_pandas(current.assign(target=[0, 1, 0, 0, 0, 0]), data_definition=definition)
        if with_reference
        else None
    )
    metric = FBetaTopK(k=1, beta=beta, no_feedback_users=no_feedback_users)
    snapshot = Report([metric]).run(Dataset.from_pandas(current, data_definition=definition), reference)

    result = snapshot._context.get_metric_result(metric)
    scale = 0.5 if no_feedback_users else 1.0
    np.testing.assert_allclose(result.value["value"], [0.0, 0.0, current_last * scale])
    if with_reference:
        reference_result = snapshot._context._reference_metrics[metric.metric_id]
        np.testing.assert_allclose(
            reference_result.value["value"], [0.0, reference_second * scale, current_last * scale]
        )
