#!/bin/bash
set -e

# remove migration images
docker rmi opg-data-casrec-migration_validation
docker rmi opg-data-casrec-migration_load_to_target
docker rmi opg-data-casrec-migration_integration
docker rmi opg-data-casrec-migration_transform_casrec

# restore sirus
docker rm /opg-data-casrec-migration_postgres-sirius_1 -f
docker-compose up --no-deps -d postgres-sirius
docker-compose run --rm wait-for-it -address postgres-sirius:5432 --timeout=30 -debug
docker-compose up --no-deps -d postgres-sirius-restore

#r run migration
docker-compose run --rm transform_casrec python3 app.py --clear=True -vv
docker-compose run --rm integration integration/integration.sh
docker-compose run --rm load_to_target python3 app.py
docker-compose run --rm validation validation/validate.sh
