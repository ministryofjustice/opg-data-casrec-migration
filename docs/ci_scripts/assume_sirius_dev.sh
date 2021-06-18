#!/usr/bin/env bash
set -e

DEVELOPMENT_ACCOUNT="288342028542"

export SECRET_STRING=$(aws sts assume-role \
--role-arn "arn:aws:iam::${DEVELOPMENT_ACCOUNT}:role/integrations-ci" \
--role-session-name AWSCLI-Session | \
jq -r '.Credentials.SessionToken + " " + .Credentials.SecretAccessKey + " " + .Credentials.AccessKeyId')

#local export so they only exist in this stage
export AWS_ACCESS_KEY_ID=$(echo "${SECRET_STRING}" | awk -F' ' '{print $3}')
export AWS_SECRET_ACCESS_KEY=$(echo "${SECRET_STRING}" | awk -F' ' '{print $2}')
export AWS_SESSION_TOKEN=$(echo "${SECRET_STRING}" | awk -F' ' '{print $1}')
