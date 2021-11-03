resource "aws_s3_bucket" "casrec_migration_mappings" {
  bucket        = "casrec-migration-mappings-${local.environment}"
  acl           = "private"
  force_destroy = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    enabled = true

    expiration {
      days = 365
    }

    noncurrent_version_expiration {
      days = 180
    }
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
  tags = local.default_tags
}

resource "aws_s3_bucket_object" "object_staged" {
  bucket                 = aws_s3_bucket.casrec_migration_mappings.bucket
  acl                    = "private"
  key                    = "staged/"
  content_type           = "application/x-directory"
  server_side_encryption = "AES256"
}

resource "aws_s3_bucket_object" "object_merged" {
  bucket                 = aws_s3_bucket.casrec_migration_mappings.bucket
  acl                    = "private"
  key                    = "merged/"
  content_type           = "application/x-directory"
  server_side_encryption = "AES256"
}

resource "aws_s3_bucket_public_access_block" "casrec_migration_mappings" {
  bucket = aws_s3_bucket.casrec_migration_mappings.bucket

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "casrec_migration" {
  bucket = aws_s3_bucket_public_access_block.casrec_migration_mappings.bucket
  policy = data.aws_iam_policy_document.casrec_migration.json
}

data "aws_iam_policy_document" "casrec_migration" {
  policy_id = "PutObjPolicy"

  statement {
    sid    = "DenyUnEncryptedObjectUploads"
    effect = "Deny"

    principals {
      identifiers = ["*"]
      type        = "AWS"
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.casrec_migration_mappings.arn}/*"]

    condition {
      test     = "StringNotEquals"
      values   = ["AES256"]
      variable = "s3:x-amz-server-side-encryption"
    }
  }
}
