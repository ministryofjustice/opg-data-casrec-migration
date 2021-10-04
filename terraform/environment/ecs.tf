resource "aws_ecs_cluster" "migration" {
  name = "casrec-migration-${local.environment}"
  tags = local.default_tags
}

resource "aws_cloudwatch_log_group" "casrec_migration" {
  name              = "casrec-migration-${local.environment}"
  retention_in_days = 180
  tags              = local.default_tags
}

//EXECUTION ROLES

resource "aws_iam_role" "execution_role" {
  name               = "migration-execution-role.${local.environment}"
  assume_role_policy = data.aws_iam_policy_document.execution_role_assume_policy.json
  tags               = local.default_tags
}

data "aws_iam_policy_document" "execution_role_assume_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_iam_role_policy" "execution_role" {
  policy = data.aws_iam_policy_document.execution_role.json
  role   = aws_iam_role.execution_role.id
}

data "aws_iam_policy_document" "execution_role" {
  statement {
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "ssm:GetParameters",
      "secretsmanager:GetSecretValue",
    ]
  }
}

//TASK ROLE

resource "aws_iam_role" "etl" {
  assume_role_policy = data.aws_iam_policy_document.task_role_assume_policy.json
  name               = "casrec-migration-${local.environment}"
  tags               = local.default_tags
}

data "aws_iam_policy_document" "task_role_assume_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "etl_task" {
  statement {
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "s3:GetObject",
      "s3:ListObjectVersions",
      "s3:ListBucketVersions",
      "s3:GetObjectTagging",
      "s3:ListObjects",
      "s3:ListBucket",
      "s3:PutObject",
      "s3:PutObjectAcl"
    ]
  }
  statement {
    effect = "Allow"
    resources = [
      aws_ssm_parameter.additional_data.arn,
      aws_ssm_parameter.allowed_entities.arn,
      aws_ssm_parameter.generate_progress.arn,
      aws_ssm_parameter.lay_team.arn,
      aws_ssm_parameter.match_existing_data.arn,
      aws_ssm_parameter.row_counts.arn
    ]

    actions = [
      "ssm:GetParameter*"
    ]
  }
}

resource "aws_iam_role_policy" "etl_task" {
  name   = "casrec-migration-task-logs.${local.environment}"
  policy = data.aws_iam_policy_document.etl_task.json
  role   = aws_iam_role.etl.id
}

// SECURITY GROUP
resource "aws_security_group" "etl" {
  name_prefix = "casrec-migration-ecs-${terraform.workspace}-"
  vpc_id      = data.aws_vpc.sirius.id
  description = "ETL1 ECS task"

  lifecycle {
    create_before_destroy = true
  }

  tags = merge(
    local.default_tags,
    map("Name", "etl1-ecs-${terraform.workspace}")
  )
}

//RULES FOR APP ACCESS
resource "aws_security_group_rule" "etl_to_api_egress" {
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = 80
  to_port                  = 80
  security_group_id        = aws_security_group.etl.id
  source_security_group_id = data.aws_security_group.sirius_ecs_api.id
  description              = "Outbound ETL to Sirius API"
}

resource "aws_security_group_rule" "etl_to_frontend_egress" {
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = 80
  to_port                  = 80
  security_group_id        = aws_security_group.etl.id
  source_security_group_id = data.aws_security_group.sirius_frontend.id
  description              = "Outbound ETL to Sirius Frontend"
}

resource "aws_security_group_rule" "etl_to_membrane_egress" {
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = 80
  to_port                  = 80
  security_group_id        = aws_security_group.etl.id
  source_security_group_id = data.aws_security_group.sirius_membrane.id
  description              = "Outbound ETL to Sirius Membrane"
}

//RULES FOR DB ACCESS
resource "aws_security_group_rule" "etl_to_db_egress" {
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = 5432
  to_port                  = 5432
  security_group_id        = aws_security_group.etl.id
  source_security_group_id = aws_security_group.db.id
  description              = "Outbound ETL to Casrec Migration DB"
}

resource "aws_security_group_rule" "etl_to_sirius_db_egress" {
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = 5432
  to_port                  = 5432
  security_group_id        = aws_security_group.etl.id
  source_security_group_id = data.aws_security_group.sirius_db.id
  description              = "Outbound ETL to Sirius DB"
}

resource "aws_security_group_rule" "etl_to_casrec_load_db_ingress" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.etl.id
  security_group_id        = data.aws_security_group.casrec_load_db.id
  description              = "ETL ECS tasks to Casrec Load RDS inbound"
}

resource "aws_security_group_rule" "etl_to_casrec_load_db_egress" {
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = 5432
  to_port                  = 5432
  security_group_id        = aws_security_group.etl.id
  source_security_group_id = data.aws_security_group.casrec_load_db.id
  description              = "Outbound ETL to Casrec Load DB"
}

//RULES FOR ENDPOINTS ACCESS

resource "aws_security_group_rule" "etl_to_ecr_api_egress" {
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = 443
  to_port                  = 443
  security_group_id        = aws_security_group.etl.id
  source_security_group_id = data.aws_security_group.vpc_endpoints.id
  description              = "Outbound ETL to ECR API Endpoints SG"
}

resource "aws_security_group_rule" "etl_to_s3_egress" {
  type              = "egress"
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
  security_group_id = aws_security_group.etl.id
  prefix_list_ids   = toset([for i in local.account.s3_vpc_endpoint_ids : data.aws_vpc_endpoint.s3_endpoint[i].prefix_list_id])
  description       = "Outbound ETL to S3 Endpoint"
}

data "aws_security_group" "sirius_db" {
  filter {
    name   = "tag:Name"
    values = ["rds-api-${local.account.sirius_env}"]
  }
}

data "aws_security_group" "sirius_membrane" {
  filter {
    name   = "tag:Name"
    values = ["membrane-ecs-${local.account.sirius_env}"]
  }
}

data "aws_security_group" "casrec_load_db" {
  filter {
    name   = "tag:Name"
    values = ["casrec-load-${local.account.account_name}"]
  }
}

resource "aws_security_group_rule" "etl_to_sirius_db_ingress" {
  count                    = local.account.name == "production" ? 0 : 1
  type                     = "ingress"
  protocol                 = "tcp"
  description              = "ETL direct access to Sirius DB for migration"
  from_port                = 5432
  to_port                  = 5432
  security_group_id        = data.aws_security_group.sirius_db.id
  source_security_group_id = aws_security_group.etl.id
}

// Add access for our API test
data "aws_security_group" "sirius_frontend" {
  filter {
    name   = "tag:Name"
    values = ["frontend-ecs-${local.account.sirius_env}"]
  }
}

resource "aws_security_group_rule" "etl_to_frontend_sirius_ingress" {
  count                    = local.account.name == "production" ? 0 : 1
  type                     = "ingress"
  protocol                 = "tcp"
  description              = "ETL direct access to frontend for API tests"
  from_port                = 80
  to_port                  = 80
  security_group_id        = data.aws_security_group.sirius_frontend.id
  source_security_group_id = aws_security_group.etl.id
}
