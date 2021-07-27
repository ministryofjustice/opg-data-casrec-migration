#!/usr/bin/env bash

while getopts w:k: option
do
  case "${option}"
  in
    w) WORKSPACE=${OPTARG};;
    k) API_KEY=${OPTARG};;
    *) echo "usage: $0 [-w] [-k]" >&2
           exit 1 ;;
  esac
done

GREP_RETURN_CODE=0
WAITED=0
SECS_TO_WAIT=30
LAST_BUILD_URL="${JOB_URL}/lastBuild/api/json"

echo "Checking if previous job is running against ${WORKSPACE}"
while [ $GREP_RETURN_CODE -eq 0 ]
do
    # Grep will return 0 while a build is running
    curl --silent ${LAST_BUILD_URL} --user jenkins-opg:${API_KEY} | jq ".result" | grep "null" > /dev/null
    GREP_RETURN_CODE=$?
    sleep ${SECS_TO_WAIT}
    WAITED=$((WAITED + SECS_TO_WAIT))
    echo "Waiting on previous job to finish for ${WAITED} seconds"
done

JOB_URL="https://jenkins.opg.service.justice.gov.uk/job/Sirius/job/Deploy_to_CasRec_Data_Migration_Preproduction"
#Run the build
echo "Running jenkins restore job against ${WORKSPACE}"

curl -X POST ${JOB_URL}/buildWithParameters?WORKSPACE=${WORKSPACE}\&restore_data=true --user jenkins-opg:${API_KEY}

sleep 30
BUILD_NO=$(curl --silent ${LAST_BUILD_URL} --user jenkins-opg:${API_KEY} | jq ".number")
echo "Got build number: ${BUILD_NO}"

BUILD_URL="${JOB_URL}/${BUILD_NO}/api/json"

GREP_RETURN_CODE=0
WAITED=30
SECS_TO_WAIT=30

while [ $GREP_RETURN_CODE -eq 0 ]
do
    sleep ${SECS_TO_WAIT}
    WAITED=$((WAITED + SECS_TO_WAIT))
    echo "Job has been running for ${WAITED} seconds"
    # Grep will return 0 while the build is running
    curl --silent ${BUILD_URL} --user jenkins-opg:${API_KEY} | jq ".result" | grep "null" > /dev/null
    GREP_RETURN_CODE=$?
done

RESULT=$(curl --silent ${BUILD_URL} --user jenkins-opg:${API_KEY} | jq ".result")

echo "Jenkins Job finished with result: ${RESULT}"
if [ ${RESULT} == "\"SUCCESS\"" ]
then
  exit 0
else
  exit 1
fi
