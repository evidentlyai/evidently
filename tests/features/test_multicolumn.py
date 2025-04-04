from typing import List
from typing import Optional

import pandas as pd

from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.feature_generator import FeatureGenerator
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.metrics import ColumnSummaryMetric
from evidently.legacy.options.base import Options
from evidently.legacy.report import Report
from evidently.legacy.utils.data_preprocessing import DataDefinition


class MultiColumnFeature(GeneratedFeatures):
    class Config:
        alias_required = False

    source_column: str
    _called_count: int = PrivateAttr(0)

    def generate_features(self, data: pd.DataFrame, data_definition: DataDefinition, options: Options) -> pd.DataFrame:
        self._called_count += 1
        col = data[self.source_column]
        return pd.DataFrame({"+1": col + 1, "+5": col + 5})

    def list_columns(self) -> List["ColumnName"]:
        return [self._create_column(subcolumn="+1"), self._create_column(subcolumn="+5")]

    def get_type(self, subcolumn: Optional[str] = None):
        return ColumnType.Numerical


def test_feature_generator():
    f1 = MultiColumnFeature(
        source_column="a",
    )
    f2 = MultiColumnFeature(source_column="b")
    report = FeatureGenerator(
        features=[
            f1,
            f2,
        ]
    )
    cur = pd.DataFrame({"a": [1, 2], "b": [11, 12]})
    ref = pd.DataFrame({"a": [3, 4], "b": [13, 14]})
    report.run(current_data=cur, reference_data=ref)

    f1_cur, f1_ref = report.get_features(f1)
    pd.testing.assert_frame_equal(
        f1_cur, pd.DataFrame({f"{f1.get_fingerprint()}.+1": [2, 3], f"{f1.get_fingerprint()}.+5": [6, 7]})
    )
    pd.testing.assert_frame_equal(
        f1_ref, pd.DataFrame({f"{f1.get_fingerprint()}.+1": [4, 5], f"{f1.get_fingerprint()}.+5": [8, 9]})
    )

    f2_cur, f2_ref = report.get_features(f2)

    pd.testing.assert_frame_equal(
        f2_cur, pd.DataFrame({f"{f2.get_fingerprint()}.+1": [12, 13], f"{f2.get_fingerprint()}.+5": [16, 17]})
    )
    pd.testing.assert_frame_equal(
        f2_ref, pd.DataFrame({f"{f2.get_fingerprint()}.+1": [14, 15], f"{f2.get_fingerprint()}.+5": [18, 19]})
    )

    all_features_cur, all_features_ref = report.get_features()
    pd.testing.assert_frame_equal(all_features_cur, f1_cur.join(f2_cur))
    pd.testing.assert_frame_equal(all_features_ref, f1_ref.join(f2_ref))

    assert f1._called_count == 2  # once for cur and ref
    assert f2._called_count == 2  # once for cur and ref


def test_multicolumn_in_report():
    cur = pd.DataFrame({"a": [1, 2]})
    ref = pd.DataFrame({"a": [3, 4]})

    f1 = MultiColumnFeature(source_column="a")
    f2 = MultiColumnFeature(source_column="a")
    report = Report(
        metrics=[
            ColumnSummaryMetric(column_name=f1.as_column(subcolumn="+1")),
            ColumnSummaryMetric(column_name=f2.as_column(subcolumn="+5")),
        ]
    )
    report.run(current_data=cur, reference_data=ref)

    res_cur, res_ref = report.datasets()
    pd.testing.assert_frame_equal(
        res_cur, pd.DataFrame({"a": [1, 2], f"{f1.get_fingerprint()}.+1": [2, 3], f"{f1.get_fingerprint()}.+5": [6, 7]})
    )
    pd.testing.assert_frame_equal(
        res_ref, pd.DataFrame({"a": [3, 4], f"{f1.get_fingerprint()}.+1": [4, 5], f"{f1.get_fingerprint()}.+5": [8, 9]})
    )
    assert f1._called_count + f2._called_count == 2  # once for cur and ref
