#!/bin/bash
set -e
# Docker compose file for circle build
docker build base_image -t opg_casrec_migration_base_image:latest
docker-compose up --no-deps -d casrec_db localstack postgres-sirius
docker-compose run --rm wait-for-it -address postgres-sirius:5432 --timeout=30 -debug
docker-compose run --rm wait-for-it -address casrec_db:5432 --timeout=30 -debug
docker-compose up --no-deps -d postgres-sirius-restore
if [ "${CI}" != "true" ]
then
  docker-compose run --rm load_s3 python3 load_s3_local.py
else
  RESTORE_DOCKER_ID=$(docker ps -a | grep sirius-restore | awk {'print $1'})
  docker cp db-snapshots/api.backup ${RESTORE_DOCKER_ID}:/db-snapshots/api.backup
  docker-compose up --no-deps -d postgres-sirius-restore
fi
docker-compose run --rm prepare prepare/prepare.sh
docker-compose run --rm transform_casrec python3 app.py --clear=True
docker-compose run --rm integration integration/integration.sh
docker-compose run --rm load_to_target python3 app.py
