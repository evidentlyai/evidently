import numpy as np
import pandas as pd
from numpy.testing import assert_allclose

from evidently.legacy.metrics.recsys.pairwise_distance import PairwiseDistance
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


def test_curr():
    curr = pd.DataFrame(
        {
            "user_id": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
            "item_id": ["0a", "1a", "5a", "6a", "0a", "1a", "5a", "6a", "0a", "4a", "6a", "10a"],
            "item_f1": [1, 1, 1, -0.1, 1, 1, 1, -0.1, 1, 1, -0.1, -1],
            "item_f2": [0, 0.1, 1, 0.9, 0, 0.1, 1, 0.9, 0, 0.9, 0.9, -1],
            "target": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "prediction": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
        }
    )
    metric = PairwiseDistance(k=4, item_features=["item_f1", "item_f2"])
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=curr, column_mapping=column_mapping)

    results = metric.get_result()

    assert_allclose(
        results.dist_matrix,
        np.array(
            [
                [0.00000000e00, 4.96280979e-03, 2.92893219e-01, 1.11043153e00, 2.56705854e-01, 1.70710678e00],
                [4.96280979e-03, 0.00000000e00, 2.26042701e-01, 1.01098835e00, 1.93830203e-01, 1.77395730e00],
                [2.92893219e-01, 2.26042701e-01, 2.22044605e-16, 3.75304952e-01, 1.38217067e-03, 2.00000000e00],
                [1.11043153e00, 1.01098835e00, 3.75304952e-01, 0.00000000e00, 4.17209941e-01, 1.62469505e00],
                [2.56705854e-01, 1.93830203e-01, 1.38217067e-03, 4.17209941e-01, 1.11022302e-16, 1.99861783e00],
                [1.70710678e00, 1.77395730e00, 2.00000000e00, 1.62469505e00, 1.99861783e00, 2.22044605e-16],
            ]
        ),
        rtol=1e-6,
        atol=1e-7,
    )
    assert results.name_dict == {"0a": 0, "1a": 1, "5a": 2, "6a": 3, "4a": 4, "10a": 5}
