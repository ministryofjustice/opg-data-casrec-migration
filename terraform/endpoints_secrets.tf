resource "aws_vpc_endpoint" "secrets" {
  vpc_id              = data.aws_vpc.sirius.id
  service_name        = "com.amazonaws.eu-west-1.secretsmanager"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true
  security_group_ids  = aws_security_group.secrets_endpoint[*].id
  subnet_ids          = data.aws_subnet_ids.private.ids
  tags                = merge(local.default_tags, { Name = "migration_secrets" })
}

resource "aws_security_group" "secrets_endpoint" {
  name_prefix = "migration_secrets_endpoint"
  vpc_id      = data.aws_vpc.sirius.id
  tags        = merge(local.default_tags, { Name = "migration_secrets_endpoint" })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group_rule" "secrets_endpoint_https_in" {
  from_port         = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.secrets_endpoint.id
  to_port           = 443
  type              = "ingress"
  cidr_blocks       = [data.aws_vpc.sirius.cidr_block]
  description       = "migration_secrets_endpoint"
}
