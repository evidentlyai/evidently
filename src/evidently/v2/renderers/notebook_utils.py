from evidently.dashboard.dashboard import file_html_template, inline_template


def determine_template(mode: str):
    # pylint: disable=import-outside-toplevel
    render_mode = mode
    try:
        from IPython import get_ipython

        if mode == "auto":
            if type(get_ipython()).__module__.startswith("google.colab"):
                render_mode = "inline"
            else:
                render_mode = "nbextension"
        if render_mode == "inline":
            return file_html_template
        if render_mode == "nbextension":
            return inline_template
        raise ValueError(f"Unexpected value {mode}/{render_mode} for mode")
    except ImportError as err:
        raise Exception("Cannot import HTML from IPython.display, no way to show html") from err
