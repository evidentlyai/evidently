from typing import List
from typing import Optional

import numpy as np
import pandas as pd

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.calculations.classification_performance import get_prediction_data
from evidently.legacy.core import IncludeTags
from evidently.legacy.metric_results import PredictionData
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.renderers.html_widgets import header_text
from evidently.legacy.utils.data_operations import process_columns

DEFAULT_N_BINS = 10


class ClassificationCalibrationResults(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:ClassificationCalibrationResults"
        field_tags = {
            "current_brier_score": {IncludeTags.Current},
            "current_ece": {IncludeTags.Current},
            "reference_brier_score": {IncludeTags.Reference},
            "reference_ece": {IncludeTags.Reference},
            "n_bins": {IncludeTags.Parameter},
        }

    current_brier_score: float
    current_ece: float
    reference_brier_score: Optional[float] = None
    reference_ece: Optional[float] = None
    n_bins: int = DEFAULT_N_BINS


class ClassificationCalibrationMetrics(Metric[ClassificationCalibrationResults]):
    """Computes Brier score and Expected Calibration Error (ECE) for
    probabilistic classification predictions. Both share the same
    prediction-probability data, so they're calculated together.
    """

    class Config:
        type_alias = "evidently:metric:ClassificationCalibrationMetrics"

    n_bins: int

    def __init__(self, n_bins: int = DEFAULT_N_BINS, options: AnyOptions = None):
        self.n_bins = n_bins
        super().__init__(options=options)

    def calculate(self, data: InputData) -> ClassificationCalibrationResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        if target_name is None:
            raise ValueError("The column 'target' should be present")

        curr_predictions = get_prediction_data(data.current_data, dataset_columns, data.column_mapping.pos_label)
        if curr_predictions.prediction_probas is None:
            raise ValueError("Brier score / ECE can be calculated only on probabilistic predictions")
        curr_brier, curr_ece = self._compute(data.current_data[target_name], curr_predictions)

        ref_brier: Optional[float] = None
        ref_ece: Optional[float] = None
        if data.reference_data is not None:
            ref_predictions = get_prediction_data(data.reference_data, dataset_columns, data.column_mapping.pos_label)
            if ref_predictions.prediction_probas is not None:
                ref_brier, ref_ece = self._compute(data.reference_data[target_name], ref_predictions)

        return ClassificationCalibrationResults(
            current_brier_score=curr_brier,
            current_ece=curr_ece,
            reference_brier_score=ref_brier,
            reference_ece=ref_ece,
            n_bins=self.n_bins,
        )

    def _compute(self, target_data: pd.Series, prediction: PredictionData):
        probas = prediction.prediction_probas
        labels = prediction.labels
        assert probas is not None

        # Brier score: mean over labels of the one-vs-rest Brier score.
        # For binary classification the two one-vs-rest terms are equal,
        # so this reduces exactly to the classic Brier score. For
        # multiclass it's the standard "mean Brier score" generalization.
        target_values = target_data.to_numpy()
        per_label_brier = []
        for label in labels:
            indicator = (target_values == label).astype(float)
            per_label_brier.append(float(np.mean((probas[label].to_numpy() - indicator) ** 2)))
        brier_score = float(np.mean(per_label_brier))

        # ECE: bin samples by predicted confidence (max probability across
        # labels) and compare each bin's average confidence to its accuracy.
        confidence = probas.max(axis=1).to_numpy()
        predicted_label = probas.idxmax(axis=1).to_numpy()
        correct = (predicted_label == target_values).astype(float)

        bin_edges = np.linspace(0.0, 1.0, self.n_bins + 1)
        bin_idx = np.clip(np.digitize(confidence, bin_edges, right=True) - 1, 0, self.n_bins - 1)

        n = len(confidence)
        ece = 0.0
        for b in range(self.n_bins):
            mask = bin_idx == b
            if not np.any(mask):
                continue
            bin_confidence = confidence[mask].mean()
            bin_accuracy = correct[mask].mean()
            ece += (mask.sum() / n) * abs(bin_accuracy - bin_confidence)

        return brier_score, float(ece)


@default_renderer(wrap_type=ClassificationCalibrationMetrics)
class ClassificationCalibrationMetricsRenderer(MetricRenderer):
    def render_html(self, obj: ClassificationCalibrationMetrics) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        widgets: List[BaseWidgetInfo] = [
            header_text(label="Calibration metrics"),
            counter(
                counters=[
                    CounterData.float("Brier score", result.current_brier_score, 3),
                    CounterData.float("ECE", result.current_ece, 3),
                ],
                title="Current",
            ),
        ]
        if result.reference_brier_score is not None and result.reference_ece is not None:
            widgets.append(
                counter(
                    counters=[
                        CounterData.float("Brier score", result.reference_brier_score, 3),
                        CounterData.float("ECE", result.reference_ece, 3),
                    ],
                    title="Reference",
                )
            )
        return widgets
