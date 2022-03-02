#!/bin/bash
set -e

REBUILD_CASREC_CSV_SCHEMA="y"
SYNC_CASREC_CSVS="y"
SKIP_LOAD="false"
PRESERVE_SCHEMAS=""
CORREFS=""
GENERATE_DOCS="false"
FULL_SIRIUS_APP="n"
COMPOSE_ARGS=""
MAPPING_SHA=$(find migration_steps/shared/mapping_spreadsheet/ -type f -print0 | sort -z | xargs -0 sha1sum | sha1sum | awk '{print $1}')
S3_HOST_AND_PORT=localstack:4572

if [ "${CI}" != "true" ]
then
  # Skip this if sure the data in casrec_csv schema is correct)
  read -rp "Rebuild casrec_csv schema from .csv files? (y/n) [n]: " REBUILD_CASREC_CSV_SCHEMA
  REBUILD_CASREC_CSV_SCHEMA=${REBUILD_CASREC_CSV_SCHEMA:-n}
  echo "${REBUILD_CASREC_CSV_SCHEMA}"
  if [ "${REBUILD_CASREC_CSV_SCHEMA}" == "y" ]
  then
      read -rp "Sync local .csv files from S3? (y/n) [n]: " SYNC_CASREC_CSVS
      SYNC_CASREC_CSVS=${SYNC_CASREC_CSVS:-n}
      echo "${SYNC_CASREC_CSVS}"
  else
    PRESERVE_SCHEMAS="casrec_csv"
    SKIP_LOAD="true"
  fi

  read -rp "Migrate specific Correfs? (comma-separated list) [All]: " CORREFS
  if [ "${CORREFS}" == "" ]
  then
      echo "Migrating ALL Correfs"
  else
      echo "Migrating Correfs ${CORREFS} only"
  fi

  read -rp "Migrate to full sirius app? (y/n) [n]: " FULL_SIRIUS_APP
  FULL_SIRIUS_APP=${FULL_SIRIUS_APP:-n}
  echo "${FULL_SIRIUS_APP}"
  if [ "${FULL_SIRIUS_APP}" == "y" ]
  then
      S3_HOST_AND_PORT=localstack:4598
      COMPOSE_ARGS="-f docker-compose.sirius.yml -f docker-compose.override.yml"
  fi

  if [[ "$(cat mappings/spreadsheet_sha | awk '{print $1}')" == "$MAPPING_SHA" ]]
  then
    echo "Mapping spreadsheets unchanged"
  else
    echo "Difference in mapping spreadsheets detected, running mapping generation"
    docker-compose run --rm generate python3 app/app.py
    find migration_steps/shared/mapping_spreadsheet/ -type f -print0 | sort -z | xargs -0 sha1sum | sha1sum | awk '{print $1}' > mappings/spreadsheet_sha
  fi
fi

START_TIME=$(date +%s)

# Docker compose file for circle build
docker-compose ${COMPOSE_ARGS} up --no-deps -d casrec_db localstack
docker build base_image -t opg_casrec_migration_base_image:latest

if [ "${FULL_SIRIUS_APP}" == "n" ]
then
  docker-compose ${COMPOSE_ARGS} up --no-deps -d postgres-sirius
  docker-compose ${COMPOSE_ARGS} run --rm wait-for-it -address postgres-sirius:5432 --timeout=30 -debug
  docker-compose ${COMPOSE_ARGS} up --no-deps -d postgres-sirius-restore
fi
docker-compose ${COMPOSE_ARGS} run --rm wait-for-it -address casrec_db:5432 --timeout=30 -debug
docker-compose ${COMPOSE_ARGS} run --rm wait-for-it -address $S3_HOST_AND_PORT --timeout=30 -debug

