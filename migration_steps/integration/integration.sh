#!/bin/bash
set -e

if [ "${ENVIRONMENT}" == "local" ] \
  || [ "${ENVIRONMENT}" == "development" ] \
  || [ "${ENVIRONMENT}" == "preproduction" ] \
  || [ "${ENVIRONMENT}" == "qa" ]
  then

  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

  #python3 "${DIR}/schema_setup/app/app.py"
  #python3 "${DIR}/fixtures/app/app.py"
  python3 "${DIR}/reindex_ids/app/app.py" "$@" --clear=True
  python3 "${DIR}/business_rules/app/app.py"  "$@" --clear=True
  python3 "${DIR}/load_to_staging/app/app.py"  "$@" --clear=True
else
  echo "This job should not run on ${ENVIRONMENT}"
fi
