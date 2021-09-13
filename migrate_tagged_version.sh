#!/bin/bash
set -e

ENV_VARS=$(cat <<-END
    \n
    1. Preproduction\n
    2. PreQA\n
    3. QA\n
END
)

FILTER_VARS=$(cat <<-END
    \n
    1. all\n
    2. master\n
    3. qa\n
END
)

set_response () {
  echo "${1}"
  eval "echo \$$3"
  read -rp "Pick from above options: " $2
  eval "echo Variable $2 set to \$$2"
}

CIRCLE_TOKEN=$(aws-vault exec identity --  docker-compose -f docker-compose.commands.yml run --rm migrate_tagged_version python3 migrate_tagged_version/app.py --cmd get_secret_key)

echo "===== RUN A MIGRATION INTO AN ENVIRONMENT ====="
echo ""

set_response "Tag filter to use: " FILTER FILTER_VARS
if [ ${FILTER} == "1" ]
then
  TAG_FILTER="all"
elif [ ${FILTER} == "2" ]
then
  TAG_FILTER="master"
elif [ ${FILTER} == "3" ]
then
  TAG_FILTER="qa"
else
  echo "You need to choose a valid option from [1-4]. Exiting...."
  exit 1
fi

echo "===== LIST OF TAGS BASED ON FILTER OF: $TAG_FILTER ====="
echo ""
aws-vault exec identity -- docker-compose -f docker-compose.commands.yml run --rm migrate_tagged_version python3 migrate_tagged_version/app.py --cmd list_of_tagged_builds --tag_filter "${TAG_FILTER}"
echo ""
read -rp "Copy and paste from the above tags, the tag you want to use for the migration (eg IN999-890d72): " TAG
echo ""

set_response "Environment to run migration to [1-4]: " ENVIRONMENT ENV_VARS
if [ $ENVIRONMENT == "1" ]
then
  ENV="Preproduction"
  RUN_PREPROD="true"
  RUN_PRE_QA="false"
  RUN_QA="false"
elif [ $ENVIRONMENT == "2" ]
then
  ENV="PreQA"
  RUN_PREPROD="false"
  RUN_PRE_QA="true"
  RUN_QA="false"
elif [ $ENVIRONMENT == "3" ]
then
  ENV="QA"
  RUN_PREPROD="false"
  RUN_PRE_QA="false"
  RUN_QA="true"
else
  echo "You need to choose a valid option from [1-4]. Exiting...."
  exit 1
fi

echo "You will be deploying tag $TAG to $ENV"
echo ""
read -rp "Do you want to deploy with the above details (y/n): " DEPLOY
if [ "${DEPLOY}" == "y" ]
then
  curl --request POST \
              --url https://circleci.com/api/v2/project/github/ministryofjustice/opg-data-casrec-migration/pipeline \
              --header "Circle-Token: ${CIRCLE_TOKEN}" \
              --header 'content-type: application/json' \
              --data "{\"branch\":\"master\", \"parameters\":{\"run_master\": false, \"run_preprod\": $RUN_PREPROD, \"run_qa\": $RUN_QA, \"run_preqa\": $RUN_PRE_QA, \"override_tag\": \"$TAG\"}}"
else
  echo "You chose not to deploy. Good bye!"
  exit 0
fi
