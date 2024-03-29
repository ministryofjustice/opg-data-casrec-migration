#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 migration_steps/load_s3/load_s3_local.py
cd migration_steps/load_s3
python3 load_s3_local.py
cd ${DIR}

./migration_steps/initialise_environments/initialise_pre_delete.sh
./migration_steps/initialise_environments/initialise_post_delete.sh
cd migration_steps/initialise_environments
./initialise_environments.sh
cd ${DIR}

python3 migration_steps/load_casrec/app/app.py
cd migration_steps/load_casrec/app
python3 app.py
cd ${DIR}

./migration_steps/transform_casrec/transform.sh
cd migration_steps/transform_casrec
./transform.sh
cd ${DIR}

./migration_steps/integration/integration.sh
cd migration_steps/integration
./integration.sh
cd ${DIR}


./migration_steps/load_to_sirius/load_to_sirius
cd migration_steps/load_to_sirius
./load_to_sirius.sh
#python3 migration_steps/load_to_target/app/app.py
