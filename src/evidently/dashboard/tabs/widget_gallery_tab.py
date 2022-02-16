from evidently.dashboard.tabs.base_tab import Tab, Verbose
from evidently.dashboard.widgets.bar_widget import BarWidget
from evidently.dashboard.widgets.counter_widget import CounterWidget
from evidently.dashboard.widgets.expandable_list_widget import ExpandableListWidget
from evidently.dashboard.widgets.percent_widget import PercentWidget


class WidgetGalleryTab(Tab):
    widgets = [
        (BarWidget(""), Verbose.ALWAYS),
        (CounterWidget(""), Verbose.ALWAYS),
        (PercentWidget(""), Verbose.ALWAYS),
        (ExpandableListWidget("Some title"), Verbose.ALWAYS),
    ]
