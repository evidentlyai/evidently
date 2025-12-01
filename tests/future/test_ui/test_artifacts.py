import pytest
from litestar.testing import TestClient

from evidently.descriptors import TextLength
from evidently.sdk.configs import DescriptorContent


@pytest.fixture
def created_project(test_client: TestClient):
    """Create a test project via API."""
    response = test_client.post(
        "/api/projects",
        json={
            "name": "Test Project",
            "description": "Test project for artifacts",
        },
    )
    assert response.status_code == 201
    project_id = response.json()
    return project_id


def test_list_artifacts(test_client: TestClient, created_project):
    """GET /api/artifacts"""
    response = test_client.get(f"/api/artifacts?project_id={created_project}")
    assert response.status_code == 200
    assert response.json() == []

    # Create an artifact
    artifact_data = {"name": "test artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201
    created_artifact = response.json()

    response = test_client.get(f"/api/artifacts?project_id={created_project}")
    assert response.status_code == 200
    artifacts = response.json()
    assert len(artifacts) == 1
    assert artifacts[0]["id"] == created_artifact["id"]


def test_create_and_get_artifact_by_id(test_client: TestClient, created_project):
    """GET /api/artifacts/{artifact_id}"""
    artifact_data = {"name": "my artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201
    artifact = response.json()
    assert artifact["name"] == "my artifact"
    assert artifact["project_id"] == str(created_project)

    response = test_client.get(f"/api/artifacts/{artifact['id']}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["id"] == artifact["id"]
    assert fetched["name"] == "my artifact"


def test_get_artifact_by_name(test_client: TestClient, created_project):
    """GET /api/artifacts/by-name/{name}"""
    artifact_data = {"name": "some artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201

    response = test_client.get(f"/api/artifacts/by-name/some artifact?project_id={created_project}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["name"] == "some artifact"

    response = test_client.get(f"/api/artifacts/by-name/nonexistent?project_id={created_project}")
    assert response.status_code == 404


def test_list_versions(test_client: TestClient, created_project):
    """GET /api/artifacts/{artifact_id}/versions"""
    artifact_data = {"name": "versioned artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201
    artifact = response.json()

    response = test_client.get(f"/api/artifacts/{artifact['id']}/versions")
    assert response.status_code == 200
    versions = response.json()
    assert versions == []


def test_create_and_get_version(test_client: TestClient, created_project):
    """POST /api/artifacts/{artifact_id}/versions and GET /api/artifacts/{artifact_id}/versions/{version}"""
    artifact_data = {"name": "v artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201
    artifact = response.json()

    descriptor = TextLength(column_name="test_col", alias="test")
    content = DescriptorContent.from_value(descriptor)
    version_data = {
        "version": 1,
        "content": content.dict(),
        "content_type": content.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/artifacts/{artifact['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    response.json()

    response = test_client.get(f"/api/artifacts/{artifact['id']}/versions/1")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["version"] == 1
    # Note: content comparison would need proper deserialization


def test_bump_artifact_version(test_client: TestClient, created_project):
    """Test bumping artifact versions"""
    artifact_data = {"name": "bump artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201
    artifact = response.json()

    # Create first version
    descriptor1 = TextLength(column_name="col1", alias="v1")
    content1 = DescriptorContent.from_value(descriptor1)
    version_data = {
        "version": 1,
        "content": content1.dict(),
        "content_type": content1.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/artifacts/{artifact['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version1 = response.json()
    assert version1["version"] == 1

    # Create second version
    descriptor2 = TextLength(column_name="col2", alias="v2")
    content2 = DescriptorContent.from_value(descriptor2)
    version_data = {
        "version": 2,
        "content": content2.dict(),
        "content_type": content2.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/artifacts/{artifact['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version2 = response.json()
    assert version2["version"] == 2

    # Create third version
    descriptor3 = TextLength(column_name="col3", alias="v3")
    content3 = DescriptorContent.from_value(descriptor3)
    version_data = {
        "version": 3,
        "content": content3.dict(),
        "content_type": content3.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/artifacts/{artifact['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version3 = response.json()
    assert version3["version"] == 3


def test_delete_artifact(test_client: TestClient, created_project):
    """DELETE /api/artifacts/{artifact_id}"""
    response = test_client.get(f"/api/artifacts?project_id={created_project}")
    assert response.status_code == 200
    assert len(response.json()) == 0

    artifact_data = {"name": "test artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201
    artifact = response.json()

    response = test_client.get(f"/api/artifacts?project_id={created_project}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = test_client.delete(f"/api/artifacts/{artifact['id']}")
    assert response.status_code == 204

    response = test_client.get(f"/api/artifacts?project_id={created_project}")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_delete_artifact_version(test_client: TestClient, created_project):
    """DELETE /api/artifacts/artifact-versions/{artifact_version_id}"""
    artifact_data = {"name": "test artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201
    artifact = response.json()

    descriptor = TextLength(column_name="test_col", alias="test")
    content = DescriptorContent.from_value(descriptor)
    version_data = {
        "version": 1,
        "content": content.dict(),
        "content_type": content.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/artifacts/{artifact['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version = response.json()

    response = test_client.get(f"/api/artifacts/{artifact['id']}/versions")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = test_client.delete(f"/api/artifacts/artifact-versions/{version['id']}")
    assert response.status_code == 204

    response = test_client.get(f"/api/artifacts/{artifact['id']}/versions")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_update_artifact(test_client: TestClient, created_project):
    """PUT /api/artifacts/{artifact_id}"""
    artifact_data = {"name": "test artifact", "metadata": {}}
    response = test_client.post(
        f"/api/artifacts?project_id={created_project}",
        json=artifact_data,
    )
    assert response.status_code == 201
    artifact = response.json()

    updated_data = {
        "id": artifact["id"],
        "project_id": artifact["project_id"],
        "name": "test artifact 2",
        "metadata": artifact["metadata"],
    }
    response = test_client.put(
        f"/api/artifacts/{artifact['id']}",
        json=updated_data,
    )
    assert response.status_code == 200

    response = test_client.get(f"/api/artifacts/{artifact['id']}")
    assert response.status_code == 200
    updated_artifact = response.json()
    assert updated_artifact["name"] == "test artifact 2"
