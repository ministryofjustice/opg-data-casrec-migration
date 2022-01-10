#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ "${RUN_API_TESTS}" == "True" ]
then
  cd "${DIR}/api_tests/light_touch_tests"
  echo "== Running Light Touch API tests =="
  python3 app.py
  echo $?
  echo "== Finished Light Touch API tests =="
fi