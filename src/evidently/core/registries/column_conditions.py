# ruff: noqa: E501
# fmt: off
from evidently.core.datasets import ColumnCondition
from evidently.pydantic_utils import register_type_alias

register_type_alias(ColumnCondition, "evidently.tests.descriptors.EqualsColumnCondition", "evidently:column_condition:EqualsColumnCondition")
register_type_alias(ColumnCondition, "evidently.tests.descriptors.GreaterColumnCondition", "evidently:column_condition:GreaterColumnCondition")
register_type_alias(ColumnCondition, "evidently.tests.descriptors.GreaterEqualColumnCondition", "evidently:column_condition:GreaterEqualColumnCondition")
register_type_alias(ColumnCondition, "evidently.tests.descriptors.IsInColumnCondition", "evidently:column_condition:IsInColumnCondition")
register_type_alias(ColumnCondition, "evidently.tests.descriptors.IsNotInColumnCondition", "evidently:column_condition:IsNotInColumnCondition")
register_type_alias(ColumnCondition, "evidently.tests.descriptors.LessColumnCondition", "evidently:column_condition:LessColumnCondition")
register_type_alias(ColumnCondition, "evidently.tests.descriptors.LessEqualColumnCondition", "evidently:column_condition:LessEqualColumnCondition")
register_type_alias(ColumnCondition, "evidently.tests.descriptors.NotEqualsColumnCondition", "evidently:column_condition:NotEqualsColumnCondition")
