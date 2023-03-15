#!/usr/bin/env python
# coding: utf-8
import abc
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from evidently.metric_results import DatasetColumns
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@dataclass
class BaseAnalyzerResult:
    """Base class for all analyzers results.

    If you want to add a new analyzer, inherit a results class from the class.
    For correct initiation you should add a decorator `@dataclass` to children classes too.

        For example:

        @dataclass
        class RegressionPerformanceAnalyzerResults(BaseAnalyzerResult):
            my_result: str
    """

    columns: DatasetColumns


class Analyzer:
    @abc.abstractmethod
    def calculate(
        self, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame], column_mapping: ColumnMapping
    ) -> BaseAnalyzerResult:
        raise NotImplementedError()

    options_provider: OptionsProvider
