"""Tests for Workspace SDK: prompts, artifacts, and configs."""

import pytest

from evidently.llm.models import LLMMessage
from evidently.llm.prompts.content import MessagesPromptContent
from evidently.llm.prompts.content import PromptContent
from evidently.sdk.models import ProjectModel
from evidently.sdk.prompts import Prompt
from evidently.sdk.prompts import PromptMetadata
from evidently.ui.workspace import Workspace


@pytest.fixture
def workspace(tmp_path):
    """Create a Workspace instance with a temporary directory."""
    return Workspace(str(tmp_path))


@pytest.fixture
def test_project_id(workspace: Workspace):
    """Create a test project and return its ID."""
    project_data = ProjectModel(name="test project", description="test")
    project = workspace.add_project(project_data)
    return project.id


def test_workspace_prompts_list(workspace: Workspace, test_project_id):
    """Test Workspace.prompts.list_prompts()."""
    # Initially empty
    prompts = workspace.prompts.list_prompts(test_project_id)
    assert len(prompts) == 0

    # Create a prompt
    prompt = workspace.prompts.create_prompt(test_project_id, "test prompt")
    assert prompt.name == "test prompt"

    # List prompts
    prompts = workspace.prompts.list_prompts(test_project_id)
    assert len(prompts) == 1
    assert prompts[0].id == prompt.id
    assert prompts[0].name == "test prompt"


def test_workspace_prompts_get(workspace: Workspace, test_project_id):
    """Test Workspace.prompts.get_prompt()."""
    # Create a prompt
    created = workspace.prompts.create_prompt(test_project_id, "my prompt")

    # Get by ID
    retrieved = workspace.prompts.get_prompt_by_id(test_project_id, created.id)
    assert retrieved.id == created.id
    assert retrieved.name == "my prompt"

    # Get by name
    retrieved_by_name = workspace.prompts.get_prompt(test_project_id, "my prompt")
    assert retrieved_by_name.id == created.id
    assert retrieved_by_name.name == "my prompt"


def test_workspace_prompts_get_or_create(workspace: Workspace, test_project_id):
    """Test Workspace.prompts.get_or_create_prompt()."""
    # Get or create (should create)
    prompt1 = workspace.prompts.get_or_create_prompt(test_project_id, "new prompt")
    assert prompt1.name == "new prompt"

    # Get or create (should get existing)
    prompt2 = workspace.prompts.get_or_create_prompt(test_project_id, "new prompt")
    assert prompt2.id == prompt1.id
    assert prompt2.name == "new prompt"


def test_workspace_prompts_versions(workspace: Workspace, test_project_id):
    """Test Workspace.prompts version operations."""
    # Create a prompt
    prompt = workspace.prompts.create_prompt(test_project_id, "versioned prompt")

    # Initially no versions
    versions = workspace.prompts.list_versions(prompt.id)
    assert len(versions) == 0

    # Create a version with PromptContent (using MessagesPromptContent)
    prompt_content = MessagesPromptContent(
        messages=[
            LLMMessage(role="system", content="You are a helpful assistant."),
            LLMMessage(role="user", content="Hello!"),
        ]
    )

    version = workspace.prompts.create_version(prompt.id, 1, prompt_content)
    assert version.version == 1
    assert version.prompt_id == prompt.id

    # List versions
    versions = workspace.prompts.list_versions(prompt.id)
    assert len(versions) == 1

    # Get version
    retrieved = workspace.prompts.get_version(prompt.id, 1)
    assert retrieved.version == 1
    assert isinstance(retrieved.content, PromptContent)

    # Get latest
    latest = workspace.prompts.get_version(prompt.id, "latest")
    assert latest.version == 1


def test_workspace_prompts_bump_version(workspace: Workspace, test_project_id):
    """Test Workspace.prompts.bump_prompt_version()."""
    # Create a prompt
    prompt = workspace.prompts.create_prompt(test_project_id, "bump prompt")

    # Bump version (creates version 1)
    prompt_content1 = MessagesPromptContent(
        messages=[
            LLMMessage(role="system", content="Version 1"),
        ]
    )
    version1 = workspace.prompts.bump_prompt_version(prompt.id, prompt_content1)
    assert version1.version == 1

    # Bump again (creates version 2)
    prompt_content2 = MessagesPromptContent(
        messages=[
            LLMMessage(role="system", content="Version 2"),
        ]
    )
    version2 = workspace.prompts.bump_prompt_version(prompt.id, prompt_content2)
    assert version2.version == 2

    # Get latest should be version 2
    latest = workspace.prompts.get_version(prompt.id, "latest")
    assert latest.version == 2


