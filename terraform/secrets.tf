resource "aws_secretsmanager_secret" "casrec_migration" {
  name = "${local.account.name}/casrec-migration-database-password"
  tags = local.default_tags
}

data "aws_secretsmanager_secret_version" "database_password" {
  secret_id = aws_secretsmanager_secret.casrec_migration.id
}

resource "aws_secretsmanager_secret" "api_tests" {
  name = "${local.account.name}/migration-api-test-password"
  tags = local.default_tags
}

data "aws_secretsmanager_secret_version" "api_tests" {
  secret_id = aws_secretsmanager_secret.api_tests.id
}