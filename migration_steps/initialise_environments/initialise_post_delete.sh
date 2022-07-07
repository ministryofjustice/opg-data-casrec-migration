#!/bin/bash
set -e
while getopts i: option
do
  case "${option}"
  in
    i) SCHEMAS=${OPTARG};;
    *) echo "usage: $0 [-i]" >&2
           exit 1 ;;
  esac
done

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 "${DIR}/delete_existing_data/app.py" --pre_delete_setup=true
python3 "${DIR}/counts_verification/app.py" --stage=pre_delete
python3 "${DIR}/delete_existing_data/app.py" --pre_delete_setup=false
python3 "${DIR}/counts_verification/app.py" --stage=post_delete
python3 "${DIR}/create_stage_schema/app/app.py"
python3 "${DIR}/counts_verification/app.py" --stage=pre_migration

# envcheck - skeleton data should ONLY be created on dev databases
if [ "${ENVIRONMENT}" == "local" ] \
  || [ "${ENVIRONMENT}" == "development" ]
  then
  python3 "${DIR}/create_skeleton_data/app/app.py"
else
  echo "create_skeleton_data should not run on ${ENVIRONMENT}"
fi
