resource "aws_ecs_task_definition" "etl1" {
  family                   = "etl1-${terraform.workspace}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 2048
  memory                   = 4096
  container_definitions    = "[${local.etl1}]"
  task_role_arn            = aws_iam_role.etl.arn
  execution_role_arn       = aws_iam_role.execution_role.arn
  tags = merge(local.default_tags,
    { "Role" = "casrec-migration-${local.environment}" },
  )
}

locals {
  etl1 = jsonencode({
    cpu       = 0,
    essential = true,
    image     = local.images.etl1,
    name      = "etl1",
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = aws_cloudwatch_log_group.casrec_migration.name,
        awslogs-region        = "eu-west-1",
        awslogs-stream-prefix = "casrec-migration-etl1-${local.environment}"
      }
    },
    secrets = [
      {
        name      = "DB_PASSWORD",
        valueFrom = aws_secretsmanager_secret.casrec_migration.arn
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
        name  = "S3_PATH",
        value = local.account.s3_path
      },
      {
        name  = "SIRIUS_ACCOUNT",
        value = local.account.account_id
      }
    ]
  })
}