if [ "${REBUILD_CASREC_CSV_SCHEMA}" == "y" ]
then
  if [ "${CI}" != "true" ]
  then
      if [ ${SYNC_CASREC_CSVS} == "y" ]
      then
        aws-vault exec identity -- docker-compose ${COMPOSE_ARGS} run --rm load_s3 ./local_s3.sh -s TRUE
      else
        docker-compose ${COMPOSE_ARGS} run --rm load_s3 ./local_s3.sh
      fi
  else
    RESTORE_DOCKER_ID=$(docker ps -a | grep sirius-restore | awk {'print $1'})
    docker cp sirius_db/db_snapshots/api.backup "${RESTORE_DOCKER_ID}":/db_snapshots/api.backup
    docker-compose up --no-deps -d postgres-sirius-restore
  fi
fi

docker-compose ${COMPOSE_ARGS} run --rm initialise initialise_environments/initialise_pre_delete.sh -i "${PRESERVE_SCHEMAS}"
docker-compose ${COMPOSE_ARGS} run --rm initialise initialise_environments/initialise_post_delete.sh -i "${PRESERVE_SCHEMAS}"

if [ "${REBUILD_CASREC_CSV_SCHEMA}" == "y" ]
then
  docker rm casrec_load_1 &>/dev/null || echo "casrec_load_1 does not exist. This is OK"
  docker rm casrec_load_2 &>/dev/null || echo "casrec_load_2 does not exist. This is OK"
  docker rm casrec_load_3 &>/dev/null || echo "casrec_load_3 does not exist. This is OK"
  docker rm casrec_load_4 &>/dev/null || echo "casrec_load_4 does not exist. This is OK"
  docker-compose ${COMPOSE_ARGS} run --rm --name casrec_load_1 load_casrec python3 load_casrec/app/app.py -p "1" -t "4" >> docker_load.log &
  P1=$!
  docker-compose ${COMPOSE_ARGS} run --rm --name casrec_load_2 load_casrec python3 load_casrec/app/app.py -p "2" -t "4" >> docker_load.log &
  P2=$!
  docker-compose ${COMPOSE_ARGS} run --rm --name casrec_load_3 load_casrec python3 load_casrec/app/app.py -p "3" -t "4" >> docker_load.log &
  P3=$!
  docker-compose ${COMPOSE_ARGS} run --rm --name casrec_load_4 load_casrec python3 load_casrec/app/app.py -p "4" -t "4" >> docker_load.log &
  P4=$!
  wait $P1 $P2 $P3 $P4
  cat docker_load.log
  rm docker_load.log
fi
echo "=== Step 0 - Filter data ==="
docker-compose ${COMPOSE_ARGS} run --rm initialise prepare_source_data/prepare_source_data.sh --correfs="${CORREFS}"
echo "=== Step 1 - Transform ==="
docker-compose ${COMPOSE_ARGS} run --rm transform_casrec transform_casrec/transform.sh --correfs="${CORREFS}"
echo "=== Step 2 - Integrate with Sirius ==="
docker-compose ${COMPOSE_ARGS} run --rm integration integration/integration.sh --correfs="${CORREFS}"
echo "=== Step 3 - Validate Staging ==="
docker-compose ${COMPOSE_ARGS} run --rm validation python3 /validation/validate_db/app/app.py --correfs="${CORREFS}" --staging
echo "=== Step 4 - Load to Sirius ==="
docker-compose ${COMPOSE_ARGS} run --rm load_to_target load_to_sirius/load_to_sirius.sh
echo "=== Step 5 - Validate Sirius ==="
docker-compose ${COMPOSE_ARGS} run --rm validation validation/validate.sh --correfs="${CORREFS}"
echo "=== Step 6 - API Tests ==="
docker-compose ${COMPOSE_ARGS} run --rm validation validation/response_api_tests.sh
echo "=== Step 7 - Light Touch API Tests ==="
docker-compose ${COMPOSE_ARGS} run --rm validation validation/light_touch_api_tests.sh
echo "=== Step 8 - Functional API Tests ==="
docker-compose ${COMPOSE_ARGS} run --rm validation validation/functional_api_tests.sh

if [ "${GENERATE_DOCS}" == "true" ]
  then
  echo "=== Generating new docs for Github Pages ==="
  python3 docs/create_report/run.py
fi
echo "=== FINISHED! ==="

END_TIME=$(date +%s)
RUN_TIME=$((END_TIME-START_TIME))

echo "Total Run Time: ${RUN_TIME} seconds"
