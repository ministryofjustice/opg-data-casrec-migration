data "aws_secretsmanager_secret" "casrec_migration" {
  name = "${local.account.name}/casrec-migration-database-password"
}

data "aws_secretsmanager_secret_version" "database_password" {
  secret_id = data.aws_secretsmanager_secret.casrec_migration.id
}
