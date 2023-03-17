import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import Text


class EntityNotFoundError(Exception):
    """EntityNotFoundError"""


def list_periods(reports_dir: Path) -> List[Text]:
    """List periods subdirectories inside reports directory.

    Args:
        reports_dir (Path): Reports directory path.

    Raises:
        EntityNotFoundError: If reports directory does not exist.

    Returns:
        List[Text]: List of periods subdirectories
    """

    try:
        return sorted(
            list(filter(lambda e: (reports_dir / e).is_dir(), os.listdir(reports_dir)))
        )
    except FileNotFoundError as e:
        raise EntityNotFoundError(e)


def period_dir_to_dates_range(period_dir_name: Text) -> Text:
    """_summary_

    Args:
        period_dir_name (Text): _description_

    Returns:
        Text: _description_
    """

    return period_dir_name.replace("_", " - ")


def get_report_name(path: Path) -> Text:
    """Convert report path to human readable name.

    Args:
        path (Path): Report path.

    Returns:
        Text: human readable name.
    """

    name: Text = path.with_suffix("").name.replace("_", " ").capitalize()

    return name


def get_reports_mapping(period_dir: Text) -> Dict[Text, Path]:
    """Build dictionary where human readable names corresponds to paths.
    Note: each directory gets suffix ` (folder)`.

    Args:
        paths (List[Path]): List of paths.

    Returns:
        Dict[Text, Path]: Dictionary with structure:
        {
            <Name>: <path>
        }

    Examples:
    >>> paths = [
        'reports/2011-02-12_2011-02-18/data_quality',
        'reports/2011-02-12_2011-02-18/model_performance',
        'reports/2011-02-12_2011-02-18/data_drift.html',
        'reports/2011-02-12_2011-02-18/data_quality.html',
        'reports/2011-02-12_2011-02-18/model_performance.html',
        'reports/2011-02-12_2011-02-18/target_drift.html'
    ]
    >>> report_paths_to_names(paths)
    {
        'Data drift': 'Path(reports/2011-02-12_2011-02-18/data_drifts.html)',
        'Data quality(folder)': 'Path(reports/2011-02-12_2011-02-18/data_quality)',
        'Data quality': 'Path(reports/2011-02-12_2011-02-18/data_quality.html)',
        'Model performance (folder)': 'Path(reports/2011-02-12_2011-02-18/model_performance)',
        'Model performance': 'Path(reports/2011-02-12_2011-02-18/model_performance.html)',
        'Target drift': 'Path(reports/2011-02-12_2011-02-18/target_drift.html)'
    }
    """

    names: List[Text] = []
    paths: List[Path] = []

    for filename in os.listdir(period_dir):
        if not filename.startswith("."):
            paths.append(Path(f"{period_dir}/{filename}"))
    paths.sort()

    for path in paths:
        name: Text = get_report_name(path)
        if path.is_dir():
            name += " (folder)"
        names.append(name)

    return dict(zip(names, paths))
