"""Additional types, classes, dataclasses, etc."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

# type for numeric because of mypy bug https://github.com/python/mypy/issues/3186
Numeric = Union[float, int]

# type for distributions - list of tuples (value, count)
ColumnDistribution = Dict[Any, Numeric]


class ApproxValue:
    """Class for approximate scalar value calculations"""

    DEFAULT_RELATIVE = 1e-6
    DEFAULT_ABSOLUTE = 1e-12
    value: Numeric
    _relative: Numeric
    _absolute: Numeric

    def __init__(self, value: Numeric, relative: Optional[Numeric] = None, absolute: Optional[Numeric] = None):
        self.value = value

        if relative is not None and relative <= 0:
            raise ValueError("Relative value for approx should be greater than 0")

        if relative is None:
            self._relative = self.DEFAULT_RELATIVE

        else:
            self._relative = relative

        if absolute is None:
            self._absolute = self.DEFAULT_ABSOLUTE

        else:
            self._absolute = absolute

    @property
    def tolerance(self) -> Numeric:
        relative_value = abs(self.value) * self._relative
        return max(relative_value, self._absolute)

    def __format__(self, format_spec):
        return f"{format(self.value, format_spec)} ± {format(self.tolerance, format_spec)}"

    def __repr__(self):
        return f"{self.value} ± {self.tolerance}"

    def __eq__(self, other):
        tolerance = self.tolerance
        return (self.value - tolerance) <= other <= (self.value + tolerance)

    def __lt__(self, other):
        return self.value + self.tolerance < other

    def __le__(self, other):
        return self.value - self.tolerance <= other

    def __gt__(self, other):
        return self.value - self.tolerance > other

    def __ge__(self, other):
        return self.value + self.tolerance >= other

    def as_dict(self) -> dict:
        result = {"value": self.value}

        if self._relative is not None:
            result["relative"] = self._relative

        if self._absolute is not None:
            result["absolute"] = self._absolute

        return result
