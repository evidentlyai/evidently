import json

import numpy as np
import pandas as pd

from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.metrics import PrecisionTopKMetric
from evidently.legacy.metrics.recsys.base_top_k import TopKMetricResult
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report
from evidently.legacy.utils import NumpyEncoder


def test_value():
    result = TopKMetricResult(
        k=2, current=pd.Series([0, 1]), current_value=1, reference=pd.Series([2, 3]), reference_value=3
    )
    payload = json.loads(json.dumps(result.dict(), cls=NumpyEncoder))
    payload2 = {k: v for k, v in payload.items() if not k.endswith("_value")}
    result2 = parse_obj_as(MetricResult, payload2)
    assert json.loads(json.dumps(result2.dict(), cls=NumpyEncoder)) == payload


def test_precision_value():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = PrecisionTopKMetric(k=2)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert results.current[0] == 0.5
    assert results.current[1] == 0.25
    assert np.isclose(results.current[2], 0.333333)


def test_precision_value_judged_only():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = PrecisionTopKMetric(k=3, no_feedback_users=True)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert np.isclose(results.current[0], 0.333333)
    assert np.isclose(results.current[1], 0.166666)
    assert np.isclose(results.current[2], 0.222222)


def test_precision_value_judged_only_scores():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1.25, 1.0, 0.3, 0.9, 0.8, 0.7, 1.0, 0.5, 0.3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = PrecisionTopKMetric(k=3, no_feedback_users=True)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping()
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert np.isclose(results.current[0], 0.333333)
    assert np.isclose(results.current[1], 0.166666)
    assert np.isclose(results.current[2], 0.222222)
