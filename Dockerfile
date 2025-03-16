FROM public.ecr.aws/lambda/python:3.12

# Set the working directory to /var/task
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy source code and config
COPY lambda_function/lambda_handler.py ./lambda_handler.py
COPY src ./src
COPY config ./config
COPY .env ./.env

# Command to run the Lambda handler function
CMD [ "lambda_handler.lambda_handler" ]
