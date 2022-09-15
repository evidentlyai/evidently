from my_widgets.target_distribution_hist_widget import TargetDistributionHistWidget
from my_widgets.target_distribution_widget import TargetDistributionWidget

from evidently.dashboard.tabs.base_tab import Tab
from evidently.dashboard.tabs.base_tab import Verbose


class MySimpleTab(Tab):
    widgets = [
        (TargetDistributionWidget("Target distribution"), Verbose.ALWAYS),
        (TargetDistributionHistWidget("Target distribution hist"), Verbose.ALWAYS),
    ]
