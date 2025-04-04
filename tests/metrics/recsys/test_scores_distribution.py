import numpy as np
import pandas as pd

from evidently.legacy.metrics import ScoreDistribution
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


def test_score_distribution():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1.25, 1.0, 0.3, 0.9, 0.8, 0.7, 1.0, 0.5, 0.3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = ScoreDistribution(k=3)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping()
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert np.isclose(results.current_entropy, 2.15148438)
