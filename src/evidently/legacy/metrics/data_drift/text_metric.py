from typing import List

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.core import IncludeTags
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import text_widget


class CommentResults(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:CommentResults"
        dict_include = False
        tags = {IncludeTags.Render}

    text: str


class Comment(Metric[CommentResults]):
    class Config:
        type_alias = "evidently:metric:Comment"

    text: str

    def __init__(self, text: str, options: AnyOptions = None):
        self.text = text
        super().__init__(options=options)

    def calculate(self, data: InputData) -> CommentResults:
        return CommentResults(text=self.text)


@default_renderer(wrap_type=Comment)
class CommentRenderer(MetricRenderer):
    def render_html(self, obj: Comment) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        return [text_widget(text=result.text, title="")]
