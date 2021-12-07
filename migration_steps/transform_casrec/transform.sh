#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 "${DIR}/transform/app/app.py"  "$@" --clear=True
python3 "${DIR}/additional_data/app/app.py"  --clear=True

