# import aws_cdk as cdk
import aws_cdk as cdk
from aws_cdk import App, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from aws_cdk import aws_s3 as s3
from constructs import Construct

# from aws_cdk import aws_s3 as s3


class MyResumeClusterStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "my-resume")

        # Create a VPC for the ECS cluster
        vpc = ec2.Vpc(self, "my-resume-vpc", max_azs=2)

        # Create the ECS cluster
        cluster = ecs.Cluster(self, "MyResumeCluster", vpc=vpc)

        # Create the IAM roles
        execution_policy = iam.PolicyStatement(
            actions=[
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
            ],
            resources=["*"],
        )
        execution_role = iam.Role(
            self,
            "MyResumeExecutionRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        execution_role.add_to_policy(execution_policy)

        task_role = iam.Role(
            self,
            "MyResumeTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )
        task_role.add_to_policy(
            iam.PolicyStatement(
                actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                resources=[logs.LogGroup(self, "MyLogGroup").log_group_arn],
            )
        )
        bucket.grant_read(task_role)

        # Create the task definition
        task_definition = ecs.FargateTaskDefinition(
            self,
            "ChatBot",
            memory_limit_mib=512,
            cpu=256,
            execution_role=execution_role,
            task_role=task_role,
        )

        # Add a container to the task definition
        container = task_definition.add_container(
            "webservice",
            image=ecs.ContainerImage.from_registry(
                "257033485100.dkr.ecr.ap-southeast-2.amazonaws.com/resume-chat:latest"
            ),
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="WebServiceContainer",
                log_group=logs.LogGroup(
                    self, "ResumeLogGroup", removal_policy=cdk.RemovalPolicy.DESTROY
                ),
            ),
            port_mappings=[ecs.PortMapping(container_port=5050)],
        )

        # Create the service
        service = ecs.FargateService(
            self,
            "MyResumeService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
            security_groups=[self.create_security_group(vpc)],
            assign_public_ip=True,
        )

    def create_security_group(self, vpc: ec2.Vpc) -> ec2.SecurityGroup:
        # Create a security group for the ECS service
        security_group = ec2.SecurityGroup(
            self, "MyResumeSecurityGroup", vpc=vpc, allow_all_outbound=True
        )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5050))

        return security_group


app = cdk.App()
MyResumeClusterStack(app, "MyECSClusterStack")
app.synth()
