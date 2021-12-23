resource "aws_ecs_task_definition" "etl5" {
  family                   = "etl5-${terraform.workspace}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 2048
  memory                   = 4096
  container_definitions    = "[${local.etl5}]"
  task_role_arn            = aws_iam_role.etl.arn
  execution_role_arn       = aws_iam_role.execution_role.arn
  tags = merge(local.default_tags,
    { "Role" = "casrec-migration-${local.environment}" },
  )
}

locals {
  etl5 = jsonencode({
    cpu       = 0,
    essential = true,
    image     = local.images.etl5,
    name      = "etl5",
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = aws_cloudwatch_log_group.casrec_migration.name,
        awslogs-region        = "eu-west-1",
        awslogs-stream-prefix = "casrec-migration-etl5-${local.environment}"
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
      {
        name      = "API_TEST_PASSWORD"
        valueFrom = aws_secretsmanager_secret.api_tests.arn
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
        value = local.account.name == "production" ? "NOT_SET" : data.aws_rds_cluster.sirius.endpoint
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
        name  = "ENVIRONMENT",
        value = terraform.workspace
      },
      {
        name  = "DEFAULT_CHUNK_SIZE",
        value = local.account.default_chunk_size
      },
      {
        name  = "ACCOUNT_NAME",
        value = local.account.account_name
      },
      {
        name  = "RUN_API_TESTS",
        value = local.account.run_api_tests
      },
      {
        name  = "SIRIUS_FRONT_URL",
        value = local.account.name == "production" ? "NOT_SET" : "http://frontend.${local.account.sirius_env}.ecs"
      },
      {
        name  = "SIRIUS_ACCOUNT",
        value = local.account.account_id
      },
      {
        name  = "LIGHT_TOUCH_COUNT",
        value = local.account.name == "development" ? "500" : "5000"
      }
    ]
  })
}
