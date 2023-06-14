from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
from typing import Text


def set_page_container_style() -> None:
    """Set report container style."""

    margins_css = """
    <style>
        /* Configuration of paddings of containers inside main area */
        .main > div {
            max-width: 100%;
            padding-left: 10%;
        }

        /*Font size in tabs */
        button[data-baseweb="tab"] div p {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """
    st.markdown(margins_css, unsafe_allow_html=True)


def display_sidebar_header() -> None:

    # Logo
    logo = Image.open("static/logo.png")
    with st.sidebar:
        st.image(logo, use_column_width=True)
        col1, col2 = st.columns(2)
        repo_link: Text = '#'
        evidently_docs: Text = 'https://docs.evidentlyai.com/'
        col1.markdown(
            f"<a style='display: block; text-align: center;' href={repo_link}>Source code</a>",
            unsafe_allow_html=True,
        )
        col2.markdown(
            f"<a style='display: block; text-align: center;' href={evidently_docs}>Evidently docs</a>",
            unsafe_allow_html=True,
        )
        st.header('')  # add space between logo and selectors


def display_header(report_name: Text, window_size: int) -> None:
    """Display report header.

    Args:
        report_name (Text): Report name.
        window_size (int): Size of prediction data on which report built.
    """

    st.header(f'Report: {report_name}')
    st.caption(f'Window size: {window_size}')


@st.cache_data
def display_report(report: Text) -> Text:
    """Display report.

    Args:
        report (Text): Report content.

    Returns:
        Text: Report content.
    """

    components.html(report, width=1000, height=500, scrolling=True)

    return report
