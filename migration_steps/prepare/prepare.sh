#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 "${DIR}/prepare_target/app/app.py"
python3 "${DIR}/create_stage_schema/app/app.py"
