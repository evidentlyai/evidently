import pytest

from evidently.legacy.core import new_id
from evidently.ui.service.storage.local.snapshot_links import FileSnapshotDatasetLinksManager
from evidently.ui.service.storage.sql.snapshot_links import SQLSnapshotDatasetLinksManager


@pytest.fixture
def tmp_path():
    """Create a temporary directory."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def file_snapshot_links_manager(tmp_path):
    """Create file-based snapshot links manager."""
    return FileSnapshotDatasetLinksManager(base_path=tmp_path)


@pytest.fixture
def sql_snapshot_links_manager(sqlite_engine):
    """Create SQL-based snapshot links manager."""
    return SQLSnapshotDatasetLinksManager(engine=sqlite_engine)


@pytest.fixture
def test_project_id():
    """Create a test project ID."""
    return new_id()


@pytest.fixture
def test_snapshot_id():
    """Create a test snapshot ID."""
    return new_id()


@pytest.fixture
def test_dataset_id():
    """Create a test dataset ID."""
    return new_id()


@pytest.mark.asyncio
async def test_file_snapshot_links_link_dataset(
    file_snapshot_links_manager, test_project_id, test_snapshot_id, test_dataset_id
):
    """Test linking a dataset in FileSnapshotDatasetLinksManager."""
    await file_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, test_dataset_id, "input", "current"
    )


@pytest.mark.asyncio
async def test_file_snapshot_links_get_links(
    file_snapshot_links_manager, test_project_id, test_snapshot_id, test_dataset_id
):
    """Test getting links from FileSnapshotDatasetLinksManager."""
    # Add links
    await file_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, test_dataset_id, "input", "current"
    )

    input_dataset_id = new_id()
    await file_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, input_dataset_id, "input", "reference"
    )

    output_dataset_id = new_id()
    await file_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, output_dataset_id, "output", "current"
    )

    # Get links
    links = await file_snapshot_links_manager.get_links(test_project_id, test_snapshot_id)

    assert links is not None
    assert links.datasets is not None
    assert links.datasets.input is not None
    assert links.datasets.input.current == test_dataset_id
    assert links.datasets.input.reference == input_dataset_id

    assert links.datasets.output is not None
    assert links.datasets.output.current == output_dataset_id


@pytest.mark.asyncio
async def test_file_snapshot_links_get_empty_links(file_snapshot_links_manager, test_project_id, test_snapshot_id):
    """Test getting links when none exist."""
    links = await file_snapshot_links_manager.get_links(test_project_id, test_snapshot_id)
    assert links is not None
    assert links.datasets is not None
    assert links.datasets.input.current is None
    assert links.datasets.input.reference is None
    assert links.datasets.output.current is None
    assert links.datasets.output.reference is None


@pytest.mark.asyncio
async def test_sql_snapshot_links_link_dataset(
    sql_snapshot_links_manager, test_project_id, test_snapshot_id, test_dataset_id
):
    """Test linking a dataset in SQLSnapshotDatasetLinksManager."""
    await sql_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, test_dataset_id, "input", "current"
    )


@pytest.mark.asyncio
async def test_sql_snapshot_links_get_links(
    sql_snapshot_links_manager, test_project_id, test_snapshot_id, test_dataset_id
):
    """Test getting links from SQLSnapshotDatasetLinksManager."""
    # Add links
    await sql_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, test_dataset_id, "input", "current"
    )

    input_dataset_id = new_id()
    await sql_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, input_dataset_id, "input", "reference"
    )

    output_dataset_id = new_id()
    await sql_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, output_dataset_id, "output", "current"
    )

    # Get links
    links = await sql_snapshot_links_manager.get_links(test_project_id, test_snapshot_id)

    assert links is not None
    assert links.datasets is not None
    assert links.datasets.input is not None
    assert links.datasets.input.current == test_dataset_id
    assert links.datasets.input.reference == input_dataset_id

    assert links.datasets.output is not None
    assert links.datasets.output.current == output_dataset_id


@pytest.mark.asyncio
async def test_sql_snapshot_links_get_empty_links(sql_snapshot_links_manager, test_project_id, test_snapshot_id):
    """Test getting links when none exist."""
    links = await sql_snapshot_links_manager.get_links(test_project_id, test_snapshot_id)
    assert links is not None
    assert links.datasets is not None
    assert links.datasets.input.current is None
    assert links.datasets.input.reference is None
    assert links.datasets.output.current is None
    assert links.datasets.output.reference is None


@pytest.mark.asyncio
async def test_snapshot_links_multiple_snapshots(file_snapshot_links_manager, test_project_id):
    """Test links for multiple snapshots."""
    snapshot1 = new_id()
    snapshot2 = new_id()
    dataset1 = new_id()
    dataset2 = new_id()

    await file_snapshot_links_manager.link_dataset_snapshot(test_project_id, snapshot1, dataset1, "input", "current")
    await file_snapshot_links_manager.link_dataset_snapshot(test_project_id, snapshot2, dataset2, "input", "current")

    links1 = await file_snapshot_links_manager.get_links(test_project_id, snapshot1)
    links2 = await file_snapshot_links_manager.get_links(test_project_id, snapshot2)

    assert links1.datasets.input.current == dataset1
    assert links2.datasets.input.current == dataset2
    assert links1.datasets.input.current != dataset2
    assert links2.datasets.input.current != dataset1


@pytest.mark.asyncio
async def test_snapshot_links_additional_subtype(
    file_snapshot_links_manager, test_project_id, test_snapshot_id, test_dataset_id
):
    """Test linking with additional subtype."""
    await file_snapshot_links_manager.link_dataset_snapshot(
        test_project_id, test_snapshot_id, test_dataset_id, "input", "custom_type"
    )

    links = await file_snapshot_links_manager.get_links(test_project_id, test_snapshot_id)
    assert links.datasets.input.additional["custom_type"] == test_dataset_id
