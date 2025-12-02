import pytest
from litestar.testing import TestClient

from evidently.llm.prompts.content import TextPromptContent


@pytest.fixture
def created_project(test_client: TestClient):
    """Create a test project via API."""
    response = test_client.post(
        "/api/projects",
        json={
            "name": "Test Project",
            "description": "Test project for prompts",
        },
    )
    assert response.status_code == 201
    project_id = response.json()
    return project_id


def test_list_prompts(test_client: TestClient, created_project):
    """GET /api/prompts"""
    response = test_client.get(f"/api/prompts?project_id={created_project}")
    assert response.status_code == 200
    assert response.json() == []

    # Create a prompt
    prompt_data = {"name": "test prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    created_prompt = response.json()

    response = test_client.get(f"/api/prompts?project_id={created_project}")
    assert response.status_code == 200
    prompts = response.json()
    assert len(prompts) == 1
    assert prompts[0]["id"] == created_prompt["id"]


def test_create_and_get_prompt_by_id(test_client: TestClient, created_project):
    """GET /api/prompts/{prompt_id}"""
    prompt_data = {"name": "my prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()
    assert prompt["name"] == "my prompt"
    assert prompt["project_id"] == str(created_project)

    response = test_client.get(f"/api/prompts/{prompt['id']}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["id"] == prompt["id"]
    assert fetched["name"] == "my prompt"


def test_get_prompt_by_name(test_client: TestClient, created_project):
    """GET /api/prompts/by-name/{name}"""
    prompt_data = {"name": "some prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201

    response = test_client.get(f"/api/prompts/by-name/some prompt?project_id={created_project}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["name"] == "some prompt"

    response = test_client.get(f"/api/prompts/by-name/nonexistent?project_id={created_project}")
    assert response.status_code == 404


def test_list_versions(test_client: TestClient, created_project):
    """GET /api/prompts/{prompt_id}/versions"""
    prompt_data = {"name": "versioned prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()

    response = test_client.get(f"/api/prompts/{prompt['id']}/versions")
    assert response.status_code == 200
    versions = response.json()
    assert versions == []


def test_create_and_get_version(test_client: TestClient, created_project):
    """POST /api/prompts/{prompt_id}/versions and GET /api/prompts/{prompt_id}/versions/{version}"""
    prompt_data = {"name": "v prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()

    content = TextPromptContent(text="Hello world")
    version_data = {
        "version": 1,
        "content": content.dict(),
        "content_type": content.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/prompts/{prompt['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version = response.json()
    assert version["version"] == 1

    response = test_client.get(f"/api/prompts/{prompt['id']}/versions/1")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["version"] == 1


def test_get_version_by_id(test_client: TestClient, created_project):
    """GET /api/prompts/prompt-versions/{prompt_version_id}"""
    prompt_data = {"name": "test prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()

    content = TextPromptContent(text="Test content")
    version_data = {
        "version": 1,
        "content": content.dict(),
        "content_type": content.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/prompts/{prompt['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version = response.json()

    response = test_client.get(f"/api/prompts/prompt-versions/{version['id']}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["id"] == version["id"]
    assert fetched["version"] == 1


def test_get_version_by_latest(test_client: TestClient, created_project):
    """GET /api/prompts/{prompt_id}/versions/latest"""
    prompt_data = {"name": "test prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()

    content = TextPromptContent(text="Latest version")
    version_data = {
        "version": 1,
        "content": content.dict(),
        "content_type": content.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/prompts/{prompt['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version = response.json()

    response = test_client.get(f"/api/prompts/{prompt['id']}/versions/latest")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["id"] == version["id"]
    assert fetched["version"] == 1


def test_bump_prompt_version(test_client: TestClient, created_project):
    """Test creating multiple prompt versions"""
    prompt_data = {"name": "bump prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()

    # Create first version
    content1 = TextPromptContent(text="Version 1")
    version_data = {
        "version": 1,
        "content": content1.dict(),
        "content_type": content1.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/prompts/{prompt['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version1 = response.json()
    assert version1["version"] == 1

    # Create second version
    content2 = TextPromptContent(text="Version 2")
    version_data = {
        "version": 2,
        "content": content2.dict(),
        "content_type": content2.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/prompts/{prompt['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version2 = response.json()
    assert version2["version"] == 2

    # Create third version
    content3 = TextPromptContent(text="Version 3")
    version_data = {
        "version": 3,
        "content": content3.dict(),
        "content_type": content3.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/prompts/{prompt['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version3 = response.json()
    assert version3["version"] == 3


def test_delete_prompt(test_client: TestClient, created_project):
    """DELETE /api/prompts/{prompt_id}"""
    response = test_client.get(f"/api/prompts?project_id={created_project}")
    assert response.status_code == 200
    assert len(response.json()) == 0

    prompt_data = {"name": "test prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()

    response = test_client.get(f"/api/prompts?project_id={created_project}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = test_client.delete(f"/api/prompts/{prompt['id']}")
    assert response.status_code == 204

    response = test_client.get(f"/api/prompts?project_id={created_project}")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_delete_prompt_version(test_client: TestClient, created_project):
    """DELETE /api/prompts/prompt-versions/{prompt_version_id}"""
    prompt_data = {"name": "test prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()

    content = TextPromptContent(text="Test content")
    version_data = {
        "version": 1,
        "content": content.dict(),
        "content_type": content.get_type().value,
        "metadata": {},
    }
    response = test_client.post(
        f"/api/prompts/{prompt['id']}/versions",
        json=version_data,
    )
    assert response.status_code == 201
    version = response.json()

    response = test_client.get(f"/api/prompts/{prompt['id']}/versions")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = test_client.delete(f"/api/prompts/prompt-versions/{version['id']}")
    assert response.status_code == 204

    response = test_client.get(f"/api/prompts/{prompt['id']}/versions")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_update_prompt(test_client: TestClient, created_project):
    """PUT /api/prompts/{prompt_id}"""
    prompt_data = {"name": "test prompt", "metadata": {}}
    response = test_client.post(
        f"/api/prompts?project_id={created_project}",
        json=prompt_data,
    )
    assert response.status_code == 201
    prompt = response.json()

    updated_data = {
        "id": prompt["id"],
        "project_id": prompt["project_id"],
        "name": "test prompt 2",
        "metadata": prompt["metadata"],
    }
    response = test_client.put(
        f"/api/prompts/{prompt['id']}",
        json=updated_data,
    )
    assert response.status_code == 200

    response = test_client.get(f"/api/prompts/{prompt['id']}")
    assert response.status_code == 200
    updated_prompt = response.json()
    assert updated_prompt["name"] == "test prompt 2"
