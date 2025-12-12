#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

## Start the live server
npx live-server $SCRIPT_DIR/dist &

## Start the nodemon process to generate the documentation
npx nodemon -e 'py' --exec "$SCRIPT_DIR/generate.py --local-source-code"
