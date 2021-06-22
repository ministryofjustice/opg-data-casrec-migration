//data "aws_route_tables" "private" {
//    filter {
//    name   = "tag:Name"
//    values = ["private.*"]
//  }
//}
//
//resource "aws_vpc_endpoint" "s3" {
//  service_name      = "com.amazonaws.eu-west-1.s3"
//  vpc_id            = data.aws_vpc.sirius.id
//  vpc_endpoint_type = "Gateway"
//  route_table_ids   = data.aws_route_tables.private.ids
//  tags              = merge(local.default_tags, { Name = "migration_s3" })
//}
