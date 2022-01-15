from datetime import datetime
from typing import Dict, Optional, Union

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection


class DataDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "data_drift"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [DataDriftAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results) -> None:
        data_drift_results = DataDriftAnalyzer.get_results(analyzers_results)
        metrics_dict: Dict[str, Union[int, bool, float, Dict]] = {
            'n_features': data_drift_results.metrics.n_features,
            'n_drifted_features': data_drift_results.metrics.n_drifted_features,
            'share_drifted_features': data_drift_results.metrics.share_drifted_features,
            'dataset_drift': data_drift_results.metrics.dataset_drift
        }
        # add metrics to a flat dict with data drift results
        for feature_name, feature_metrics in data_drift_results.metrics.features.items():
            metrics_dict[feature_name] = {
                'current_small_hist': feature_metrics.current_small_hist,
                'ref_small_hist': feature_metrics.ref_small_hist,
                'feature_type': feature_metrics.feature_type,
                'p_value': feature_metrics.p_value,
            }

        self._result = {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': {
                'utility_columns': data_drift_results.utility_columns.as_dict(),
                'cat_feature_names': data_drift_results.cat_feature_names,
                'num_feature_names': data_drift_results.num_feature_names,
                'target_names': data_drift_results.target_names,
                'options': data_drift_results.options.as_dict(),
                'metrics': metrics_dict
            }
        }

    def get_results(self) -> Optional[Dict[str, Union[str, Dict]]]:
        return self._result
