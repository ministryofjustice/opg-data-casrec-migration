#!/bin/bash
set -e

ENV_VARS=$(cat <<-END
    \n
    1. Preproduction\n
    2. PreQA\n
    3. QA\n
    4. Rehearsal_1\n
    5. Rehearsal_2\n
    6. Rehearsal_3\n
    7. Production_1\n
    8. Production_2\n
    9. Production_3\n
END
)

FILTER_VARS=$(cat <<-END
    \n
    1. all\n
    2. main\n
    3. qa\n
    4. production\n
END
)

set_response () {
  echo "${1}"
  eval "echo \$$3"
  read -rp "Pick from above options: " $2
  eval "echo Variable $2 set to \$$2"
}

CIRCLE_TOKEN=$(aws-vault exec identity -- docker-compose -f docker-compose.commands.yml run --rm migrate_tagged_version python3 migrate_tagged_version/app.py --cmd get_secret_key)

echo "===== RUN A MIGRATION INTO AN ENVIRONMENT ====="
echo ""

set_response "Tag filter to use: " FILTER FILTER_VARS
if [ ${FILTER} == "1" ]
then
  TAG_FILTER="all"
elif [ ${FILTER} == "2" ]
then
  TAG_FILTER="main"
elif [ ${FILTER} == "3" ]
then
  TAG_FILTER="qa"
elif [ ${FILTER} == "4" ]
then
  TAG_FILTER="production"
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

set_response "Environment to run migration to [1-5]: " ENVIRONMENT ENV_VARS
if [ $ENVIRONMENT == "1" ]
then
  ENV="Preproduction"
  RUN_PREPROD="true"
  RUN_PRE_QA="false"
  RUN_QA="false"
  RUN_REHEARSAL_1="false"
  RUN_REHEARSAL_2="false"
  RUN_REHEARSAL_3="false"
  RUN_PROD_1="false"
  RUN_PROD_2="false"
  RUN_PROD_3="false"
elif [ $ENVIRONMENT == "2" ]
then
  ENV="PreQA"
  RUN_PREPROD="false"
  RUN_PRE_QA="true"
  RUN_QA="false"
  RUN_REHEARSAL_1="false"
  RUN_REHEARSAL_2="false"
  RUN_REHEARSAL_3="false"
  RUN_PROD_1="false"
  RUN_PROD_2="false"
  RUN_PROD_3="false"
elif [ $ENVIRONMENT == "3" ]
then
  ENV="QA"
  RUN_PREPROD="false"
  RUN_PRE_QA="false"
  RUN_QA="true"
  RUN_REHEARSAL_1="false"
  RUN_REHEARSAL_2="false"
  RUN_REHEARSAL_3="false"
  RUN_PROD_1="false"
  RUN_PROD_2="false"
  RUN_PROD_3="false"
elif [ $ENVIRONMENT == "4" ]
then
  ENV="Rehearsal_1"
  RUN_PREPROD="false"
  RUN_PRE_QA="false"
  RUN_QA="false"
  RUN_REHEARSAL_1="true"
  RUN_REHEARSAL_2="false"
  RUN_REHEARSAL_3="false"
  RUN_PROD_1="false"
  RUN_PROD_2="false"
  RUN_PROD_3="false"
elif [ $ENVIRONMENT == "5" ]
then
  ENV="Rehearsal_2"
  RUN_PREPROD="false"
  RUN_PRE_QA="false"
  RUN_QA="false"
  RUN_REHEARSAL_1="false"
  RUN_REHEARSAL_2="true"
  RUN_REHEARSAL_3="false"
  RUN_PROD_1="false"
  RUN_PROD_2="false"
  RUN_PROD_3="false"
elif [ $ENVIRONMENT == "6" ]
then
  ENV="Rehearsal_3"
  RUN_PREPROD="false"
  RUN_PRE_QA="false"
  RUN_QA="false"
  RUN_REHEARSAL_1="false"
  RUN_REHEARSAL_2="false"
  RUN_REHEARSAL_3="true"
  RUN_PROD_1="false"
  RUN_PROD_2="false"
  RUN_PROD_3="false"
elif [ $ENVIRONMENT == "7" ]
then
  ENV="Production_1"
  RUN_PREPROD="false"
  RUN_PRE_QA="false"
  RUN_QA="false"
  RUN_REHEARSAL_1="false"
  RUN_REHEARSAL_2="false"
  RUN_REHEARSAL_3="false"
  RUN_PROD_1="true"
  RUN_PROD_2="false"
  RUN_PROD_3="false"
elif [ $ENVIRONMENT == "8" ]
then
  ENV="Production_2"
  RUN_PREPROD="false"
  RUN_PRE_QA="false"
  RUN_QA="false"
  RUN_REHEARSAL_1="false"
  RUN_REHEARSAL_2="false"
  RUN_REHEARSAL_3="false"
  RUN_PROD_1="false"
  RUN_PROD_2="true"
  RUN_PROD_3="false"
elif [ $ENVIRONMENT == "9" ]
then
  ENV="Production_3"
  RUN_PREPROD="false"
  RUN_PRE_QA="false"
  RUN_QA="false"
  RUN_REHEARSAL_1="false"
  RUN_REHEARSAL_2="false"
  RUN_REHEARSAL_3="false"
  RUN_PROD_1="false"
  RUN_PROD_2="false"
  RUN_PROD_3="true"
else
  echo "You need to choose a valid option from [1-5]. Exiting...."
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
              --data "{\"branch\":\"main\", \"parameters\":{\"run_main\": false, \"run_preprod\": $RUN_PREPROD, \"run_qa\": $RUN_QA, \"run_preqa\": $RUN_PRE_QA, \"run_rehearsal_1\": $RUN_REHEARSAL_1, \"run_rehearsal_2\": $RUN_REHEARSAL_2, \"run_rehearsal_3\": $RUN_REHEARSAL_3, \"run_production_1\": $RUN_PROD_1, \"run_production_2\": $RUN_PROD_2, \"run_production_3\": $RUN_PROD_3, \"override_tag\": \"$TAG\"}}"
else
  echo "You chose not to deploy. Good bye!"
  exit 0
fi