def test_workspace_prompts_update(workspace: Workspace, test_project_id):
    """Test Workspace.prompts.update_prompt()."""
    # Create a prompt
    prompt = workspace.prompts.create_prompt(test_project_id, "original name")

    # Update it
    updated = Prompt(
        id=prompt.id,
        project_id=prompt.project_id,
        name="updated name",
        metadata=PromptMetadata(),
    )
    workspace.prompts.update_prompt(updated)

    # Verify update
    retrieved = workspace.prompts.get_prompt_by_id(test_project_id, prompt.id)
    assert retrieved.name == "updated name"


def test_workspace_prompts_delete(workspace: Workspace, test_project_id):
    """Test Workspace.prompts.delete_prompt()."""
    # Create a prompt
    prompt = workspace.prompts.create_prompt(test_project_id, "to delete")

    # Delete it
    workspace.prompts.delete_prompt(prompt.id)

    # Should not exist
    prompts = workspace.prompts.list_prompts(test_project_id)
    assert len(prompts) == 0


def test_workspace_prompts_delete_version(workspace: Workspace, test_project_id):
    """Test Workspace.prompts.delete_version()."""
    # Create a prompt with a version
    prompt = workspace.prompts.create_prompt(test_project_id, "versioned prompt")

    prompt_content = MessagesPromptContent(
        messages=[
            LLMMessage(role="system", content="Test"),
        ]
    )
    version = workspace.prompts.create_version(prompt.id, 1, prompt_content)

    # Delete the version
    workspace.prompts.delete_version(version.id)

    # Version should not exist
    versions = workspace.prompts.list_versions(prompt.id)
    assert len(versions) == 0


def test_workspace_prompts_get_version_by_id(workspace: Workspace, test_project_id):
    """Test Workspace.prompts.get_version_by_id()."""
    # Create a prompt with a version
    prompt = workspace.prompts.create_prompt(test_project_id, "versioned prompt")

    prompt_content = MessagesPromptContent(
        messages=[
            LLMMessage(role="system", content="Test"),
        ]
    )
    version = workspace.prompts.create_version(prompt.id, 1, prompt_content)

    # Get version by ID
    retrieved = workspace.prompts.get_version_by_id(version.id)
    assert retrieved.id == version.id
    assert retrieved.version == 1


def test_workspace_prompts_multiple_prompts(workspace: Workspace, test_project_id):
    """Test Workspace.prompts with multiple prompts."""
    # Create multiple prompts
    workspace.prompts.create_prompt(test_project_id, "prompt 1")
    workspace.prompts.create_prompt(test_project_id, "prompt 2")
    workspace.prompts.create_prompt(test_project_id, "prompt 3")

    # List all prompts
    prompts = workspace.prompts.list_prompts(test_project_id)
    assert len(prompts) == 3

    # Verify all prompts are present
    prompt_names = {p.name for p in prompts}
    assert prompt_names == {"prompt 1", "prompt 2", "prompt 3"}


def test_workspace_prompts_multiple_versions(workspace: Workspace, test_project_id):
    """Test Workspace.prompts with multiple versions."""
    # Create a prompt
    prompt = workspace.prompts.create_prompt(test_project_id, "multi-version prompt")

    # Create multiple versions
    for i in range(1, 4):
        prompt_content = MessagesPromptContent(
            messages=[
                LLMMessage(role="system", content=f"Version {i}"),
            ]
        )
        workspace.prompts.create_version(prompt.id, i, prompt_content)

    # List all versions
    versions = workspace.prompts.list_versions(prompt.id)
    assert len(versions) == 3

    # Verify versions are in order
    version_numbers = [v.version for v in versions]
    assert version_numbers == [1, 2, 3]

    # Get specific versions
    v1 = workspace.prompts.get_version(prompt.id, 1)
    v2 = workspace.prompts.get_version(prompt.id, 2)
    v3 = workspace.prompts.get_version(prompt.id, 3)

    assert v1.version == 1
    assert v2.version == 2
    assert v3.version == 3

    # Latest should be version 3
    latest = workspace.prompts.get_version(prompt.id, "latest")
    assert latest.version == 3
