#!/bin/bash
set -e
while getopts c: option
do
  case "${option}"
  in
    c) CASE_REFERENCE=${OPTARG};;
    *) echo "usage: $0 [-c]" >&2
           exit 1 ;;
  esac
done

cd terraform
echo "----- INITIALIZING TERRAFORM -----"
export TF_WORKSPACE=default
export TF_VAR_default_role=operator
export TF_VAR_management_role=operator
export TF_CLI_ARGS_init="-backend-config=role_arn=arn:aws:iam::311462405659:role/operator -upgrade=true"
aws-vault exec identity -- terraform init -input=false -upgrade=true -reconfigure
export TF_WORKSPACE=preproduction
TF_VAR_image_tag=$(aws-vault exec identity -- terraform output -json container_definition | sed 's/\\//g' | sed 's/^"\(.*\)"$/\1/' | jq '.[].image' | sed 's/^"\(.*\)"$/\1/' | awk -F':' '{print $2}')
export TF_VAR_image_tag=$TF_VAR_image_tag
echo "----- CREATING TEMPLATE FILE TO RUN EXTRACT JOB -----"
aws-vault exec identity -- terraform apply -input=false -auto-approve -target=local_file.output_casrec
cd ..
echo "----- RUNNING ECS TASK TO EXTRACT DATA TO S3 -----"
aws-vault exec identity -- docker-compose -f docker-compose.commands.yml run --rm case_to_s3 python3 case_details_to_s3.py -c "${CASE_REFERENCE}"
echo "----- PULLING ANON S3 DATA FROM PREPROD TO LOCAL -----"
aws-vault exec identity -- docker-compose run --rm load_s3 python3 synchronise_s3.py -e preproduction
echo "----- RESULTS MERGED WITH LOCAL DATA -----"
