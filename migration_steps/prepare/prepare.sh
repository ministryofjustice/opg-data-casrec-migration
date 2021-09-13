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

python3 "${DIR}/prepare_target/app/app.py" --preserve_schemas="${SCHEMAS}"

if [ "${ENVIRONMENT}" == "local" ] \
  || [ "${ENVIRONMENT}" == "development" ] \
  || [ "${ENVIRONMENT}" == "preproduction" ] \
  || [ "${ENVIRONMENT}" == "preqa" ] \
  || [ "${ENVIRONMENT}" == "qa" ]
  then
  python3 "${DIR}/delete_existing_data/app.py"
else
  echo "delete_existing_data should not run on ${ENVIRONMENT}"
fi

if [ "${ENVIRONMENT}" == "local" ] \
  || [ "${ENVIRONMENT}" == "development" ] \
  || [ "${ENVIRONMENT}" == "preproduction" ] \
  || [ "${ENVIRONMENT}" == "preqa" ] \
  || [ "${ENVIRONMENT}" == "qa" ]
  then
  python3 "${DIR}/create_stage_schema/app/app.py"
else
  echo "create_stage_schema should not run on ${ENVIRONMENT}"
fi

if [ "${ENVIRONMENT}" == "local" ] \
  || [ "${ENVIRONMENT}" == "development" ]
  then
  python3 "${DIR}/create_skeleton_data/app/app.py"
else
  echo "create_skeleton_data should not run on ${ENVIRONMENT}"
fi
