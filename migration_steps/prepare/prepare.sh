#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 "${DIR}/prepare_target/app/app.py"
python3 "${DIR}/create_stage_schema/app/app.py"

docker rm prepare_1 &>/dev/null || echo "prepare_1 does not exist. This is OK"
docker rm prepare_2 &>/dev/null || echo "prepare_2 does not exist. This is OK"
docker rm prepare_3 &>/dev/null || echo "prepare_3 does not exist. This is OK"
docker rm prepare_4 &>/dev/null || echo "prepare_4 does not exist. This is OK"

docker-compose run --rm --name prepare_1 prepare python3 /prepare/load_casrec/app/app.py >> docker_load.log &
P1=$!
sleep 1
docker-compose run --rm --name prepare_2 prepare python3 /prepare/load_casrec/app/app.py >> docker_load.log &
P2=$!
sleep 1
docker-compose run --rm --name prepare_3 prepare python3 /prepare/load_casrec/app/app.py >> docker_load.log &
P3=$!
sleep 1
docker-compose run --rm --name prepare_4 prepare python3 /prepare/load_casrec/app/app.py >> docker_load.log &
P4=$!
wait $P1 $P2 $P3 $P4
cat docker_load.log
rm docker_load.log
