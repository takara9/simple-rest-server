# インタンスIDを調べる

## S3

```console
ubuntu@ws1:~/simple-rest-server/terraform$ aws s3 ls --profile takara
2026-06-05 10:30:02 aws-cloudtrail-logs-609356922798-c01aeb1f
2026-06-05 16:46:43 codepipeline-tfstate-bucket
2026-06-04 16:17:38 takara-strudy-aws-and-tf-bucket-609356922798-ap-northeast-1
2026-07-07 11:48:48 web-takara

ubuntu@ws1:~/simple-rest-server/terraform$ aws s3api list-buckets --query 'Buckets[*].Name' --output table --profile takara
-----------------------------------------------------------------
|                          ListBuckets                          |
+---------------------------------------------------------------+
|  aws-cloudtrail-logs-609356922798-c01aeb1f                    |
|  codepipeline-tfstate-bucket                                  |
|  takara-strudy-aws-and-tf-bucket-609356922798-ap-northeast-1  |
|  web-takara                                                   |
+---------------------------------------------------------------+
```

## ECS

```console
# クラスター一覧
ubuntu@ws1:~/simple-rest-server/terraform$ aws ecs list-clusters --output table
---------------------------------------------------------------
|                        ListClusters                         |
+-------------------------------------------------------------+
||                        clusterArns                        ||
|+-----------------------------------------------------------+|
||  arn:aws:ecs:ap-northeast-1:609356922798:cluster/default  ||
|+-----------------------------------------------------------+|

# 指定クラスター内のサービス一覧
ubuntu@ws1:~/simple-rest-server/terraform$ aws ecs list-services --cluster default --output table
----------------------------------------------------------------------------------------
|                                     ListServices                                     |
+--------------------------------------------------------------------------------------+
||                                     serviceArns                                    ||
|+------------------------------------------------------------------------------------+|
||  arn:aws:ecs:ap-northeast-1:609356922798:service/default/simple-rest-backend-432e  ||
|+------------------------------------------------------------------------------------+|


# 指定クラスター内の実行中タスク一覧
ubuntu@ws1:~/simple-rest-server/terraform$ aws ecs list-tasks --cluster default --output table
---------------------------------------------------------------------------------------------
|                                         ListTasks                                         |
+-------------------------------------------------------------------------------------------+
||                                        taskArns                                         ||
|+-----------------------------------------------------------------------------------------+|
||  arn:aws:ecs:ap-northeast-1:609356922798:task/default/874b139f64224d62b5642b561270650f  ||
|+-----------------------------------------------------------------------------------------+|

# タスク定義一覧
ubuntu@ws1:~/simple-rest-server/terraform$ aws ecs list-task-definitions --output table
--------------------------------------------------------------------------------------------------
|                                       ListTaskDefinitions                                      |
+------------------------------------------------------------------------------------------------+
||                                      taskDefinitionArns                                      ||
|+----------------------------------------------------------------------------------------------+|
||  arn:aws:ecs:ap-northeast-1:609356922798:task-definition/default-simple-rest-backend-432e:1  ||
||  arn:aws:ecs:ap-northeast-1:609356922798:task-definition/default-simple-rest-backend-fc48:1  ||
|+----------------------------------------------------------------------------------------------+|
```

## RDS

```console
ubuntu@ws1:~/simple-rest-server/terraform$ aws rds describe-db-instances \
  --query 'DBInstances[*].{ID:DBInstanceIdentifier,Engine:Engine,Status:DBInstanceStatus,Endpoint:Endpoint.Address}' \
  --output table
-----------------------------------------------------------------------------------------------------
|                                        DescribeDBInstances                                        |
+-----------------------------------------------------------+-----------+-------------+-------------+
|                         Endpoint                          |  Engine   |     ID      |   Status    |
+-----------------------------------------------------------+-----------+-------------+-------------+
|  database-1.cl2misoamn2u.ap-northeast-1.rds.amazonaws.com |  postgres |  database-1 |  available  |
+-----------------------------------------------------------+-----------+-------------+-------------+
```

## SG


