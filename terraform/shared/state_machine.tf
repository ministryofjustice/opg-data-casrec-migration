data "aws_iam_role" "execution_role" {
  name = "migration-execution-role.${local.environment}"
}

data "aws_iam_role" "etl" {
  name = "casrec-migration-${local.environment}"
}

resource "aws_iam_role" "state_machine" {
  assume_role_policy = data.aws_iam_policy_document.state_assume.json
  name               = "casrec-mig-state-machine.${local.environment}"
  tags               = local.default_tags
}

data "aws_iam_policy_document" "state_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["states.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "state_machine" {
  statement {
    effect = "Allow"
    resources = [
      data.aws_iam_role.etl.arn,
      data.aws_iam_role.execution_role.arn
    ]
    actions = [
      "iam:GetRole",
      "iam:PassRole"
    ]
  }
  statement {
    effect = "Allow"
    resources = [
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/etl0-${terraform.workspace}*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/etl1-${terraform.workspace}*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/etl2-${terraform.workspace}*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/etl3-${terraform.workspace}*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/etl4-${terraform.workspace}*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/etl5-${terraform.workspace}*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/initialise-environments-${terraform.workspace}*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/load-casrec-db-${terraform.workspace}*",
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/reset-elasticsearch-${terraform.workspace}*"
    ]
    actions = ["ecs:RunTask"]
  }
  statement {
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "ecs:StopTask",
      "ecs:DescribeTasks"
    ]
  }
  statement {
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "events:PutTargets",
      "events:PutRule",
      "events:DescribeRule"
    ]
  }
  statement {
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "xray:PutTraceSegments",
      "xray:PutTelemetryRecords",
      "xray:GetSamplingRules",
      "xray:GetSamplingTargets"
    ]
  }
}

resource "aws_iam_role_policy" "state_machine" {
  name   = "casrec-mig-state.${local.environment}"
  policy = data.aws_iam_policy_document.state_machine.json
  role   = aws_iam_role.state_machine.id
}

resource "aws_sfn_state_machine" "casrec_migration_load" {
  name       = "casrec-mig-load-state-machine-${local.account.name}"
  role_arn   = aws_iam_role.state_machine.arn
  definition = local.load_casrec_definition
}



locals {
  subnets_string         = join(",", [for s in data.aws_subnet_ids.private.ids : format("%q", s)])
  load_casrec_definition = <<EOF
{
    "StartAt": "Initialise Environments For Migration",
    "States": {
        "Initialise Environments For Migration": {
            "Type": "Task",
            "Next": "Parrallel Load Casrec",
            "OutputPath": "$$.Execution.Input",
            "Resource": "arn:aws:states:::ecs:runTask.sync",
            "Parameters": {
                "LaunchType": "FARGATE",
                "PlatformVersion": "1.4.0",
                "Cluster": "${data.aws_ecs_cluster.migration.arn}",
                "TaskDefinition": "${aws_ecs_task_definition.load_casrec.arn}",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "Subnets": [${local.subnets_string}],
                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                        "AssignPublicIp": "DISABLED"
                    }
                },
                "Overrides": {
                    "ContainerOverrides": [{
                        "Name": "initialise-environments",
                        "Command": ["initialise_environments/load_casrec_db.sh"]
                    }]
                }
            }
        },
        "Parrallel Load Casrec": {
            "Type": "Parallel",
            "End": true,
            "Branches": [
                {
                    "StartAt": "Run Load Casrec Task 1",
                    "States": {
                        "Run Load Casrec Task 1": {
                            "Type": "Task",
                            "Resource": "arn:aws:states:::ecs:runTask.sync",
                            "Parameters": {
                                "LaunchType": "FARGATE",
                                "Cluster": "${data.aws_ecs_cluster.migration.arn}",
                                "TaskDefinition": "${aws_ecs_task_definition.load_casrec_db.arn}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "load-casrec-db",
                                        "Command": ["python3","load_casrec/app/app.py","--process=1","--process_total=4"]
                                    }]
                                }
                            },
                            "End": true
                        }
                    }
                },
                {
                    "StartAt": "Run Load Casrec Task 2",
                    "States": {
                        "Run Load Casrec Task 2": {
                            "Type": "Task",
                            "Resource": "arn:aws:states:::ecs:runTask.sync",
                            "Parameters": {
                                "LaunchType": "FARGATE",
                                "Cluster": "${data.aws_ecs_cluster.migration.arn}",
                                "TaskDefinition": "${aws_ecs_task_definition.load_casrec_db.arn}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "load-casrec-db",
                                        "Command": ["python3","load_casrec/app/app.py","--process=2","--process_total=4"]
                                    }]
                                }
                            },
                            "End": true
                        }
                    }
                },
                {
                    "StartAt": "Run Load Casrec Task 3",
                    "States": {
                        "Run Load Casrec Task 3": {
                            "Type": "Task",
                            "Resource": "arn:aws:states:::ecs:runTask.sync",
                            "Parameters": {
                                "LaunchType": "FARGATE",
                                "Cluster": "${data.aws_ecs_cluster.migration.arn}",
                                "TaskDefinition": "${aws_ecs_task_definition.load_casrec_db.arn}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "load-casrec-db",
                                        "Command": ["python3","load_casrec/app/app.py","--process=3","--process_total=4"]
                                    }]
                                }
                            },
                            "End": true
                        }
                    }
                },
                {
                    "StartAt": "Run Load Casrec Task 4",
                    "States": {
                        "Run Load Casrec Task 4": {
                            "Type": "Task",
                            "Resource": "arn:aws:states:::ecs:runTask.sync",
                            "Parameters": {
                                "LaunchType": "FARGATE",
                                "Cluster": "${data.aws_ecs_cluster.migration.arn}",
                                "TaskDefinition": "${aws_ecs_task_definition.load_casrec_db.arn}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "load-casrec-db",
                                        "Command": ["python3","load_casrec/app/app.py","--process=4","--process_total=4"]
                                    }]
                                }
                            },
                            "End": true
                        }
                    }
                }
            ]
        }
    }
}
EOF
}
