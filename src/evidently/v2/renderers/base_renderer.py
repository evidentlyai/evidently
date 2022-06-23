import abc

import dataclasses
from typing import List

from evidently.model.widget import BaseWidgetInfo
from evidently.v2.tests.base_test import TestResult


class MetricRenderer:
    @abc.abstractmethod
    def render(self, obj) -> BaseWidgetInfo:
        raise NotImplementedError()


@dataclasses.dataclass
class DetailsInfo:
    id: str
    title: str
    info: BaseWidgetInfo


@dataclasses.dataclass
class TestHtmlInfo:
    name: str
    description: str
    status: str
    details: List[DetailsInfo]


class TestRenderer:
    @abc.abstractmethod
    def render_html(self, obj: TestResult) -> TestHtmlInfo:
        return TestHtmlInfo(name=obj.name, description=obj.description, status=obj.status, details=[])

    @abc.abstractmethod
    def render_json(self, obj: TestResult) -> dict:
        return {
            "name": obj.name,
            "description": obj.description,
            "status": obj.status,
        }