```console
ubuntu@ws1:~/simple-rest-server/terraform$ aws ec2 describe-security-groups \
  --query 'SecurityGroups[*].{ID:GroupId,Name:GroupName,VPC:VpcId}' \
  --output table
-------------------------------------------------------------------------------------------------------------
|                                          DescribeSecurityGroups                                           |
+----------------------+----------------------------------------------------------+-------------------------+
|          ID          |                          Name                            |           VPC           |
+----------------------+----------------------------------------------------------+-------------------------+
|  sg-0235b05dd05106b13|  ecs-express-gateway-alb-sg-1783388771928                |  vpc-0b7450109948726d6  |
|  sg-04ee992d20ba44f86|  default-simple-rest-backend-432e-vpc-0b7450109948726d6  |  vpc-0b7450109948726d6  |
|  sg-0c879636d67d46f2c|  default                                                 |  vpc-0b7450109948726d6  |
+----------------------+----------------------------------------------------------+-------------------------+
```


## Subnet

```console
ubuntu@ws1:~/simple-rest-server/terraform$ aws ec2 describe-subnets \
  --query 'Subnets[*].{ID:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,VPC:VpcId}' \
  --output table
--------------------------------------------------------------------------------------------
|                                      DescribeSubnets                                     |
+-----------------+-----------------+----------------------------+-------------------------+
|       AZ        |      CIDR       |            ID              |           VPC           |
+-----------------+-----------------+----------------------------+-------------------------+
|  ap-northeast-1c|  172.31.0.0/20  |  subnet-099858569966e7740  |  vpc-0b7450109948726d6  |
|  ap-northeast-1d|  172.31.16.0/20 |  subnet-0650c2412beab4738  |  vpc-0b7450109948726d6  |
|  ap-northeast-1a|  172.31.32.0/20 |  subnet-018cd7dcb17fccce2  |  vpc-0b7450109948726d6  |
+-----------------+-----------------+----------------------------+-------------------------+
```


## VPC


