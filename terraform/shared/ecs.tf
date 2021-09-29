data "aws_ecs_cluster" "migration" {
  cluster_name = "casrec-migration-${local.environment}"
}

data "aws_ecs_task_definition" "prepare" {
  task_definition = "etl0-${terraform.workspace}"
}

data "aws_ecs_task_definition" "load_casrec_db" {
  task_definition = "etl1-${terraform.workspace}"
}
