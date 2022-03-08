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

python3 "${DIR}/initialise_source/app/app.py" --preserve_schemas="${SCHEMAS}"
python3 "${DIR}/counts_verification/app.py" --stage=pre_delete