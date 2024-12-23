from evidently.pydantic_utils import register_type_alias
from evidently.ui.dashboards.base import DashboardPanel

register_type_alias(
    DashboardPanel, "evidently.v2.backport.DashboardPanelV2", "evidently:dashboard_panel:DashboardPanelV2"
)
register_type_alias(
    DashboardPanel,
    "evidently.v2.backport.SingleValueDashboardPanel",
    "evidently:dashboard_panel:SingleValueDashboardPanel",
)
