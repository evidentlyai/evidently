import json

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metric_results import PredictionData
from evidently.legacy.metrics import ClassificationLiftTable
from evidently.legacy.metrics.classification_performance.lift_table_metric import ClassificationLiftTableRenderer
from evidently.legacy.metrics.classification_performance.lift_table_metric import ClassificationLiftTableResults
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report

LABELS = [
    ["cat", "dog"],
    ["cat", "dog", "bird"],
    ["猫", "犬"],
    ["猫", "犬", "鳥"],
    [0, 1],
    [0, 1, 2],
]


def _prediction_data(labels):
    target = pd.Series(labels * 2)
    probabilities = np.full((len(target), len(labels)), 0.1 / (len(labels) - 1))
    probabilities[np.arange(len(target)), np.tile(np.arange(len(labels)), 2)] = 0.9
    return target, PredictionData(
        predictions=target,
        labels=labels,
        prediction_probas=pd.DataFrame(probabilities, columns=labels),
    )


@pytest.mark.parametrize("labels", LABELS)
def test_lift_table_keeps_class_labels_and_values(labels):
    target, prediction = _prediction_data(labels)
    encoded_target, encoded_prediction = _prediction_data(list(range(len(labels))))
    metric = ClassificationLiftTable()

    result = metric.calculate_metrics(target, prediction)
    encoded = metric.calculate_metrics(encoded_target, encoded_prediction)

    expected_labels = labels[:1] if len(labels) == 2 else labels
    assert list(result) == expected_labels
    for index, label in enumerate(expected_labels):
        np.testing.assert_array_equal(result[label], encoded[index])
        final_row = result[label][-1]
        assert final_row[:2] == [100, len(target)]
        assert final_row[3:7] == [2, len(target) - 2, round(100 / len(labels), 1), 100]
        assert final_row[8:11] == [1, 1, 1]


@pytest.mark.parametrize("labels", LABELS[:4])
@pytest.mark.parametrize("with_reference", [False, True])
def test_text_labels_work_through_report_serialization_and_rendering(labels, with_reference):
    target, prediction = _prediction_data(labels)
    data = prediction.prediction_probas.copy()
    data["target"] = target
    original = data.copy(deep=True)
    metric = ClassificationLiftTable()
    report = Report(metrics=[metric])

    report.run(
        current_data=data,
        reference_data=data.copy() if with_reference else None,
        column_mapping=ColumnMapping(target="target", prediction=labels, pos_label=labels[0]),
    )

    result = metric.get_result()
    expected_labels = labels[:1] if len(labels) == 2 else labels
    assert list(result.current_lift_table) == expected_labels
    if with_reference:
        assert result.reference_lift_table == result.current_lift_table
    else:
        assert result.reference_lift_table is None
    serialized = json.loads(report.json())["metrics"][0]["result"]
    assert serialized["current_lift_table"] == result.current_lift_table
    restored = ClassificationLiftTableResults.parse_raw(result.json())
    assert restored.current_lift_table == result.current_lift_table
    assert restored.reference_lift_table == result.reference_lift_table
    widgets = ClassificationLiftTableRenderer().render_html(metric)
    assert len(widgets) == 1 + with_reference
    if len(labels) > 2:
        assert [tab.title for tab in widgets[0].tabs] == labels
    pd.testing.assert_frame_equal(data, original)


def test_integer_table_keys_survive_a_json_round_trip():
    target, prediction = _prediction_data([0, 1, 2])
    tables = ClassificationLiftTable().calculate_metrics(target, prediction)
    result = ClassificationLiftTableResults(current_lift_table=tables)

    restored = ClassificationLiftTableResults.parse_raw(result.json())

    assert restored.current_lift_table == tables
    assert all(isinstance(label, int) for label in restored.current_lift_table)
