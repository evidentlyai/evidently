import pandas as pd
import pytest

from evidently.calculations.stattests import get_stattest


@pytest.mark.parametrize(
    "feature_type,stattest_name",
    [
        ("num", "anderson"),
        ("cat", "chisquare"),
        ("num", "cramer_von_mises"),
        ("num", "ed"),
        ("num", "es"),
        ("cat", "fisher_exact"),
        ("cat", "g_test"),
        ("cat", "hellinger"),
        ("num", "hellinger"),
        ("cat", "jensenshannon"),
        ("num", "jensenshannon"),
        ("cat", "kl_div"),
        ("num", "kl_div"),
        ("num", "ks"),
        ("num", "mannw"),
        ("num", "emperical_mmd"),
        ("cat", "psi"),
        ("num", "psi"),
        ("num", "t_test"),
        ("text", "text_content_drift"),
        ("cat", "TVD"),
        ("num", "wasserstein"),
        ("cat", "z"),
    ],
)
def test_use_stattest_by_name(feature_type: str, stattest_name: str):
    assert get_stattest(pd.Series(), pd.Series(), feature_type, stattest_name)
