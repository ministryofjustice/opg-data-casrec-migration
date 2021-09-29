resource "aws_s3_bucket" "casrec_migration" {
  bucket        = "casrec-migration-${local.environment}"
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
      days = 10
    }
  }
  tags = local.default_tags
}

resource "aws_s3_bucket_public_access_block" "casrec_migration" {
  bucket = aws_s3_bucket.casrec_migration.bucket

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "casrec_migration" {
  bucket = aws_s3_bucket_public_access_block.casrec_migration.bucket
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
    resources = ["${aws_s3_bucket.casrec_migration.arn}/*"]

    condition {
      test     = "StringNotEquals"
      values   = ["AES256"]
      variable = "s3:x-amz-server-side-encryption"
    }
  }

  statement {
    sid     = "DenyNoneSSLRequests"
    effect  = "Deny"
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.casrec_migration.arn,
      "${aws_s3_bucket.casrec_migration.arn}/*"
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = [false]
    }

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}
