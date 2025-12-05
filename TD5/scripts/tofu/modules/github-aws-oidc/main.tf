resource "aws_iam_openid_connect_provider" "github" {
  url             = var.provider_url
  client_id_list  = [var.audience]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]

  tags = {
    Name = "github-oidc-provider"
  }
}
