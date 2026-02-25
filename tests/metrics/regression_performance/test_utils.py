import pandas as pd

from evidently.legacy.metrics.regression_performance.utils import apply_func_to_binned_data
from evidently.legacy.metrics.utils import make_target_bins_for_reg_plots


def test_apply_func_to_binned_data():
    data = pd.DataFrame(
        data={
            "b": list(range(1000)),
            "b_pred": list(range(1000)),
        }
    )
    ref_data = pd.DataFrame(
        data={
            "b": list(range(1000)),
            "b_pred": list(range(1000)),
        }
    )
    binned_data = make_target_bins_for_reg_plots(data, "b", "b_pred", ref_data)
    res = apply_func_to_binned_data(binned_data, lambda x, y: max(max(x), max(y)), "b", "b_pred", is_ref_data=True)
    assert res is not None
    assert res.current.bins == [-0.999, 99.9, 199.8, 299.7, 399.6, 499.5, 599.4, 699.3, 799.2, 899.1, 999]
    assert res.current.values == [99, 199, 299, 399, 499, 599, 699, 799, 899, 999]
    assert res.reference.bins == [-0.999, 99.9, 199.8, 299.7, 399.6, 499.5, 599.4, 699.3, 799.2, 899.1, 999]
    assert res.reference.values == [99, 199, 299, 399, 499, 599, 699, 799, 899, 999]
