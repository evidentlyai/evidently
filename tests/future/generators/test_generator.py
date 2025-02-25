import pandas as pd

from evidently.future.generators import ColumnMetricGenerator
from evidently.future.presets import ValueStats
from evidently.future.report import Report


def test_generator_renders():
    generator = ColumnMetricGenerator(ValueStats, columns=["a", "b"])
    report = Report([generator])
    snapshot = report.run(pd.DataFrame(data={"a": [1, 2, 3, 4], "b": [1, 2, 3, 4]}))
    assert len(snapshot._widgets) == 2
