"""Tests for RemoteWorkspace SDK: prompts, artifacts, and configs."""

from unittest.mock import patch

import pytest
from litestar.testing import TestClient

from evidently.llm.prompts.content import PromptContent
from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactMetadata
from evidently.sdk.configs import DescriptorContent
from evidently.ui.workspace import RemoteWorkspace


@pytest.fixture
def remote_workspace(test_client: TestClient):
    """Create a RemoteWorkspace pointing to the test client."""
    # Get the base URL from the test client and convert to string
    base_url = str(test_client.base_url)

    # Mock Session.send to use test client
    from requests import Response as RequestsResponse
    from requests import Session
    from requests.structures import CaseInsensitiveDict

    def mock_send(self, request, **kwargs):
        # Extract path from URL
        url = request.url
        path = url.replace(base_url, "")
        if not path.startswith("/"):
            path = "/" + path

        # Extract query params from URL
        from urllib.parse import parse_qs
        from urllib.parse import urlparse

        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        # Convert lists to single values
        query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}

        # Extract body from request
        body = None
        if request.body:
            import json as json_lib

            try:
                body = json_lib.loads(request.body)
            except (json_lib.JSONDecodeError, TypeError):
                body = request.body

        # Use test client to make the request
        method = request.method.upper()
        if method == "GET":
            response = test_client.get(path, params=query_params)
        elif method == "POST":
            response = test_client.post(path, json=body, params=query_params)
        elif method == "PUT":
            response = test_client.put(path, json=body, params=query_params)
        elif method == "DELETE":
            response = test_client.delete(path, params=query_params)
        else:
            raise ValueError(f"Unsupported method: {method}")

        # Create a mock response object that mimics requests.Response
        mock_response = RequestsResponse()
        mock_response.status_code = response.status_code
        mock_response._content = response.content
        mock_response.headers = CaseInsensitiveDict(response.headers)
        mock_response.url = url

        def json():
            return response.json()

        mock_response.json = json

        def raise_for_status():
            if mock_response.status_code >= 400:
                from requests.exceptions import HTTPError

                raise HTTPError(f"HTTP {mock_response.status_code}", response=mock_response)
            return mock_response

        mock_response.raise_for_status = raise_for_status

        return mock_response

    with patch.object(Session, "send", mock_send):
        workspace = RemoteWorkspace(base_url=base_url, verify=False)
        yield workspace


@pytest.fixture
def test_project_id(remote_workspace: RemoteWorkspace):
    """Create a test project and return its ID."""
    from evidently.sdk.models import ProjectModel

    project_data = ProjectModel(name="test project", description="test")
    project = remote_workspace.add_project(project_data)
    return project.id


