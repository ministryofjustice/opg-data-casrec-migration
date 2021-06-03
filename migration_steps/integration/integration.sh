#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#python3 "${DIR}/schema_setup/app/app.py"
#python3 "${DIR}/fixtures/app/app.py"
python3 "${DIR}/reindex_ids/app/app.py" "$@" --clear=True
python3 "${DIR}/business_rules/app/app.py"  "$@" --clear=True
python3 "${DIR}/load_to_staging/app/app.py"  "$@" --clear=True

