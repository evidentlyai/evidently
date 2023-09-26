#!/usr/bin/env bash
set -e

virtualenv venv
source ./venv/bin/activate
pip install -e ".[dev]"
