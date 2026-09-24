"""Regression tests for issue #1706 — GroupBy(ValueDrift) display_name not
shown properly. Before the fix the rendered widget for ValueDrift always
read "Drift in column 'X'" even when wrapped in GroupBy, dropping the group
column / label suffix."""

from __future__ import annotations

import numpy as np
import pandas as pd

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.report import Report
from evidently.metrics.column_statistics import ValueDrift
from evidently.metrics.group_by import GroupBy


def _build_datasets():
    rng = np.random.default_rng(0)
    df = pd.DataFrame(
        {
            "value": np.concatenate([rng.normal(size=100), rng.normal(loc=2, size=100)]),
            "group": ["a"] * 100 + ["b"] * 100,
        }
    )
    ref = Dataset.from_pandas(df, data_definition=DataDefinition())
    cur = Dataset.from_pandas(df.copy(), data_definition=DataDefinition())
    return cur, ref


def _counter_titles_for(metrics):
    """Run a report with the given metrics and return the list of counter
    titles (i.e. the prominent header text on each ValueDrift widget)."""
    cur, ref = _build_datasets()
    snap = Report(metrics).run(cur, ref)
    ctx = snap.context
    titles: list[str] = []
    for fp in snap.metric_results:
        res = ctx.get_metric_result(fp)
        widgets = res.widget if isinstance(res.widget, list) else [res.widget]
        for w in widgets:
            params = (w.dict() if hasattr(w, "dict") else w).get("params") or {}
            for c in params.get("counters") or []:
                # `value` is the header; `label` is the description text.
                titles.append(c.get("value", ""))
    return titles


def test_groupby_value_drift_widget_uses_decorated_display_name() -> None:
    """In a GroupBy(ValueDrift(...)) the rendered widget title must include
    the group-by suffix (`group by '<col>' for label: '<label>'`)."""
    titles = _counter_titles_for([GroupBy(ValueDrift(column="value"), "group")])
    decorated = [t for t in titles if "group by 'group'" in t and "for label:" in t]
    assert len(decorated) >= 2, (
        "Expected the GroupBy decoration to appear in widget titles for both "
        f"groups (a and b); got titles={titles!r}"
    )


def test_plain_value_drift_keeps_default_widget_title() -> None:
    """Outside a GroupBy the widget keeps the historical 'Drift in column'
    wording so this fix is not a regression for existing reports."""
    titles = _counter_titles_for([ValueDrift(column="value")])
    assert any(
        "Drift in column 'value'" in t for t in titles
    ), f"Plain ValueDrift must keep its historical widget title; got {titles!r}"
