#!/bin/bash
docker kill $(docker ps -q)
docker container prune -f
docker network prune -f
for i in `docker image ls | grep casrec | awk '{print $3}'`; do docker rmi -f $i; done
for i in `docker image ls | grep none | awk '{print $3}'`; do docker rmi -f $i; done
for i in `docker image ls | grep localstack | awk '{print $3}'`; do docker rmi -f $i; done
test -z "$(docker ps -q 2>/dev/null)" && osascript -e 'quit app "Docker"'
sleep 5
open --background -a Docker
git pull origin main

echo ""
echo "NOW WAIT FOR DOCKER TO COME UP FULLY BEFORE YOU RUN ./migrate.sh"
