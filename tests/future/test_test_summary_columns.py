import pandas as pd
import pytest

from evidently.core.datasets import ColumnTest
from evidently.core.datasets import Dataset
from evidently.core.datasets import TestSummary
from evidently.core.datasets import TestSummaryInfo
from evidently.core.report import Report
from evidently.presets import TextEvals
from evidently.tests import eq


def _dataset_with_summary(**kwargs) -> Dataset:
    dataset = Dataset.from_pandas(pd.DataFrame({"a": [1, 1, 2]}))
    dataset.add_descriptor(ColumnTest("a", eq(1)))
    dataset.add_descriptor(TestSummary(alias="summary", **kwargs))
    return dataset


def _summary_info(dataset: Dataset) -> TestSummaryInfo:
    infos = [i for i in dataset.data_definition.special_columns if isinstance(i, TestSummaryInfo)]
    assert len(infos) == 1
    return infos[0]


def _generated_columns(info: TestSummaryInfo):
    preset = info.get_metrics()[0]
    return sorted(getattr(m, "column", None) for m in preset.generate_metrics(None))


def test_has_all_follows_all_column():
    info = TestSummaryInfo(all_column="all_col", any_column=None)
    assert info.has_all is True
    assert info.has_any is False


def test_has_any_follows_any_column():
    info = TestSummaryInfo(all_column=None, any_column="any_col")
    assert info.has_any is True
    assert info.has_all is False


def test_success_all_summary_produces_aggregation_metric():
    """`TestSummary(success_all=True)` is the default configuration: the report must
    contain the "all tests passed" aggregation for the produced column."""
    info = _summary_info(_dataset_with_summary(success_all=True))
    assert info.all_column is not None
    assert _generated_columns(info) == [info.all_column]


def test_success_any_summary_does_not_require_all_column():
    """`success_any` alone used to build an aggregation metric on a missing `all_column`."""
    dataset = _dataset_with_summary(success_all=False, success_any=True)
    info = _summary_info(dataset)
    assert info.any_column is not None
    assert _generated_columns(info) == [info.any_column]
    Report(metrics=[TextEvals()]).run(current_data=dataset)


@pytest.mark.parametrize(
    "kwargs,expect_all_panel,expect_any_panel",
    [
        ({"success_all": True}, True, False),
        ({"success_all": False, "success_any": True}, False, True),
        ({"success_all": True, "success_any": True}, True, True),
    ],
)
def test_text_evals_renders_summary_panels(kwargs, expect_all_panel, expect_any_panel):
    dataset = _dataset_with_summary(**kwargs)
    snapshot = Report(metrics=[TextEvals()]).run(current_data=dataset)

    def titles(widgets):
        found = []
        for w in widgets:
            if getattr(w, "title", None):
                found.append(w.title)
            found.extend(titles(getattr(w, "widgets", None) or []))
            found.extend(titles([t.widget for t in getattr(w, "tabs", None) or []]))
        return found

    rendered = titles(list(snapshot._widgets))
    assert ("All tests passed" in rendered) is expect_all_panel, rendered
    assert ("Any tests passed" in rendered) is expect_any_panel, rendered
