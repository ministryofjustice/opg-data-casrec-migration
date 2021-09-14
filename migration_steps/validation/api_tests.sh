#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# todo IN-908
if [[ "${ENVIRONMENT}" == "local" || "${ENVIRONMENT}" == "development" ]]
then
  python3 "${DIR}/api_test_data_s3_upload/app/app.py"
fi

if [ "${RUN_API_TESTS}" == "True" ]
then
  cd "${DIR}/api_tests/response_tests"
  echo "== Running API tests =="
  python3 app.py
  echo $?
  echo "== Finished API tests =="
fi
