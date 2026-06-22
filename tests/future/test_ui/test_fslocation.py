import pytest

from evidently.ui.service.storage.fslocation import FSLocation


def test_safe_path_allows_valid_path():
    location = FSLocation("/tmp/workspace")

    result = location._safe_path("datasets/test.csv")

    assert result.endswith("datasets/test.csv")


def test_safe_path_rejects_path_traversal():
    location = FSLocation("/tmp/workspace")

    with pytest.raises(ValueError, match="Path escapes storage root"):
        location._safe_path("../../secret.csv")


def test_open_rejects_path_traversal():
    location = FSLocation("/tmp/workspace")

    with pytest.raises(ValueError, match="Path escapes storage root"):
        with location.open("../../secret.csv"):
            pass


def test_open_rejects_absolute_path():
    location = FSLocation("/tmp/workspace")

    with pytest.raises(ValueError):
        with location.open("/tmp/secret.csv"):
            pass

def test_safe_path_rejects_absolute_path():
    location = FSLocation("/tmp/workspace")

    with pytest.raises(ValueError, match="Path escapes storage root"):
        location._safe_path("/tmp/secret.csv")