import pandas
import pytest

from evidently.model_profile.sections.base_profile_section import \
    ProfileSection
from evidently.pipeline.column_mapping import ColumnMapping


def test_not_implemented_methods_in_base_profile_section() -> None:
    base_profile = ProfileSection()

    with pytest.raises(NotImplementedError):
        base_profile.analyzers()

    with pytest.raises(NotImplementedError):
        base_profile.part_id()

    with pytest.raises(NotImplementedError):
        base_profile.calculate(
            reference_data=pandas.DataFrame(),
            current_data=None,
            column_mapping=ColumnMapping(),
            analyzers_results={},
        )

    with pytest.raises(NotImplementedError):
        base_profile.get_results()
