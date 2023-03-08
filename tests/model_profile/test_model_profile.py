from typing import Type

import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.model_profile import Profile
from evidently.model_profile.sections import (
    CatTargetDriftProfileSection,
    ClassificationPerformanceProfileSection,
    DataDriftProfileSection,
    DataQualityProfileSection,
    NumTargetDriftProfileSection,
    ProbClassificationPerformanceProfileSection,
    RegressionPerformanceProfileSection,
)
from evidently.model_profile.sections.base_profile_section import ProfileSection


@pytest.mark.parametrize(
    "section_class, raises_value_error",
    (
        (ClassificationPerformanceProfileSection, False),
        (RegressionPerformanceProfileSection, False),
        (DataQualityProfileSection, False),
        (DataDriftProfileSection, True),
        (CatTargetDriftProfileSection, True),
        (NumTargetDriftProfileSection, True),
    ),
)
def test_model_profile_without_current_data(
    section_class: Type[ProfileSection], raises_value_error: bool
) -> None:
    """Check that profiles
    - that can be executed with one dataset only do not get an error
    - that cannot be executed with one dataset raise correct error
    """
    my_profile = Profile([section_class()])
    test_data = pd.DataFrame(
        {
            "target": [1, 0, 1],
            "prediction": [1, 0, 0],
            "num_feature": [1, 2, 3],
            "cat_feature": [3, 2, 1],
        }
    )
    data_mapping = ColumnMapping(
        numerical_features=["num_feature"], categorical_features=["cat_feature"]
    )

    if raises_value_error:
        with pytest.raises(ValueError) as error:
            my_profile.calculate(test_data, column_mapping=data_mapping)

        assert error.value.args[0] == "current_data should be present"

    else:
        my_profile.calculate(test_data)
        result = my_profile.json()
        assert result is not None

    my_profile.calculate(test_data, test_data, data_mapping)
    result = my_profile.json()
    assert result is not None


def test_model_profile_without_current_data_prob_classification() -> None:
    test_data = pd.DataFrame(
        {
            "target": ["0", "1", "0", "1"],
            "0": [0.1, 0.2, 0.3, 0.4],
            "1": [0.5, 0.6, 0.7, 0.8],
        }
    )
    data_mapping = ColumnMapping(
        target="target",
        prediction=["0", "1"],
    )
    my_profile = Profile([ProbClassificationPerformanceProfileSection()])
    my_profile.calculate(test_data)
    result = my_profile.json()
    assert result is not None

    my_profile.calculate(test_data, test_data, data_mapping)
    result = my_profile.json()
    assert result is not None