```console

# VPC一覧
ubuntu@ws1:~/simple-rest-server/terraform$ aws ec2 describe-vpcs --query 'Vpcs[*].{ID:VpcId,CIDR:CidrBlock,Name:Tags[?Key==`Name`]|[0].Value}' --output table
----------------------------------------------------
|                   DescribeVpcs                   |
+----------------+-------------------------+-------+
|      CIDR      |           ID            | Name  |
+----------------+-------------------------+-------+
|  172.31.0.0/16 |  vpc-0b7450109948726d6  |  None |
+----------------+-------------------------+-------+

# そのVPC配下のSGだけ
ubuntu@ws1:~/simple-rest-server/terraform$ aws ec2 describe-security-groups --filters "Name=vpc-id,Values=vpc-0b7450109948726d6" --output table
--------------------------------------------------------------------------------------------------------------------------------------------
|                                                          DescribeSecurityGroups                                                          |
+------------------------------------------------------------------------------------------------------------------------------------------+
||                                                             SecurityGroups                                                             ||
|+----------------------+-----------------------------------------------------------------------------------------------------------------+|
||  Description         |  ECS Express Gateway security group - allows HTTP/HTTPS inbound with managed outbound rules                     ||
||  GroupId             |  sg-0235b05dd05106b13                                                                                           ||
||  GroupName           |  ecs-express-gateway-alb-sg-1783388771928                                                                       ||
||  OwnerId             |  609356922798                                                                                                   ||
||  SecurityGroupArn    |  arn:aws:ec2:ap-northeast-1:609356922798:security-group/sg-0235b05dd05106b13                                    ||
||  VpcId               |  vpc-0b7450109948726d6                                                                                          ||
|+----------------------+-----------------------------------------------------------------------------------------------------------------+|
|||                                                             IpPermissions                                                            |||
||+-----------------------------------------------------------------------------------------+--------------------------------------------+||
|||  FromPort                                                                               |  80                                        |||
|||  IpProtocol                                                                             |  tcp                                       |||
|||  ToPort                                                                                 |  80                                        |||
||+-----------------------------------------------------------------------------------------+--------------------------------------------+||
||||                                                              IpRanges                                                              ||||
|||+-------------------------------------+----------------------------------------------------------------------------------------------+|||
||||  CidrIp                             |  0.0.0.0/0                                                                                   ||||
||||  Description                        |  HTTP access from anywhere (IPv4)                                                            ||||
|||+-------------------------------------+----------------------------------------------------------------------------------------------+|||
||||                                                             Ipv6Ranges                                                             ||||
|||+-------------------------------------+----------------------------------------------------------------------------------------------+|||
||||  CidrIpv6                           |  ::/0                                                                                        ||||
||||  Description                        |  HTTP access from anywhere (IPv6)                                                            ||||
|||+-------------------------------------+----------------------------------------------------------------------------------------------+|||
|||                                                             IpPermissions                                                            |||
||+-----------------------------------------------------------------------------------------+--------------------------------------------+||
|||  FromPort                                                                               |  443                                       |||
|||  IpProtocol                                                                             |  tcp                                       |||
|||  ToPort                                                                                 |  443                                       |||
||+-----------------------------------------------------------------------------------------+--------------------------------------------+||
||||                                                              IpRanges                                                              ||||
|||+-------------------------------------+----------------------------------------------------------------------------------------------+|||
||||  CidrIp                             |  0.0.0.0/0                                                                                   ||||
||||  Description                        |  HTTPS access from anywhere (IPv4)                                                           ||||
|||+-------------------------------------+----------------------------------------------------------------------------------------------+|||
||||                                                             Ipv6Ranges                                                             ||||
|||+-------------------------------------+----------------------------------------------------------------------------------------------+|||
||||  CidrIpv6                           |  ::/0                                                                                        ||||
||||  Description                        |  HTTPS access from anywhere (IPv6)                                                           ||||
|||+-------------------------------------+----------------------------------------------------------------------------------------------+|||
|||                                                          IpPermissionsEgress                                                         |||
||+---------------------------------------------------------------------------------------------+----------------------------------------+||
|||  FromPort                                                                                   |                                        |||
|||  IpProtocol                                                                                 |  -1                                    |||
|||  ToPort                                                                                     |                                        |||
||+---------------------------------------------------------------------------------------------+----------------------------------------+||
||||                                                          UserIdGroupPairs                                                          ||||
|||+-----------------------------------+------------------------------------------------------------------------------------------------+|||
||||  Description                      |  Placeholder rule to reserve capacity                                                          ||||
||||  GroupId                          |  sg-0235b05dd05106b13                                                                          ||||
||||  UserId                           |  609356922798                                                                                  ||||
|||+-----------------------------------+------------------------------------------------------------------------------------------------+|||
|||                                                          IpPermissionsEgress                                                         |||
||+-------------------------------------------------------------------------------------+------------------------------------------------+||
|||  FromPort                                                                           |  5000                                          |||
|||  IpProtocol                                                                         |  tcp                                           |||
|||  ToPort                                                                             |  5000                                          |||
||+-------------------------------------------------------------------------------------+------------------------------------------------+||
||||                                                          UserIdGroupPairs                                                          ||||
|||+-------------------------------------------+----------------------------------------------------------------------------------------+|||
||||  Description                              |  Egress Rule to ECS Service                                                            ||||
||||  GroupId                                  |  sg-04ee992d20ba44f86                                                                  ||||
||||  UserId                                   |  609356922798                                                                          ||||
|||+-------------------------------------------+----------------------------------------------------------------------------------------+|||
|||                                                                 Tags                                                                 |||
||+----------------------------------------+---------------------------------------------------------------------------------------------+||
|||  Key                                   |  AmazonECSManaged                                                                           |||
|||  Value                                 |  true                                                                                       |||
||+----------------------------------------+---------------------------------------------------------------------------------------------+||
||                                                             SecurityGroups                                                             ||
|+------------------+---------------------------------------------------------------------------------------------------------------------+|
||  Description     |  Security group for ECS service: arn:aws:ecs:ap-northeast-1:609356922798:service/default/simple-rest-backend-432e   ||
||  GroupId         |  sg-04ee992d20ba44f86                                                                                               ||
||  GroupName       |  default-simple-rest-backend-432e-vpc-0b7450109948726d6                                                             ||
||  OwnerId         |  609356922798                                                                                                       ||
||  SecurityGroupArn|  arn:aws:ec2:ap-northeast-1:609356922798:security-group/sg-04ee992d20ba44f86                                        ||
||  VpcId           |  vpc-0b7450109948726d6                                                                                              ||
|+------------------+---------------------------------------------------------------------------------------------------------------------+|
|||                                                             IpPermissions                                                            |||
||+-------------------------------------------------------------------------------------+------------------------------------------------+||
|||  FromPort                                                                           |  5000                                          |||
|||  IpProtocol                                                                         |  tcp                                           |||
|||  ToPort                                                                             |  5000                                          |||
||+-------------------------------------------------------------------------------------+------------------------------------------------+||
||||                                                          UserIdGroupPairs                                                          ||||
|||+----------------------------------------+-------------------------------------------------------------------------------------------+|||
||||  GroupId                               |  sg-0235b05dd05106b13                                                                     ||||
||||  UserId                                |  609356922798                                                                             ||||
|||+----------------------------------------+-------------------------------------------------------------------------------------------+|||
|||                                                          IpPermissionsEgress                                                         |||
||+---------------------------------------------------------------------------------------------+----------------------------------------+||
|||  IpProtocol                                                                                 |  -1                                    |||
||+---------------------------------------------------------------------------------------------+----------------------------------------+||
||||                                                              IpRanges                                                              ||||
|||+--------------------------------------------------------+---------------------------------------------------------------------------+|||
||||  CidrIp                                                |  0.0.0.0/0                                                                ||||
|||+--------------------------------------------------------+---------------------------------------------------------------------------+|||
|||                                                                 Tags                                                                 |||
||+----------------------------------------+---------------------------------------------------------------------------------------------+||
|||  Key                                   |  AmazonECSManaged                                                                           |||
|||  Value                                 |  true                                                                                       |||
||+----------------------------------------+---------------------------------------------------------------------------------------------+||
||                                                             SecurityGroups                                                             ||
|+--------------------------+-------------------------------------------------------------------------------------------------------------+|
||  Description             |  default VPC security group                                                                                 ||
||  GroupId                 |  sg-0c879636d67d46f2c                                                                                       ||
||  GroupName               |  default                                                                                                    ||
||  OwnerId                 |  609356922798                                                                                               ||
||  SecurityGroupArn        |  arn:aws:ec2:ap-northeast-1:609356922798:security-group/sg-0c879636d67d46f2c                                ||
||  VpcId                   |  vpc-0b7450109948726d6                                                                                      ||
|+--------------------------+-------------------------------------------------------------------------------------------------------------+|
|||                                                             IpPermissions                                                            |||
||+---------------------------------------------------------------------------------------------+----------------------------------------+||
|||  IpProtocol                                                                                 |  -1                                    |||
||+---------------------------------------------------------------------------------------------+----------------------------------------+||
||||                                                          UserIdGroupPairs                                                          ||||
|||+----------------------------------------+-------------------------------------------------------------------------------------------+|||
||||  GroupId                               |  sg-0c879636d67d46f2c                                                                     ||||
||||  UserId                                |  609356922798                                                                             ||||
|||+----------------------------------------+-------------------------------------------------------------------------------------------+|||
|||                                                          IpPermissionsEgress                                                         |||
||+---------------------------------------------------------------------------------------------+----------------------------------------+||
|||  IpProtocol                                                                                 |  -1                                    |||
||+---------------------------------------------------------------------------------------------+----------------------------------------+||
||||                                                              IpRanges                                                              ||||
|||+--------------------------------------------------------+---------------------------------------------------------------------------+|||
||||  CidrIp                                                |  0.0.0.0/0                                                                ||||
|||+--------------------------------------------------------+---------------------------------------------------------------------------+|||


# そのVPC配下のSubnetだけ
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-0b7450109948726d6" --output table
ubuntu@ws1:~/simple-rest-server/terraform$ aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-0b7450109948726d6" --output table
--------------------------------------------------------------------------------------------------------------
|                                               DescribeSubnets                                              |
+------------------------------------------------------------------------------------------------------------+
||                                                  Subnets                                                 ||
|+------------------------------+---------------------------------------------------------------------------+|
||  AssignIpv6AddressOnCreation |  False                                                                    ||
||  AvailabilityZone            |  ap-northeast-1c                                                          ||
||  AvailabilityZoneId          |  apne1-az1                                                                ||
||  AvailableIpAddressCount     |  4090                                                                     ||
||  CidrBlock                   |  172.31.0.0/20                                                            ||
||  DefaultForAz                |  True                                                                     ||
||  EnableDns64                 |  False                                                                    ||
||  Ipv6Native                  |  False                                                                    ||
||  MapCustomerOwnedIpOnLaunch  |  False                                                                    ||
||  MapPublicIpOnLaunch         |  True                                                                     ||
||  OwnerId                     |  609356922798                                                             ||
||  State                       |  available                                                                ||
||  SubnetArn                   |  arn:aws:ec2:ap-northeast-1:609356922798:subnet/subnet-099858569966e7740  ||
||  SubnetId                    |  subnet-099858569966e7740                                                 ||
||  VpcId                       |  vpc-0b7450109948726d6                                                    ||
|+------------------------------+---------------------------------------------------------------------------+|
|||                                         BlockPublicAccessStates                                        |||
||+-----------------------------------------------------------------------------------+--------------------+||
|||  InternetGatewayBlockMode                                                         |  off               |||
||+-----------------------------------------------------------------------------------+--------------------+||
|||                                      PrivateDnsNameOptionsOnLaunch                                     |||
||+-------------------------------------------------------------------------------+------------------------+||
|||  EnableResourceNameDnsAAAARecord                                              |  False                 |||
|||  EnableResourceNameDnsARecord                                                 |  False                 |||
|||  HostnameType                                                                 |  ip-name               |||
||+-------------------------------------------------------------------------------+------------------------+||
||                                                  Subnets                                                 ||
|+------------------------------+---------------------------------------------------------------------------+|
||  AssignIpv6AddressOnCreation |  False                                                                    ||
||  AvailabilityZone            |  ap-northeast-1d                                                          ||
||  AvailabilityZoneId          |  apne1-az2                                                                ||
||  AvailableIpAddressCount     |  4088                                                                     ||
||  CidrBlock                   |  172.31.16.0/20                                                           ||
||  DefaultForAz                |  True                                                                     ||
||  EnableDns64                 |  False                                                                    ||
||  Ipv6Native                  |  False                                                                    ||
||  MapCustomerOwnedIpOnLaunch  |  False                                                                    ||
||  MapPublicIpOnLaunch         |  True                                                                     ||
||  OwnerId                     |  609356922798                                                             ||
||  State                       |  available                                                                ||
||  SubnetArn                   |  arn:aws:ec2:ap-northeast-1:609356922798:subnet/subnet-0650c2412beab4738  ||
||  SubnetId                    |  subnet-0650c2412beab4738                                                 ||
||  VpcId                       |  vpc-0b7450109948726d6                                                    ||
|+------------------------------+---------------------------------------------------------------------------+|
|||                                         BlockPublicAccessStates                                        |||
||+-----------------------------------------------------------------------------------+--------------------+||
|||  InternetGatewayBlockMode                                                         |  off               |||
||+-----------------------------------------------------------------------------------+--------------------+||
|||                                      PrivateDnsNameOptionsOnLaunch                                     |||
||+-------------------------------------------------------------------------------+------------------------+||
|||  EnableResourceNameDnsAAAARecord                                              |  False                 |||
|||  EnableResourceNameDnsARecord                                                 |  False                 |||
|||  HostnameType                                                                 |  ip-name               |||
||+-------------------------------------------------------------------------------+------------------------+||
||                                                  Subnets                                                 ||
|+------------------------------+---------------------------------------------------------------------------+|
||  AssignIpv6AddressOnCreation |  False                                                                    ||
||  AvailabilityZone            |  ap-northeast-1a                                                          ||
||  AvailabilityZoneId          |  apne1-az4                                                                ||
||  AvailableIpAddressCount     |  4090                                                                     ||
||  CidrBlock                   |  172.31.32.0/20                                                           ||
||  DefaultForAz                |  True                                                                     ||
||  EnableDns64                 |  False                                                                    ||
||  Ipv6Native                  |  False                                                                    ||
||  MapCustomerOwnedIpOnLaunch  |  False                                                                    ||
||  MapPublicIpOnLaunch         |  True                                                                     ||
||  OwnerId                     |  609356922798                                                             ||
||  State                       |  available                                                                ||
||  SubnetArn                   |  arn:aws:ec2:ap-northeast-1:609356922798:subnet/subnet-018cd7dcb17fccce2  ||
||  SubnetId                    |  subnet-018cd7dcb17fccce2                                                 ||
||  VpcId                       |  vpc-0b7450109948726d6                                                    ||
|+------------------------------+---------------------------------------------------------------------------+|
|||                                         BlockPublicAccessStates                                        |||
||+-----------------------------------------------------------------------------------+--------------------+||
|||  InternetGatewayBlockMode                                                         |  off               |||
||+-----------------------------------------------------------------------------------+--------------------+||
|||                                      PrivateDnsNameOptionsOnLaunch                                     |||
||+-------------------------------------------------------------------------------+------------------------+||
|||  EnableResourceNameDnsAAAARecord                                              |  False                 |||
|||  EnableResourceNameDnsARecord                                                 |  False                 |||
|||  HostnameType                                                                 |  ip-name               |||
||+-------------------------------------------------------------------------------+------------------------+||

```

