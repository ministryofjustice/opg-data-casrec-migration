#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 "${DIR}/filter_data/app/app.py"

if [ "${ENVIRONMENT}" == "local" ] \
  || [ "${ENVIRONMENT}" == "development" ]
  then
  python3 "${DIR}/load_casrec_fixtures/app/app.py"
else
  echo "load_casrec_fixtures should not run on ${ENVIRONMENT}"
fi

python3 "${DIR}/counts_verification/count_existing_pc1.py"
python3 "${DIR}/counts_verification/count_casrec_source.py"
