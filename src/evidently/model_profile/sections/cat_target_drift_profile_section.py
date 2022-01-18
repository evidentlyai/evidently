from datetime import datetime

from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection


class CatTargetDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'cat_target_drift'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [CatTargetDriftAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = CatTargetDriftAnalyzer.get_results(analyzers_results)
        result_as_json = result.columns.as_dict()
        result_as_json['metrics'] = {}

        if result.target_metrics:
            result_as_json['metrics']['target_name'] = result.target_metrics.column_name
            result_as_json['metrics']['target_type'] = 'cat'
            result_as_json['metrics']['target_drift'] = result.target_metrics.drift

        if result.prediction_metrics:
            result_as_json['metrics']['prediction_name'] = result.prediction_metrics.column_name
            result_as_json['metrics']['prediction_type'] = 'cat'
            result_as_json['metrics']['prediction_drift'] = result.prediction_metrics.drift

        self._result = {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result_as_json
        }

    def get_results(self):
        return self._result
