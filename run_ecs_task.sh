#!/bin/bash
set -e

cd terraform
echo "----- INITIALIZING TERRAFORM -----"
export TF_WORKSPACE=default
export TF_VAR_default_role=breakglass
export TF_VAR_management_role=operator
export TF_VAR_image_tag=fake_tag
export management_role
export TF_CLI_ARGS_init="-backend-config=role_arn=arn:aws:iam::311462405659:role/operator -upgrade=true"
aws-vault exec identity -- terraform init -input=false -upgrade=true -reconfigure
export TF_WORKSPACE=preproduction
echo "----- CREATING TEMPLATE FILE TO RUN EXTRACT JOB -----"
aws-vault exec identity -- terraform apply -input=false -auto-approve -target=local_file.output_casrec
cd ..
echo "----- RUNNING ECS TASK TO EXTRACT DATA TO S3 -----"
aws-vault exec identity -- docker-compose -f docker-compose.commands.yml run --rm case_to_s3 python3 run_ecs_task.py -c 10020349
echo "----- PULLING ANON S3 DATA FROM PREPROD TO LOCAL -----"
aws-vault exec identity -- docker-compose run --rm load_s3 python3 synchronise_s3.py -e preproduction
echo "----- RESULTS MERGED WITH LOCAL DATA -----"
