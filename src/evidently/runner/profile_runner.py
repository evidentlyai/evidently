import json
from dataclasses import dataclass
from typing import Dict

from evidently.model_profile import Profile
from evidently.model_profile.sections.cat_target_drift_profile_section import CatTargetDriftProfileSection
from evidently.model_profile.sections.classification_performance_profile_section import (
    ClassificationPerformanceProfileSection,
)
from evidently.model_profile.sections.data_drift_profile_section import DataDriftProfileSection
from evidently.model_profile.sections.data_quality_profile_section import DataQualityProfileSection
from evidently.model_profile.sections.num_target_drift_profile_section import NumTargetDriftProfileSection
from evidently.model_profile.sections.prob_classification_performance_profile_section import (
    ProbClassificationPerformanceProfileSection,
)
from evidently.model_profile.sections.regression_performance_profile_section import RegressionPerformanceProfileSection
from evidently.runner.runner import Runner
from evidently.runner.runner import RunnerOptions
from evidently.utils import NumpyEncoder


@dataclass
class ProfileRunnerOptions(RunnerOptions):
    profile_parts: Dict[str, Dict[str, str]]
    pretty_print: bool


parts_mapping = dict(
    data_drift=DataDriftProfileSection,
    cat_target_drift=CatTargetDriftProfileSection,
    classification_performance=ClassificationPerformanceProfileSection,
    prob_classification_performance=ProbClassificationPerformanceProfileSection,
    num_target_drift=NumTargetDriftProfileSection,
    regression_performance=RegressionPerformanceProfileSection,
    data_quality=DataQualityProfileSection,
)


class ProfileRunner(Runner):
    def __init__(self, options: ProfileRunnerOptions):
        super().__init__(options)
        self.options = options

    def run(self):
        (reference_data, current_data) = self._parse_data()

        parts = []

        for part, _ in self.options.profile_parts.items():
            part_class = parts_mapping.get(part, None)
            if part_class is None:
                raise ValueError(f"Unknown profile section {part}")
            parts.append(part_class())

        profile = Profile(sections=parts, options=self.options.options)
        profile.calculate(reference_data, current_data, self.options.column_mapping)
        output_path = (
            self.options.output_path
            if self.options.output_path.endswith(".json")
            else self.options.output_path + ".json"
        )

        with open(output_path, "w", encoding="utf-8") as out_file:
            json.dump(profile.object(), out_file, indent=2 if self.options.pretty_print else None, cls=NumpyEncoder)
