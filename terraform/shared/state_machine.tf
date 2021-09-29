data "aws_iam_role" "state_machine" {
  name = "casrec-mig-state-machine.${local.environment}"
}

resource "aws_sfn_state_machine" "casrec_migration_load" {
  name       = "casrec-mig-load-state-machine-${local.account.name}"
  role_arn   = data.aws_iam_role.state_machine.arn
  definition = local.load_casrec_definition
}



locals {
  subnets_string         = join(",", [for s in data.aws_subnet_ids.private.ids : format("%q", s)])
  load_casrec_definition = <<EOF
{
    "StartAt": "Prepare For Migration",
    "States": {
        "Prepare For Migration": {
            "Type": "Task",
            "Next": "Parrallel Load Casrec",
            "OutputPath": "$$.Execution.Input",
            "Resource": "arn:aws:states:::ecs:runTask.sync",
            "Parameters": {
                "LaunchType": "FARGATE",
                "PlatformVersion": "1.4.0",
                "Cluster": "${data.aws_ecs_cluster.migration.arn}",
                "TaskDefinition": "${data.aws_ecs_task_definition.prepare.id}",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "Subnets": [${local.subnets_string}],
                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                        "AssignPublicIp": "DISABLED"
                    }
                },
                "Overrides": {
                    "ContainerOverrides": [{
                        "Name": "etl0",
                        "Command.$": "$.prep"
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
                                "TaskDefinition": "${data.aws_ecs_task_definition.load_casrec_db.id}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "etl1",
                                        "Command.$": "$.load1"
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
                                "TaskDefinition": "${data.aws_ecs_task_definition.load_casrec_db.id}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "etl1",
                                        "Command.$": "$.load2"
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
                                "TaskDefinition": "${data.aws_ecs_task_definition.load_casrec_db.id}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "etl1",
                                        "Command.$": "$.load3"
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
                                "TaskDefinition": "${data.aws_ecs_task_definition.load_casrec_db.id}",
                                "NetworkConfiguration": {
                                    "AwsvpcConfiguration": {
                                        "Subnets": [${local.subnets_string}],
                                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                                        "AssignPublicIp": "DISABLED"
                                    }
                                },
                                "Overrides": {
                                    "ContainerOverrides": [{
                                        "Name": "etl1",
                                        "Command.$": "$.load4"
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
