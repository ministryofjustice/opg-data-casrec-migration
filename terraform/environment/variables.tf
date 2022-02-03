variable "default_role" {
  default = "migrations-ci"
}

variable "management_role" {
  default = "migrations-ci"
}

variable "image_tag" {}

locals {
  account = contains(keys(var.accounts), terraform.workspace) ? var.accounts[terraform.workspace] : var.accounts["development"]

  environment = terraform.workspace

  mandatory_moj_tags = {
    business-unit    = "OPG"
    application      = "CasRec-Migration"
    account          = local.account.name
    environment-name = terraform.workspace
    is-production    = tostring(local.account.is_production)
    owner            = "opgteam@digital.justice.gov.uk"
  }

  optional_tags = {
    source-code            = "https://github.com/ministryofjustice/opg-data-casrec-migration"
    infrastructure-support = "opgteam@digital.justice.gov.uk"
  }

  default_tags = merge(local.mandatory_moj_tags, local.optional_tags)

  sirius_db_endpoint = local.account.name == "production" ? "NOT_SET" : data.aws_rds_cluster.sirius.endpoint
  sirius_db_password = local.account.name == "production" ? "NOT_SET" : data.aws_secretsmanager_secret.sirius_db.arn
}

variable "accounts" {
  type = map(
    object({
      name                    = string
      account_id              = string
      vpc_id                  = string
      is_production           = bool
      db_subnet_prefix        = string
      s3_path                 = string
      sirius_env              = string
      sirius-api-role-suffix  = string
      sirius-exec_role-suffix = string
      run_api_tests           = string
      min_db_capacity         = number
      max_db_capacity         = number
      run_audit               = string
      account_name            = string
      s3_vpc_endpoint_ids     = set(string)
      default_chunk_size      = string
    })
  )
}
