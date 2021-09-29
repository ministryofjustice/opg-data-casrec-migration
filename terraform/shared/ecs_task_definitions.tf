data "aws_cloudwatch_log_group" "casrec_migration" {
  name = "casrec-migration-${local.environment}"
}

data "aws_iam_role" "etl_task" {
  name = "casrec-migration-${local.environment}"
}

data "aws_iam_role" "etl_execution" {
  name = "migration-execution-role.${local.environment}"
}

resource "aws_ecs_task_definition" "prepare_load_casrec" {
  family                   = "prepare-${terraform.workspace}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 2048
  memory                   = 4096
  container_definitions    = "[${local.prepare_load_casrec}]"
  task_role_arn            = data.aws_iam_role.etl_task.arn
  execution_role_arn       = data.aws_iam_role.etl_execution.arn
  tags = merge(local.default_tags,
    { "Role" = "casrec-migration-${local.environment}" },
  )
}

resource "aws_ecs_task_definition" "load_casrec_db" {
  family                   = "load-casrec-db-${terraform.workspace}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 2048
  memory                   = 4096
  container_definitions    = "[${local.load_casrec_db}]"
  task_role_arn            = data.aws_iam_role.etl_task.arn
  execution_role_arn       = data.aws_iam_role.etl_execution.arn
  tags = merge(local.default_tags,
    { "Role" = "casrec-migration-${local.environment}" },
  )
}

locals {
  prepare_load_casrec = jsonencode({
    cpu       = 0,
    essential = true,
    image     = local.images.etl0,
    name      = "etl0",
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = data.aws_cloudwatch_log_group.casrec_migration.name,
        awslogs-region        = "eu-west-1",
        awslogs-stream-prefix = "casrec-migration-prepare-load-casrec-${local.environment}"
      }
    },
    secrets = [
      {
        name      = "DB_PASSWORD",
        valueFrom = data.aws_secretsmanager_secret.casrec_migration.arn
      },
    ],
    environment = [
      {
        name  = "DB_HOST",
        value = aws_rds_cluster.casrec_load_db.endpoint
      },
      {
        name  = "DB_PORT",
        value = tostring(aws_rds_cluster.casrec_load_db.port)
      },
      {
        name  = "DB_NAME",
        value = aws_rds_cluster.casrec_load_db.database_name
      },
      {
        name  = "DB_USER",
        value = aws_rds_cluster.casrec_load_db.master_username
      },
      {
        name  = "ACCOUNT_NAME",
        value = terraform.workspace
      },
      {
        name  = "ENVIRONMENT",
        value = terraform.workspace
      },
      {
        name  = "DEFAULT_CHUNK_SIZE",
        value = "20000"
      }
    ]
  })
  load_casrec_db = jsonencode({
    cpu       = 0,
    essential = true,
    image     = local.images.etl1,
    name      = "etl1",
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = data.aws_cloudwatch_log_group.casrec_migration.name,
        awslogs-region        = "eu-west-1",
        awslogs-stream-prefix = "casrec-migration-prepare-load-casrec-${local.environment}"
      }
    },
    secrets = [
      {
        name      = "DB_PASSWORD",
        valueFrom = data.aws_secretsmanager_secret.casrec_migration.arn
      },
    ],
    environment = [
      {
        name  = "DB_HOST",
        value = aws_rds_cluster.casrec_load_db.endpoint
      },
      {
        name  = "DB_PORT",
        value = tostring(aws_rds_cluster.casrec_load_db.port)
      },
      {
        name  = "DB_NAME",
        value = aws_rds_cluster.casrec_load_db.database_name
      },
      {
        name  = "DB_USER",
        value = aws_rds_cluster.casrec_load_db.master_username
      },
      {
        name  = "ACCOUNT_NAME",
        value = terraform.workspace
      },
      {
        name  = "ENVIRONMENT",
        value = terraform.workspace
      },
      {
        name  = "DEFAULT_CHUNK_SIZE",
        value = "20000"
      }
    ]
  })
}
