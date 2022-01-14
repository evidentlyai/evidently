from evidently.tabs.base_tab import Tab, Verbose
from my_widgets.target_distribution_widget import TargetDistributionWidget
from my_widgets.target_distribution_hist_widget import TargetDistributionHistWidget

class MySimpleTab(Tab):
    widgets = [
        (TargetDistributionWidget('Target distribution'), Verbose.ALWAYS),
        (TargetDistributionHistWidget('Target distribution hist'), Verbose.ALWAYS)
    ]