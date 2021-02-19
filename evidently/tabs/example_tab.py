from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.tabs_widget import TabsWidget
from evidently.widgets.widget import Widget


class ExampleTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        return [TabsWidget()]
