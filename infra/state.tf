resource "aws_s3_bucket" "terraform_state" {
  bucket = "crypto-ci-terraform-state"
}
