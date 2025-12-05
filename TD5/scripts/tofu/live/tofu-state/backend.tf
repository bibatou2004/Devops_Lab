terraform {
  backend "s3" {
    bucket         = "bibawandaogo-devops-tfstate"
    key            = "td5/tofu-state"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "bibawandaogo-devops-tfstate-lock"
  }
}
