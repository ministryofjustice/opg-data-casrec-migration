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

resource "aws_secretsmanager_secret" "circle_token" {
  count = local.account.name == "development" ? 1 : 0
  name  = "${local.account.name}/migration_circleci_token"
  tags  = local.default_tags
}

data "aws_secretsmanager_secret_version" "circle_token" {
  count     = local.account.name == "development" ? 1 : 0
  secret_id = aws_secretsmanager_secret.circle_token.0.id
}

data "aws_secretsmanager_secret" "casrec_migration_load" {
  name = "${local.account.account_name}/casrec-migration-load-database-password"
}
