#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# envcheck - not sure where this should run so leaving it alone
if [[ "${ENVIRONMENT}" == "local" || "${ENVIRONMENT}" == "development" ]]
then
  if [ "${RUN_API_TESTS}" == "True" ]
  then
    cd "${DIR}/api_tests/functional_tests"
    echo "== Running API tests =="
    python3 app.py
    echo $?
    echo "== Finished API tests =="
  fi
fi
