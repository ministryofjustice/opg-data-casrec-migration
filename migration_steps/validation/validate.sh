#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 "${DIR}/validate_db/app/app.py" "$@"
python3 "${DIR}/post_migration_tests/app/app.py"
