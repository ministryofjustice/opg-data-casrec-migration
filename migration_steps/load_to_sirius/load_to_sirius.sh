#!/bin/bash
set -e
# envcheck - leaving this here to make absolutely sure we can't change prod without noticing
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
