"""Tests for artifact storage implementations."""

import pytest

from evidently.legacy.core import new_id
from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactMetadata
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionMetadata
from evidently.ui.service.storage.local.artifacts import FileArtifactStorage
from evidently.ui.service.storage.sql.artifacts import SQLArtifactStorage


@pytest.fixture
def tmp_path():
    """Create a temporary directory."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def file_storage(tmp_path):
    """Create file-based artifact storage."""
    return FileArtifactStorage(base_path=tmp_path)


@pytest.fixture
def sql_storage(sqlite_engine):
    """Create SQL-based artifact storage."""
    return SQLArtifactStorage(sqlite_engine)


@pytest.fixture
def test_project_id():
    """Create a test project ID."""
    return new_id()


@pytest.fixture
def sample_artifact(test_project_id):
    """Create a sample artifact."""
    return Artifact(
        id=new_id(),
        project_id=test_project_id,
        name="test artifact",
        metadata=ArtifactMetadata(description="Test description"),
    )


@pytest.fixture
def sample_content():
    """Create sample content."""
    from evidently.descriptors import TextLength
    from evidently.sdk.configs import DescriptorContent

    descriptor = TextLength(column_name="test_col", alias="test")
    return DescriptorContent.from_value(descriptor)


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_add_and_get_artifact(request, storage, test_project_id, sample_artifact):
    """Test adding and retrieving an artifact."""
    storage_instance = request.getfixturevalue(storage)

    # Add artifact
    added = await storage_instance.add_artifact(test_project_id, sample_artifact)
    # Storage generates new ID (file storage always generates, SQL only if ZERO_UUID)
    assert added.id is not None
    assert added.name == sample_artifact.name
    assert added.name == sample_artifact.name

    # Get artifact
    retrieved = await storage_instance.get_artifact(added.id)
    assert retrieved is not None
    assert retrieved.id == added.id
    assert retrieved.name == added.name
    assert retrieved.project_id == test_project_id


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_get_artifact_by_name(request, storage, test_project_id, sample_artifact):
    """Test retrieving an artifact by name."""
    storage_instance = request.getfixturevalue(storage)

    await storage_instance.add_artifact(test_project_id, sample_artifact)

    retrieved = await storage_instance.get_artifact_by_name(test_project_id, sample_artifact.name)
    assert retrieved is not None
    assert retrieved.name == sample_artifact.name
    assert retrieved.id is not None


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_list_artifacts(request, storage, test_project_id, sample_artifact):
    """Test listing artifacts."""
    storage_instance = request.getfixturevalue(storage)

    # Initially empty
    artifacts = await storage_instance.list_artifacts(test_project_id)
    assert len(artifacts) == 0

    # Add artifact
    await storage_instance.add_artifact(test_project_id, sample_artifact)

    # Should have one
    artifacts = await storage_instance.list_artifacts(test_project_id)
    assert len(artifacts) == 1
    assert artifacts[0].id is not None
    assert artifacts[0].name == sample_artifact.name


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_update_artifact(request, storage, test_project_id, sample_artifact):
    """Test updating an artifact."""
    storage_instance = request.getfixturevalue(storage)

    # Add artifact
    added = await storage_instance.add_artifact(test_project_id, sample_artifact)

    # Update it
    updated = Artifact(
        id=added.id,
        project_id=added.project_id,
        name="updated name",
        metadata=ArtifactMetadata(description="Updated description"),
    )
    await storage_instance.update_artifact(added.id, updated)

    # Verify update
    retrieved = await storage_instance.get_artifact(added.id)
    assert retrieved.name == "updated name"
    assert retrieved.metadata.description == "Updated description"


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_delete_artifact(request, storage, test_project_id, sample_artifact):
    """Test deleting an artifact."""
    storage_instance = request.getfixturevalue(storage)

    # Add artifact
    added = await storage_instance.add_artifact(test_project_id, sample_artifact)

    # Delete it
    await storage_instance.delete_artifact(added.id)

    # Should not exist
    retrieved = await storage_instance.get_artifact(added.id)
    assert retrieved is None


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_add_and_get_artifact_version(request, storage, test_project_id, sample_artifact, sample_content):
    """Test adding and retrieving an artifact version."""
    storage_instance = request.getfixturevalue(storage)

    # Add artifact first
    artifact = await storage_instance.add_artifact(test_project_id, sample_artifact)

    # Create version
    version = ArtifactVersion(
        artifact_id=artifact.id,
        version=1,
        content=sample_content,
        metadata=ArtifactVersionMetadata(comment="First version"),
    )

    # Add version
    added_version = await storage_instance.add_artifact_version(artifact.id, version)
    assert added_version.version == 1
    assert added_version.artifact_id == artifact.id

    # Get version
    retrieved = await storage_instance.get_artifact_version(added_version.id)
    assert retrieved is not None
    assert retrieved.version == 1
    assert retrieved.artifact_id == artifact.id


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_list_artifact_versions(request, storage, test_project_id, sample_artifact, sample_content):
    """Test listing artifact versions."""
    storage_instance = request.getfixturevalue(storage)

    # Add artifact
    artifact = await storage_instance.add_artifact(test_project_id, sample_artifact)

    # Initially empty
    versions = await storage_instance.list_artifact_versions(artifact.id)
    assert len(versions) == 0

    # Add versions
    for v in [1, 2, 3]:
        version = ArtifactVersion(
            artifact_id=artifact.id,
            version=v,
            content=sample_content,
            metadata=ArtifactVersionMetadata(comment=f"Version {v}"),
        )
        await storage_instance.add_artifact_version(artifact.id, version)

    # Should have 3 versions
    versions = await storage_instance.list_artifact_versions(artifact.id)
    assert len(versions) == 3
    assert sorted([v.version for v in versions]) == [1, 2, 3]


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_get_artifact_version_by_version(request, storage, test_project_id, sample_artifact, sample_content):
    """Test getting artifact version by version number."""
    storage_instance = request.getfixturevalue(storage)

    # Add artifact
    artifact = await storage_instance.add_artifact(test_project_id, sample_artifact)

    # Add versions
    for v in [1, 2, 3]:
        version = ArtifactVersion(
            artifact_id=artifact.id,
            version=v,
            content=sample_content,
            metadata=ArtifactVersionMetadata(comment=f"Version {v}"),
        )
        await storage_instance.add_artifact_version(artifact.id, version)

    # Get specific version
    version_2 = await storage_instance.get_artifact_version_by_version(artifact.id, 2)
    assert version_2 is not None
    assert version_2.version == 2

    # Get latest
    latest = await storage_instance.get_artifact_version_by_version(artifact.id, "latest")
    assert latest is not None
    assert latest.version == 3


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_delete_artifact_version(request, storage, test_project_id, sample_artifact, sample_content):
    """Test deleting an artifact version."""
    storage_instance = request.getfixturevalue(storage)

    # Add artifact
    artifact = await storage_instance.add_artifact(test_project_id, sample_artifact)

    # Add version
    version = ArtifactVersion(
        artifact_id=artifact.id,
        version=1,
        content=sample_content,
        metadata=ArtifactVersionMetadata(comment="Version 1"),
    )
    added_version = await storage_instance.add_artifact_version(artifact.id, version)

    # Delete it
    await storage_instance.delete_artifact_version(added_version.id)

    # Should not exist
    retrieved = await storage_instance.get_artifact_version(added_version.id)
    assert retrieved is None


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_get_nonexistent_artifact(request, storage, test_project_id):
    """Test getting a non-existent artifact."""
    storage_instance = request.getfixturevalue(storage)

    fake_id = new_id()
    retrieved = await storage_instance.get_artifact(fake_id)
    assert retrieved is None


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
@pytest.mark.asyncio
async def test_get_nonexistent_artifact_version(request, storage, test_project_id, sample_artifact):
    """Test getting a non-existent artifact version."""
    storage_instance = request.getfixturevalue(storage)

    # Add artifact
    artifact = await storage_instance.add_artifact(test_project_id, sample_artifact)

    fake_id = new_id()
    retrieved = await storage_instance.get_artifact_version(fake_id)
    assert retrieved is None

    # Also test getting version by version number
    retrieved = await storage_instance.get_artifact_version_by_version(artifact.id, 999)
    assert retrieved is None
