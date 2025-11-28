#!/bin/bash
set -e

SCHEMA="evidently-openapi-schema.yml"
UI_DTS_PREFIX="ui/packages/evidently-ui-lib/src/api/types"

python src/evidently/utils/schema.py $SCHEMA
node .github/scripts/support-litestar-openapi-tuples.mjs $SCHEMA
npx openapi-typescript@6 ./$SCHEMA -o $UI_DTS_PREFIX/endpoints.d.ts
