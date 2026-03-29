resource "aws_ecr_repository" "api" {
  name = "crypto-api"
}

resource "aws_ecr_repository" "frontend" {
  name = "crypto-frontend"
}
