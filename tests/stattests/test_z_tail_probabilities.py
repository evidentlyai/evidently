import math

import pandas as pd
import pytest

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.legacy.calculations.stattests.z_stattest import proportions_diff_z_test
from evidently.legacy.calculations.stattests.z_stattest import z_stat_test
from evidently.legacy.core import ColumnType
from evidently.metrics import ValueDrift


@pytest.mark.parametrize("z_stat", [-9.0, 0.0, 9.0, 12.0])
@pytest.mark.parametrize("alternative", ["two-sided", "greater", "less"])
def test_z_test_retains_representable_tail_probabilities(z_stat, alternative):
    if alternative == "two-sided":
        expected = math.erfc(abs(z_stat) / math.sqrt(2))
    elif alternative == "greater":
        expected = 0.5 * math.erfc(z_stat / math.sqrt(2))
    else:
        expected = 0.5 * math.erfc(-z_stat / math.sqrt(2))

    actual = proportions_diff_z_test(z_stat, alternative)

    assert actual == pytest.approx(expected, rel=1e-12, abs=0)
    assert actual > 0


def populations():
    reference = pd.Series(["absent"] * 300 + ["present"] * 200)
    current = pd.Series(["absent"] * 150 + ["present"] * 350)
    z_stat = (0.4 - 0.7) / math.sqrt(0.55 * 0.45 * (2 / 500))
    return reference, current, math.erfc(abs(z_stat) / math.sqrt(2))


@pytest.mark.parametrize("threshold_factor", [0.5, 2.0])
@pytest.mark.parametrize("reverse", [False, True])
def test_categorical_drift_uses_the_nonzero_tail_for_threshold_decisions(threshold_factor, reverse):
    reference, current, expected = populations()
    if reverse:
        reference, current = current, reference

    result = z_stat_test(reference, current, ColumnType.Categorical, expected * threshold_factor)

    assert result.drift_score == pytest.approx(expected, rel=1e-12, abs=0)
    assert result.drifted == (threshold_factor > 1)


def test_value_drift_report_preserves_the_z_test_tail_probability():
    reference, current, expected = populations()
    definition = DataDefinition(categorical_columns=["flag"])
    reference_data = Dataset.from_pandas(pd.DataFrame({"flag": reference}), definition)
    current_data = Dataset.from_pandas(pd.DataFrame({"flag": current}), definition)

    snapshot = Report(metrics=[ValueDrift(column="flag", method="z", threshold=expected / 2)]).run(
        current_data, reference_data
    )

    result = next(iter(snapshot.metric_results.values()))
    assert result.value == pytest.approx(expected, rel=1e-12, abs=0)


def test_z_test_still_rejects_an_unknown_alternative():
    with pytest.raises(ValueError, match="alternative not recognized"):
        proportions_diff_z_test(1.0, "unknown")