@pytest.mark.asyncio
async def test_remote_workspace_artifacts_list(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.artifacts.list_artifacts()."""
    # Initially empty
    artifacts = remote_workspace.artifacts.list_artifacts(test_project_id)
    assert len(artifacts) == 0

    # Create an artifact
    artifact = remote_workspace.artifacts.create_artifact(test_project_id, "test artifact")
    assert artifact.name == "test artifact"

    # List artifacts
    artifacts = remote_workspace.artifacts.list_artifacts(test_project_id)
    assert len(artifacts) == 1
    assert artifacts[0].id == artifact.id
    assert artifacts[0].name == "test artifact"


@pytest.mark.asyncio
async def test_remote_workspace_artifacts_get(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.artifacts.get_artifact()."""
    # Create an artifact
    created = remote_workspace.artifacts.create_artifact(test_project_id, "my artifact")

    # Get by ID
    retrieved = remote_workspace.artifacts.get_artifact_by_id(test_project_id, created.id)
    assert retrieved.id == created.id
    assert retrieved.name == "my artifact"

    # Get by name
    retrieved_by_name = remote_workspace.artifacts.get_artifact(test_project_id, "my artifact")
    assert retrieved_by_name.id == created.id
    assert retrieved_by_name.name == "my artifact"


@pytest.mark.asyncio
async def test_remote_workspace_artifacts_versions(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.artifacts version operations."""
    # Create an artifact
    artifact = remote_workspace.artifacts.create_artifact(test_project_id, "versioned artifact")

    # Initially no versions
    versions = remote_workspace.artifacts.list_versions(artifact.id)
    assert len(versions) == 0

    # Create a version
    from evidently.descriptors import TextLength
    from evidently.sdk.configs import DescriptorContent

    descriptor = TextLength(column_name="test_col", alias="test")
    content = DescriptorContent.from_value(descriptor)

    version = remote_workspace.artifacts.create_version(artifact.id, 1, content)
    assert version.version == 1
    assert version.artifact_id == artifact.id

    # List versions
    versions = remote_workspace.artifacts.list_versions(artifact.id)
    assert len(versions) == 1

    # Get version
    retrieved = remote_workspace.artifacts.get_version(artifact.id, 1)
    assert retrieved.version == 1

    # Get latest
    latest = remote_workspace.artifacts.get_version(artifact.id, "latest")
    assert latest.version == 1


@pytest.mark.asyncio
async def test_remote_workspace_artifacts_bump_version(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.artifacts.bump_artifact_version()."""
    # Create an artifact
    artifact = remote_workspace.artifacts.create_artifact(test_project_id, "bump artifact")

    # Bump version (creates version 1)
    from evidently.descriptors import TextLength

    descriptor1 = TextLength(column_name="v1_col", alias="v1")
    content1 = DescriptorContent.from_value(descriptor1)
    version1 = remote_workspace.artifacts.bump_artifact_version(artifact.id, content1)
    assert version1.version == 1

    # Bump again (creates version 2)
    descriptor2 = TextLength(column_name="v2_col", alias="v2")
    content2 = DescriptorContent.from_value(descriptor2)
    version2 = remote_workspace.artifacts.bump_artifact_version(artifact.id, content2)
    assert version2.version == 2

    # Get latest should be version 2
    latest = remote_workspace.artifacts.get_version(artifact.id, "latest")
    assert latest.version == 2


@pytest.mark.asyncio
async def test_remote_workspace_prompts_list(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.prompts.list_prompts()."""
    # Initially empty
    prompts = remote_workspace.prompts.list_prompts(test_project_id)
    assert len(prompts) == 0

    # Create a prompt
    prompt = remote_workspace.prompts.create_prompt(test_project_id, "test prompt")
    assert prompt.name == "test prompt"

    # List prompts
    prompts = remote_workspace.prompts.list_prompts(test_project_id)
    assert len(prompts) == 1
    assert prompts[0].id == prompt.id
    assert prompts[0].name == "test prompt"


@pytest.mark.asyncio
async def test_remote_workspace_prompts_get(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.prompts.get_prompt()."""
    # Create a prompt
    created = remote_workspace.prompts.create_prompt(test_project_id, "my prompt")

    # Get by ID
    retrieved = remote_workspace.prompts.get_prompt_by_id(test_project_id, created.id)
    assert retrieved.id == created.id
    assert retrieved.name == "my prompt"

    # Get by name
    retrieved_by_name = remote_workspace.prompts.get_prompt(test_project_id, "my prompt")
    assert retrieved_by_name.id == created.id
    assert retrieved_by_name.name == "my prompt"


@pytest.mark.asyncio
async def test_remote_workspace_prompts_versions(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.prompts version operations."""
    # Create a prompt
    prompt = remote_workspace.prompts.create_prompt(test_project_id, "versioned prompt")

    # Initially no versions
    versions = remote_workspace.prompts.list_versions(prompt.id)
    assert len(versions) == 0

    # Create a version with PromptContent (using MessagesPromptContent)
    from evidently.llm.models import LLMMessage
    from evidently.llm.prompts.content import MessagesPromptContent

    prompt_content = MessagesPromptContent(
        messages=[
            LLMMessage(role="system", content="You are a helpful assistant."),
            LLMMessage(role="user", content="Hello!"),
        ]
    )

    version = remote_workspace.prompts.create_version(prompt.id, 1, prompt_content)
    assert version.version == 1
    assert version.prompt_id == prompt.id

    # List versions
    versions = remote_workspace.prompts.list_versions(prompt.id)
    assert len(versions) == 1

    # Get version
    retrieved = remote_workspace.prompts.get_version(prompt.id, 1)
    assert retrieved.version == 1
    assert isinstance(retrieved.content, PromptContent)

    # Get latest
    latest = remote_workspace.prompts.get_version(prompt.id, "latest")
    assert latest.version == 1


@pytest.mark.asyncio
async def test_remote_workspace_prompts_bump_version(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.prompts.bump_prompt_version()."""
    # Create a prompt
    prompt = remote_workspace.prompts.create_prompt(test_project_id, "bump prompt")

    # Bump version (creates version 1)
    from evidently.llm.models import LLMMessage
    from evidently.llm.prompts.content import MessagesPromptContent

    prompt_content1 = MessagesPromptContent(
        messages=[
            LLMMessage(role="system", content="Version 1"),
        ]
    )
    version1 = remote_workspace.prompts.bump_prompt_version(prompt.id, prompt_content1)
    assert version1.version == 1

    # Bump again (creates version 2)
    prompt_content2 = MessagesPromptContent(
        messages=[
            LLMMessage(role="system", content="Version 2"),
        ]
    )
    version2 = remote_workspace.prompts.bump_prompt_version(prompt.id, prompt_content2)
    assert version2.version == 2

    # Get latest should be version 2
    latest = remote_workspace.prompts.get_version(prompt.id, "latest")
    assert latest.version == 2


@pytest.mark.asyncio
async def test_remote_workspace_configs_list(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.configs.list_configs()."""
    # Initially empty
    configs = remote_workspace.configs.list_configs(test_project_id)
    assert len(configs) == 0

    # Create a config
    config = remote_workspace.configs.create_config(test_project_id, "test config")
    assert config.name == "test config"

    # List configs
    configs = remote_workspace.configs.list_configs(test_project_id)
    assert len(configs) == 1
    assert configs[0].id == config.id
    assert configs[0].name == "test config"


@pytest.mark.asyncio
async def test_remote_workspace_configs_get(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.configs.get_config()."""
    # Create a config
    created = remote_workspace.configs.create_config(test_project_id, "my config")

    # Get by ID
    retrieved = remote_workspace.configs.get_config_by_id(test_project_id, created.id)
    assert retrieved.id == created.id
    assert retrieved.name == "my config"

    # Get by name
    retrieved_by_name = remote_workspace.configs.get_config(test_project_id, "my config")
    assert retrieved_by_name.id == created.id
    assert retrieved_by_name.name == "my config"


@pytest.mark.asyncio
async def test_remote_workspace_configs_versions(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.configs version operations."""
    # Create a config
    config = remote_workspace.configs.create_config(test_project_id, "versioned config")

    # Initially no versions
    versions = remote_workspace.configs.list_versions(config.id)
    assert len(versions) == 0

    # Create a version with DescriptorContent
    from evidently.descriptors import TextLength

    descriptor = TextLength(column_name="test_col", alias="test")
    content = DescriptorContent.from_value(descriptor)

    version = remote_workspace.configs.create_version(config.id, 1, content)
    assert version.version == 1
    assert version.artifact_id == config.id

    # List versions
    versions = remote_workspace.configs.list_versions(config.id)
    assert len(versions) == 1

    # Get version
    retrieved = remote_workspace.configs.get_version(config.id, 1)
    assert retrieved.version == 1

    # Get latest
    latest = remote_workspace.configs.get_version(config.id, "latest")
    assert latest.version == 1


@pytest.mark.asyncio
async def test_remote_workspace_configs_bump_version(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.configs.bump_config_version()."""
    # Create a config
    config = remote_workspace.configs.create_config(test_project_id, "bump config")

    # Bump version (creates version 1)
    from evidently.descriptors import TextLength

    descriptor1 = TextLength(column_name="v1_col", alias="v1")
    content1 = DescriptorContent.from_value(descriptor1)
    version1 = remote_workspace.configs.bump_config_version(config.id, content1)
    assert version1.version == 1

    # Bump again (creates version 2)
    descriptor2 = TextLength(column_name="v2_col", alias="v2")
    content2 = DescriptorContent.from_value(descriptor2)
    version2 = remote_workspace.configs.bump_config_version(config.id, content2)
    assert version2.version == 2

    # Get latest should be version 2
    latest = remote_workspace.configs.get_version(config.id, "latest")
    assert latest.version == 2


@pytest.mark.asyncio
async def test_remote_workspace_configs_add_descriptor(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.configs.add_descriptor() helper method."""
    # Add descriptor (creates config if needed)
    from evidently.descriptors import TextLength

    descriptor = TextLength(column_name="test_col", alias="test")
    version = remote_workspace.configs.add_descriptor(test_project_id, "my descriptor", descriptor)
    assert version.version == 1

    # Get the descriptor back
    retrieved = remote_workspace.configs.get_descriptor(test_project_id, "my descriptor")
    assert retrieved.column_name == "test_col"
    assert retrieved.alias == "test"

    # Add another version
    descriptor2 = TextLength(column_name="test2_col", alias="test2")
    version2 = remote_workspace.configs.add_descriptor(test_project_id, "my descriptor", descriptor2)
    assert version2.version == 2

    # Get latest
    retrieved_latest = remote_workspace.configs.get_descriptor(test_project_id, "my descriptor", "latest")
    assert retrieved_latest.column_name == "test2_col"
    assert retrieved_latest.alias == "test2"


@pytest.mark.asyncio
async def test_remote_workspace_prompts_update(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.prompts.update_prompt()."""
    # Create a prompt
    prompt = remote_workspace.prompts.create_prompt(test_project_id, "original name")

    # Update it
    from evidently.sdk.prompts import Prompt
    from evidently.sdk.prompts import PromptMetadata

    updated = Prompt(
        id=prompt.id,
        project_id=prompt.project_id,
        name="updated name",
        metadata=PromptMetadata(),
    )
    remote_workspace.prompts.update_prompt(updated)

    # Verify update
    retrieved = remote_workspace.prompts.get_prompt_by_id(test_project_id, prompt.id)
    assert retrieved.name == "updated name"


@pytest.mark.asyncio
async def test_remote_workspace_artifacts_update(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.artifacts.update_artifact()."""
    # Create an artifact
    artifact = remote_workspace.artifacts.create_artifact(test_project_id, "original name")

    # Update it
    updated = Artifact(
        id=artifact.id,
        project_id=artifact.project_id,
        name="updated name",
        metadata=ArtifactMetadata(description="Updated description"),
    )
    remote_workspace.artifacts.update_artifact(updated)

    # Verify update
    retrieved = remote_workspace.artifacts.get_artifact_by_id(test_project_id, artifact.id)
    assert retrieved.name == "updated name"
    assert retrieved.metadata.description == "Updated description"


@pytest.mark.asyncio
async def test_remote_workspace_configs_update(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.configs.update_config()."""
    # Create a config
    config = remote_workspace.configs.create_config(test_project_id, "original name")

    # Update it
    from evidently.sdk.configs import ConfigMetadata
    from evidently.sdk.configs import GenericConfig

    updated = GenericConfig(
        id=config.id,
        project_id=config.project_id,
        name="updated name",
        metadata=ConfigMetadata(description="Updated description"),
    )
    remote_workspace.configs.update_config(updated)

    # Verify update
    retrieved = remote_workspace.configs.get_config_by_id(test_project_id, config.id)
    assert retrieved.name == "updated name"
    assert retrieved.metadata.description == "Updated description"


@pytest.mark.asyncio
async def test_remote_workspace_prompts_delete(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.prompts.delete_prompt()."""
    # Create a prompt
    prompt = remote_workspace.prompts.create_prompt(test_project_id, "to delete")

    # Delete it
    remote_workspace.prompts.delete_prompt(prompt.id)

    # Should not exist
    prompts = remote_workspace.prompts.list_prompts(test_project_id)
    assert len(prompts) == 0


@pytest.mark.asyncio
async def test_remote_workspace_artifacts_delete(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.artifacts.delete_artifact()."""
    # Create an artifact
    artifact = remote_workspace.artifacts.create_artifact(test_project_id, "to delete")

    # Delete it
    remote_workspace.artifacts.delete_artifact(artifact.id)

    # Should not exist
    artifacts = remote_workspace.artifacts.list_artifacts(test_project_id)
    assert len(artifacts) == 0


@pytest.mark.asyncio
async def test_remote_workspace_configs_delete(remote_workspace: RemoteWorkspace, test_project_id):
    """Test RemoteWorkspace.configs.delete_config()."""
    # Create a config
    config = remote_workspace.configs.create_config(test_project_id, "to delete")

    # Delete it
    remote_workspace.configs.delete_config(config.id)

    # Should not exist
    configs = remote_workspace.configs.list_configs(test_project_id)
    assert len(configs) == 0
