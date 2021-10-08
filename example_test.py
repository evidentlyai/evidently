import os
import sys

excludes = ['bicycle_demand_monitoring.py']


if __name__ == '__main__':
    failed_scripts = []

    for entry, _, files in os.walk("example_scripts"):
        for file in files:
            if file.endswith('.py'):
                if file in excludes:
                    continue
                result = os.system(f"python example_scripts/{file}")
                if result != 0:
                    failed_scripts.append((file, result))

    if failed_scripts:
        for fail, errcode in failed_scripts:
            print(f"Script {fail} failed with error code {errcode}", file=sys.stderr)
        sys.exit(len(failed_scripts))
