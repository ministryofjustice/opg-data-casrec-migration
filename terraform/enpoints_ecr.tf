resource "aws_vpc_endpoint" "ecr" {
  vpc_id              = data.aws_vpc.sirius.id
  service_name        = "com.amazonaws.eu-west-1.ecr.dkr"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true
  security_group_ids  = aws_security_group.ecr_endpoint[*].id
  subnet_ids          = data.aws_subnet_ids.private.ids
  tags                = merge(local.default_tags, { Name = "migration_ecr" })
}

resource "aws_security_group" "ecr_endpoint" {
  name_prefix = "migration_ecr_endpoint"
  vpc_id      = data.aws_vpc.sirius.id
  tags        = merge(local.default_tags, { Name = "migration_ecr_endpoint" })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group_rule" "ecr_endpoint_https_in" {
  from_port         = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.ecr_endpoint.id
  to_port           = 443
  type              = "ingress"
  cidr_blocks       = [data.aws_vpc.sirius.cidr_block]
  description       = "migration_ecr_endpoint"
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = data.aws_vpc.sirius.id
  service_name        = "com.amazonaws.eu-west-1.ecr.api"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true
  security_group_ids  = aws_security_group.ecr_api_endpoint[*].id
  subnet_ids          = data.aws_subnet_ids.private.ids
  tags                = merge(local.default_tags, { Name = "migration_ecr_api" })
}

resource "aws_security_group" "ecr_api_endpoint" {
  name_prefix = "migration_ecr_api_endpoint"
  vpc_id      = data.aws_vpc.sirius.id
  tags        = merge(local.default_tags, { Name = "migration_ecr_api_endpoint" })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group_rule" "ecr_api_endpoint_https_in" {
  from_port         = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.ecr_api_endpoint.id
  to_port           = 443
  type              = "ingress"
  cidr_blocks       = [data.aws_vpc.sirius.cidr_block]
  description       = "migration_ecr_api_endpoint"
}
