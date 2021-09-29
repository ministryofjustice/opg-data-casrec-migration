data "aws_ecs_cluster" "migration" {
  cluster_name = "casrec-migration-${local.environment}"
}
