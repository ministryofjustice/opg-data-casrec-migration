locals {
  images = {
    etl0 = "${data.aws_ecr_repository.images["etl0"].repository_url}:${var.image_tag}"
    etl1 = "${data.aws_ecr_repository.images["etl1"].repository_url}:${var.image_tag}"
  }

  repositories = [
    "etl0",
    "etl1"
  ]
}

data "aws_ecr_repository" "images" {
  for_each = toset(local.repositories)

  name     = "casrec-migration/${each.key}"
  provider = aws.management
}
