resource "aws_iam_role" "migration_commands" {
  name               = "migration-commands.${local.environment}"
  assume_role_policy = data.aws_iam_policy_document.migration_commands_role_assume_policy.json
  tags               = local.default_tags
}

data "aws_iam_policy_document" "migration_commands_role_assume_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = [
        "arn:aws:iam::631181914621:user/james.warren",
        "arn:aws:iam::631181914621:user/jack.goodby",
        "arn:aws:iam::631181914621:user/elliot.smith",
        "arn:aws:iam::631181914621:user/dimitar.kokov",
        "arn:aws:sts::${local.account.account_id}:assumed-role/operator/james.warren"
      ]
      type = "AWS"
    }
  }
}

resource "aws_iam_role_policy" "migration_commands_role" {
  policy = data.aws_iam_policy_document.migration_commands.json
  role   = aws_iam_role.migration_commands.id
}

data "aws_iam_policy_document" "migration_commands" {
  statement {
    effect = "Allow"
    resources = [
      aws_iam_role.execution_role.arn,
      aws_iam_role.migration_commands.arn,
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

  statement {
    effect = "Allow"
    resources = [
      "arn:aws:s3:::casrec-migration-${local.account.name}/*"
    ]

    actions = [
      "s3:*"
    ]
  }

  statement {
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "s3:ListAllMyBuckets",
      "s3:ListBucket",
      "s3:getBucketVersioning"
    ]
  }

  statement {
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "states:ListActivities",
      "states:ListStateMachines",
      "states:ListTagsForResource",
      "states:DescribeActivity",
      "states:DescribeExecution",
      "states:DescribeStateMachine",
      "states:DescribeStateMachineForExecution",
      "states:GetActivityTask",
      "states:GetExecutionHistory"
    ]
  }

  statement {
    effect    = "Allow"
    resources = ["arn:aws:states:eu-west-1:${local.account.account_id}:stateMachine:casrec-mig-state-machine-${local.account.name}"]
    actions = [
      "states:StartExecution",
      "states:ListExecutions"
    ]
  }
}
