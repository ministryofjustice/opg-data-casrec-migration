data "aws_ecs_cluster" "migration" {
  cluster_name = "casrec-migration-${local.environment}"
}

data "aws_cloudwatch_log_group" "casrec_migration" {
  name = "casrec-migration-${local.environment}"
}

data "aws_iam_role" "etl_task" {
  name = "casrec-migration-${local.environment}"
}

data "aws_iam_role" "etl_execution" {
  name = "migration-execution-role.${local.environment}"
}
