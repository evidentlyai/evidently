import math

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.calculations.classification_performance import calculate_lift_table
from evidently.legacy.calculations.classification_performance import calculate_pr_table
from evidently.legacy.metrics import ClassificationLiftTable
from evidently.legacy.metrics import ClassificationPRTable
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


def _reference_table(pairs, lift):
    pairs = sorted(pairs, key=lambda pair: pair[1], reverse=True)
    size = len(pairs)
    positives = sum(pair[0] for pair in pairs)
    step_size = max(math.floor(size * 0.01), 1) if lift else max(round(size * 0.05), 1)
    end = size + 1 if lift else size + step_size
    rows = []
    for step in np.arange(step_size, end, step_size):
        count = min(step, size)
        # Each expected row is defined independently from its selected population.
        tp = sum(pair[0] for pair in pairs[:count])
        top = round(100 * count / size) if lift else round(100 * count / size, 1)
        precision = round(100 * tp / count, 1)
        recall = round(100 * tp / positives, 1)
        row = [top, count, round(pairs[min(step, size - 1)][1], 2), tp, count - tp, precision, recall]
        if lift:
            max_lift = round(100 * count / positives / top, 2) if count <= positives else round(100 / top, 2)
            lift_value = round(recall / top, 2)
            row += [
                round(2 / (1 / precision + 1 / recall), 1),
                lift_value,
                max_lift,
                round(lift_value / max_lift, 2),
                round(100 * positives / size, 2),
            ]
        rows.append(row)
    return rows


@pytest.mark.parametrize("size", [0, 1, 3, 19, 99, 100, 101, 199, 200, 275, 1000])
@pytest.mark.parametrize("lift", [False, True])
def test_tables_match_independent_prefix_counts_for_all_row_boundaries(size, lift):
    rng = np.random.RandomState(size)
    targets = rng.randint(2, size=size).tolist()
    scores = np.linspace(1, 0, size).tolist()
    if size:
        targets[0] = 1
    pairs = list(zip(targets, scores))
    rng.shuffle(pairs)
    original = pairs.copy()

    result = (calculate_lift_table if lift else calculate_pr_table)(pairs)

    assert result == _reference_table(original, lift)
    assert pairs == sorted(original, key=lambda pair: pair[1], reverse=True)


@pytest.mark.parametrize("lift", [False, True])
def test_tied_probabilities_preserve_the_original_stable_order(lift):
    pairs = [(1, 0.9), (0, 0.8), (1, 0.8), (0, 0.8), (1, 0.3), (0, 0.1)] * 40
    expected = _reference_table(pairs, lift)

    result = (calculate_lift_table if lift else calculate_pr_table)(pairs)

    assert result == expected


@pytest.mark.parametrize("class_count", [2, 3])
@pytest.mark.parametrize("lift", [False, True])
def test_native_reports_keep_current_and_reference_tables(class_count, lift):
    labels = [str(label) for label in range(class_count)]
    target = pd.Series(labels * 35)
    data = pd.DataFrame({label: np.where(target == label, 0.9, 0.1 / (class_count - 1)) for label in labels})
    data["target"] = target
    reference = data.iloc[::-1].copy()
    metric = ClassificationLiftTable() if lift else ClassificationPRTable()
    report = Report(metrics=[metric])

    report.run(
        current_data=data,
        reference_data=reference,
        column_mapping=ColumnMapping(target="target", prediction=labels, pos_label=labels[0]),
    )

    result = metric.get_result()
    current_tables = result.current_lift_table if lift else result.current
    reference_tables = result.reference_lift_table if lift else result.reference
    for label in labels[:1] if class_count == 2 else labels:
        expected_current = _reference_table(list(zip((data.target == label).astype(int), data[label])), lift)
        expected_reference = _reference_table(
            list(zip((reference.target == label).astype(int), reference[label])), lift
        )
        assert current_tables[int(label)] == expected_current
        assert reference_tables[int(label)] == expected_reference
