provider "aws" {
  region = var.aws_region
}

module "state" {
  source = "../../modules/state-bucket"

  name              = var.state_bucket_name
  dynamodb_table    = var.dynamodb_table_name
  aws_region        = var.aws_region
  enable_versioning = true
}
