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
    def render_html(self, obj) -> TestHtmlInfo:
        result = obj.get_result()
        return TestHtmlInfo(name=result.name, description=result.description, status=result.status, details=[])

    def render_json(self, obj) -> dict:
        result = obj.get_result()
        return {
            "name": result.name,
            "description": result.description,
            "status": result.status,
            "group": obj.group,
            "parameters": {},
        }


@dataclasses.dataclass
class RenderersDefinitions:
    typed_renderers: dict = dataclasses.field(default_factory=dict)
    default_html_test_renderer: Optional[TestRenderer] = None
    default_html_metric_renderer: Optional[MetricRenderer] = None


def default_renderer(test_type):
    def wrapper(cls):
        DEFAULT_RENDERERS.typed_renderers[test_type] = cls()
        return cls

    return wrapper


DEFAULT_RENDERERS = RenderersDefinitions(default_html_test_renderer=TestRenderer())
