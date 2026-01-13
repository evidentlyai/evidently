"""SDK for programmatic access to Evidently artifacts and configurations.

The SDK provides APIs for managing:
- Artifacts: Stored evaluation results and data
- Prompts: LLM prompt templates and versions
- Configs: Reusable evaluation configurations
- Datasets: Dataset metadata and storage
- Panels: Dashboard panel configurations

SDK classes work with both local (`Workspace`) and remote (`RemoteWorkspace`,
`CloudWorkspace`) storage backends.

Example:
```python
from evidently.ui import Workspace

workspace = Workspace.create("my_workspace")
# Access SDK via workspace properties
artifacts = workspace.artifacts
prompts = workspace.prompts
configs = workspace.configs
```
"""
