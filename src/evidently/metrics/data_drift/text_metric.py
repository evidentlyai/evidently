from typing import ClassVar
from typing import List

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.core import IncludeTags
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import AnyOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import text_widget


class CommentResults(MetricResult):
    __type_alias__: ClassVar = "evidently:metric_result:CommentResults"
    __dict_include__: ClassVar = False
    __tags__: ClassVar = {IncludeTags.Render}

    text: str


class Comment(Metric[CommentResults]):
    __type_alias__: ClassVar = "evidently:metric:Comment"

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
