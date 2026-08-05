import os

import pytest

from evidently.ui.service.storage.fslocation import FSLocation


def test_relative_paths_stay_under_base_path(tmp_path):
    base_path = tmp_path / "workspace"
    location = FSLocation(str(base_path))
    location.makedirs("nested")

    with location.open("nested/data.csv", "wb") as file:
        file.write(b"data")

    assert (base_path / "nested" / "data.csv").read_bytes() == b"data"


@pytest.mark.parametrize(
    "path",
    [
        "../outside.csv",
        "nested/../../outside.csv",
        "..\\outside.csv",
        "C:\\outside.csv",
    ],
)
def test_paths_outside_base_path_are_rejected(tmp_path, path):
    location = FSLocation(str(tmp_path / "workspace"))

    with pytest.raises(ValueError, match="Path must be relative"):
        with location.open(path, "wb"):
            pass


def test_absolute_path_is_rejected(tmp_path):
    location = FSLocation(str(tmp_path / "workspace"))

    with pytest.raises(ValueError, match="Path must be relative"):
        with location.open(str(tmp_path / "outside.csv"), "wb"):
            pass


def test_path_through_symlink_outside_base_is_rejected(tmp_path):
    base_path = tmp_path / "workspace"
    outside_path = tmp_path / "outside"
    base_path.mkdir()
    outside_path.mkdir()
    try:
        os.symlink(outside_path, base_path / "link", target_is_directory=True)
    except OSError:
        pytest.skip("Symlinks are not available")
    location = FSLocation(str(base_path))

    with pytest.raises(ValueError, match="Path must be relative"):
        with location.open("link/data.csv", "wb"):
            pass
