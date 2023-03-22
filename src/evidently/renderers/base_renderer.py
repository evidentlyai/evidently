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


class BaseRenderer:
    """Base class for all renderers"""

    color_options: ColorOptions

    def __init__(self, color_options: Optional[ColorOptions] = None) -> None:
        if color_options is None:
            self.color_options = ColorOptions()

        else:
            self.color_options = color_options


class MetricRenderer(BaseRenderer):
    def render_pandas(self, obj: "Metric[TResult]") -> pd.DataFrame:
        return obj.get_result().get_pandas()

    def render_json(self, obj: "Metric[TResult]") -> dict:
        result = obj.get_result()
        return result.get_dict()

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

    def with_details(self, title: str, info: BaseWidgetInfo):
        self.details.append(DetailsInfo(title, info))
        return self


class TestRenderer(BaseRenderer):
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


def default_renderer(wrap_type):
    def wrapper(cls):
        DEFAULT_RENDERERS.typed_renderers[wrap_type] = cls()
        return cls

    return wrapper


DEFAULT_RENDERERS = RenderersDefinitions(default_html_test_renderer=TestRenderer())
