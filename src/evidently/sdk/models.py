from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import validator
from evidently.legacy.core import new_id
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import PanelID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TabID


class DashboardTabModel(BaseModel):
    """Model for a dashboard tab.

    Represents a single tab in a dashboard configuration. Tabs organize panels
    into logical groups for better visualization organization.
    """

    id: TabID = Field(default_factory=uuid6.uuid7)
    """Unique tab identifier."""
    title: Optional[str]
    """Optional tab title."""
    panels: List[PanelID]
    """List of panel IDs in this tab."""


class PanelMetric(BaseModel):
    """Configuration for a metric displayed in a dashboard panel.

    Specifies which metric to display and how it should be rendered. Used in
    `DashboardPanelPlot.values` to configure what metrics appear in a panel.
    """

    legend: Optional[str] = None
    """Optional legend text for the metric."""
    tags: List[str] = Field(default_factory=list)
    """List of tags associated with the metric."""
    metadata: Dict[str, str] = Field(default_factory=dict)
    """Additional metadata as key-value pairs."""
    metric: str
    """Metric identifier (e.g., `"evidently:metric_v2:ColumnSummary"`)."""
    metric_labels: Dict[str, str] = Field(default_factory=dict)
    """Labels for metric values. Maps metric value keys to display labels."""
    view_params: Dict[str, Any] = Field(default_factory=dict)
    """Parameters for customizing the metric view. Format depends on the metric type."""

    @validator("metric")
    def metric_is_alias(cls, v):
        if not v.startswith("evidently:metric_v2:"):
            v = f"evidently:metric_v2:{v}"
        return v


class DashboardPanelPlot(BaseModel):
    """Model for a dashboard panel displaying metrics.

    Represents a single visualization panel in a dashboard. Panels can display
    one or more metrics using various visualization types (text, counter, line plot, etc.).
    Use panel factory functions like `text_panel` or `bar_plot_panel` to create instances.
    """

    id: PanelID = Field(default_factory=uuid6.uuid7)
    """Unique panel identifier."""
    title: str
    """Panel title."""
    subtitle: Optional[str]
    """Optional panel subtitle."""
    size: Optional[str]
    """Optional panel size specification."""
    values: List[PanelMetric]
    """List of `PanelMetric` objects to display in this panel."""
    plot_params: Dict[str, Any] = Field(default_factory=dict)
    """Parameters for customizing the plot visualization. Format depends on plot type (e.g., `plot_type`, `aggregation`, `is_stacked`)."""


class DashboardModel(BaseModel):
    """Complete dashboard configuration.

    Contains all tabs and panels that make up a project's dashboard. Used to
    configure how metrics are organized and displayed in the UI.
    """

    tabs: List[DashboardTabModel]
    """List of `DashboardTabModel` objects representing dashboard tabs."""
    panels: List[DashboardPanelPlot]
    """List of `DashboardPanelPlot` objects representing dashboard panels."""


class ProjectModel(BaseModel):
    """Model for an Evidently project.

    Represents a project that organizes evaluations, snapshots, and datasets.
    Projects are the top-level organizational unit in Evidently workspaces.
    """

    id: ProjectID = Field(default_factory=new_id)
    """Unique project identifier."""
    name: str
    """Project name."""
    description: Optional[str] = None
    """Optional project description."""
    org_id: Optional[OrgID] = None
    """Optional organization ID (for cloud workspaces)."""
    version: str = "2"
    """Project version string."""


class SnapshotLink(BaseModel):
    """Link between a snapshot and a dataset.

    Associates a snapshot (evaluation run) with a dataset, specifying the dataset's
    role (reference vs current) and subtype (e.g., production, training).
    """

    snapshot_id: SnapshotID
    """ID of the snapshot."""
    dataset_type: str
    """Type of dataset (e.g., `"reference"`, `"current"`)."""
    dataset_subtype: str
    """Subtype of dataset (e.g., `"production"`, `"training"`)."""


class SnapshotMetadataModel(BaseModel):
    """Metadata for a snapshot (evaluation run).

    Contains information about a snapshot including its ID, name, tags, timestamp,
    and links to associated datasets. Returned when listing or querying snapshots.
    """

    id: SnapshotID
    """Unique snapshot identifier."""
    name: Optional[str]
    """Optional snapshot name."""
    metadata: Dict[str, str]
    """Additional metadata as key-value pairs."""
    tags: List[str]
    """List of tags associated with the snapshot."""
    timestamp: datetime
    """Timestamp when the snapshot was created."""
    links: SnapshotLinks
    """Links to datasets associated with this snapshot. Maps dataset types to `SnapshotLink` objects."""
