"""Dataset-level text evaluation metrics.

Provides aggregate metrics for evaluating text quality across a dataset,
including ROUGE score for summarisation and generation tasks.
"""

from typing import List
from typing import Optional
from typing import Tuple

import pandas as pd

from evidently.core.datasets import Dataset
from evidently.core.datasets import DatasetColumn
from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.core.report import Context
from evidently.legacy.core import ColumnType
from evidently.legacy.metric_results import HistogramData
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.options import ColorOptions
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.renderers.html_widgets import plotly_figure
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.utils.visualizations import get_distribution_for_column
from evidently.legacy.utils.visualizations import plot_distr_with_perc_button
from evidently.tests import Reference
from evidently.tests import eq

VALID_ROUGE_TYPES = ("rouge1", "rouge2", "rougeL", "rougeLsum")
VALID_SCORE_TYPES = ("f", "precision", "recall")


def _compute_rouge_series(
    df: pd.DataFrame,
    prediction_column: str,
    reference_column: str,
    rouge_type: str,
    score_type: str,
) -> pd.Series:
    """Compute per-row ROUGE scores between prediction and reference columns."""
    from rouge_score import rouge_scorer

    scorer = rouge_scorer.RougeScorer([rouge_type], use_stemmer=False)
    scores = []
    for pred, ref in zip(
        df[prediction_column].fillna("").tolist(),
        df[reference_column].fillna("").tolist(),
    ):
        result = scorer.score(str(ref), str(pred))
        score_obj = result[rouge_type]
        if score_type == "f":
            scores.append(score_obj.fmeasure)
        elif score_type == "precision":
            scores.append(score_obj.precision)
        else:
            scores.append(score_obj.recall)
    return pd.Series(scores, index=df.index)


class RougeScoreMetric(SingleValueMetric):
    """Mean ROUGE score across all rows for a prediction vs reference column pair.

    Computes ROUGE (Recall-Oriented Understudy for Gisting Evaluation) between
    each row's prediction and reference text, then returns the dataset-level mean.
    Also renders a histogram of the per-row score distribution.

    Requires the ``rouge-score`` package (``pip install evidently[llm]``).

    Args:
        prediction_column: Column containing generated/predicted text.
        reference_column: Column containing the reference/ground-truth text.
        rouge_type: ROUGE variant — ``'rouge1'`` (unigrams), ``'rouge2'`` (bigrams),
            or ``'rougeL'`` (longest common subsequence). Default ``'rouge1'``.
        score_type: Which score component to return — ``'f'`` (F1, default),
            ``'precision'``, or ``'recall'``.
        tests: Optional pass/fail conditions on the mean score.

    Example::

        from evidently import Report
        from evidently.metrics import RougeScoreMetric

        report = Report([
            RougeScoreMetric(
                prediction_column="response",
                reference_column="ground_truth",
                rouge_type="rouge1",
            )
        ])
        result = report.run(current_dataset, reference_dataset)
    """

    prediction_column: str
    reference_column: str
    rouge_type: str = "rouge1"
    score_type: str = "f"

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_single(self.get_fingerprint())]


class RougeScoreMetricCalculation(SingleValueCalculation[RougeScoreMetric]):
    def calculate(
        self,
        context: "Context",
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        m = self.metric
        if m.rouge_type not in VALID_ROUGE_TYPES:
            raise ValueError(f"rouge_type must be one of {VALID_ROUGE_TYPES}, got '{m.rouge_type}'")
        if m.score_type not in VALID_SCORE_TYPES:
            raise ValueError(f"score_type must be one of {VALID_SCORE_TYPES}, got '{m.score_type}'")

        cur_df = current_data.as_dataframe()
        cur_scores = _compute_rouge_series(
            cur_df, m.prediction_column, m.reference_column, m.rouge_type, m.score_type
        )
        cur_mean = float(cur_scores.mean())

        ref_mean: Optional[float] = None
        ref_scores: Optional[pd.Series] = None
        if reference_data is not None:
            ref_df = reference_data.as_dataframe()
            ref_scores = _compute_rouge_series(
                ref_df, m.prediction_column, m.reference_column, m.rouge_type, m.score_type
            )
            ref_mean = float(ref_scores.mean())

        cur_col = DatasetColumn(type=ColumnType.Numerical, data=cur_scores)
        ref_col = DatasetColumn(type=ColumnType.Numerical, data=ref_scores) if ref_scores is not None else None

        widget = self._build_widget(cur_mean, ref_mean, cur_col, ref_col)

        current_result = self.result(cur_mean)
        current_result.widget = widget

        ref_result = self.result(ref_mean) if ref_mean is not None else None
        return current_result, ref_result

    def _build_widget(
        self,
        cur_mean: float,
        ref_mean: Optional[float],
        cur_col: DatasetColumn,
        ref_col: Optional[DatasetColumn],
    ) -> List[BaseWidgetInfo]:
        m = self.metric
        title = self.display_name()

        counter_items = [CounterData.float(label="current", value=cur_mean, precision=3)]
        if ref_mean is not None:
            counter_items.append(CounterData.float(label="reference", value=ref_mean, precision=3))

        distr_cur, distr_ref = get_distribution_for_column(
            column_type=ColumnType.Numerical.value,
            current=cur_col.data,
            reference=ref_col.data if ref_col is not None else None,
        )
        distr_fig = plot_distr_with_perc_button(
            hist_curr=HistogramData.from_distribution(distr_cur),
            hist_ref=HistogramData.from_distribution(distr_ref),
            xaxis_name=f"{m.rouge_type.upper()} {m.score_type}",
            yaxis_name="Count",
            yaxis_name_perc="Percent",
            same_color=False,
            color_options=ColorOptions(),
            subplots=False,
            to_json=False,
            current_name="current",
            reference_name="reference",
        )

        return [
            counter(title=title, counters=counter_items),
            plotly_figure(title=f"{title}: distribution", figure=distr_fig, size=WidgetSize.FULL),
        ]

    def display_name(self) -> str:
        m = self.metric
        variant = m.rouge_type.upper()
        return f"Mean {variant} ({m.score_type}) — '{m.prediction_column}' vs '{m.reference_column}'"
