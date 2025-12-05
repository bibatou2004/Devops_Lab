# Politique de confiance pour OIDC
data "aws_iam_policy_document" "github_oidc_trust" {
  statement {
    effect = "Allow"

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }

    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:*"]
    }
  }
}

# === RÔLE POUR LES TESTS ===
resource "aws_iam_role" "github_test_role" {
  name               = "${var.name}-test-role"
  assume_role_policy = data.aws_iam_policy_document.github_oidc_trust.json

  tags = {
    Name = "${var.name}-test-role"
  }
}

resource "aws_iam_role_policy" "github_test_policy" {
  name = "${var.name}-test-policy"
  role = aws_iam_role.github_test_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:GetFunction",
          "apigateway:GET",
          "iam:GetRole"
        ]
        Resource = "*"
      }
    ]
  })
}

# === RÔLE POUR LE PLAN ===
resource "aws_iam_role" "github_plan_role" {
  name               = "${var.name}-plan-role"
  assume_role_policy = data.aws_iam_policy_document.github_oidc_trust.json

  tags = {
    Name = "${var.name}-plan-role"
  }
}

resource "aws_iam_role_policy" "github_plan_policy" {
  name = "${var.name}-plan-policy"
  role = aws_iam_role.github_plan_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:GetFunction",
          "apigateway:GET",
          "iam:GetRole"
        ]
        Resource = "*"
      }
    ]
  })
}

# === RÔLE POUR L'APPLY ===
resource "aws_iam_role" "github_apply_role" {
  name               = "${var.name}-apply-role"
  assume_role_policy = data.aws_iam_policy_document.github_oidc_trust.json

  tags = {
    Name = "${var.name}-apply-role"
  }
}

resource "aws_iam_role_policy" "github_apply_policy" {
  name = "${var.name}-apply-policy"
  role = aws_iam_role.github_apply_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:*",
          "apigateway:*",
          "iam:*",
          "s3:*",
          "dynamodb:*"
        ]
        Resource = "*"
      }
    ]
  })
}
