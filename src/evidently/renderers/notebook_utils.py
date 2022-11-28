from evidently.utils.dashboard import file_html_template
from evidently.utils.dashboard import inline_template


def determine_template(mode: str):
    # pylint: disable=import-outside-toplevel
    render_mode = mode
    try:
        from IPython import get_ipython

        is_colab = type(get_ipython()).__module__.startswith("google.colab")
    except ImportError:
        is_colab = False

    if mode == "auto":
        if is_colab:
            render_mode = "inline"
        else:
            render_mode = "nbextension"
    if render_mode == "inline":
        return file_html_template
    if render_mode == "nbextension":
        return inline_template
    raise ValueError(f"Unexpected value {mode}/{render_mode} for mode")
