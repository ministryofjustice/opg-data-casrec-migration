#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 "${DIR}/move_data/app.py"
python3 "${DIR}/post_migration_db_tasks/app.py"