#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ "${ENVIRONMENT}" == "local" ]]
then
  python3 "${DIR}/api_test_data_s3_upload/app/app.py"
fi

cd "${DIR}/api_tests"
echo "== Running API tests =="
python3 app.py
echo $?
echo "== Finished API tests =="
