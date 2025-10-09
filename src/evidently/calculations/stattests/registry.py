from typing import Callable, Dict
from dataclasses import dataclass


@dataclass
class StatTest:
    name: str
    display_name: str
    func: Callable
    allowed_feature_types: list


STAT_TESTS: Dict[str, StatTest] = {}


def register_stattest(test: StatTest):
    STAT_TESTS[test.name] = test
