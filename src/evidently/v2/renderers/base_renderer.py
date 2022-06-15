import abc

import dataclasses
from typing import List

from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.v2.tests.base_test import TestResult


class HtmlRenderer:
    @abc.abstractmethod
    def render(self, obj) -> BaseWidgetInfo:
        raise NotImplementedError()


@dataclasses.dataclass
class DetailsInfo:
    id: str
    title: str
    info: AdditionalGraphInfo


@dataclasses.dataclass
class TestHtmlInfo:
    name: str
    description: str
    status: str
    details: List[DetailsInfo]


class TestHtmlRenderer:
    def render(self, obj: TestResult) -> TestHtmlInfo:
        return TestHtmlInfo(name=obj.name, description=obj.description, status=obj.status, details=[])
