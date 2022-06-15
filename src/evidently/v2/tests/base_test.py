from dataclasses import dataclass


@dataclass
class TestResult:
    name: str
    description: str
    status: str


class Test:
    def check(self, metrics: list, tests: list):
        return None

