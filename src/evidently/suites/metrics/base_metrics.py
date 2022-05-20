from dataclasses import asdict
from dataclasses import is_dataclass
from typing import Any
from typing import ClassVar
from typing import Optional

import pandas as pd


class BaseCalculation:
    """Base class for all calculations - metrics, tests, etc."""
    name: str
    description: str
    parent: Optional["BaseCalculation"] = None
    result: Optional[Any] = None

    @property
    def id(self) -> str:
        if self.parent:
            return f"{self.parent.id}.{self.name}"
        else:
            return self.name

    def calculate(self) -> None:
        pass

    def get_result_as_dict(self, verbose: bool = False):
        if is_dataclass(self.result):
            result = asdict(self.result)

        else:
            result = self.result

        result = {"result": result}

        if verbose:
            result["name"] = self.name
            result["description"] = self.description

        return result


class OneSourceDatasetMetric(BaseCalculation):
    """Metric with calculations with one source dataset"""
    dataset: pd.DataFrame


class BothSourceDatasetMetric(BaseCalculation):
    """Analyzer with calculations on both source datasets"""
    reference_dataset: pd.DataFrame
    current_dataset: pd.DataFrame


class BaseTest(BaseCalculation):
    required_analyzer = ClassVar[OneSourceDatasetMetric]
    calculated_analyzer: Optional[OneSourceDatasetMetric] = None
    result: bool

    def get_details(self) -> str:
        pass

    def get_result_as_dict(self, verbose: bool = False):
        result = super(BaseTest, self).get_result_as_dict(verbose=verbose)

        if verbose:
            result["details"] = self.get_details()

        return result
