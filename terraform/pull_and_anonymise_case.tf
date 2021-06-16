resource "aws_iam_role" "migration_pull_case_role" {
  name               = "migration-pull-case-role.${local.environment}"
  assume_role_policy = data.aws_iam_policy_document.migration_pull_case_role_assume_policy.json
  tags               = local.default_tags
}

data "aws_iam_policy_document" "migration_pull_case_role_assume_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = [
        "arn:aws:iam::631181914621:user/james.warren",
        "arn:aws:iam::631181914621:user/farzan.fatemifar",
        "arn:aws:iam::631181914621:user/jack.goodby",
        "arn:aws:iam::631181914621:user/jennifer.mackown"
      ]
      type = "AWS"
    }
  }
}

resource "aws_iam_role_policy" "migration_pull_case_role" {
  policy = data.aws_iam_policy_document.migration_pull_case_role.json
  role   = aws_iam_role.migration_pull_case_role.id
}

data "aws_iam_policy_document" "migration_pull_case_role" {
  statement {
    effect = "Allow"
    resources = [
      aws_iam_role.execution_role.arn,
      aws_iam_role.migration_pull_case_role.arn,
      aws_iam_role.etl.arn
    ]

    actions = [
      "iam:PassRole",
    ]
  }

  statement {
    effect = "Allow"
    resources = [
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/etl0-${local.account.name}:*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task/casrec-migration-${local.account.name}*"
    ]

    actions = [
      "ecs:*"
    ]
  }

}