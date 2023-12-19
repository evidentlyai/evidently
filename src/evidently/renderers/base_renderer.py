import dataclasses
import uuid
from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions

if TYPE_CHECKING:
    from evidently.base_metric import Metric
    from evidently.base_metric import TResult
    from evidently.core import IncludeOptions
    from evidently.tests.base_test import Test


class GraphIdGenerator:
    def __init__(self, base_id: str):
        self.base_id = base_id
        self.counter = 0

    def get_id(self) -> str:
        val = f"{self.base_id}-{self.counter}"
        self.counter += 1
        return val


class BaseRenderer:
    """Base class for all renderers"""

    color_options: ColorOptions
    graph_id_generator: GraphIdGenerator

    def __init__(self, color_options: Optional[ColorOptions] = None) -> None:
        if color_options is None:
            self.color_options = ColorOptions()

        else:
            self.color_options = color_options


class MetricRenderer(BaseRenderer):
    def render_pandas(self, obj: "Metric[TResult]") -> pd.DataFrame:
        return obj.get_result().get_pandas()

    def render_json(
        self,
        obj: "Metric[TResult]",
        include_render: bool = False,
        include: "IncludeOptions" = None,
        exclude: "IncludeOptions" = None,
    ) -> dict:
        result = obj.get_result()
        return result.get_dict(include_render=include_render, include=include, exclude=exclude)

    def render_html(self, obj) -> List[BaseWidgetInfo]:
        raise NotImplementedError()


@dataclasses.dataclass
class DetailsInfo:
    title: str
    info: BaseWidgetInfo
    id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))


@dataclasses.dataclass
class TestHtmlInfo:
    name: str
    description: str
    status: str
    details: List[DetailsInfo]
    groups: Dict[str, str]

    graph_id_generator: GraphIdGenerator

    def with_details(self, title: str, info: BaseWidgetInfo):
        self.details.append(DetailsInfo(title, info, id=self.graph_id_generator.get_id()))
        return self


class TestRenderer(BaseRenderer):
    def html_description(self, obj: "Test"):
        return obj.get_result().description

    def json_description(self, obj: "Test"):
        return obj.get_result().description

    def render_html(self, obj) -> TestHtmlInfo:
        result = obj.get_result()
        return TestHtmlInfo(
            name=result.name,
            description=self.html_description(obj),
            status=result.status.value,
            details=[],
            groups=result.groups,
            graph_id_generator=self.graph_id_generator,
        )

    def render_json(
        self,
        obj: "Test",
        include_render: bool = False,
        include: "IncludeOptions" = None,
        exclude: "IncludeOptions" = None,
    ) -> dict:
        return obj.get_result().get_dict(include_render=include_render, include=include, exclude=exclude)


@dataclasses.dataclass
class RenderersDefinitions:
    typed_renderers: dict = dataclasses.field(default_factory=dict)
    default_html_test_renderer: Optional[TestRenderer] = None
    default_html_metric_renderer: Optional[MetricRenderer] = None


def default_renderer(wrap_type):
    def wrapper(cls):
        DEFAULT_RENDERERS.typed_renderers[wrap_type] = cls()
        return cls

    return wrapper


DEFAULT_RENDERERS = RenderersDefinitions(default_html_test_renderer=TestRenderer())
