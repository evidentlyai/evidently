import plotly.graph_objs as go

from evidently.legacy.options.agg_data import RenderOptions
from evidently.legacy.options.base import Options
from evidently.legacy.renderers.base_renderer import BaseRenderer
from evidently.legacy.renderers.render_utils import get_distribution_plot_figure
from evidently.legacy.renderers.render_utils import plot_distr
from evidently.legacy.metric_results import Distribution
from evidently.legacy.metric_results import HistogramData
from evidently.legacy.options import ColorOptions


def test_render_options_defaults():
    opts = RenderOptions()
    assert opts.current_name == "Current"
    assert opts.reference_name == "Reference"


def test_render_options_custom_names():
    opts = RenderOptions(current_name="Production", reference_name="Staging")
    assert opts.current_name == "Production"
    assert opts.reference_name == "Staging"


def test_options_dict_initialization():
    opts = Options(**{"render": {"current_name": "ModelA", "reference_name": "ModelB"}})
    assert opts.render_options.current_name == "ModelA"
    assert opts.render_options.reference_name == "ModelB"


def test_options_dict_partial():
    opts = Options(**{"render": {"current_name": "Testing"}})
    assert opts.render_options.current_name == "Testing"
    assert opts.render_options.reference_name == "Reference"


def test_options_default_backwards_compat():
    opts = Options()
    assert opts.render_options.current_name == "Current"
    assert opts.render_options.reference_name == "Reference"


def test_base_renderer_has_render_options():
    renderer = BaseRenderer()
    assert renderer.render_options is not None
    assert renderer.render_options.current_name == "Current"
    assert renderer.render_options.reference_name == "Reference"


def test_plot_distr_custom_names():
    import pandas as pd

    hist_curr = HistogramData(name="curr", x=pd.Series([1, 2, 3]), count=pd.Series([10, 20, 30]))
    hist_ref = HistogramData(name="ref", x=pd.Series([1, 2, 3]), count=pd.Series([15, 25, 35]))
    color_options = ColorOptions()

    fig = plot_distr(
        hist_curr=hist_curr,
        hist_ref=hist_ref,
        color_options=color_options,
        current_name="Train",
        reference_name="Test",
    )

    trace_names = [t.name for t in fig.data]
    assert "Train" in trace_names
    assert "Test" in trace_names
    assert "current" not in trace_names
    assert "reference" not in trace_names


def test_plot_distr_default_names():
    import pandas as pd

    hist_curr = HistogramData(name="curr", x=pd.Series([1, 2, 3]), count=pd.Series([10, 20, 30]))
    color_options = ColorOptions()

    fig = plot_distr(hist_curr=hist_curr, color_options=color_options)

    trace_names = [t.name for t in fig.data]
    assert "Current" in trace_names


def test_get_distribution_plot_figure_custom_names():
    curr = Distribution(x=[1, 2, 3], y=[10, 20, 30])
    ref = Distribution(x=[1, 2, 3], y=[15, 25, 35])
    color_options = ColorOptions()

    fig = get_distribution_plot_figure(
        current_distribution=curr,
        reference_distribution=ref,
        color_options=color_options,
        current_name="Baseline",
        reference_name="Candidate",
    )

    trace_names = [t.name for t in fig.data]
    assert "Baseline" in trace_names
    assert "Candidate" in trace_names


def test_options_from_list():
    render_opts = RenderOptions(current_name="A", reference_name="B")
    opts = Options.from_any_options([render_opts])
    assert opts.render_options.current_name == "A"
    assert opts.render_options.reference_name == "B"
