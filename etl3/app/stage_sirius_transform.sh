#!/bin/bash
export PGPASSWORD=${DB_PASSWORD}
pg_dump -U ${DB_USER} -n etl2 -h ${DB_HOST} ${DB_NAME} > ./etl2.sql
cat ./etl2.sql | sed 's/etl2/etl3/' | sed 's/CREATE SCHEMA etl3;/DROP SCHEMA IF EXISTS etl3 CASCADE; CREATE SCHEMA etl3;/' > ./etl3.sql
psql -U ${DB_USER} -h ${DB_HOST} ${DB_NAME} < ./etl3.sql
psql -U ${DB_USER} -h ${DB_HOST} ${DB_NAME} < ./sql/sirius_id_cols.sql
python3 fixtures.py
python3 app.py
