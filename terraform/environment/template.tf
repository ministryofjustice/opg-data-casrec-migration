data "aws_security_group" "sirius_ecs_api" {
  filter {
    name   = "tag:Name"
    values = ["api-ecs-${local.account.sirius_env}"]
  }
}

data "aws_security_group" "sirius_ecs_es" {
  filter {
    name   = "tag:Name"
    values = ["search-ecs-${local.account.sirius_env}"]
  }
}

resource "local_file" "output" {
  content = templatefile("${path.module}/tasks.toml",
    {
      cluster                                        = local.account.sirius_env,
      sec-group-api                                  = data.aws_security_group.sirius_ecs_api.id,
      sec-group-es                                   = data.aws_security_group.sirius_ecs_es.id,
      sec-group-membrane                             = data.aws_security_group.sirius_membrane.id,
      subnets                                        = join("\", \"", data.aws_subnet_ids.private.ids),
      account                                        = local.account.account_id,
      casrec-cluster                                 = aws_ecs_cluster.migration.name,
      casrec-sec-group                               = aws_security_group.etl.id,
      casrec-subnets                                 = local.subnets_string,
      casrec-task-definition-initialise-environments = aws_ecs_task_definition.etl0.arn,
      casrec-task-definition-load-casrec             = aws_ecs_task_definition.etl1.arn,
      casrec-task-definition-transform               = aws_ecs_task_definition.etl2.arn,
      casrec-task-definition-integration             = aws_ecs_task_definition.etl3.arn,
      casrec-task-definition-load-sirius             = aws_ecs_task_definition.etl4.arn,
      casrec-task-definition-validation              = aws_ecs_task_definition.etl5.arn
  })
  filename = "${path.module}/terraform.output.json"
}

output "container_definition" {
  value       = aws_ecs_task_definition.etl0.container_definitions
  description = "Container Definitions."
}
