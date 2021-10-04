locals {
  images = {
    etl0 = "${data.aws_ecr_repository.images["etl0"].repository_url}:${var.image_tag}"
    etl1 = "${data.aws_ecr_repository.images["etl1"].repository_url}:${var.image_tag}"
    etl2 = "${data.aws_ecr_repository.images["etl2"].repository_url}:${var.image_tag}"
    etl3 = "${data.aws_ecr_repository.images["etl3"].repository_url}:${var.image_tag}"
    etl4 = "${data.aws_ecr_repository.images["etl4"].repository_url}:${var.image_tag}"
    etl5 = "${data.aws_ecr_repository.images["etl5"].repository_url}:${var.image_tag}"
  }

  repositories = [
    "etl0",
    "etl1",
    "etl2",
    "etl3",
    "etl4",
    "etl5",
  ]
}

data "aws_ecr_repository" "images" {
  for_each = toset(local.repositories)

  name     = "casrec-migration/${each.key}"
  provider = aws.management
}
