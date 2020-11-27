#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 "${DIR}/prepare_target/app/app.py"
"${DIR}/pre_prepare/pre_prepare.sh"
python3 "${DIR}/fixtures/app/app.py"
python3 "${DIR}/merge_target_ids/app/app.py"
