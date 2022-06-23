import abc

import dataclasses
from typing import List, Optional

from evidently.model.widget import BaseWidgetInfo


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
    def render_html(self, obj) -> TestHtmlInfo:
        return TestHtmlInfo(name=obj.name, description=obj.description, status=obj.status, details=[])

    @abc.abstractmethod
    def render_json(self, obj) -> dict:
        return {
            "name": obj.name,
            "description": obj.description,
            "status": obj.status,
        }


@dataclasses.dataclass
class RenderersDefinitions:
    typed_renderers: dict = dataclasses.field(default_factory=dict)
    default_html_test_renderer: Optional[TestRenderer] = None
    default_html_metric_renderer: Optional[MetricRenderer] = None


DEFAULT_RENDERERS = RenderersDefinitions(default_html_test_renderer=TestRenderer())
