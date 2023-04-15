import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Any
from typing import Dict

import yaml

from evidently._config import TELEMETRY_ADDRESS
from evidently._config import TELEMETRY_ENABLED
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.runner.loader import SamplingOptions
from evidently.runner.runner import DataOptions
from evidently.runner.runner import parse_options
from evidently.telemetry import TelemetrySender


@dataclass
class DataFormatOptions:
    header: bool
    separator: str
    date_column: str


@dataclass
class Sampling:
    reference: SamplingOptions
    current: SamplingOptions


@dataclass
class CalculateOptions:
    data_format: DataFormatOptions
    column_mapping: Dict[str, Any]
    sampling: Sampling


@dataclass
class DashboardOptions(CalculateOptions):
    dashboard_tabs: Dict[str, Dict[str, object]]


@dataclass
class ProfileOptions(CalculateOptions):
    profile_parts: Dict[str, Dict[str, str]]
    pretty_print: bool = False


def __get_not_none(src: Dict, key, default):
    return default if src.get(key, None) is None else src.get(key)


def __load_config_file(config_file: str):
    with open(config_file, encoding="utf-8") as f_config:
        if config_file.endswith(".yaml") or config_file.endswith(".yml"):
            opts_data = yaml.load(f_config, Loader=yaml.SafeLoader)
        elif config_file.endswith(".json"):
            opts_data = json.load(f_config)
        else:
            raise Exception(f"config .{config_file.split('.')[-1]} not supported")
    return opts_data


def help_handler(**_kv):
    parser.print_help()
    sys.exit(1)


def _add_default_parameters(configurable_parser, default_output_name: str):
    configurable_parser.add_argument("--reference", dest="reference", required=True, help="Path to reference data")
    configurable_parser.add_argument("--current", dest="current", help="Path to current data")
    configurable_parser.add_argument("--output_path", dest="output_path", required=True, help="Path to store report")
    configurable_parser.add_argument(
        "--report_name", dest="report_name", default=default_output_name, help="Report name"
    )
    configurable_parser.add_argument("--config", dest="config", required=True, help="Path to configuration")


logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()

parsers = parser.add_subparsers()
parser.set_defaults(handler=help_handler)
calculate_parser = parsers.add_parser("calculate")
calc_subparsers = calculate_parser.add_subparsers()


parsed = parser.parse_args(sys.argv[1:])

parsed.handler(**parsed.__dict__)
