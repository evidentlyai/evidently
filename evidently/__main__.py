import argparse
import json
import os
import sys

from evidently.runner.runner import Runner, RunnerOptions, DataOptions

parser = argparse.ArgumentParser()
parser.add_argument("--reference", dest="reference", required=True, help="Path to reference data")
parser.add_argument("--reference-opts", dest="reference_opts", required=True, help="Path to reference data")
parser.add_argument("--output", dest="output", required=True, help="Path to store HTML report")
parser.add_argument("--production", dest="production", help="Path to production data")
parser.add_argument("--production-opts", dest="production_opts", help="Path to production data")
parser.add_argument("--report_name", dest="report_name", default="report", help="Report name")


parsed = parser.parse_args(sys.argv[1:])
if parsed.reference_opts:
    with open(parsed.reference_opts) as rof:
        ref_opts = json.load(rof)
else:
    ref_opts = None

if parsed.production_opts:
    with open(parsed.production_opts) as pof:
        prod_opts = json.load(pof)
else:
    prod_opts = None


runner = Runner(RunnerOptions(
    reference_data_path=parsed.reference,
    reference_data_options=DataOptions(**ref_opts) if ref_opts else DataOptions(),
    production_data_path=parsed.production,
    production_data_options=DataOptions(**prod_opts) if prod_opts else DataOptions(),
    output_path=os.path.join(parsed.output, parsed.report_name + ".html"),
))
runner.run()
