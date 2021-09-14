#!/bin/bash
set -e
# todo IN-908
if [ "${ENVIRONMENT}" == "local" ] \
  || [ "${ENVIRONMENT}" == "development" ] \
  || [ "${ENVIRONMENT}" == "preproduction" ] \
  || [ "${ENVIRONMENT}" == "preqa" ] \
  || [ "${ENVIRONMENT}" == "qa" ]
  then
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
  python3 "${DIR}/move_data/app.py"
  python3 "${DIR}/post_migration_db_tasks/app.py"
else
  echo "This job should not run on ${ENVIRONMENT}"
fi
