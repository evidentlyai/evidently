import abc
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.pipeline import Pipeline
from evidently.pipeline.stage import PipelineStage


class ModelMonitoringMetric:
    def __init__(self, name: str, labels: List[str] = None):
        self.name = name
        self.labels = labels if labels is not None else []

    def create(self, value: float, labels: Optional[Dict[str, str]] = None):
        _labels = labels if labels is not None else {}
        if len(_labels) == 0 and len(self.labels) == 0:
            return self, value, None
        if set(_labels.keys()) != set(self.labels):
            raise ValueError(
                f"Trying to create metric with"
                f" incorrect labels got {set(_labels.keys())} expected {set(self.labels)}"
            )
        return self, value, _labels


MetricsType = Tuple[ModelMonitoringMetric, float, Optional[Dict[str, str]]]


class ModelMonitor(PipelineStage):
    def calculate(
        self,
        reference_data: pandas.DataFrame,
        current_data: pandas.DataFrame,
        column_mapping: ColumnMapping,
        analyzers_results: Dict[Type[Analyzer], Any],
    ):
        pass

    @abc.abstractmethod
    def monitor_id(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def analyzers(self) -> List[Type[Analyzer]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def metrics(self, analyzer_results):
        raise NotImplementedError()


class ModelMonitoring(Pipeline):
    def __init__(
        self, monitors: Sequence[ModelMonitor], options: Optional[list] = None
    ):
        if options is None:
            options = []

        super().__init__(monitors, options)
        self.monitors = list(monitors)

    def get_analyzers(self):
        return list({analyzer for tab in self.monitors for analyzer in tab.analyzers()})

    def metrics(self) -> Generator[MetricsType, None, None]:
        for monitor in self.monitors:
            for metric in monitor.metrics(self.analyzers_results):
                yield metric
