import argparse
import json
import logging
import os
import sys
from typing import Any
from typing import Dict

import yaml
from dataclasses import dataclass

from evidently._config import TELEMETRY_ADDRESS
from evidently._config import TELEMETRY_ENABLED
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.runner.dashboard_runner import DashboardRunner
from evidently.runner.dashboard_runner import DashboardRunnerOptions
from evidently.runner.loader import SamplingOptions
from evidently.runner.profile_runner import ProfileRunner
from evidently.runner.profile_runner import ProfileRunnerOptions
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


def calculate_dashboard(
    config: str, reference: str, current: str, output_path: str, report_name: str, **_kv
):
    usage = dict(type="dashboard")

    opts_data = __load_config_file(config)

    sampling = __get_not_none(opts_data, "sampling", {})
    ref_sampling = __get_not_none(sampling, "reference", {})
    cur_sampling = __get_not_none(sampling, "current", {})

    usage["tabs"] = opts_data["dashboard_tabs"]
    usage["sampling"] = sampling
    opts = DashboardOptions(
        data_format=DataFormatOptions(**opts_data["data_format"]),
        column_mapping=opts_data["column_mapping"],
        dashboard_tabs=opts_data["dashboard_tabs"],
        sampling=Sampling(
            reference=SamplingOptions(**ref_sampling),
            current=SamplingOptions(**cur_sampling),
        ),
    )

    runner = DashboardRunner(
        DashboardRunnerOptions(
            reference_data_path=reference,
            reference_data_options=DataOptions(
                date_column=opts.data_format.date_column,
                separator=opts.data_format.separator,
                header=opts.data_format.header,
            ),
            reference_data_sampling=opts.sampling.reference,
            current_data_path=current,
            current_data_options=DataOptions(
                date_column=opts.data_format.date_column,
                separator=opts.data_format.separator,
                header=opts.data_format.header,
            ),
            current_data_sampling=opts.sampling.current,
            dashboard_tabs=opts.dashboard_tabs,
            options=parse_options(opts_data["options"]),
            column_mapping=ColumnMapping(**opts.column_mapping),
            output_path=os.path.join(output_path, report_name),
        )
    )
    runner.run()
    if TELEMETRY_ENABLED:
        sender = TelemetrySender(TELEMETRY_ADDRESS)
        sender.send(usage)


def calculate_profile(
    config: str, reference: str, current: str, output_path: str, report_name: str, **_kv
):
    usage = dict(type="profile")

    opts_data = __load_config_file(config)

    sampling = __get_not_none(opts_data, "sampling", {})
    ref_sampling = __get_not_none(sampling, "reference", {})
    cur_sampling = __get_not_none(sampling, "current", {})
    usage["parts"] = opts_data["profile_sections"]
    usage["sampling"] = sampling
    opts = ProfileOptions(
        data_format=DataFormatOptions(**opts_data["data_format"]),
        column_mapping=opts_data["column_mapping"],
        profile_parts=opts_data["profile_sections"],
        pretty_print=opts_data["pretty_print"],
        sampling=Sampling(
            reference=SamplingOptions(**ref_sampling),
            current=SamplingOptions(**cur_sampling),
        ),
    )

    runner = ProfileRunner(
        ProfileRunnerOptions(
            reference_data_path=reference,
            reference_data_options=DataOptions(
                date_column=opts.data_format.date_column,
                separator=opts.data_format.separator,
                header=opts.data_format.header,
            ),
            reference_data_sampling=opts.sampling.reference,
            current_data_path=current,
            current_data_options=DataOptions(
                date_column=opts.data_format.date_column,
                separator=opts.data_format.separator,
                header=opts.data_format.header,
            ),
            current_data_sampling=opts.sampling.current,
            profile_parts=opts.profile_parts,
            column_mapping=ColumnMapping(**opts.column_mapping),
            options=parse_options(opts_data.get("options", None)),
            output_path=os.path.join(output_path, report_name),
            pretty_print=opts.pretty_print,
        )
    )
    runner.run()
    if TELEMETRY_ENABLED:
        sender = TelemetrySender(TELEMETRY_ADDRESS)
        sender.send(usage)


def help_handler(**_kv):
    parser.print_help()
    sys.exit(1)


def _add_default_parameters(configurable_parser, default_output_name: str):
    configurable_parser.add_argument(
        "--reference", dest="reference", required=True, help="Path to reference data"
    )
    configurable_parser.add_argument(
        "--current", dest="current", help="Path to current data"
    )
    configurable_parser.add_argument(
        "--output_path", dest="output_path", required=True, help="Path to store report"
    )
    configurable_parser.add_argument(
        "--report_name",
        dest="report_name",
        default=default_output_name,
        help="Report name",
    )
    configurable_parser.add_argument(
        "--config", dest="config", required=True, help="Path to configuration"
    )


logging.basicConfig(level=logging.INFO)

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
