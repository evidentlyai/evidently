import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metrics import HitRateKMetric
from evidently.legacy.metrics.recsys.hit_rate_k import HitRateKMetricRenderer
from evidently.legacy.metrics.recsys.hit_rate_k import HitRateKMetricResult
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.report import Report


def test_hit_rate_value():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = HitRateKMetric(k=2)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert np.isclose(results.current[0], 0.5)
    assert np.isclose(results.current[1], 0.5)
    assert np.isclose(results.current[2], 1)


def test_hit_rate_value_judged_only():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = HitRateKMetric(k=3, no_feedback_users=True)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert np.isclose(results.current[0], 0.3333333)
    assert np.isclose(results.current[1], 0.3333333)
    assert np.isclose(results.current[2], 0.6666666)


def test_hit_rate_value_judged_only_scores():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1.25, 1.0, 0.3, 0.9, 0.8, 0.7, 1.0, 0.5, 0.3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = HitRateKMetric(k=3, no_feedback_users=True)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping()
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert np.isclose(results.current[0], 0.3333333)
    assert np.isclose(results.current[1], 0.3333333)
    assert np.isclose(results.current[2], 0.6666666)


def test_hit_rate_scalar_values_use_position_after_index_round_trip():
    # Index labels may be strings after JSON serialization of a pandas Series.
    result = HitRateKMetricResult(
        k=3,
        current=pd.Series([0.25, 0.5, 0.75], index=["0", "1", "2"]),
        reference=pd.Series([0.2, 0.4, 0.6], index=["0", "1", "2"]),
    )
    assert result.current_value == pytest.approx(0.75)
    assert result.reference_value == pytest.approx(0.6)


def test_hit_rate_scalar_value_without_reference():
    result = HitRateKMetricResult(k=2, current=pd.Series([0.1, 0.9]))
    assert result.current_value == pytest.approx(0.9)
    assert result.reference_value is None


def test_hit_rate_snapshot_render_after_loading(tmp_path):
    # A serialized pandas Series can have string index labels. HTML
    # rendering must select HitRate@k by position rather than label.
    current = pd.DataFrame(
        {
            "user_id": ["a"] * 12 + ["b"] * 12,
            "prediction": list(range(1, 13)) * 2,
            "target": [1] + [0] * 11 + [0] * 11 + [1],
        }
    )
    report = Report(metrics=[HitRateKMetric(k=10)])
    report.run(
        reference_data=None,
        current_data=current,
        column_mapping=ColumnMapping(recommendations_type=RecomType.RANK),
    )
    snapshot = tmp_path / "hit-rate-k10-report.json"
    report.save(str(snapshot))

    loaded = Report.load(str(snapshot))
    _, dashboard, _ = loaded._build_dashboard_info()
    assert dashboard is not None


@pytest.mark.parametrize("with_reference", [False, True])
def test_hit_rate_renderer_selects_rank_after_index_restore(monkeypatch, with_reference):
    # A string-labeled Series reproduces the post-snapshot indexing failure
    # even on pandas versions that no longer fall back to positional indexing.
    current = pd.Series(range(12), index=[str(i) for i in range(12)])
    reference = pd.Series(range(12), index=[str(i) for i in range(12)]) if with_reference else None
    result = HitRateKMetricResult(k=10, current=current, reference=reference)
    metric = HitRateKMetric(k=10)
    monkeypatch.setattr(HitRateKMetric, "get_result", lambda self: result)

    calls = []
    original_float = CounterData.float

    def capture_float(*, label, value, precision):
        calls.append((label, value))
        return original_float(label=label, value=value, precision=precision)

    monkeypatch.setattr(CounterData, "float", staticmethod(capture_float))
    HitRateKMetricRenderer().render_html(metric)

    assert calls[0] == ("current", 9.0)
    if with_reference:
        assert calls[1] == ("reference", 9.0)
    else:
        assert len(calls) == 1
