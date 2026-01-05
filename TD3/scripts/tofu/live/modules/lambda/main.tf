resource "aws_lambda_function" "this" {
  filename         = data.archive_file.this.output_path
  function_name    = var.name
  role             = aws_iam_role.this.arn
  handler          = var.handler
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  source_code_hash = data.archive_file.this.output_base64sha256
  
  environment {
    variables = var.environment_variables
  }
}

data "archive_file" "this" {
  type        = "zip"
  source_dir  = var.src_dir
  output_path = "/tmp/${var.name}-${filemd5("${var.src_dir}/index.js")}.zip"
}

resource "aws_iam_role" "this" {
  name = "${var.name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
