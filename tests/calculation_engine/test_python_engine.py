import pandas as pd

from evidently.legacy.base_metric import GenericInputData
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.calculation_engine.engine import metric_implementation
from evidently.legacy.calculation_engine.python_engine import PythonEngine
from evidently.legacy.calculation_engine.python_engine import PythonMetricImplementation
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.renderers.base_renderer import DEFAULT_RENDERERS
from evidently.legacy.suite.base_suite import Context
from evidently.legacy.suite.base_suite import States


class OldTypeSimpleMetric(Metric[int]):
    class Config:
        alias_required = False

    value: int

    def __init__(self, value: int):
        self.value = value
        super().__init__()

    def calculate(self, data: InputData) -> int:
        return self.value + 15


class SimpleMetric(Metric[int]):
    class Config:
        alias_required = False

    value: int

    def __init__(self, value: int):
        self.value = value
        super().__init__()

    def calculate(self, data: InputData) -> int:
        raise NotImplementedError()


@metric_implementation(SimpleMetric)
class PythonSimpleMetric(PythonMetricImplementation[SimpleMetric]):
    def calculate(self, context, data: InputData):
        return self.metric.value + 10


def test_python_engine_registration():
    engine = PythonEngine()
    engine.set_metrics([SimpleMetric(10)])
    impl = engine.get_metric_implementation(SimpleMetric(10))
    assert impl is not None
    assert impl.calculate(None, None) == 20


def test_python_engine():
    metric = SimpleMetric(10)
    engine = PythonEngine()
    engine.set_metrics([metric])
    ctx = Context(None, [metric], [], dict(), dict(), States.Verified, renderers=DEFAULT_RENDERERS)
    engine.execute_metrics(ctx, GenericInputData(pd.DataFrame(), pd.DataFrame(), ColumnMapping(), None, {}))
    assert ctx.metric_results[metric] == 20


def test_python_engine2():
    metric = OldTypeSimpleMetric(10)
    engine = PythonEngine()
    engine.set_metrics([metric])
    ctx = Context(None, [metric], [], dict(), dict(), States.Verified, renderers=DEFAULT_RENDERERS)
    engine.execute_metrics(ctx, GenericInputData(pd.DataFrame(), pd.DataFrame(), ColumnMapping(), None, {}))
    assert ctx.metric_results[metric] == 25
