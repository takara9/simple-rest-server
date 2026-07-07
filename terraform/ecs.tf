# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "default"
resource "aws_ecs_cluster" "default" {
  name     = "default"
  region   = "ap-northeast-1"
  tags     = {}
  tags_all = {}
  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}
