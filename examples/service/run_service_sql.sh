#!/bin/bash
# Run Evidently UI Service with SQL Storage

set -e
evidently ui --conf-path sql_config.yaml "$@"
