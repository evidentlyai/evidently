import pandas as pd

from evidently.core.report import Report
from evidently.generators import ColumnMetricGenerator
from evidently.presets import ValueStats
from evidently.tests import gt


def test_generator_renders():
    generator = ColumnMetricGenerator(ValueStats, columns=["a", "b"])
    report = Report([generator])
    snapshot = report.run(pd.DataFrame(data={"a": [1, 2, 3, 4], "b": [1, 2, 3, 4]}))
    assert len(snapshot._widgets) == 2


def test_generator_kwargs():
    generator = ColumnMetricGenerator(ValueStats, columns=["a", "b"], metric_kwargs={"tests": [gt(0)]})
    generator2 = ColumnMetricGenerator(ValueStats, columns=["a", "b"], tests=[gt(0)])

    assert generator.dict() == generator2.dict()