## Terraform のHCL作成

terraformer import aws --resources=vpc,subnet,sg,ecs --regions=ap-northeast-1

```console
$ terraform init
$ cat import.tf 
import {
  to = aws_ecs_cluster.default
  id = "default"
}

ubuntu@ws1:~/simple-rest-server/terraform$ vi import.tf 

ubuntu@ws1:~/simple-rest-server/terraform$ cat import.tf 
import {
  to = aws_ecs_cluster.default
  id = "default"
}

ubuntu@ws1:~/simple-rest-server/terraform$ terraform plan -generate-config-out=generated_ecs.tf
aws_ecs_cluster.default: Preparing import... [id=default]
aws_ecs_cluster.default: Refreshing state... [id=arn:aws:ecs:ap-northeast-1:609356922798:cluster/default]

Terraform will perform the following actions:

  # aws_ecs_cluster.default will be imported
  # (config will be generated)
    resource "aws_ecs_cluster" "default" {
        arn      = "arn:aws:ecs:ap-northeast-1:609356922798:cluster/default"
        id       = "arn:aws:ecs:ap-northeast-1:609356922798:cluster/default"
        name     = "default"
        region   = "ap-northeast-1"
        tags     = {}
        tags_all = {}

        setting {
            name  = "containerInsights"
            value = "disabled"
        }
    }

Plan: 1 to import, 0 to add, 0 to change, 0 to destroy.
╷
│ Warning: Config generation is experimental
│ 
│ Generating configuration during import is currently experimental, and the generated configuration format may change in future versions.
╵

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Terraform has generated configuration and written it to generated_ecs.tf. Please review the configuration and edit it as necessary before adding it to version control.

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now
```



