import json
from dataclasses import dataclass
from typing import List

from evidently.model_profile import Profile
from evidently.profile_parts.data_drift_profile_part import DataDriftProfilePart
from evidently.runner.runner import RunnerOptions, Runner


@dataclass
class ProfileRunnerOptions(RunnerOptions):
    profile_parts: List[str]
    pretty_print: bool


parts_mapping = dict(
    data_drift=DataDriftProfilePart,
)


class ProfileRunner(Runner):
    def __init__(self, options: ProfileRunnerOptions):
        super().__init__(options)
        self.options = options

    def run(self):
        (reference_data, production_data) = self._parse_data()

        parts = []

        for part in self.options.profile_parts:
            part_class = parts_mapping.get(part, None)
            if part_class is None:
                raise ValueError(f"Unknown profile part {part}")
            parts.append(part_class)

        profile = Profile(parts=parts)
        profile.calculate(reference_data, production_data, self.options.column_mapping)
        output_path = self.options.output_path \
            if self.options.output_path.endswith(".json") \
            else self.options.output_path + ".json"

        with open(output_path, 'w') as f:
            json.dump(profile.object(), f, indent=2 if self.options.pretty_print else None)
