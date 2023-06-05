from typing import List

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.core import IncludeTags
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import text_widget


class CommentResults(MetricResult):
    class Config:
        dict_include = False
        tags = {IncludeTags.Render}

    text: str


class Comment(Metric[CommentResults]):
    def __init__(self, text: str):
        self.text = text

    def calculate(self, data: InputData) -> CommentResults:
        return CommentResults(text=self.text)


@default_renderer(wrap_type=Comment)
class CommentRenderer(MetricRenderer):
    def render_html(self, obj: Comment) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        return [text_widget(text=result.text, title="")]