```console
ubuntu@ws1:~/simple-rest-server/terraform$ terraform apply
aws_ecs_cluster.default: Preparing import... [id=default]
aws_ecs_cluster.default: Refreshing state... [id=arn:aws:ecs:ap-northeast-1:609356922798:cluster/default]

Terraform will perform the following actions:

  # aws_ecs_cluster.default will be imported
    resource "aws_ecs_cluster" "default" {
        arn      = "arn:aws:ecs:ap-northeast-1:609356922798:cluster/default"
        id       = "arn:aws:ecs:ap-northeast-1:609356922798:cluster/default"
        name     = "default"
        region   = "ap-northeast-1"
        tags     = {}
        tags_all = {}

        setting {
            name  = "containerInsights"
            value = "disabled"
        }
    }

Plan: 1 to import, 0 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_ecs_cluster.default: Importing... [id=default]
aws_ecs_cluster.default: Import complete [id=default]

Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
```



```console
ubuntu@ws1:~/simple-rest-server/terraform$ terraform state list
aws_ecs_cluster.default

ubuntu@ws1:~/simple-rest-server/terraform$ terraform plan
aws_ecs_cluster.default: Refreshing state... [id=arn:aws:ecs:ap-northeast-1:609356922798:cluster/default]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.


ubuntu@ws1:~/simple-rest-server/terraform$ terraform state list
aws_ecs_cluster.default

ubuntu@ws1:~/simple-rest-server/terraform$ terraform plan
aws_ecs_cluster.default: Refreshing state... [id=arn:aws:ecs:ap-northeast-1:609356922798:cluster/default]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.
```

