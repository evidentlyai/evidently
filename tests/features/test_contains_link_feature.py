import pandas as pd

from evidently.legacy.features.contains_link_feature import ContainsLink
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition


def test_contains_link_feature():
    # Initialize the ContainsLink feature generator for column_1
    feature_generator = ContainsLink("column_1")

    # Sample data with varying texts that contain or don't contain links
    data = pd.DataFrame(
        dict(
            column_1=[
                "Check out https://example.com for more info",  # Contains a valid link
                "Visit our website at http://www.test.com.",  # Contains a valid link
                "No link here, just plain text",  # No link
                "Another string without a link",  # No link
                "Here is a malformed link: www.test.com",  # Invalid link (missing scheme)
            ]
        )
    )

    # Generate the feature
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )

    # Expected result: True for valid links, False otherwise
    expected_result = pd.DataFrame(dict(column_1=[True, True, False, False, False]))

    # Assert that the generated result matches the expected result
    assert result.equals(expected_result)
