"""Common methods for testing sections"""
from typing import ClassVar


def check_profile_section_result_common_part(section_result: dict, section_result_name: str) -> None:
    """Check all common fields for all sections results"""
    assert 'name' in section_result
    assert section_result['name'] == section_result_name
    assert 'datetime' in section_result
    assert isinstance(section_result['datetime'], str)
    assert 'data' in section_result
    assert isinstance(section_result['data'], dict)


def check_section_no_calculation_results(profile_section_class: ClassVar, part_id: str) -> None:
    """Check creation of a section and results without calculations"""
    data_drift_profile_section = profile_section_class()
    assert data_drift_profile_section.part_id() == part_id
    empty_result = data_drift_profile_section.get_results()
    assert empty_result is None
