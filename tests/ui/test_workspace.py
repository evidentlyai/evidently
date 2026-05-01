import re
import uuid

import pytest

from evidently.ui.workspace import RemoteWorkspace

# Shared expected message — kept as a constant so the test fails loudly
# if anyone silently removes or waters-down the user-facing guidance.
_EXPECTED_MSG = "The Snapshot API is not yet implemented for RemoteWorkspace. Please use a local Workspace instead."


@pytest.fixture()
def remote_workspace():
    """Return a RemoteWorkspace that skips the server-health check."""
    return RemoteWorkspace(base_url="http://localhost:0", verify=False)


class RemoteWorkspaceSnapshotAPITest:
    """Verify that unimplemented snapshot methods raise an actionable error."""

    def test_list_runs_raises_not_implemented(self, remote_workspace):
        with pytest.raises(NotImplementedError, match=re.escape(_EXPECTED_MSG)):
            remote_workspace.list_runs(str(uuid.uuid4()))

    def test_get_run_raises_not_implemented(self, remote_workspace):
        with pytest.raises(NotImplementedError, match=re.escape(_EXPECTED_MSG)):
            remote_workspace.get_run(str(uuid.uuid4()), str(uuid.uuid4()))

    def test_delete_run_raises_not_implemented(self, remote_workspace):
        with pytest.raises(NotImplementedError, match=re.escape(_EXPECTED_MSG)):
            remote_workspace.delete_run(str(uuid.uuid4()), str(uuid.uuid4()))
