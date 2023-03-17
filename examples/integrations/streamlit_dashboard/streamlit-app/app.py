import os
from pathlib import Path
import streamlit as st
from typing import Dict
from typing import List
from typing import Text

from src.ui import display_header
from src.ui import display_report
from src.ui import display_sidebar_header
from src.ui import select_period
from src.ui import select_project
from src.ui import select_report
from src.ui import set_page_container_style
from src.utils import EntityNotFoundError
from src.utils import get_reports_mapping
from src.utils import list_periods

PROJECTS_DIR: Path = Path("../projects")
REPORTS_DIR_NAME: Text = "reports"


if __name__ == "__main__":

    # Configure some styles
    set_page_container_style()

    # Extract available project names and reports directory name
    projects: List[Text] = []
    for path in os.listdir(PROJECTS_DIR):
        if not path.startswith("."):
            projects.append(path)

    try:

        # Sidebar: Logo and links
        display_sidebar_header()

        # Sidebar: Select project (UI) and build reports directory path
        selected_project: Path = PROJECTS_DIR / select_project(projects)
        reports_dir: Path = selected_project / REPORTS_DIR_NAME

        # Sidebar: Select period
        periods: List[Text] = list_periods(reports_dir)
        selected_period: Text = select_period(periods)
        period_dir: Path = reports_dir / selected_period

        # Sidebar: Select report (UI)

        report_mapping: Dict[Text, Path] = get_reports_mapping(period_dir)
        selected_report_name: Text = select_report(report_mapping)
        selected_report: Path = report_mapping[selected_report_name]

        # Display report header (UI)
        display_header(
            project_name=selected_project.name,
            period=selected_period,
            report_name=selected_report_name,
        )
        # Display selected report(UI)
        display_report(selected_report)

    except EntityNotFoundError as e:
        # If some entity (periods directories, specific period or report files)
        # not found then display error in UI
        st.error(e)

    except Exception as e:
        raise e
