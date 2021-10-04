#!/bin/bash
set -e
while getopts t:i:n:c:l: option
do
  case "${option}"
  in
    t) TAG=${OPTARG};;
    i) ID=${OPTARG};;
    n) NAME=${OPTARG};;
    c) CMD=${OPTARG};;
    l) LOG=${OPTARG};;
    *) echo "usage: $0 [-t][-i][-n][-c][-l]" >&2
           exit 1 ;;
  esac
done

cd /terraform/environment
echo "----- INITIALIZING TERRAFORM -----"
export TF_WORKSPACE=default
export TF_VAR_default_role=breakglass
export TF_VAR_management_role=operator
export TF_VAR_image_tag=$TAG
export management_role
export TF_CLI_ARGS_init="-backend-config=role_arn=arn:aws:iam::311462405659:role/operator -upgrade=true"
terraform init -input=false -upgrade=true -reconfigure
export TF_WORKSPACE=${WORKSPACE}
echo "----- CREATING TEMPLATE FILE TO RUN EXTRACT JOB -----"
terraform apply -input=false -auto-approve -target=local_file.output_casrec
cd /
echo "----- RUNNING ECS TASK -----"
python3 run_ecs_task.py -i "${ID}" -n "${NAME}" -c "${CMD}" -l "${LOG}"
