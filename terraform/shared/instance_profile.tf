resource "aws_iam_instance_profile" "cloud9_profile" {
  name = "migration_c9_profile.${local.environment}"
  role = aws_iam_role.c9_profile.name
}

resource "aws_iam_role" "c9_profile" {
  name               = "migration-c9-profile.${local.environment}"
  assume_role_policy = data.aws_iam_policy_document.c9_profile.json
  tags               = local.default_tags
}

data "aws_iam_policy_document" "c9_profile" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["ec2.amazonaws.com"]
      type        = "Service"
    }
  }
}
