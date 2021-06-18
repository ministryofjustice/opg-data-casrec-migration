data "aws_security_group" "sirius_ecs_api" {
  filter {
    name   = "tag:Name"
    values = ["api-ecs-${local.account.sirius_env}"]
  }
}

resource "local_file" "output" {
  content = templatefile("${path.module}/sirius_tasks.toml",
    {
      cluster            = local.account.sirius_env,
      sec_group          = data.aws_security_group.sirius_ecs_api.id,
      sec_group_membrane = data.aws_security_group.sirius_membrane.id,
      subnets            = join("\", \"", data.aws_subnet_ids.private.ids),
      account            = local.account.account_id
  })
  filename = "${path.module}/terraform.output.json"
}

resource "local_file" "output_casrec" {
  content = templatefile("${path.module}/casrec_migration_tasks.toml",
    {
      cluster                     = aws_ecs_cluster.migration.name,
      sec_group                   = aws_security_group.etl.id,
      subnets                     = local.subnets_string,
      account                     = local.account.account_id
      task-definition-prepare     = aws_ecs_task_definition.etl0.arn
      task-definition-load-casrec = aws_ecs_task_definition.etl1.arn
      task-definition-transform   = aws_ecs_task_definition.etl2.arn
      task-definition-integration = aws_ecs_task_definition.etl3.arn
      // Not adding load step as it's too risky as manual option
      task-definition-validation = aws_ecs_task_definition.etl5.arn
  })
  filename = "${path.module}/terraform.output_casrec_migration.json"
}

output "container_definition" {
  value       = aws_ecs_task_definition.etl0.container_definitions
  description = "Container Definitions."
}
