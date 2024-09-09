from dataclass.compress import CompressFile
from dataclass.lambda_function import LambdaFunction
from dataclass.queue import SQS

import concurrent.futures
import boto3
import time
import io

def multiple_simultaneous_calls(num_executions: int, function_name: str, lambda_client: boto3.client) -> None:
    try:
        print(f"\n    [INFO] Call lambda function {function_name}() {num_executions} times.\n")
        # Create a thread pool executor with the desired number of threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_executions) as executor:
            # List to store the future objects
            futures = []

            # Submit the Lambda invocations to the executor
            for _ in range(num_executions):
                future = executor.submit(
                    lambda_client.invoke,
                    FunctionName=function_name,
                    InvocationType="RequestResponse",
                )
                futures.append(future)

            # Process the results as they become available
            for future in concurrent.futures.as_completed(futures):
                print("-" * 40)
                response = future.result()
                payload = response["Payload"]
                txt = io.BytesIO(payload.read()).read().decode("utf-8")
                print(f"\n           > Response:\n{txt}\n")

    except Exception as e:
        print(f"\n    [ERROR] An error occurred in multiple_simultaneous_calls(): \n {e}")


if __name__ == "__main__":

    # Variaveis
    lambda_filename = "lambda_proc.py"
    lambda_compress = "lambda_proc.zip"

    lambda_function_name = "lambda_proc"    # Change Function Name in AWS Lambda
    handler_function_name = "do_something"  # Funcion name in file lambda_proc.py
    username = "leticiacb1"     

    timeout = 15
    concurrent_executions_limit = 2
    num_executions = 2                       # Define the number of concurrent executions/calls 
                                             # Change to 10 to test the limit and the error that appears

    handler = lambda_filename.split('.')[0] + "." + handler_function_name
    function_name = "do_something_concurrent_" + "_" + username 

    try: 
        
        # Instances
        compress = CompressFile()
        _lambda = LambdaFunction()
        sqs = SQS()

        # Compress
        compress.run(lambda_filename=lambda_filename, compress_filename=lambda_compress)

        # Lambda Function
        _lambda.create_client()
        _lambda.read_function(compress_filename=lambda_compress)
        _lambda.create_function_zip(function_handler= handler, function_name=function_name, timeout=timeout)

        time.sleep(1) # Wait lambda function to be deployed

        _lambda.check_function(function_name=function_name)
        _lambda.see_all_lambda_functions()

        _lambda.set_lambda_limits(function_name=function_name, concurrent_executions=concurrent_executions_limit)

        # Test the simultaneous calls to the lambda function
        multiple_simultaneous_calls(num_executions= num_executions, function_name= function_name, lambda_client= _lambda.lambda_client)

    except Exception as e:
        print(f"\n    [ERROR] An error occurred: \n {e}")
    finally:
        # Cleaning:
        _lambda.cleanup(function_name=function_name)