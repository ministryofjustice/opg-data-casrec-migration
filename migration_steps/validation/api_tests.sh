#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "${DIR}/api_tests"
echo "== Installing requirements for API tests =="
pip3 install -r requirements.txt > /dev/null
echo "== Running API tests =="
pytest -s .
echo $?
echo "== Finished API tests =="
