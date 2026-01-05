terraform {
  backend "s3" {
    bucket         = "bibawandaogo-devops-tfstate"
    key            = "td5/lambda-sample"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "bibawandaogo-devops-tfstate-lock"
  }
}
