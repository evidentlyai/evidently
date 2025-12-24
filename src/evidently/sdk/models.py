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

    Args:
    * `id`: Unique tab identifier.
    * `title`: Optional tab title.
    * `panels`: List of panel IDs in this tab.
    """

    id: TabID = Field(default_factory=uuid6.uuid7)
    """Unique tab identifier."""
    title: Optional[str]
    """Optional tab title."""
    panels: List[PanelID]
    """List of panel IDs in this tab."""


class PanelMetric(BaseModel):
    """Configuration for a metric displayed in a dashboard panel.

    Args:
    * `legend`: Optional legend text for the metric.
    * `tags`: List of tags associated with the metric.
    * `metadata`: Additional metadata as key-value pairs.
    * `metric`: Metric identifier (e.g., "evidently:metric_v2:ColumnSummary").
    * `metric_labels`: Labels for metric values.
    * `view_params`: Parameters for customizing the metric view.
    """

    legend: Optional[str] = None
    """Optional legend text for the metric."""
    tags: List[str] = Field(default_factory=list)
    """List of tags associated with the metric."""
    metadata: Dict[str, str] = Field(default_factory=dict)
    """Additional metadata as key-value pairs."""
    metric: str
    """Metric identifier (e.g., "evidently:metric_v2:ColumnSummary")."""
    metric_labels: Dict[str, str] = Field(default_factory=dict)
    """Labels for metric values."""
    view_params: Dict[str, Any] = Field(default_factory=dict)
    """Parameters for customizing the metric view."""

    @validator("metric")
    def metric_is_alias(cls, v):
        if not v.startswith("evidently:metric_v2:"):
            v = f"evidently:metric_v2:{v}"
        return v


class DashboardPanelPlot(BaseModel):
    """Model for a dashboard panel displaying metrics.

    Args:
    * `id`: Unique panel identifier.
    * `title`: Panel title.
    * `subtitle`: Optional panel subtitle.
    * `size`: Optional panel size specification.
    * `values`: List of metrics to display in this panel.
    * `plot_params`: Parameters for customizing the plot visualization.
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
    """List of metrics to display in this panel."""
    plot_params: Dict[str, Any] = Field(default_factory=dict)
    """Parameters for customizing the plot visualization."""


class DashboardModel(BaseModel):
    """Complete dashboard configuration.

    Args:
    * `tabs`: List of dashboard tabs.
    * `panels`: List of dashboard panels.
    """

    tabs: List[DashboardTabModel]
    """List of dashboard tabs."""
    panels: List[DashboardPanelPlot]
    """List of dashboard panels."""


class ProjectModel(BaseModel):
    """Model for an Evidently project.

    Args:
    * `id`: Unique project identifier.
    * `name`: Project name.
    * `description`: Optional project description.
    * `org_id`: Optional organization ID (for cloud workspaces).
    * `version`: Project version string.
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

    Args:
    * `snapshot_id`: ID of the snapshot.
    * `dataset_type`: Type of dataset (e.g., "reference", "current").
    * `dataset_subtype`: Subtype of dataset (e.g., "production", "training").
    """

    snapshot_id: SnapshotID
    """ID of the snapshot."""
    dataset_type: str
    """Type of dataset (e.g., "reference", "current")."""
    dataset_subtype: str
    """Subtype of dataset (e.g., "production", "training")."""


class SnapshotMetadataModel(BaseModel):
    """Metadata for a snapshot (evaluation run).

    Args:
    * `id`: Unique snapshot identifier.
    * `name`: Optional snapshot name.
    * `metadata`: Additional metadata as key-value pairs.
    * `tags`: List of tags associated with the snapshot.
    * `timestamp`: Timestamp when the snapshot was created.
    * `links`: Links to datasets associated with this snapshot.
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
    """Links to datasets associated with this snapshot."""
