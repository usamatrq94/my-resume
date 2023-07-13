#!/bin/bash

# Set your AWS credentials and ecr repo and image tags
AWS_REGION="ap-southeast-2"
AWS_ACCOUNT_ID="257033485100"
ECR_REPOSITORY="resume-chat"
IMAGE_TAG="latest"


# Set your ECR repository details
ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# Docker build and tag the image
docker build -t "$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" .

# Retrieve an ECR authentication token
# AWS_PASSWORD=$(aws ecr get-login-password --region "$AWS_REGION")  
# echo "$AWS_PASSWORD" | docker login --username AWS --password-stdin "$ECR_REGISTRY"

# # Tag the docker image
# docker tag $ECR_REPOSITORY:$IMAGE_TAG "$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"

# # Push the image to ECR
# docker push "$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"

# # Logout from ECR
# docker logout "$ECR_REGISTRY"