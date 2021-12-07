resource "aws_ssm_parameter" "additional_data" {
  name  = "${local.account.name}-additional-data"
  type  = "String"
  value = "False"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "allowed_entities" {
  name  = "${local.account.name}-allowed-entities"
  type  = "String"
  value = "client"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "generate_progress" {
  name  = "${local.account.name}-generate-progress"
  type  = "String"
  value = "False"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "correfs" {
  name  = "${local.account.name}-correfs"
  type  = "String"
  value = "0"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "match_existing_data" {
  name  = "${local.account.name}-match-existing-data"
  type  = "String"
  value = "False"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "row_counts" {
  name  = "${local.account.name}-row-counts"
  type  = "String"
  value = "False"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}
