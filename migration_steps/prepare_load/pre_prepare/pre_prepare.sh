#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ -f "${DIR}/../../.env" ]
then
  source "${DIR}/../../.env"
else
  echo "no env file, using normal env vars"
fi

mkdir -p ${DIR}/sql/schemas
export PGPASSWORD=${DB_PASSWORD}
pg_dump -U ${DB_USER} -n etl2 -h ${DB_HOST} -p ${DB_PORT} ${DB_NAME} > "${DIR}/sql/schemas/etl2.sql"
cat "${DIR}/sql/schemas/etl2.sql" | sed 's/etl2/pre_migrate/' | sed 's/CREATE SCHEMA pre_migrate;/DROP SCHEMA IF EXISTS pre_migrate CASCADE; CREATE SCHEMA pre_migrate;/' > "${DIR}/sql/schemas/pre_migrate.sql"
psql -U ${DB_USER} -h ${DB_HOST} -p ${DB_PORT} ${DB_NAME} < "${DIR}/sql/schemas/pre_migrate.sql"
psql -U ${DB_USER} -h ${DB_HOST} -p ${DB_PORT} ${DB_NAME} < "${DIR}/sql/sirius_id_cols.sql"
