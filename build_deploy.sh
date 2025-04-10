#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

echo "Environment variables loaded."

# Check if the ECR repository exists, create it if it does not
if ! aws ecr describe-repositories --repository-names ${REPOSITORY_NAME} --region ${AWS_REGION} 2>/dev/null; then
    echo "Repository ${REPOSITORY_NAME} does not exist. Creating..."
    aws ecr create-repository --repository-name ${REPOSITORY_NAME} --region ${AWS_REGION}
    echo "Repository ${REPOSITORY_NAME} created."
else
    echo "Repository ${REPOSITORY_NAME} already exists."
fi

# Create a clean requirements.txt without local project dependency
# To make your image compatible with Lambda, you must use the --provenance=false option.
echo "Generating requirements.txt..."
uv pip freeze --exclude-editable > lambda_function/requirements.txt

# Build Docker image
echo "Building Docker image ${IMAGE_NAME}..."
docker buildx build --platform linux/amd64 --provenance=false -t ${IMAGE_NAME}:latest .

# Authenticate Docker to your Amazon ECR registry
echo "Authenticating Docker to ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Tag the Docker image
echo "Tagging Docker image..."
docker tag ${IMAGE_NAME}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}:latest

# Push the Docker image to Amazon ECR
echo "Pushing Docker image to ECR..."
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}:latest

# Create a new IAM role with Lambda and Bedrock full access
echo "Checking IAM role..."

# Check if the role exists
if ! aws iam get-role --role-name ${ROLE_NAME} --region ${AWS_REGION} 2>/dev/null; then
    echo "Creating new IAM role for Lambda with Bedrock access..."
    # Create the IAM role
    aws iam create-role --role-name ${ROLE_NAME} --assume-role-policy-document file://assume-role.json --region ${AWS_REGION}

    # Attach the Lambda execution policy to the role
    aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole --region ${AWS_REGION}

    # Attach the Bedrock InvokeModel policy to the role
    aws iam put-role-policy --role-name ${ROLE_NAME} --policy-name ${ROLE_POLICY_NAME} --policy-document '{
      "Version": "2012-10-17",
      "Statement": [
        {
            "Sid": "InvokeBedrockModels",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:*::foundation-model/*"
        }
      ]
    }' --region ${AWS_REGION}
    
    echo "IAM role created and policies attached."
    echo "Waiting for IAM role to propagate (10 seconds)..."
    sleep 10
else
    echo "IAM role ${ROLE_NAME} already exists. Skipping role creation."
fi

# Check if the Lambda function exists, create it if it does not
if ! aws lambda get-function --function-name ${LAMBDA_FUNCTION_NAME} --region ${AWS_REGION} 2>/dev/null; then
    echo "Lambda function ${LAMBDA_FUNCTION_NAME} does not exist. Creating..."
    aws lambda create-function \
        --function-name ${LAMBDA_FUNCTION_NAME} \
        --package-type Image \
        --code ImageUri=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}:latest \
        --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/${ROLE_NAME} \
        --region ${AWS_REGION} \
        --timeout 300 \
        --memory-size 1024
else
    echo "Lambda function ${LAMBDA_FUNCTION_NAME} already exists. Updating..."
    aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --image-uri ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}:latest
fi

echo "Deployment complete."
