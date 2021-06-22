//data "aws_security_group" "ecr_endpoint" {
//  tags   = { Name = "migrations_ecr_endpoint" }
//  vpc_id = data.aws_vpc.sirius.id
//}
//
//data "aws_security_group" "ecr_api_endpoint" {
//  tags   = { Name = "migrations_ecr_api_endpoint" }
//  vpc_id = data.aws_vpc.sirius.id
//}
//
//data "aws_security_group" "logs_endpoint" {
//  tags   = { Name = "migrations_logs_endpoint" }
//  vpc_id = data.aws_vpc.sirius.id
//}
//
data "aws_vpc_endpoint" "s3_endpoint" {
  service_name = "com.amazonaws.eu-west-1.s3"
  vpc_id       = data.aws_vpc.sirius.id
  id           = "vpce-0d1a2425df0aae7a6"
}
//
//data "aws_security_group" "ssm_endpoint" {
//  tags   = { Name = "migrations_ssm_endpoint" }
//  vpc_id = data.aws_vpc.sirius.id
//}
//
//data "aws_security_group" "secrets_endpoint" {
//  tags   = { Name = "migrations_secrets_endpoint" }
//  vpc_id = data.aws_vpc.sirius.id
//}
