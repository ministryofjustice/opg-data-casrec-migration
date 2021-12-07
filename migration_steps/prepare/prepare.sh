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

# envcheck - linked skeleton data should NOT be deleted on prod
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

python3 "${DIR}/prepare_source/app/app.py" --preserve_schemas="${SCHEMAS}"
python3 "${DIR}/create_stage_schema/app/app.py"


# envcheck - skeleton data should ONLY be created on dev databases
if [ "${ENVIRONMENT}" == "local" ] \
  || [ "${ENVIRONMENT}" == "development" ]
  then
  python3 "${DIR}/create_skeleton_data/app/app.py"
else
  echo "create_skeleton_data should not run on ${ENVIRONMENT}"
fi
