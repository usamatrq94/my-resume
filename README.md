```mermaid
graph LR
    vpc[VPC]
    cluster[ECS Cluster] --> vpc
    lb[Application Load Balancer] --> vpc
    service[Fargate Service] --> cluster
    task_definition[Task Definition] --> service
    container[Container] --> task_definition
    openai_key[SSM Parameter]
    container --> openai_key
    execution_role[Execution IAM Role] --> task_definition
    task_role[Task IAM Role] --> task_definition
    bucket[S3 Bucket] --> task_role
    logs[CloudWatch Logs] --> container
