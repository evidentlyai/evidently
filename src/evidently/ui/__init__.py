"""UI and workspace management for storing and visualizing evaluations.

This module provides interfaces for:
- `Workspace`: Local file-based storage for projects and runs
- `RemoteWorkspace`: Remote API-based storage
- `CloudWorkspace`: Evidently Cloud storage
- `EvidentlyUIRunner`: Run the Evidently UI service

Workspaces allow you to persist evaluation results, organize them into projects,
and visualize them over time. Use workspaces to:
- Store multiple evaluation runs
- Compare results across time or model versions
- Build dashboards with custom visualizations
- Share results with your team

**Documentation**:
- [Platform Overview](https://docs.evidentlyai.com/docs/platform/overview) for workspace concepts
- [Self-hosting Guide](https://docs.evidentlyai.com/docs/setup/self-hosting) for local setup

Example:
```python
from evidently.ui import Workspace

workspace = Workspace.create("my_workspace")
project = workspace.add_project(ProjectModel(name="My Project"))
workspace.add_run(project.id, snapshot)
```
"""

from evidently.ui import runner
from evidently.ui import workspace

__all__ = ["workspace", "runner"]
