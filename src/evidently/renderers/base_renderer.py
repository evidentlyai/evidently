import abc

import dataclasses
from typing import List, Optional, Dict

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
    groups: Dict[str, str]


class TestRenderer:
    def html_description(self, obj):
        return obj.get_result().description

    def json_description(self, obj):
        return obj.get_result().description

    def render_html(self, obj) -> TestHtmlInfo:
        result = obj.get_result()
        return TestHtmlInfo(
            name=result.name,
            description=self.html_description(obj),
            status=result.status,
            details=[],
            groups=result.groups,
        )

    def render_json(self, obj) -> dict:
        result = obj.get_result()
        return {
            "name": result.name,
            "description": self.json_description(obj),
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
