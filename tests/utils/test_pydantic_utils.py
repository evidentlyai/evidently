import pytest

from evidently.base_metric import MetricResult


class MockMetricResultField(MetricResult):
    nested_field: str


class MockMetricResult(MetricResult):
    field1: MockMetricResultField
    field2: int


def test_field_path():
    assert MockMetricResult.fields().list_fields() == ["type", "field1", "field2"]
    assert MockMetricResult.fields().field1.list_fields() == ["field1.type", "field1.nested_field"]
    assert MockMetricResult.fields().list_nested_fields() == ["type", "field1.type", "field1.nested_field", "field2"]

    with pytest.raises(AttributeError):
        MockMetricResult.fields().field3.list_fields()
