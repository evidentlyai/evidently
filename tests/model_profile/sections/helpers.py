"""Common methods for testing sections"""
import json
from typing import Optional, Type

import pandas

from evidently.model_profile.sections.base_profile_section import \
    ProfileSection
from evidently.options import DataDriftOptions, OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils import NumpyEncoder


def check_profile_section_result_common_part(section_result: dict, section_result_name: str) -> None:
    """Check all common fields for all sections results"""
    assert "name" in section_result
    assert section_result["name"] == section_result_name
    assert "datetime" in section_result
    assert isinstance(section_result["datetime"], str)
    assert "data" in section_result
    result_data = section_result["data"]
    assert isinstance(result_data, dict)

    assert "utility_columns" in result_data
    assert isinstance(result_data["utility_columns"], dict)
    assert "cat_feature_names" in result_data
    assert isinstance(result_data["cat_feature_names"], list)
    assert "num_feature_names" in result_data
    assert isinstance(result_data["num_feature_names"], list)
    assert "target_names" in result_data
    assert "metrics" in result_data


def check_section_without_calculation_results(profile_section_class: Type[ProfileSection], part_id: str) -> None:
    """Check creation of a section and results without calculations"""
    data_drift_profile_section = profile_section_class()
    assert data_drift_profile_section.part_id() == part_id
    empty_result = data_drift_profile_section.get_results()
    assert empty_result is None


def calculate_section_results(
    profile_section_class: Type[ProfileSection],
    reference_data: Optional[pandas.DataFrame],
    current_data: Optional[pandas.DataFrame],
    columns_mapping: Optional[ColumnMapping] = None,
) -> Optional[dict]:
    """Run profile section calculations, check json serialization and return the results"""
    options_provider = OptionsProvider()
    options_provider.add(DataDriftOptions())
    profile_section = profile_section_class()

    if columns_mapping is None:
        columns_mapping = ColumnMapping()

    analyzers_results = {}

    for analyzer_class in profile_section.analyzers():
        analyzer = analyzer_class()
        analyzer.options_provider = options_provider
        analyzers_results[analyzer_class] = analyzer.calculate(reference_data, current_data, columns_mapping)

    profile_section.calculate(reference_data, current_data, columns_mapping, analyzers_results)
    section_result = profile_section.get_results()
    check_json_serialization(section_result)
    return section_result


def check_json_serialization(section_result: dict):
    """Try to serialize the dict to json with custom Numpy encoder"""
    json.dumps(section_result, cls=NumpyEncoder), section_result
