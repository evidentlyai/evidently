"""
Test for the correct DataFrame test UX.
"""

import pandas as pd
import pytest

from evidently import Report
from evidently.core.metric_types import DataframeCalculation
from evidently.core.metric_types import DataframeMetric
from evidently.legacy.tests.base_test import TestStatus
from evidently.tests.aliases import gt
from evidently.tests.aliases import gte
from evidently.tests.aliases import lt
from evidently.tests.aliases import lte


class TestDataframeMetric(DataframeMetric):
    """Test DataFrame metric."""

    def to_calculation(self):
        return TestDataframeCalculation(self.get_metric_id(), self)


class TestDataframeCalculation(DataframeCalculation[TestDataframeMetric]):
    """Test calculation that returns a DataFrame."""

    def calculate(self, context, current_data, reference_data=None):
        # Return the input data as DataFrame result
        df = current_data.as_dataframe()
        result = self.result(df)
        return result, None

    def display_name(self):
        return "Test DataFrame Metric"


# Test data fixtures
def create_basic_test_data():
    """Create basic test data with category, subcategory, score, and value columns."""
    return pd.DataFrame({"category": ["A", "B"], "subcategory": ["X", "Y"], "score": [0.8, 0.6], "value": [1.0, 2.0]})


def create_extended_test_data():
    """Create extended test data with 4 rows for complex filtering tests."""
    return pd.DataFrame(
        {
            "category": ["A", "A", "B", "B"],
            "subcategory": ["X", "Y", "X", "Y"],
            "score": [0.8, 0.6, 0.9, 0.7],  # A,X=0.8, A,Y=0.6, B,X=0.9, B,Y=0.7
            "value": [1.0, 2.0, 3.0, 4.0],
        }
    )


def create_multi_column_test_data():
    """Create test data with multiple numeric columns."""
    return pd.DataFrame(
        {
            "category": ["A", "B"],
            "subcategory": ["X", "Y"],
            "score": [0.8, 0.6],
            "confidence": [0.85, 0.95],
            "value": [1.0, 2.0],
        }
    )


def run_report_and_get_tests(metric, current_data, reference_data=None):
    """Helper function to run a report and extract test results."""
    if reference_data is None:
        reference_data = current_data.copy()

    report = Report(metrics=[metric])
    snapshot = report.run(reference_data=reference_data, current_data=current_data)

    report_data = snapshot.dict()
    assert "tests" in report_data
    return report_data["tests"]


def assert_test_result(test_result, expected_status, expected_description_contains=None):
    """Helper function to assert test result properties."""
    assert test_result["status"] == expected_status
    if expected_description_contains:
        assert expected_description_contains in test_result["description"]


def test_correct_dataframe_test_config():
    """Test the correct DataFrame test configuration."""

    # Create a DataFrame metric with proper test configuration
    metric = TestDataframeMetric(
        tests={
            "score": [
                gt(0.5, label_filters={"category": "A"}),
                gte(0.6, label_filters={"category": "B"}),
            ],
            "confidence": [
                lt(0.9, label_filters={"subcategory": "X"}),
                lte(0.9, label_filters={"category": "A"}),
            ],
        }
    )

    # Test that the metric has the correct test configuration
    assert isinstance(metric.tests, dict)
    assert "score" in metric.tests
    assert "confidence" in metric.tests
    assert len(metric.tests["score"]) == 2
    assert len(metric.tests["confidence"]) == 2

    # Check that tests have the expected attributes
    for column_tests in metric.tests.values():
        for test in column_tests:
            assert hasattr(test, "threshold")
            assert hasattr(test, "label_filters")

    # Check specific test configurations
    score_gt_test = metric.tests["score"][0]
    assert score_gt_test.threshold == 0.5
    assert score_gt_test.label_filters == {"category": "A"}

    confidence_lt_test = metric.tests["confidence"][0]
    assert confidence_lt_test.threshold == 0.9
    assert confidence_lt_test.label_filters == {"subcategory": "X"}


@pytest.mark.parametrize(
    "test_config,expected_status,expected_description",
    [
        # Successful test cases
        ({"score": [gt(0.7, label_filters={"category": "A"})]}, TestStatus.SUCCESS, None),
        # Failing test cases
        (
            {"score": [gt(0.9, label_filters={"category": "A"})]},  # 0.8 > 0.9 = FAIL
            TestStatus.FAIL,
            None,
        ),
        # Error test cases
        ({"score": [gt(0.7, label_filters={"category": "NonExistent"})]}, TestStatus.ERROR, "No matching value found"),
    ],
)
def test_dataframe_test_execution(test_config, expected_status, expected_description):
    """Test DataFrame test execution with different scenarios."""

    # Create metric with test configuration
    metric = TestDataframeMetric(tests=test_config)

    # Use basic test data
    current_data = create_basic_test_data()

    # Run report and get test results
    tests_data = run_report_and_get_tests(metric, current_data)

    # Verify test execution
    assert len(tests_data) == 1
    test_result = tests_data[0]

    # Assert test result
    assert_test_result(test_result, expected_status, expected_description)

    # Additional assertions for successful tests
    if expected_status == TestStatus.SUCCESS:
        assert "score" in test_result["name"]
        assert "Greater" in test_result["name"]


def test_multiple_label_filters():
    """Test DataFrame test with multiple label filters."""

    # Create a DataFrame metric with tests using multiple label filters
    metric = TestDataframeMetric(
        tests={
            "score": [
                gt(0.7, label_filters={"category": "A", "subcategory": "X"}),
                lt(0.9, label_filters={"category": "B", "subcategory": "Y"}),
            ]
        }
    )

    # Use extended test data for complex filtering
    current_data = create_extended_test_data()

    # Run report and get test results
    tests_data = run_report_and_get_tests(metric, current_data)

    # Verify tests were executed
    assert len(tests_data) == 2

    # Verify both tests passed
    for test_result in tests_data:
        assert_test_result(test_result, TestStatus.SUCCESS)


def test_multiple_columns():
    """Test DataFrame test with multiple columns."""

    # Create a DataFrame metric with tests on multiple columns
    metric = TestDataframeMetric(
        tests={
            "score": [
                gt(0.7, label_filters={"category": "A"}),
            ],
            "confidence": [
                lt(0.9, label_filters={"category": "A"}),
            ],
        }
    )

    # Use multi-column test data
    current_data = create_multi_column_test_data()

    # Run report and get test results
    tests_data = run_report_and_get_tests(metric, current_data)

    # Verify tests were executed
    assert len(tests_data) == 2

    # Verify both tests passed
    for test_result in tests_data:
        assert_test_result(test_result, TestStatus.SUCCESS)
