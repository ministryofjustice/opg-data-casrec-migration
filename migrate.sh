#!/bin/bash
set -e
# Docker compose file for circle build
docker build base_image -t opg_casrec_migration_base_image:latest
docker-compose up --no-deps -d casrec_db localstack
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
docker rm casrec_load_1 &>/dev/null || echo "casrec_load_1 does not exist. This is OK"
docker rm casrec_load_2 &>/dev/null || echo "casrec_load_2 does not exist. This is OK"
docker rm casrec_load_3 &>/dev/null || echo "casrec_load_3 does not exist. This is OK"
docker rm casrec_load_4 &>/dev/null || echo "casrec_load_4 does not exist. This is OK"
docker-compose run --rm --name casrec_load_1 load_casrec python3 app.py >> docker_load.log &
P1=$!
sleep 1
docker-compose run --rm --name casrec_load_2 load_casrec python3 app.py >> docker_load.log &
P2=$!
sleep 1
docker-compose run --rm --name casrec_load_3 load_casrec python3 app.py >> docker_load.log &
P3=$!
sleep 1
docker-compose run --rm --name casrec_load_4 load_casrec python3 app.py >> docker_load.log &
P4=$!
wait $P1 $P2 $P3 $P4
cat docker_load.log
rm docker_load.log
docker-compose run --rm transform_casrec python3 app.py --clear=True
docker-compose run --rm integration integration/integration.sh
docker-compose run --rm load_to_target python3 app.py
