import os
from typing import Text

import requests
import streamlit as st

from streamlit_app.utils.ui import (
    set_page_container_style,
    display_sidebar_header,
    display_header,
    display_report
)


if __name__ == '__main__':

    # Configure some styles
    set_page_container_style()
    # Sidebar: Logo and links
    display_sidebar_header()
    host: Text = os.getenv('FASTAPI_APP_HOST', 'localhost')
    base_route: Text = f'http://{host}:5000'

    try:

        window_size: int = st.sidebar.number_input(
            label='window_size',
            min_value=1,
            step=1,
            value=3000
        )
        clicked_model_performance: bool = st.sidebar.button(
            label='Model performance'
        )
        clicked_target_drift: bool = st.sidebar.button(label='Target drift')

        report_selected: bool = False
        request_url: Text = base_route
        report_name: Text = ''

        if clicked_model_performance:
            report_selected = True
            request_url += f'/monitor-model?window_size={window_size}'
            report_name = 'Model performance'

        if clicked_target_drift:
            report_selected = True
            request_url += f'/monitor-target?window_size={window_size}'
            report_name = 'Target drift'

        if report_selected:
            resp: requests.Response = requests.get(request_url)
            display_header(report_name, window_size)
            display_report(resp.content)

    except Exception as e:
        st.error(e)
