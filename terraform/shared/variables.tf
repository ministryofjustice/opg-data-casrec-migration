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
}

variable "accounts" {
  type = map(
    object({
      name             = string
      account_id       = string
      vpc_id           = string
      is_production    = bool
      db_subnet_prefix = string
    })
  )
}
