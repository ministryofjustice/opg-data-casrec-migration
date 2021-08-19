data "aws_subnet_ids" "public" {
  vpc_id = data.aws_vpc.sirius.id

  filter {
    name   = "tag:Name"
    values = ["public-*"]
  }
}

locals {
  cloud9_id = local.account.name == "preproduction" ? aws_cloud9_environment_ec2.shared[0].id : "1b01031b9fef4ac0ad89b6858fa4fd70"
}

resource "aws_cloud9_environment_ec2" "shared" {
  count                       = local.account.name == "preproduction" ? 1 : 0
  instance_type               = "t2.micro"
  name                        = "casrec-mig-cloud9-env"
  automatic_stop_time_minutes = 20
  description                 = "Shared Cloud9 instance to be used by casrec mig devs"
  subnet_id                   = tolist(data.aws_subnet_ids.public.ids)[0]
  owner_arn                   = "arn:aws:iam::${var.accounts[terraform.workspace].account_id}:assumed-role/operator/james.warren"
  tags                        = local.default_tags
}

data "aws_security_group" "cloud9" {
  filter {
    name = "tag:aws:cloud9:environment"
    values = [
      local.cloud9_id
    ]
  }
}
