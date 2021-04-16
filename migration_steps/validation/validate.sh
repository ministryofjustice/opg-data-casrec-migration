#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ "${ENVIRONMENT}" == "local" || "${ENVIRONMENT}" == "development" ]]
then
  python3 "${DIR}/api_test_data_s3_upload/app/app.py"
fi

python3 "${DIR}/validate_db/app/app.py" "$@"
python3 "${DIR}/post_migration_tests/app/app.py" -vv

if [ "${RUN_API_TESTS}" == "True" ]
then
  cd "${DIR}/api_tests"
  echo "== Installing requirements for API tests =="
  pip3 install -r requirements.txt > /dev/null
  echo "== Running API tests =="
  pytest -s .
fi
