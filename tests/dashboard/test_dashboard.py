from typing import ClassVar

import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
from evidently.dashboard.tabs import DataQualityTab
from evidently.dashboard.tabs import NumTargetDriftTab
from evidently.dashboard.tabs import CatTargetDriftTab
from evidently.dashboard.tabs import RegressionPerformanceTab
from evidently.dashboard.tabs import ClassificationPerformanceTab
from evidently.dashboard.tabs import ProbClassificationPerformanceTab
from evidently.dashboard.tabs.base_tab import Tab


@pytest.mark.parametrize(
    "tab_class, raises_value_error",
    (
        (DataQualityTab, False),
        (RegressionPerformanceTab, False),
        (ClassificationPerformanceTab, False),
        (DataDriftTab, True),
        (NumTargetDriftTab, True),
        (CatTargetDriftTab, True),
    ),
)
def test_dashboards_without_current_data(tab_class: ClassVar[Tab], raises_value_error: bool) -> None:
    """Check that dashboards
    - that can be executed with one dataset only do not get an error
    - that cannot be executed with one dataset raise correct error
    """
    test_data = pd.DataFrame(
        {"target": [1, 0, 1], "prediction": [1, 0, 0], "num_feature": [1, 2, 3], "cat_feature": [3, 2, 1]}
    )
    dashboard = Dashboard(tabs=[tab_class()])
    data_mapping = ColumnMapping(numerical_features=["num_feature"], categorical_features=["cat_feature"])

    if raises_value_error:
        with pytest.raises(ValueError) as error:
            dashboard.calculate(test_data, column_mapping=data_mapping)

        assert error.value.args[0] == "current_data should be present"

    else:
        dashboard.calculate(test_data, column_mapping=data_mapping)
        assert dashboard.analyzers_results is not None

    dashboard.calculate(test_data, test_data, data_mapping)
    assert dashboard.analyzers_results is not None


def test_dashboards_without_current_data_prob_classification() -> None:
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
    dashboard = Dashboard(tabs=[ProbClassificationPerformanceTab()])
    dashboard.calculate(test_data, column_mapping=data_mapping)
    assert dashboard.analyzers_results is not None
    dashboard.calculate(test_data, test_data, data_mapping)
    assert dashboard.analyzers_results is not None
