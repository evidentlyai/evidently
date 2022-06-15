import abc
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, Tuple

import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping

TResult = TypeVar("TResult")


@dataclass
class InputData:
    reference_data: Optional[pd.DataFrame]
    current_data: pd.DataFrame
    column_mapping: ColumnMapping


class Metric(Generic[TResult]):
    @abc.abstractmethod
    def calculate(self, data: InputData, metrics: dict) -> TResult:
        raise NotImplementedError()

    @classmethod
    def get_results(cls, results) -> TResult:
        return results[cls]


@dataclass
class NumberRange:
    exact: Optional[int] = None
    left_side_threshold: Optional[int] = None
    right_side_threshold: Optional[int] = None
    is_in: Optional[Tuple[int, int]] = None

    def get_range(self) -> Tuple[int, int]:
        if self.exact is not None:
            if any([self.left_side_threshold, self.right_side_threshold, self.is_in]):
                raise ValueError("Can be only set one of: exact, left_side_threshold/right_size_threshold, is_in.")
            return self.exact, self.exact
        if self.left_side_threshold is not None or self.right_side_threshold is not None:
            if self.is_in is not None:
                raise ValueError("Can be only set one of: exact, left_side_threshold/right_size_threshold, is_in.")
            return self.left_side_threshold, self.right_side_threshold
        if self.is_in is not None:
            if len(self.is_in) != 2:
                raise ValueError("Parameter is_in should have exactly two value.")
            return self.is_in
        raise ValueError("Some parameters (exact, left_side_threshold, right_side_threshold, is_in) should be set.")
