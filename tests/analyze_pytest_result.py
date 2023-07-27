#!/usr/bin/env python3
import json
import sys
from collections import defaultdict

COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_END = "\033[0m"


if __name__ == "__main__":
    pytest_report_fpath = "pytest_result.jsonl" if len(sys.argv) < 2 else sys.argv[1]

    current_nodeid = None
    all_nodeid = set()
    driver_usage_warnings = defaultdict(list)

    for line in open(pytest_report_fpath):
        jsonline = json.loads(line.rstrip())
        if "nodeid" in jsonline and jsonline["$report_type"] != "CollectReport":
            # TODO: extract Metric name from nodeid
            current_nodeid = jsonline["nodeid"]
            all_nodeid.add(current_nodeid)

        if "PandasAPIOnSparkAdviceWarning" == jsonline.get("category"):
            driver_usage_warnings[current_nodeid].append(jsonline["message"])

    for nodeid in sorted(all_nodeid):
        warnings = driver_usage_warnings[nodeid]
        if warnings:
            print(f"{COLOR_RED}FAILED{COLOR_END} {nodeid}")
            for warning in warnings:
                print(f"- PandasAPIOnSparkAdviceWarning: {warning}")
        else:
            print(f"{COLOR_GREEN}PASSED{COLOR_END} {nodeid}")
