import os

from typer import Typer

pretty_exceptions_enable = os.environ.get("PRETTY_EXCEPTIONS_DISABLED") is None
app = Typer(context_settings={"help_option_names": ["-h", "--help"]}, pretty_exceptions_enable=pretty_exceptions_enable)


@app.callback(no_args_is_help=True, invoke_without_command=True)
def evidently_callback():
    """\b
    Evidently is tool to help you evaluate, test and monitor your data and ML models.
    Documentation: https://docs.evidentlyai.com
    """