```console
ubuntu@ws1:~/simple-rest-server/terraform$ rm import.tf
ubuntu@ws1:~/simple-rest-server/terraform$ mv generated_ecs.tf ecs.tf
ubuntu@ws1:~/simple-rest-server/terraform$ ls
MEMO-investigate-instgance-id.md  ecs.tf  terraform.tfstate
```

```console
ubuntu@ws1:~/simple-rest-server/terraform$ aws ecs list-services --cluster default
{
    "serviceArns": [
        "arn:aws:ecs:ap-northeast-1:609356922798:service/default/simple-rest-backend-432e"
    ]
}

ubuntu@ws1:~/simple-rest-server/terraform$ aws ecs list-task-definitions
{
    "taskDefinitionArns": [
        "arn:aws:ecs:ap-northeast-1:609356922798:task-definition/default-simple-rest-backend-432e:1",
        "arn:aws:ecs:ap-northeast-1:609356922798:task-definition/default-simple-rest-backend-fc48:1"
    ]
}
```

```console
ubuntu@ws1:~/simple-rest-server/terraform$ aws ecs describe-services --cluster default --services simple-rest-backend-432e \
  --query 'services[0].taskDefinition'
null

ubuntu@ws1:~/simple-rest-server/terraform$ vi import.tf

ubuntu@ws1:~/simple-rest-server/terraform$ cat import.tf 
import {
  to = aws_ecs_service.simple_rest_backend
  id = "default/simple-rest-backend-432e"
}

import {
  to = aws_ecs_task_definition.simple_rest_backend_432e
  id = "default-simple-rest-backend-432e:1"
}
```

