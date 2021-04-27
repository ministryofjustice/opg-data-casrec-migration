#!/bin/bash
set -e

RELOAD="y"
RESYNC="y"
SKIP_LOAD="false"
PRESERVE_SCHEMAS=""
GENERATE_DOCS=false

if [ "${CI}" != "true" ]
then
  # Skip this if sure the data in casrec_csv schema is correct)
  read -p "Rebuild casrec_csv schema from .csv files? (y/n) [n]: " RELOAD
  RELOAD=${RELOAD:-n}
  echo $RELOAD
  if [ "${RELOAD}" == "y" ]
  then
      read -p "Sync local .csv files from S3? (y/n) [n]: " RESYNC
      RESYNC=${RESYNC:-n}
      echo $RESYNC
  else
    PRESERVE_SCHEMAS="casrec_csv"
    SKIP_LOAD="true"
  fi
  fi
fi

START_TIME=`date +%s`

# Docker compose file for circle build
docker build base_image -t opg_casrec_migration_base_image:latest
docker-compose up --no-deps -d casrec_db localstack postgres-sirius
docker-compose run --rm wait-for-it -address postgres-sirius:5432 --timeout=30 -debug
docker-compose run --rm wait-for-it -address casrec_db:5432 --timeout=30 -debug
docker-compose up --no-deps -d postgres-sirius-restore

if [ "${RELOAD}" == "y" ]
then
  if [ "${CI}" != "true" ]
  then
      if [ ${RESYNC} == "y" ]
      then
        aws-vault exec identity -- docker-compose run --rm load_s3 ./local_s3.sh -s TRUE
      else
        docker-compose run --rm load_s3 ./local_s3.sh
      fi
  else
    RESTORE_DOCKER_ID=$(docker ps -a | grep sirius-restore | awk {'print $1'})
    docker cp sirius_db/db_snapshots/api.backup ${RESTORE_DOCKER_ID}:/db_snapshots/api.backup
    docker-compose up --no-deps -d postgres-sirius-restore
  fi
fi
docker-compose run --rm prepare prepare/prepare.sh -i "${PRESERVE_SCHEMAS}"
docker rm casrec_load_1 &>/dev/null || echo "casrec_load_1 does not exist. This is OK"
docker rm casrec_load_2 &>/dev/null || echo "casrec_load_2 does not exist. This is OK"
docker rm casrec_load_3 &>/dev/null || echo "casrec_load_3 does not exist. This is OK"
docker rm casrec_load_4 &>/dev/null || echo "casrec_load_4 does not exist. This is OK"
docker-compose run --rm --name casrec_load_1 load_casrec python3 app.py --delay=0 --skip_load="${SKIP_LOAD}" >> docker_load.log &
P1=$!
docker-compose run --rm --name casrec_load_2 load_casrec python3 app.py --delay=2 --skip_load="${SKIP_LOAD}" >> docker_load.log &
P2=$!
docker-compose run --rm --name casrec_load_3 load_casrec python3 app.py --delay=3 --skip_load="${SKIP_LOAD}" >> docker_load.log &
P3=$!
docker-compose run --rm --name casrec_load_4 load_casrec python3 app.py --delay=4 --skip_load="${SKIP_LOAD}" >> docker_load.log &
P4=$!
wait $P1 $P2 $P3 $P4
cat docker_load.log
rm docker_load.log
echo "=== Step 1 - Transform ==="
docker-compose run --rm transform_casrec transform_casrec/transform.sh --clear=True
echo "=== Step 2 - Integrate with Sirius ==="
docker-compose run --rm integration integration/integration.sh
echo "=== Step 3 - Validate Staging ==="
docker-compose run --rm validation python3 /validation/validate_db/app/app.py --staging
echo "=== Step 4 - Load to Sirius ==="
docker-compose run --rm load_to_target  load_to_sirius/load_to_sirius.sh
echo "=== Step 5 - Validate Sirius ==="
docker-compose run --rm validation validation/validate.sh "$@"
if [ "${GENERATE_DOCS}" == "true" ]
  then
  echo "=== Generating new docs for Github Pages ==="
  python3 docs/create_report/run.py
fi
echo "=== FINISHED! ==="

END_TIME=`date +%s`
RUN_TIME=$((END_TIME-START_TIME))

echo "Total Run Time: ${RUN_TIME} seconds"