data "aws_security_group" "vpc_endpoints" {
  tags   = { Name = "vpc-endpoint-access-private-subnets-eu-west-1" }
  vpc_id = data.aws_vpc.sirius.id
}

data "aws_vpc_endpoint" "s3_endpoint" {
  for_each     = local.account.s3_vpc_endpoint_ids
  service_name = "com.amazonaws.eu-west-1.s3"
  vpc_id       = data.aws_vpc.sirius.id
  id           = each.value
}
