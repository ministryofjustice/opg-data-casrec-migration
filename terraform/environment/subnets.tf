data "aws_vpc" "sirius" {
  id = local.account.vpc_id
}

data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.sirius.id

  filter {
    name   = "tag:Name"
    values = ["private-*"]
  }
}