```console
ubuntu@ws1:~/simple-rest-server/terraform$ terraform plan -generate-config-out=generated_ecs2.tf
aws_ecs_task_definition.simple_rest_backend_432e: Preparing import... [id=default-simple-rest-backend-432e:1]
aws_ecs_service.simple_rest_backend: Preparing import... [id=default/simple-rest-backend-432e]
aws_ecs_cluster.default: Refreshing state... [id=arn:aws:ecs:ap-northeast-1:609356922798:cluster/default]
aws_ecs_service.simple_rest_backend: Refreshing state... [id=arn:aws:ecs:ap-northeast-1:609356922798:service/default/simple-rest-backend-432e]

Terraform planned the following actions, but then encountered a problem:

  # aws_ecs_service.simple_rest_backend will be imported
  # (config will be generated)
    resource "aws_ecs_service" "simple_rest_backend" {
        arn                                = "arn:aws:ecs:ap-northeast-1:609356922798:service/default/simple-rest-backend-432e"
        availability_zone_rebalancing      = "ENABLED"
        cluster                            = "arn:aws:ecs:ap-northeast-1:609356922798:cluster/default"
        deployment_maximum_percent         = 200
        deployment_minimum_healthy_percent = 100
        desired_count                      = 1
        enable_ecs_managed_tags            = true
        enable_execute_command             = false
        health_check_grace_period_seconds  = 0
        id                                 = "arn:aws:ecs:ap-northeast-1:609356922798:service/default/simple-rest-backend-432e"
        launch_type                        = null
        name                               = "simple-rest-backend-432e"
        platform_version                   = null
        propagate_tags                     = "SERVICE"
        region                             = "ap-northeast-1"
        scheduling_strategy                = "REPLICA"
        tags                               = {}
        tags_all                           = {}
        triggers                           = {}

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

Plan: 1 to import, 0 to add, 0 to change, 0 to destroy.
╷
│ Warning: Config generation is experimental
│ 
│ Generating configuration during import is currently experimental, and the generated configuration format may change in future versions.
╵
╷
│ Error: arn: invalid prefix
│ 
│ 
╵
ubuntu@ws1:~/simple-rest-server/terraform$ ls
MEMO-investigate-instgance-id.md  ecs.tf  generated_ecs2.tf  import.tf  terraform.tfstate
ubuntu@ws1:~/simple-rest-server/terraform$ cat generated_ecs2.tf 
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
ubuntu@ws1:~/simple-rest-server/terraform$ 

```

`Error: arn: invalid prefix` エラーが出てるので、aws インタンスから Terraform の HCLを作成する方法は、一旦断念する。
awsインスタンスから、Terraform HCL を生成するのは、熟れていない様子だった。

以上
