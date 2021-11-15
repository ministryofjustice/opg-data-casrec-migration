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
                "TaskDefinition": "${aws_ecs_task_definition.prepare_load_casrec.arn}",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "Subnets": [${local.subnets_string}],
                        "SecurityGroups": ["${data.aws_security_group.etl_ecs_tasks.id}"],
                        "AssignPublicIp": "DISABLED"
                    }
                },
                "Overrides": {
                    "ContainerOverrides": [{
                        "Name": "prepare",
                        "Command": ["prepare/prepare_load_casrec_db.sh"]
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
                                        "Command": ["python3","load_casrec/app/app.py","--skip_load=false","--delay=0"]
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
                                        "Command": ["python3","load_casrec/app/app.py","--skip_load=false","--delay=2"]
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
                                        "Command": ["python3","load_casrec/app/app.py","--skip_load=false","--delay=3"]
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
                                        "Command": ["python3","load_casrec/app/app.py","--skip_load=false","--delay=4"]
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
