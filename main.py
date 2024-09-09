from dataclass.compress import CompressFile
from dataclass.lambda_function import LambdaFunction
from dataclass.queue import SQS

import boto3
import time
import io

if __name__ == "__main__":

    # Variaveis
    lambda_filename = "lambda_send_sqs.py"
    lambda_compress = "lambda_send_sqs.zip"

    lambda_function_name = "lambda_send_sqs"    # Change Function Name in AWS Lambda
    handler_function_name = "lambda_handler"    # Funcion name in file lambda_proc.py
    username = "leticiacb1"     

    timeout = 15
 
    queue_destination_name = "lambda_destination_queue_" + username

    handler = lambda_filename.split('.')[0] + "." + handler_function_name
    function_name = "sqs_lambda" + "_" + username 

    try: 
        # Instances
        compress = CompressFile()
        _lambda = LambdaFunction()
        sqs = SQS()

        # Compress
        compress.run(lambda_filename=lambda_filename, compress_filename=lambda_compress)

        # Create Queue for queue destination
        sqs.create_client()
        sqs.create_queue(queue_name= queue_destination_name)
        sqs.check_queue()

        environment_variables = {"DESTINATION_SQS_URL": sqs.queue_url,}
        environment = {"Variables": environment_variables}

        # Lambda Function
        _lambda.create_client()
        _lambda.read_function(compress_filename=lambda_compress)
        _lambda.create_function_zip(function_handler= handler, function_name=function_name, timeout=timeout, environment=environment)

        time.sleep(1) # Wait lambda function to be deployed

        # Call the lambda function 3 times and verify if the number of messages in destination queue increases :
        _lambda.check_function(function_name=function_name)
        _lambda.check_function(function_name=function_name)
        _lambda.check_function(function_name=function_name)

        time.sleep(10)        # Wait msm get to the queue

        # Check messages in queue
        sqs.check_queue()
        sqs.read_messages()   # Read 3 messages from queue
        sqs.read_messages()
        sqs.read_messages()

        time.sleep(10)        # Wait msm get out of the queue
        sqs.check_queue()

    except Exception as e:
        print(f"\n    [ERROR] An error occurred: \n {e}")
    finally:
        # Cleaning:
        _lambda.cleanup(function_name=function_name)
        sqs.cleanup()