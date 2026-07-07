# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "default/simple-rest-backend-432e"
resource "aws_ecs_service" "simple_rest_backend" {
  availability_zone_rebalancing      = "ENABLED"
  cluster                            = "arn:aws:ecs:ap-northeast-1:609356922798:cluster/default"
  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100
  desired_count                      = 1
  enable_ecs_managed_tags            = true
  enable_execute_command             = false
  force_delete                       = null
  force_new_deployment               = null
  health_check_grace_period_seconds  = 0
  name                               = "simple-rest-backend-432e"
  propagate_tags                     = "SERVICE"
  region                             = "ap-northeast-1"
  scheduling_strategy                = "REPLICA"
  sigint_rollback                    = null
  tags                               = {}
  tags_all                           = {}
  task_definition                    = null
  triggers                           = {}
  wait_for_steady_state              = null
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  deployment_configuration {
    bake_time_in_minutes = "3"
    strategy             = "CANARY"
    canary_configuration {
      canary_bake_time_in_minutes = "3"
      canary_percent              = 5
    }
  }
  deployment_controller {
    type = "ECS"
  }
}
