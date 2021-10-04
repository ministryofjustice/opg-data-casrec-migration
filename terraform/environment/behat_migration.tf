resource "aws_ecs_task_definition" "behat" {
  count                    = local.account.name == "production" ? 0 : 1
  family                   = "behat-migration-${local.account.sirius_env}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 2048
  memory                   = 4096
  container_definitions    = "[${local.behat_migration}]"
  task_role_arn            = data.aws_iam_role.sirius_behat_task_role.arn
  execution_role_arn       = data.aws_iam_role.sirius_behat_execution_role.arn
  tags = merge(local.default_tags,
    { "Role" = "casrec-migration-${local.environment}" },
  )
}

locals {
  behat_migration = jsonencode({
    essential = true,
    image     = data.aws_ecs_container_definition.casmigrate_api.image
    command = [
      "php",
      "vendor/bin/behat",
      "--config=docker/behat_ci.yml",
      "--tags=@casrecmigration",
      "--colors",
      "-f",
      "pretty",
      "-o",
    "std"],
    name = "behat-migration-${local.account.sirius_env}",
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = aws_cloudwatch_log_group.casrec_migration.name,
        awslogs-region        = "eu-west-1",
        awslogs-stream-prefix = "casrec-migration-behat-${local.environment}"
      }
    },
    secrets     = local.sirius_api_secrets,
    environment = concat(local.sirius_shared_environment_variables, local.migration_env_vars)
  })
}
