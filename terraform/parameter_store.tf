resource "aws_ssm_parameter" "allowed_entities" {
  name  = "${local.account.name}-allowed-entities"
  type  = "String"
  value = "client"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "lay_team" {
  name  = "${local.account.name}-lay-team"
  type  = "String"
  value = "0"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}
