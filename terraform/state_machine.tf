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
    effect    = "Allow"
    resources = [aws_iam_role.etl.arn, aws_iam_role.execution_role.arn]
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
      "arn:aws:ecs:eu-west-1:${local.account.account_id}:task-definition/etl5-${terraform.workspace}*"
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

locals {
  subnets_string = join(",", [for s in data.aws_subnet_ids.private.ids : format("%q", s)])
}

resource "aws_sfn_state_machine" "casrec_migration" {
  name     = "casrec-mig-state-machine"
  role_arn = aws_iam_role.state_machine.arn

  definition = <<EOF
{
    "StartAt": "Prepare For Migration",
    "States": {
        "Prepare For Migration": {
            "Type": "Task",
            "Next": "Parrallel Load Casrec",
            "Resource": "arn:aws:states:::ecs:runTask.sync",
            "Parameters": {
                "LaunchType": "FARGATE",
                "PlatformVersion": "1.4.0",
                "Cluster": "${aws_ecs_cluster.migration.arn}",
                "TaskDefinition": "${aws_ecs_task_definition.etl0.arn}",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "Subnets": [${local.subnets_string}],
                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                        "AssignPublicIp": "DISABLED"
                    }
                },
                "Overrides": {
                    "ContainerOverrides": [{
                        "Name": "etl0",
                        "Command": ["prepare/prepare.sh"]
                    }]
                }
            }
        },
        "Parrallel Load Casrec": {
            "Type": "Parallel",
            "Next": "Run Transform Casrec",
            "Branches": [
                {
                    "StartAt": "Run Load Casrec Task 1",
                    "States": {
                        "Run Load Casrec Task 1": {
                            "Type": "Task",
                            "Resource": "arn:aws:states:::ecs:runTask.sync",
                            "Parameters": {
                                "LaunchType": "FARGATE",
                                "Cluster": "${aws_ecs_cluster.migration.arn}",
                                "TaskDefinition": "${aws_ecs_task_definition.etl1.arn}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "etl1",
                                        "Command": ["python3", "app.py"]
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
                                "Cluster": "${aws_ecs_cluster.migration.arn}",
                                "TaskDefinition": "${aws_ecs_task_definition.etl1.arn}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "etl1",
                                        "Command": ["python3", "app.py"]
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
                                "Cluster": "${aws_ecs_cluster.migration.arn}",
                                "TaskDefinition": "${aws_ecs_task_definition.etl1.arn}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "etl1",
                                        "Command": ["python3", "app.py"]
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
                                "Cluster": "${aws_ecs_cluster.migration.arn}",
                                "TaskDefinition": "${aws_ecs_task_definition.etl1.arn}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "etl1",
                                        "Command": ["python3", "app.py"]
                                    }]
                                }
                            },
                            "End": true
                        }
                    }
                }
            ]
        },
        "Run Transform Casrec": {
            "Type": "Task",
            "Next": "Run Aquire Target IDs",
            "Resource": "arn:aws:states:::ecs:runTask.sync",
            "Parameters": {
                "LaunchType": "FARGATE",
                "Cluster": "${aws_ecs_cluster.migration.arn}",
                "TaskDefinition": "${aws_ecs_task_definition.etl2.arn}",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "Subnets": [${local.subnets_string}],
                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                        "AssignPublicIp": "DISABLED"
                    }
                },
                "Overrides": {
                    "ContainerOverrides": [{
                        "Name": "etl2",
                        "Command": ["python3", "app.py", "--clear=True"]
                    }]
                }
            }
        },
        "Run Aquire Target IDs": {
            "Type": "Task",
            "Next": "Run Load To Target",
            "Resource": "arn:aws:states:::ecs:runTask.sync",
            "Parameters": {
                "LaunchType": "FARGATE",
                "PlatformVersion": "1.4.0",
                "Cluster": "${aws_ecs_cluster.migration.arn}",
                "TaskDefinition": "${aws_ecs_task_definition.etl3.arn}",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "Subnets": [${local.subnets_string}],
                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                        "AssignPublicIp": "DISABLED"
                    }
                },
                "Overrides": {
                    "ContainerOverrides": [{
                        "Name": "etl3",
                        "Command": ["integration/integration.sh"]
                    }]
                }
            }
        },
        "Run Load To Target": {
            "Type": "Task",
            "Next": "Run Validation",
            "Resource": "arn:aws:states:::ecs:runTask.sync",
            "Parameters": {
                "LaunchType": "FARGATE",
                "PlatformVersion": "1.4.0",
                "Cluster": "${aws_ecs_cluster.migration.arn}",
                "TaskDefinition": "${aws_ecs_task_definition.etl4.arn}",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "Subnets": [${local.subnets_string}],
                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                        "AssignPublicIp": "DISABLED"
                    }
                },
                "Overrides": {
                    "ContainerOverrides": [{
                        "Name": "etl4",
                        "Command": ["python3", "app.py", "--audit=${local.account.run_audit}"]
                    }]
                }
            }
        },
        "Run Validation": {
            "Type": "Task",
            "End": true,
            "Resource": "arn:aws:states:::ecs:runTask.sync",
            "Parameters": {
                "LaunchType": "FARGATE",
                "PlatformVersion": "1.4.0",
                "Cluster": "${aws_ecs_cluster.migration.arn}",
                "TaskDefinition": "${aws_ecs_task_definition.etl5.arn}",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "Subnets": [${local.subnets_string}],
                        "SecurityGroups": ["${aws_security_group.etl.id}"],
                        "AssignPublicIp": "DISABLED"
                    }
                },
                "Overrides": {
                    "ContainerOverrides": [{
                        "Name": "etl5",
                        "Command": ["validation/validate.sh"]
                    }]
                }
            }
        }
    }
}
EOF
}
