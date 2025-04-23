import json
from inspect import isabstract
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import pandas as pd
import pytest

from evidently import ColumnType
from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import ColumnTest
from evidently.core.datasets import Dataset
from evidently.core.datasets import DatasetColumn
from evidently.core.datasets import Descriptor
from evidently.core.datasets import FeatureDescriptor
from evidently.core.datasets import TestSummary
from evidently.descriptors import ContextRelevance
from evidently.descriptors import CustomColumnDescriptor
from evidently.descriptors import CustomDescriptor
from evidently.descriptors import TextLength
from evidently.tests import eq
from tests.conftest import load_all_subtypes

from .test_feature_descriptors import MockGeneratedFeature

int_data = pd.Series([1, 2, 3], name="int")
str_data = pd.Series(["a", "b", "c"], name="str")


def custom_descr(dataset: Dataset) -> DatasetColumn:
    return DatasetColumn(ColumnType.Numerical, pd.Series([1] * len(dataset.as_dataframe())))


def custom_col_descr(col: DatasetColumn) -> DatasetColumn:
    return DatasetColumn(ColumnType.Numerical, col.data)


all_descriptors: List[Tuple[Descriptor, Union[pd.Series, pd.DataFrame], Dict[str, pd.Series]]] = [
    (
        FeatureDescriptor(feature=MockGeneratedFeature(column="str", field="a"), alias="res"),
        str_data,
        {"a1702de9f83a993ea3cb4701ca9d17f7.str": pd.Series(["aa", "ba", "ca"])},
    ),
    (TextLength(column_name="str", alias="res"), str_data, {"res": pd.Series([1, 1, 1])}),
    (CustomColumnDescriptor(column_name="int", func=custom_col_descr, alias="res"), int_data, {"res": int_data}),
    (CustomDescriptor(func=custom_descr, alias="res"), int_data, {"res": pd.Series([1, 1, 1])}),
    (TestSummary(alias="res"), int_data, {"res": pd.Series([1, 0, 0])}),
    (
        ContextRelevance(alias="res", input="i", contexts="c"),
        pd.DataFrame({"i": ["input"], "c": ["context"]}),
        {"res": pd.Series([0.6781195998191833])},
    ),
]


def test_descriptors_tested():
    tested_desc_set = {type(p) for p, _, _ in all_descriptors}
    load_all_subtypes(Descriptor)
    all_desc_types = set(s for s in Descriptor.__subclasses__() if not isabstract(s))
    assert tested_desc_set == all_desc_types, "Missing tests for descriptors " + ", ".join(
        f'({t.__name__}(alias="res"), pd.Series(), {{"res":pd.Series()}})' for t in all_desc_types - tested_desc_set
    )


@pytest.mark.parametrize("descriptor,data,result", all_descriptors)
def test_descriptors(descriptor: Descriptor, data: Union[pd.Series, pd.DataFrame], result: Dict[str, pd.Series]):
    df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
    dataset = Dataset.from_pandas(df)
    if isinstance(descriptor, TestSummary):
        dataset.add_descriptor(ColumnTest(str(df.columns[0]), eq(1)))
    dataset.add_descriptor(descriptor)

    res_df = dataset.as_dataframe()
    for col, value in result.items():
        assert col in set(res_df.columns), f"no column {col}, cols: {res_df.columns}"
        assert res_df[col].tolist() == value.tolist()

    payload = json.loads(descriptor.json())
    descriptor2 = parse_obj_as(Descriptor, payload)
    assert descriptor2 == descriptor
