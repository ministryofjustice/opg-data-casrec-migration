#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 "${DIR}/filter_data/app/app.py"
python3 "${DIR}/load_casrec_fixtures/app/app.py"
