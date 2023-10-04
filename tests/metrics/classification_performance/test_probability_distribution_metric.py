import json
from typing import Dict
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently.metrics import ClassificationProbDistribution
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


@pytest.mark.parametrize(
    "current, reference, column_mapping, expected_json",
    (
        (
            pd.DataFrame(
                data={
                    "target": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                    "a": [0.8, 0.7, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.7],
                    "b": [0.1, 0.2, 0.7, 0.9, 0.8, 0.3, 0.1, 0.4, 0.8],
                    "c": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.8, 0.9],
                },
            ),
            None,
            ColumnMapping(prediction=["a", "b", "c"]),
            {},
        ),
        (
            pd.DataFrame(
                data={
                    "my_target": ["a", np.NaN, "a", "b", "b", "c"],
                    "a": [0.8, 0.7, 0.3, 0.1, 0.2, 0.2],
                    "b": [0.1, 0.2, 0.7, np.NaN, 0.8, 0.3],
                    "c": [0.1, 0.1, 0.1, 0.1, 0.1, np.NaN],
                },
            ),
            pd.DataFrame(
                data={
                    "my_target": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                    "a": [0.8, 0.7, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.7],
                    "b": [0.1, 0.2, 0.7, 0.9, 0.8, 0.3, 0.1, 0.4, 0.8],
                    "c": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.8, 0.9],
                },
            ),
            ColumnMapping(target="my_target", prediction=["a", "b", "c"]),
            {},
        ),
    ),
)
def test_classification_prob_distribution_with_report(
    current: pd.DataFrame,
    reference: Optional[pd.DataFrame],
    column_mapping: ColumnMapping,
    expected_json: Dict,
):
    report = Report(metrics=[ClassificationProbDistribution()])
    report.run(
        current_data=current, reference_data=reference, column_mapping=column_mapping
    )
    report.show()
    result_json = report.json()
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "ClassificationProbDistribution"
    assert result["metrics"][0]["result"] == expected_json
