import argparse
import json
import os
import sys
from typing import Dict, List

from dataclasses import dataclass

from evidently.runner.dashboard_runner import DashboardRunnerOptions, DashboardRunner
from evidently.runner.profile_runner import ProfileRunner, ProfileRunnerOptions
from evidently.runner.runner import DataOptions


@dataclass
class DataFormatOptions:
    header: bool
    separator: str
    date_column: str


@dataclass
class CalculateOptions:
    data_format: DataFormatOptions
    column_mapping: Dict[str, str]


@dataclass
class DashboardOptions(CalculateOptions):
    dashboard_tabs: List[str]


@dataclass
class ProfileOptions(CalculateOptions):
    profile_parts: List[str]
    pretty_print: bool = False


def calculate_dashboard(config: str, reference: str, current: str, output_path: str, report_name: str, **_kv):
    with open(config) as f_config:
        opts_data = json.load(f_config)
        opts = DashboardOptions(data_format=DataFormatOptions(**opts_data["data_format"]),
                                column_mapping=opts_data["column_mapping"],
                                dashboard_tabs=opts_data["dashboard_tabs"])

    runner = DashboardRunner(DashboardRunnerOptions(
        reference_data_path=reference,
        reference_data_options=DataOptions(date_column=opts.data_format.date_column,
                                           separator=opts.data_format.separator,
                                           header=opts.data_format.header),
        production_data_path=current,
        production_data_options=DataOptions(date_column=opts.data_format.date_column,
                                            separator=opts.data_format.separator,
                                            header=opts.data_format.header),
        dashboard_tabs=opts.dashboard_tabs,
        column_mapping=opts.column_mapping,
        output_path=os.path.join(output_path, report_name),
    ))
    runner.run()


def calculate_profile(config: str, reference: str, current: str, output_path: str, report_name: str, **_kv):
    with open(config) as f_config:
        opts_data = json.load(f_config)
        opts = ProfileOptions(data_format=DataFormatOptions(**opts_data["data_format"]),
                              column_mapping=opts_data["column_mapping"],
                              profile_parts=opts_data["profile_sections"],
                              pretty_print=opts_data["pretty_print"])

    runner = ProfileRunner(ProfileRunnerOptions(
        reference_data_path=reference,
        reference_data_options=DataOptions(date_column=opts.data_format.date_column,
                                           separator=opts.data_format.separator,
                                           header=opts.data_format.header),
        production_data_path=current,
        production_data_options=DataOptions(date_column=opts.data_format.date_column,
                                            separator=opts.data_format.separator,
                                            header=opts.data_format.header),
        profile_parts=opts.profile_parts,
        column_mapping=opts.column_mapping,
        output_path=os.path.join(output_path, report_name),
        pretty_print=opts.pretty_print,
    ))
    runner.run()


def help_handler(**_kv):
    parser.print_help()
    exit(1)


def _add_default_parameters(configurable_parser, default_output_name: str):
    configurable_parser.add_argument("--reference", dest="reference", required=True, help="Path to reference data")
    configurable_parser.add_argument("--current", dest="current", help="Path to current data")
    configurable_parser.add_argument("--output_path", dest="output_path", required=True, help="Path to store report")
    configurable_parser.add_argument("--report_name", dest="report_name", default=default_output_name, help="Report name")
    configurable_parser.add_argument("--config", dest="config", required=True, help="Path to configuration")


parser = argparse.ArgumentParser()

parsers = parser.add_subparsers()
parser.set_defaults(handler=help_handler)
calculate_parser = parsers.add_parser("calculate")
calc_subparsers = calculate_parser.add_subparsers()
profile_parser = calc_subparsers.add_parser("profile")
_add_default_parameters(profile_parser, "profile")
profile_parser.set_defaults(handler=calculate_profile)
dashboard_parser = calc_subparsers.add_parser("dashboard")
_add_default_parameters(dashboard_parser, "dashboard")
dashboard_parser.set_defaults(handler=calculate_dashboard)

parsed = parser.parse_args(sys.argv[1:])

parsed.handler(**parsed.__dict__)
