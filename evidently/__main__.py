import argparse
import json
import os
import sys
from typing import Dict, List

from dataclasses import dataclass

from evidently.runner.runner import Runner, RunnerOptions, DataOptions


@dataclass
class DataFormatOptions:
    header: bool
    separator: str
    date_column: str


@dataclass
class AnalyzeOptions:
    data_format: DataFormatOptions
    column_mapping: Dict[str, str]
    dashboard_tabs: List[str]


def analyze_handler(config: str, reference: str, current: str, output: str, report_name: str, **kv):
    with open(config) as f_config:
        opts_data = json.load(f_config)
        opts = AnalyzeOptions(data_format=DataFormatOptions(**opts_data["data_format"]),
                              column_mapping=opts_data["column_mapping"],
                              dashboard_tabs=opts_data["dashboard_tabs"])

    runner = Runner(RunnerOptions(
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
        output_path=os.path.join(output, report_name + ".html"),
    ))
    runner.run()


def help_handler(**kv):
    parser.print_help()
    exit(1)


parser = argparse.ArgumentParser()

parsers = parser.add_subparsers()
parser.set_defaults(handler=help_handler)
analyze_parser = parsers.add_parser("analyze")
analyze_parser.add_argument("--config", dest="config", required=True, help="Path to analyze configuration")
analyze_parser.add_argument("--reference", dest="reference", required=True, help="Path to reference data")
analyze_parser.add_argument("--current", dest="current", help="Path to current data")
analyze_parser.add_argument("--output", dest="output", required=True, help="Path to store HTML report")
analyze_parser.add_argument("--report_name", dest="report_name", default="report", help="Report name")
analyze_parser.set_defaults(handler=analyze_handler)

parsed = parser.parse_args(sys.argv[1:])

parsed.handler(**parsed.__dict__)
