resource "aws_secretsmanager_secret" "casrec_migration" {
  name = "${local.account.name}/casrec-migration-database-password"
  tags = local.default_tags
}

data "aws_secretsmanager_secret_version" "database_password" {
  secret_id = aws_secretsmanager_secret.casrec_migration.id
}

resource "aws_rds_cluster" "cluster_serverless" {
  cluster_identifier           = "casrec-migration-${terraform.workspace}"
  apply_immediately            = true
  backup_retention_period      = 1
  database_name                = "casrecmigration"
  db_subnet_group_name         = "data-persitance-subnet-${local.account.db_subnet_prefix}-vpc"
  deletion_protection          = false
  engine                       = "aurora-postgresql"
  engine_mode                  = "serverless"
  final_snapshot_identifier    = "casrec-migration-${terraform.workspace}-final-snapshot"
  master_username              = "casrec"
  master_password              = data.aws_secretsmanager_secret_version.database_password.secret_string
  preferred_backup_window      = "04:15-04:45"
  preferred_maintenance_window = "mon:04:50-mon:05:20"
  storage_encrypted            = true
  skip_final_snapshot          = true
  vpc_security_group_ids       = [aws_security_group.db.id]
  tags                         = local.default_tags

  scaling_configuration {
    auto_pause               = true
    max_capacity             = local.account.max_db_capacity
    min_capacity             = local.account.min_db_capacity
    seconds_until_auto_pause = 600
    timeout_action           = "RollbackCapacityChange"
  }
}

resource "aws_security_group" "db" {
  name        = "casrec-migration-${terraform.workspace}"
  description = "etl to rds access"
  vpc_id      = data.aws_vpc.sirius.id
  tags = merge(
    local.default_tags,
    { "Name" = "casrec-migration-${terraform.workspace}" },
  )
}

resource "aws_security_group_rule" "etl_to_db_ingress" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.etl.id
  security_group_id        = aws_security_group.db.id
  description              = "ETL to RDS inbound - ETL ECS tasks"
}

resource "aws_security_group_rule" "cloud9_to_db_ingress" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = data.aws_security_group.cloud9.id
  security_group_id        = aws_security_group.db.id
  description              = "Cloud9 to RDS inbound - Shared Dev Cloud9"
}

// Sirius Database

data "aws_secretsmanager_secret" "sirius_db" {
  name = "rds-api-${local.account.account_name}"
}

data "aws_rds_cluster" "sirius" {
  cluster_identifier = "api-${local.account.sirius_env}"
}
