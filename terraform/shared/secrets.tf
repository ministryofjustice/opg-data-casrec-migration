resource "aws_secretsmanager_secret" "casrec_migration_load" {
  name = "${local.account.name}/casrec-migration-load-database-password"
}

data "aws_secretsmanager_secret_version" "casrec_migration_load" {
  secret_id = aws_secretsmanager_secret.casrec_migration_load.id
}
