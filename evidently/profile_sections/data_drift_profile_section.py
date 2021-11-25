from datetime import datetime
import numpy as np

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.profile_sections.base_profile_section import ProfileSection
from evidently.widgets.data_drift_table_widget import DataDriftOptions, dataset_drift_evaluation


class DataDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "data_drift"

    def __init__(self, options: DataDriftOptions = None):
        super().__init__()
        self.options = options if options else DataDriftOptions()
        self.analyzers_types = [DataDriftAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, reference_data, current_data, analyzers_results):
        result = analyzers_results[DataDriftAnalyzer]
        nbinsx = self.options.nbinsx
        confidence = self.options.confidence
        drift_share = self.options.drift_share
        num_feature_names = result["num_feature_names"]
        cat_feature_names = result["cat_feature_names"]
        for feature_name in num_feature_names:
            if nbinsx:
                current_nbinsx = nbinsx.get(feature_name) if nbinsx.get(feature_name) else 10
            else:
                current_nbinsx = 10
            result['metrics'][feature_name]['current_small_hist'] = \
                [t.tolist() for t in
                 np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                              bins=current_nbinsx,
                              density=True)]
            result['metrics'][feature_name]['ref_small_hist'] = \
                [t.tolist() for t in
                 np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                              bins=current_nbinsx,
                              density=True)]

        for feature_name in cat_feature_names:
            if nbinsx:
                current_nbinsx = nbinsx.get(feature_name) if nbinsx.get(feature_name) else 10
            else:
                current_nbinsx = 10
            result['metrics'][feature_name]['current_small_hist'] = \
                [t.tolist() for t in
                 np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                              bins=current_nbinsx,
                              density=True)]
            result['metrics'][feature_name]['ref_small_hist'] = \
                [t.tolist() for t in
                 np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                              bins=current_nbinsx,
                              density=True)]

        n_drifted_features, share_drifted_features, dataset_drift = dataset_drift_evaluation(
            [result['metrics'][fn]['p_value'] for fn in num_feature_names + cat_feature_names],
            confidence,
            drift_share)
        result['metrics']['n_features'] = len(num_feature_names) + len(cat_feature_names)
        result['metrics']['n_drifted_features'] = n_drifted_features
        result['metrics']['share_drifted_features'] = share_drifted_features
        result['metrics']['dataset_drift'] = dataset_drift
        return {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result
        }
