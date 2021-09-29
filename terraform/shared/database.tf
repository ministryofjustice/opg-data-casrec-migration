resource "aws_rds_cluster" "casrec_load_db" {
  cluster_identifier           = "casrec-load-${terraform.workspace}"
  apply_immediately            = true
  backup_retention_period      = 1
  database_name                = "casrecload"
  db_subnet_group_name         = "data-persitance-subnet-${local.account.db_subnet_prefix}-vpc"
  deletion_protection          = false
  engine                       = "aurora-postgresql"
  engine_mode                  = "serverless"
  master_username              = "casrec"
  master_password              = data.aws_secretsmanager_secret_version.database_password.secret_string
  preferred_backup_window      = "04:15-04:45"
  preferred_maintenance_window = "mon:04:50-mon:05:20"
  storage_encrypted            = true
  skip_final_snapshot          = true
  vpc_security_group_ids       = [aws_security_group.casrec_load_db.id]
  tags                         = local.default_tags

  scaling_configuration {
    auto_pause               = true
    max_capacity             = 16
    min_capacity             = 16
    seconds_until_auto_pause = 600
    timeout_action           = "RollbackCapacityChange"
  }
}

resource "aws_security_group" "casrec_load_db" {
  name        = "casrec-load-${terraform.workspace}"
  description = "etl to casrec load rds access"
  vpc_id      = data.aws_vpc.sirius.id
  tags = merge(
    local.default_tags,
    { "Name" = "casrec-migration-${terraform.workspace}" },
  )
}

data "aws_security_group" "etl_ecs_tasks" {
  filter {
    name   = "tag:Name"
    values = ["etl1-ecs-${terraform.workspace}"]
  }
}
