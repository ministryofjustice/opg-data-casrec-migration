resource "aws_ssm_parameter" "allowed_entities" {
  name  = "${local.account.name}-allowed-entities"
  type  = "String"
  value = "client"

  tags = local.default_tags

  lifecycle {
    ignore_changes = [value]
  }
}
