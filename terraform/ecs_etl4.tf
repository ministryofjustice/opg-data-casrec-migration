resource "aws_ecs_task_definition" "etl4" {
  family                   = "etl4-${terraform.workspace}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 2048
  memory                   = 4096
  container_definitions    = "[${local.etl4}]"
  task_role_arn            = aws_iam_role.etl.arn
  execution_role_arn       = aws_iam_role.execution_role.arn
  tags = merge(local.default_tags,
    { "Role" = "casrec-migration-${local.environment}" },
  )
}

locals {
  etl4 = jsonencode({
    cpu       = 0,
    essential = true,
    image     = local.images.etl4,
    name      = "etl4",
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = aws_cloudwatch_log_group.casrec_migration.name,
        awslogs-region        = "eu-west-1",
        awslogs-stream-prefix = "casrec-migration-etl4-${local.environment}"
      }
    },
    secrets = [
      {
        name      = "DB_PASSWORD",
        valueFrom = aws_secretsmanager_secret.casrec_migration.arn
      },
      {
        name      = "SIRIUS_DB_PASSWORD"
        valueFrom = data.aws_secretsmanager_secret.sirius_db.arn
      },
    ],
    environment = [
      {
        name  = "DB_HOST",
        value = aws_rds_cluster.cluster_serverless.endpoint
      },
      {
        name  = "DB_PORT",
        value = tostring(aws_rds_cluster.cluster_serverless.port)
      },
      {
        name  = "DB_NAME",
        value = aws_rds_cluster.cluster_serverless.database_name
      },
      {
        name  = "DB_USER",
        value = aws_rds_cluster.cluster_serverless.master_username
      },
      {
        name  = "SIRIUS_DB_HOST",
        value = data.aws_rds_cluster.sirius.endpoint
      },
      {
        name  = "SIRIUS_DB_PORT",
        value = tostring(data.aws_rds_cluster.sirius.port)
      },
      {
        name  = "SIRIUS_DB_NAME",
        value = data.aws_rds_cluster.sirius.database_name
      },
      {
        name  = "SIRIUS_DB_USER",
        value = data.aws_rds_cluster.sirius.master_username
      },
      {
        name  = "ACCOUNT_NAME",
        value = local.account.account_name
      },
      {
        name  = "ENVIRONMENT",
        value = terraform.workspace
      },
    ]
  })
}
