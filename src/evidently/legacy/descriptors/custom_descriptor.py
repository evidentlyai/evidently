from typing import Callable
from typing import Union

import pandas as pd

from evidently.legacy.core import ColumnType
from evidently.legacy.core import new_id
from evidently.legacy.features.custom_feature import CustomPairColumnFeature
from evidently.legacy.features.custom_feature import CustomSingleColumnFeature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneralDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class CustomColumnEval(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:CustomColumnEval"

    func: Callable[[pd.Series], pd.Series]
    display_name: str
    feature_type: Union[str, ColumnType]
    name: str = ""

    def feature(self, column_name: str) -> GeneratedFeature:
        return CustomSingleColumnFeature(
            func=self.func,
            column_name=column_name,
            display_name=self.display_name,
            feature_type=ColumnType(self.feature_type),
            name=self.name or getattr(self.func, "__name__", str(new_id())),
        )


class CustomPairColumnEval(GeneralDescriptor):
    class Config:
        type_alias = "evidently:descriptor:CustomPairColumnEval"

    func: Callable[[pd.Series, pd.Series], pd.Series]
    display_name: str
    first_column: str
    second_column: str
    feature_type: Union[str, ColumnType]

    def feature(self) -> GeneratedFeature:
        return CustomPairColumnFeature(
            func=self.func,
            first_column=self.first_column,
            second_column=self.second_column,
            display_name=self.display_name,
            feature_type=ColumnType(self.feature_type),
        )
